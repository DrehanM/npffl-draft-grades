from bs4 import BeautifulSoup, Comment
from bs4.element import NavigableString, Tag

def get_draft_data(html_file):
    contents = open(html_file).read()
    parsed_html = BeautifulSoup(contents, "lxml")
    draft_picks = get_draft_pick_list_from(parsed_html)
    return draft_picks

def get_draft_pick_list_from(parsed_html):    
    raw_draft_pick_content = []
    
    between_comments = False
    for x in parsed_html.recursiveChildGenerator():
        if between_comments and not isinstance(x, str):
            raw_draft_pick_content.append(x)
        if isinstance(x, Comment):
            between_comments = x == " START PLAYER LOOP "
            
    draft_picks = []        
    for raw_block in raw_draft_pick_content:
        row = raw_block.find_next_sibling("tr")
        if type(row) == Tag:
            draft_pick = extract_draft_pick_data_from(row)
            draft_picks.append(draft_pick)
    return draft_picks
    

def extract_draft_pick_data_from(row):
    tds = row.find_all("td")
    
    pick_num = tds[0].get_text().strip()
    fantasy_team = tds[1].get_text().strip()
    
    # Player in the 3rd <td> is structured as <td>{player name}<br><span>{position}, {nfl team}</span>
    # So we need to extract the top level text from this td to recover the player name and then
    # extract the span to recover the position and team
    player_data = tds[2]
    player_name = player_data.find_all(text=True, recursive=False)[0].strip()
    player_position, player_nfl_team = player_data.find_all("span")[0].get_text().split(", ")
    
    return [int(pick_num), str(fantasy_team), (str(player_name), str(player_position), str(player_nfl_team))]



if __name__ == "__main__":
    contents = open("data/2021").read()
    parsed_html = BeautifulSoup(contents, "lxml")
    draft_picks = get_draft_pick_list_from(parsed_html)
    print(draft_picks)