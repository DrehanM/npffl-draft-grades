from api import LeagueAPI
import json

if __name__ == "__main__":
    config = json.load(open("config/npffl.json"))
    league = LeagueAPI(config)
    draft_diffs = league.get_draft_differentials()
    scores = league.get_draft_scores(draft_diffs)
    print(scores)
    
    