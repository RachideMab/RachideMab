from controllers.controller import Controller

if __name__ == "__main__":
    game_over = False

    while not game_over:
        # Provide the name of the tournament
        tournament_name = input("Please enter the tournament's name: ")
        # Start the game
        Controller().start_tournament(tournament_name)
        # Ask to continue or not
        new_game = input(
            "Do you want to start a new tournament ?" "select (Y/N): "
        ).upper()
        if new_game == "N":
            print("Thank you, bye!")
            game_over = True
