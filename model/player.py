from tinydb import TinyDB


class Player:
    """
    This class defines the player properties.
    """

    def __init__(
        self,
        id: int,
        last_name: str,
        first_name: str,
        birth_date: str,
        gender: str,
        ranking: int,
    ) -> None:
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.score = 0
        self.ranking = ranking

    def __str__(self) -> str:
        "This is a string representation Player class"
        output = f"<{self.first_name} {self.last_name}, "
        output += f"id: {self.id}, score: {self.score}, rank: {self.ranking}>"
        return output

    def serialize_player(self):
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "ranking": self.ranking,
        }

    @classmethod
    def get_all_players_from_db(cls):
        """
        - This method gets all players infos from the database.
        - Create an instance of Player class for each of them.
        - Then return a list of all players instances.
        params:
            - cls: is an implicit parameter that represents the class
                   in opposition of 'self' that represents an instance of the
                   class.
        """
        players_list = []

        # Opening a connection to the database as db
        with TinyDB("database.json") as db:
            # create (if 1st time) or connect (if already exists)
            # to players table
            players_table = db.table("players")
            # get all records of players table
            players_infos = players_table.all()
            for player_infos in players_infos:
                player = cls(
                    id=player_infos.doc_id,
                    last_name=player_infos["last_name"],
                    first_name=player_infos["first_name"],
                    birth_date=player_infos["birth_date"],
                    gender=player_infos["gender"],
                    ranking=player_infos["ranking"],
                )
                players_list.append(player)

        return players_list
