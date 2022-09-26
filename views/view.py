# The view is what the users see
# for a web application the view represents the Html files
# for a desktop application the view represents the code that generate a GUI
# in this specific case users will use the terminal
from itertools import groupby


class View:
    def welcome(players):
        nbr_of_players = len(players)
        players_by_name = sorted(players, key=lambda x: x.first_name)
        players_by_rank = sorted(players, key=lambda x: x.ranking)

        print("\nWelcome to Swiss System Tournament.")

        if len(players) < 8:
            output = f"\n{8 - nbr_of_players} "
            output += "players are required to start the tournament."
            print(output)

        print(f"\nThere are {nbr_of_players} players in the database")

        print("\nList of all players in the database ordered by name: ")

        for player in players_by_name:
            print(player)

        print("\nList of all players in the database ordered by ranking\n: ")

        for player in players_by_rank:
            print(player)

    def player_successfully_saved(player):
        output = f"\n{player['first_name']} {player['last_name']} "
        output += "has been saved successfully."
        print(output)

    def required_players_to_add(players):
        nbr_of_players = len(players)
        print(f"\n{8 - nbr_of_players} more players to add.")

    def display_players_by_name(players, tournament):
        # sort players by their name
        players = sorted(players, key=lambda x: x.first_name)

        output = "\nList of player ordered by name for the tournament: "
        output += f"{tournament.name}\n"
        print(output)

        for player in players:
            print(player)

        return players

    def display_players_by_rank(players, tournament):
        # sort players by their ranking
        players = sorted(players, key=lambda x: x.ranking)

        output = "\nList of player ordered by ranking for the tournament: "
        output += f"{tournament.name}\n"
        print(output)

        for player in players:
            print(player)

        return players

    def display_players_by_score_and_rank(players, tournament):
        # sort players by score in descending order
        players = sorted(players, key=lambda x: x.score, reverse=True)
        # group by score
        an_itertool = groupby(players, key=lambda x: x.score)
        players_list = []

        for _, group in an_itertool:
            # sort each group by ranking in ascending order
            group_by_rank = sorted(list(group), key=lambda x: x.ranking)
            for item in group_by_rank:
                players_list.append(item)
        players = players_list
        output = "\nList of player ordered by score first then by rank for"
        output += "the tournament: "
        output += f"{tournament.name}\n"
        print(output)
        for player in players:
            print(player)

        return players

    def display_matchs(round):
        print(f"\nList of matchs for the round : {round.round_name}")
        for match in round.matchs_list:
            print(match)

    def start_round(round):
        print(f"\nStarting the round : {round.round_name}")
        print(round)

    def enter_round_result(round):
        print(f"\nEnter the result for every single match in:"
              f"{round.round_name}\n")
        print("- 1-0 if the 1st player won")
        print("- 0-0 if nobody won")
        print("- 0-1 if the 2nd player won\n")

    def display_round(round):
        print(f"\nThe result of {round.round_name} is: \n")
        print(round)

    def display_winner(players, tournament):
        print(f"\nThe winner of the {tournament.name} is : ")
        print(players[0])
