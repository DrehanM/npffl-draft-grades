
def generate_position_ranks(draft_picks):
    rank_by_position = {
        "QB": [],
        "RB": [],
        "WR": [],
        "TE": [],
        "D/ST": [],
        "K": []
    }
    
    for draft_pick in draft_picks:
        nfl_player = draft_pick.player
        rank_by_position[nfl_player.position].append(nfl_player)
        
    return rank_by_position


    
    
    