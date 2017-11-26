import random
import os

PLAYER1_COIN = 'X'
PLAYER2_COIN = 'O'
COMPUTER_COIN = 'O'
EMPTY_SPACE = '_'

# STANDALONE FUNCTIONS

def cls():
    # Clears the command line screen
    os.system('cls' if os.name=='nt' else 'clear')

def create_slots():
    # Asks user number of slots she wants to create for her board
    # Returns number_of_slots (int)
    while True:
        try:
            number_of_slots = int(input('Enter the number of slots [min: 4, max: 9]: '))
        except Exception:
            continue
        else:
            if number_of_slots < 4 or number_of_slots > 9:
                continue
            else:
                return number_of_slots

def create_depth():
    # Asks user depth of each slot she wants to create for her board
    # Returns depth_of_slots (int)
    while True:
        try:
            depth_of_slots = int(input('Enter the depth of each slot [min: 4, max: 9]: '))
        except Exception:
            continue
        else:
            if depth_of_slots < 4 or depth_of_slots > 9:
                continue
            else:
                return depth_of_slots

def choose_gametype():
    # Asks user to choose the gametype (against computer or player 2, that is)
    # Returns user_choice (int)
    valid = False
    user_choice = 0
    while not valid:
        try:
            user_choice = int(input())
        except Exception:
            pass
        if user_choice == 1 or user_choice == 2:
            valid = True
        else:
            print("Invalid input. Please only enter either [1] or [2]:")
    return user_choice


