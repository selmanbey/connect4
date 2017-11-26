from c4gamelib import *

cls()

print('CONNECT 4 (DOS EDITION) \n')
print('Connect Four is a two-player connection game in which the players take turns dropping their coins from the top into a grid through slots. The coins fall straight down, occupying the next available space within the slot. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one\'s own coins. \n')
print('To begin the game, you first need to create a grid. Please provide the following information to create your grid. \n')

slots = create_slots()
depth = create_depth()
board = Board(slots, depth)

cls()

board.print_board()
print('Your grid is successfully created. Now, choose who you want to play against: \nEnter [1] to play against computer \nEnter [2] to play against another player \n')

gametype = choose_gametype()

cls()

game = Gameplay(board)

if gametype == 1:
    # Player VS Computer Gameplay
    board.print_board()
    game_continue_condition = True
    while game_continue_condition:
        game.play_player1()
        game_continue_condition = game.check_board(1)
        if game_continue_condition:
            game.play_computer()
            game_continue_condition = game.check_board(1)
            if game_continue_condition:
                game_continue_condition = game.check_draw() #checks if the grid is full

if gametype == 2:
    # Player VS Player Gameplay
    board.print_board()
    game_continue_condition = True
    while game_continue_condition:
        game.play_player1()
        game_continue_condition = game.check_board(2)
        if game_continue_condition:
            game.play_player2()
            game_continue_condition = game.check_board(2)
            if game_continue_condition:
                game_continue_condition = game.check_draw()
