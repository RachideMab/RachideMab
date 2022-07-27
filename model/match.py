from tinydb import TinyDB 

class Match():
    
    def __init__(self, player1, player2) -> None:
        self.players_pair = (
            [
                player1.id,
                player1.score
            ],
            [
                player2.id,
                player2.score
            ]
        )

    def __str__(self) -> str:
        "This is a string representation Match class"
        return f"{self.players_pair}"

    def enter_score(self, result):
        """
        This method adds 1 point to the winner at the end of each match.
        params:
            - result: string that take only 3 values: '1-0', '0-1' and '0-0'
        """
        if result[0] == '1':
            self.players_pair[0][1] += 1
        elif result[-1] == '1':
            self.players_pair[1][1] += 1
        else:
            # no winner
            self.players_pair[0][1] += 0.5
            self.players_pair[1][1] += 0.5