from views.view import View
from datetime import datetime
from tinydb import TinyDB
from model.match import Match
from model.player import Player
from model.round import Round
from model.tournament import Tournament
import random


class Controller:

    def format_birthdate(self, birthdate):
        """
        This function will format a date like this: '2022-03-10' -> '2022-3-10'
        So it remove the leading 0 for month and day parts.
        params:
            - birthdate: string respecting the following format 'YYYY-MM-DD'
        """
        year = birthdate[:5]
        month = birthdate[5:8]
        day = birthdate[8:]
        if month[0] == '0':
            month = month[1:]
        if day[0] == '0':
            day = day[1:]
        return year + month + day

    def add_player_into_db(self):
        """
        - This function asks the user to enter the player's infos.
        - Save player's infos into the database.
        """
        player = {}

        last_name = input("Please enter player's last name: ").capitalize()
        player['last_name'] = last_name
        first_name = input("Please enter player's first name: ").capitalize()
        player['first_name'] = first_name
        birth_date = input("Please enter player's birth_date (YYYY-MM-DD): ")
        birth_date = self.format_birthdate(birth_date)
        player['birth_date'] = birth_date
        gender = input("Please enter player's gender (M/F): ").upper()
        player['gender'] = gender
        ranking = int(input("Please enter player's ranking"
                            "(it must be a positive integer >= 1): "))
        player['ranking'] = ranking

        with TinyDB('database.json') as db:
            players_table = db.table('players')
            # inserting player infos into the database
            players_table.insert(player)
        # using view to display successfull registration
        View.player_successfully_saved(player)

    def get_all_players(self):
        """Getting all players infos from the database.
        returning a list of all records.
        """
        with TinyDB('database.json') as db:
            players_table = db.table('players')
            players = players_table.all()

        return players

    def generate_pair_1st_time(self, ids_list):
        """Generating player_ids pairs for the first round
        params:
                - ids_list: list of player Ids
        """
        # sort the list in ascending order
        # ids_list.sort()
        nbr_of_pair = int(len(ids_list)/2)
        # first upper half
        first_half = ids_list[:nbr_of_pair]
        # second lower half
        second_half = ids_list[nbr_of_pair:]
        list_of_pair = []

        for i in range(nbr_of_pair):
            pair = (first_half.pop(0), second_half.pop(0))
            list_of_pair.append(pair)

        return list_of_pair

    def generate_pair(self, ids_list):
        """Generating player_ids pairs from the 2nd round
        params:
                - ids_list: list of player Ids
        """

        # Extract player_ids at even indexes 0, 2, 4, 6
        first_half = ids_list[0::2]
        # Extract player_ids at odd indexes 1, 3, 5, 7
        second_half = ids_list[1::2]
        list_of_pair = []

        nbr_of_pair = int(len(ids_list)/2)

        for i in range(nbr_of_pair):
            pair = (first_half.pop(0), second_half.pop(0))
            list_of_pair.append(pair)

        return list_of_pair

    def get_player_from_id(self, id, players_list):
        """
        - Retrieving a player instance from its Id.
        - Returning player instance
        - params:
            - id: integer representing a player Id
            - players_list: list of players instances
        """
        for player in players_list:
            if player.id == id:
                return player

    def update_players_score(self, matchs_list, players_list):
        "Update players score to match the result"

        updated_players_list = []
        for match in matchs_list:
            id1 = match.players_pair[0][0]
            score1 = match.players_pair[0][1]
            id2 = match.players_pair[1][0]
            score2 = match.players_pair[1][1]

            for player in players_list:
                if player.id == id1:
                    player.score = score1
                    updated_players_list.append(player)
                if player.id == id2:
                    player.score = score2
                    updated_players_list.append(player)

        return updated_players_list

    def launch_round(self, players_list, players_ids_pairs, tournament,
                     round_name):
        # Associate a match to every pair
        matchs_list = []
        for pair in players_ids_pairs:
            player1 = self.get_player_from_id(pair[0], players_list)
            player2 = self.get_player_from_id(pair[1], players_list)
            match = Match(player1, player2)
            matchs_list.append(match)

        # Starting first round
        round = Round(round_name=round_name, matchs_list=matchs_list)
        View.start_round(round)

        round_over = False
        while not round_over:
            choice = input("Wait until round is over,"
                           "then enter (end): ").lower()
            if choice == 'end':
                round_over = True
                round.end_date = datetime.today()

        # Step 4: Enter results when Round is over.
        View.enter_round_result(round)

        updated_matchs_list = []
        # modifying players score to match the result
        for match in round.matchs_list:
            print(match)
            result = input("Enter score for match above : ")
            match.enter_score(result)
            updated_matchs_list.append(match)
            print('\n')

        # Updating players instances to match the result
        updated_players_list = self.update_players_score(
            matchs_list=updated_matchs_list,
            players_list=players_list
        )

        # Applying the result to the round
        round.matchs_list = updated_matchs_list

        View.display_round(round)
        View.display_matchs(round)
        players_ranking = View.display_players_by_score_and_rank(
            updated_players_list, tournament)

        return players_ranking

    def start_tournament(self, tournament_name):
        """
        Starting the tournament by following the steps below:
            - creating a tournament
            - adding 8 players
            - generating player Ids pair for the 1st round
            - Entering the result when first round is over
            - repeating step 3 and step 4 until the tournament is over.
        """
        # Step 1: Create a tournament
        tournament = Tournament(
            name=tournament_name,
            location='Bruxelles',
            time_control='blabla',
            description='This is the first tournament'
        )

        rounds = ['Round1', 'Round2', 'Round3', 'Round4']

        # Step 2: Add 8 players

        # Getting players infos from database
        players = self.get_all_players()
        View.welcome(players)

        if len(players) < 8:
            add_player = True
            while add_player:
                # Adding player into database
                self.add_player_into_db()
                players = self.get_all_players()
                if len(players) == 8:
                    add_player = False
                View.required_players_to_add(players)
        else:
            add_more_player = input("Do you whish to add more players ?"
                                    "select (Y/N): ").upper()

            if add_more_player == 'N':
                # Creating players instances from database
                players_list = Player.get_all_players_from_db()

                if len(players_list) > 8:
                    # Choosing 8 players
                    players_list = random.sample(players_list, k=8)
            else:
                number_of_players = int(input("How many players do you wish"
                                              "to add ? Enter an integer"
                                              "number (1, 2, 3, ..., 9): "))

                for n in range(number_of_players):
                    # Adding player into database
                    self.add_player_into_db()

                # Creating players instances from database
                players_list = Player.get_all_players_from_db()
                # Choosing 8 players
                players_list = random.sample(players_list, k=8)

        # Displaying the list of players
        players_list = View.display_players_by_rank(players_list, tournament)

        for n in range(len(rounds)):
            pass

            # Finding the list of player Ids
            tournament.player_ids_list = [player.id for player in players_list]

            # Step 3: Generate player_ids pairs

            if n == 0:
                players_ids_pairs = self.generate_pair_1st_time(
                    tournament.player_ids_list)
            else:
                players_ids_pairs = self.generate_pair(
                                                    tournament.player_ids_list)

            players_list = self.launch_round(players_list, players_ids_pairs,
                                             tournament, rounds[n])

        View.display_winner(players_list, tournament)
