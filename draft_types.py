class DraftPick:
    def __init__(self, number, team, player):
        self.number = number
        self.fantasy_team = team
        self.player = player 
        
    def __str__(self):
        return "{} - {} - {}".format(str(self.number), self.fantasy_team, str(self.player))  
    
    def __repr__(self):
        return self.__str__() 
    

class NFLPlayer:
    def __init__(self, name, pos, team):
        self.name = name
        self.position = pos
        self.nfl_team = team
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__() 
        
    