# CLASSES
class Board():
    """Game Board
    Methods:
        print_board()
    """

    def __init__(self, slots, depth):
        """Creates a new board
        Kwargs:
            slots(int) = number of slots (fixed)
            depth(int) = depth of each slot (fixed)
            content(list) = content of board (fixed)
        """
        self.slots = slots
        self.depth = depth
        self.content = []
        for x in range(self.depth):
            self.content.append(list(EMPTY_SPACE * self.slots))

    def print_board(self):
        # Prints board on the command line
        print('CONNECT4 - DOS EDITION')
        print('––––––––––––––––––––––\n')
        slot_indicator = ''
        for x in range(1, self.slots + 1):
            slot_indicator += ' ' + str(x)
        print(' ' * ((22 - self.slots * 2) // 2 - 1) + slot_indicator)
        for x in range(self.depth):
            print(' ' * ((22 - self.slots * 2) // 2) + ' '.join(self.content[x]))
        print(' ')
        print('––––––––––––––––––––––\n')

class Gameplay():
    """Gameplay
    Methods:
        ask_players_turn()
        process_players_turn()
        play_player1()
        play_player2()
        play_computer()
        horizantal_check()
        vertical_check()
        diagonal_check_fromleft()
        diagonal_check_fromright()
        check_who_won()
        check_board()
        check_draw()
    """

    def __init__ (self, board):
        """Creates a gameplay
        Args:
            board (list)
        """
        self.board = board

    # GAME-PLAYING METHODS
    def ask_players_turn(self, players_number):
        # Collects input from user for his current turn. Determines in which slot user drops her coin
        # Returns players_turn (int)
        while True:
            try:
                players_turn = int(input('PLAYER %s\'S TURN \n' %str(players_number) + 'Pick a slot to drop your coin: '))
            except Exception:
                print('There is no such slot. Try again.')
                pass
            else:
                if players_turn in range(1, self.board.slots + 1):
                    return players_turn
                else:
                    print('There is no such slot. Try again.')

    def process_players_turn(self, coin_number, coin_type):
        # Checks the already filled spaces in the board and places players coin in the right place
        # Changes the content of the game board (list) as a result
        x = self.board.depth - 1
        while True:
            try:
                if self.board.content[x][coin_number - 1] == EMPTY_SPACE:
                    self.board.content[x][coin_number - 1] = coin_type
                    break
                else:
                    x -= 1
            except Exception:
                if coin_type == PLAYER1_COIN:
                    self.play_player1()
                    break
                elif coin_type == PLAYER2_COIN:
                    self.play_player2()
                    break

    def play_player1(self):
        # Brings together two functions to process one full turn for player 1
        # Clears and reprints the board afterwards for the next turn
        current_coin = self.ask_players_turn(1)
        self.process_players_turn(current_coin, PLAYER1_COIN)
        cls()
        self.board.print_board()

    def play_player2(self):
        # Brings together two functions to process one full turn for player 2
        # Clears and reprints the board afterwards for the next turn
        current_coin = self.ask_players_turn(2)
        self.process_players_turn(current_coin, PLAYER2_COIN)
        cls()
        self.board.print_board()

    def play_computer(self):
        # Processes one full turn for computer
        # Changes the content of the game board (list)
        # Clears and reprints the board afterwards for the next turn
        n = random.randrange(self.board.slots)
        m = self.board.depth - 1
        while True:
            if m >= 0:
                try:
                    if self.board.content[m][n] == EMPTY_SPACE:
                        self.board.content[m][n] = COMPUTER_COIN
                        break
                    else:
                        m -= 1
                except Exception:
                    pass
            else:
                n = random.randrange(self.board.slots)
                m = self.board.depth - 1
        cls()
        self.board.print_board()

    # RESULT-CHECKING FUNCTIONS
    def horizantal_check(self):
        # Creates a string to check the board horizantally and calls it 'horizantal_board'
        # Returns horizantal_board
        horizantal_board = ''
        for x in range(self.board.depth):
            horizantal_board += ' ' #seperates each line for accurate checking
            for y in range(self.board.slots):
                horizantal_board += self.board.content[x][y]
        return horizantal_board

    def vertical_check(self):
        # Creates a string to check the board vertically and calls it 'vertical_board'
        # Returns vertical_board
        vertical_board = ''
        for x in range(self.board.slots):
            vertical_board += ' ' #seperates each line for accurate checking
            for y in range(self.board.depth):
                vertical_board += self.board.content[y][x]
        return vertical_board

    def diagonal_check_fromleft(self):
        # Creates a string to check the board diagonally from left to right and calls it 'diagonal_board_fromleft'
        # Returns diagonal_board_fromleft
        diagonal_board_fromleft = ''

        # for upper-right section from the middle
        for n in range(self.board.slots):
            x = 0
            y = 0
            diagonal_board_fromleft += ' ' #seperates each line for accurate checking
            while x in range(self.board.depth) and y in range(self.board.slots):
                    try:
                        diagonal_board_fromleft += self.board.content[x][y + n]
                    except Exception:
                        pass
                    x += 1
                    y += 1
        # for lower-left section from the middle
        for n in range(self.board.depth):
            x = 0
            y = 0
            diagonal_board_fromleft += ' ' #seperates each line for accurate checking
            while x in range(self.board.depth) and y in range(self.board.slots):
                    try:
                        diagonal_board_fromleft += self.board.content[x + n][y]
                    except Exception:
                        pass
                    x += 1
                    y += 1
        return diagonal_board_fromleft

    def diagonal_check_fromright(self):
        # Creates a string to check the board diagonally from righ to left and calls it 'diagonal_board_fromright'
        # Returns diagonal_board_fromright
        diagonal_board_fromright = ''

        # for upper-left section from the middle
        for n in range(self.board.slots):
            x = 0
            y = self.board.slots - 1
            diagonal_board_fromright += ' ' #seperates each line for accurate checking
            while x in range(self.board.depth) and y in range(self.board.slots):
                    try:
                        if y - n >= 0:
                            diagonal_board_fromright += self.board.content[x][y - n]
                    except Exception:
                        pass
                    x += 1
                    y -= 1
        # for lower-right section from the middle
        for n in range(self.board.depth):
            x = 0
            y = self.board.slots - 1
            diagonal_board_fromright += ' ' #seperates each line for accurate checking
            while x in range(self.board.depth) and y in range(self.board.slots):
                    try:
                        diagonal_board_fromright += self.board.content[x + n][y]
                    except Exception:
                        pass
                    x += 1
                    y -= 1
        return diagonal_board_fromright

    def check_who_won(self, gametype, board_name):
        # Checks if any player has 4 coins aligned consecutively in a given board, according to the given gametype
        # Returns a boolean
        if gametype == 1:
            if PLAYER1_COIN * 4 in board_name:
                print('YOU WON!')
                return False
            elif COMPUTER_COIN * 4 in board_name:
                print('YOU LOST!')
                return False
            else:
                return True
        if gametype == 2:
            if PLAYER1_COIN * 4 in board_name:
                print('PLAYER 1 WON!')
                return False
            elif PLAYER2_COIN * 4 in board_name:
                print('PLAYER 2 WON!')
                return False
            else:
                return True

    def check_board(self, gametype):
        # Checks the whole board according to the given gametype, to decide if game should continue or not
        # Returns a boolean
        game_continue_condition = self.check_who_won(gametype, self.horizantal_check())
        if game_continue_condition:
            game_continue_condition = self.check_who_won(gametype, self.vertical_check())
            if game_continue_condition:
                game_continue_condition = self.check_who_won(gametype, self.diagonal_check_fromleft())
                if game_continue_condition:
                    game_continue_condition = self.check_who_won(gametype, self.diagonal_check_fromright())
        return game_continue_condition

    def check_draw(self):
        # Checks if there is any EMPTY_SPACE left in the board, to decide if the game is ended with a draw
        # Returns a boolean
        draw_check_board = ''
        for x in range(self.board.depth):
            for y in range(self.board.slots):
                draw_check_board += self.board.content[x][y]
        draw_check_condition = True
        while draw_check_condition:
            for x in draw_check_board:
                if x == EMPTY_SPACE:
                    draw_check_condition: True
                    return True
                    break
            else:
                draw_check_condition: True
                print('DRAW!')
                return False
