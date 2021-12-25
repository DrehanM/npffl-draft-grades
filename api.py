from espn_api.football import League
from tqdm import tqdm
import json
import logging

logger = logging.Logger(name="LOGGER", level=logging.DEBUG)

class LeagueAPI:
    def __init__(self, config):
        logger.debug("Intializing League API...")
        try:
            self.league = League(league_id=config["league_id"], year=config["year"], swid=config["swid"], espn_s2=config["espn_s2"])
            logger.info("Intialized League API for League %d", self.league.league_id)
        except:
            logger.error("Error occurred while initializing API")
            exit(1)
    
    def get_draft_differentials(self):
        player_cache_file = open("data/players", "r")
        player_cache = json.loads(player_cache_file.read())
        
        draft_picks = self.league.draft
        positions_seen_so_far = {
            "QB": 0,
            "RB": 0,
            "WR": 0,
            "TE": 0,
            "D/ST": 0,
            "K": 0
        }
        
        result = []
        
        try:
            for pick in tqdm(draft_picks):
                
                # Josh Allen is missing from the player database lmao
                # So I have to manually fill in his information
                if pick.playerName == "Josh Allen":
                    positions_seen_so_far["QB"] += 1
                    result.append({
                        "player": pick.playerName,
                        "injury_status": "ACTIVE",
                        "picking_team": pick.team.team_name,
                        "draft_position_rank": positions_seen_so_far["QB"],
                        "current_position_rank": 1,
                        "differential": draft_rank - current_rank
                    })
                    player_cache["Josh Allen"] = {
                        "position": "QB",
                        "current_rank": 1,
                        "injury_status": "ACTIVE"
                    }
                    continue
                
                if pick.playerName in player_cache:
                    player = player_cache[pick.playerName]
                    primary_position = player["position"]
                    injury_status = player["injury_status"]
                    positions_seen_so_far[primary_position] += 1
                    draft_rank = positions_seen_so_far[primary_position]
                    current_rank = player["current_rank"]
                else:
                    player = self.league.player_info(pick.playerName)
                    primary_position = player.position 
                    positions_seen_so_far[primary_position] += 1
                    draft_rank = positions_seen_so_far[primary_position]
                    current_rank = player.posRank
                    injury_status = player.injuryStatus
                    if current_rank == 0:
                        injury_status = "INJURY_RESERVE"
                
                result.append({
                    "player": pick.playerName,
                    "picking_team": pick.team.team_name,
                    "injury_status": injury_status,
                    "draft_position_rank": draft_rank,
                    "current_position_rank": current_rank,
                    "differential": draft_rank - current_rank
                })
                
                if pick.playerName not in player_cache:
                    player_cache[pick.playerName] = {
                        "position": primary_position,
                        "current_rank": current_rank,
                        "injury_status": injury_status
                    }
                
                
        except Exception as err:
            print(err)
        finally:
            json.dump(player_cache, open("data/players", "w"))
            json.dump(result, open("data/draft_diffs", "w"))
        
        return result
    
    def get_draft_scores(self, diffs):
        result = {}
        for diff in diffs:
            picking_team = diff["picking_team"]
            
            if picking_team not in result:
                result[picking_team] = {
                    "sum": 0,
                    "avg": 0,
                    "max": 0,
                    "min": 0,
                    "number of players on IR": 0,
                    "sum of healthy players": 0,
                    "avg of healthy players": "N/A",
                    "picks": []
                }
            
            pick_score = diff["differential"]
            result[picking_team]["sum"] += pick_score
            result[picking_team]["picks"].append(diff)
            result[picking_team]["avg"] = result[picking_team]["sum"] / len(result[picking_team]["picks"])
            result[picking_team]["max"] = max([p["differential"] for p in result[picking_team]["picks"]])
            result[picking_team]["min"] = min([p["differential"] for p in result[picking_team]["picks"]])
            
            result[picking_team]["number of players on IR"] += int(diff["injury_status"] == "INJURY_RESERVE")
            result[picking_team]["sum of healthy players"] += int(diff["injury_status"] != "INJURY_RESERVE") * pick_score
            
            num_healthy_players = len(result[picking_team]["picks"]) - result[picking_team]["number of players on IR"]
            if num_healthy_players > 0:
                result[picking_team]["avg of healthy players"] = result[picking_team]["sum of healthy players"] / num_healthy_players
        
        json.dump(result, open("data/scores", "w"))
        return result
            
    def get_player(self, player_name):
        try:
            player = self.league.player_info(player_name)
        except:
            logger.error("Error while getting player %s" % player_name)
            exit(1)
        
        if not player:
            logger.error("League API returned null for player with name %s" % player_name)
            
        return player
            
            
        
        

        


