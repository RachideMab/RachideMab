from datetime import datetime, date
from tinydb import TinyDB


class Tournament():
    
    def __init__(self,
                 name: str,
                 location: str,
                 time_control: str,
                 description: str) -> None:
        self.name = name
        self.location = location
        self.tournament_date = date.today()
        self.rounds_nbr = 4
        self.rounds_list = []
        self.player_ids_list = []
        self.time_control = time_control
        self.description = description