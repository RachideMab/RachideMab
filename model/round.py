from datetime import datetime


class Round:
    def __init__(self, round_name: str, matchs_list: list) -> None:
        self.round_name = round_name
        self.matchs_list = matchs_list
        self.start_date = datetime.today()
        self.end_date = None

    def __str__(self) -> str:
        """This is a string representation Round class"""
        output = [str(match) for match in self.matchs_list]
        return f"<{self.round_name}, {output}>"

    def serialize_round(self):
        output = [str(match) for match in self.matchs_list]
        return {
            "round_name": self.round_name,
            "matchs_list": f"<{self.round_name}, {output}"
        }
