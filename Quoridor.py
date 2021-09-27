# Author: Jing Liu
# Date: 8/12/2021
# Description: A class named QuoridorGame for playing a board game called Quoridor. It's a program for a two-player
#              version of the game. Each player will have 10 fences. The board is formed by 9x9 cells, and the pawn
#              will move on the cells. The fence will be placed on the edges of the cells. The four sides of the
#              board are treated as fences and no more fence should be placed on top of it. The cell coordinates are
#              expressed in (x,y) where x is the column number and y is the row numberThe board positions start with
#              (0,0) and end at (8,8). At the beginning of the game, player 1 places pawn 1 (P1) on the top center of
#              the board and player 2 places pawn 2 (P2) on the bottom center of the board. The position of P1 and P2
#              is (4,0) and (4,8) when the game begins. The four edges are labeled as fences. The row of the cells
#              where the pawns are positioned at the start of the game are called base lines. A fence is 1 cell long
#              in contrast to what you find the video and PDF saying. When each player tries to place a fence on the
#              board, the position of the fence is defined by a letter and coordinates. For vertical fences, we use v
#              and for horizontal fences, we use h. As an example, for the blue fence (vertical) in the picture, we
#              use the coordinate of the top corner to define it and for the red fence (horizontal), we use coordinate
#              of the left corner to define it.

class Player:
    """
    Represents a Player to play the Quoridor Game.
    It will communicate with the QuoridorGame class as a default private date member of QuoridorGame
    init method.
    """

    def __init__(self, player_id):
        """
        Takes the player id and initializes the new player with the pawn placed in the correct initial position.
        It will have _is_winner data member represents whether this player has won or not.
        It will have 10 initial fences for this player to use.
        """
        self._player_id = player_id
        if player_id == 1:
            self._position = (4, 0)
        elif player_id == 2:
            self._position = (4, 8)
        self._is_winner = False
        self._fence_amount = 10

    def get_player_id(self):
        """
        Returns the player's id.
        """
        return self._player_id

    def get_player_position(self):
        """
        Returns the player's position.
        """
        return self._position

    def get_is_winner(self):
        """
        Returns True is the player has won, returns False if not.
        """
        return self._is_winner

    def get_fence_amount(self):
        """
        Returns the left amount of fences for the player to use.
        """
        return self._fence_amount

    def set_player_position(self, pos_tuple):
        """
        Updates the player's position.
        """
        self._position = pos_tuple

    def set_is_winner(self):
        """
        Updates the player to winner.
        """
        self._is_winner = True

    def deduct_fence_amount(self):
        """
        Updates the fence amount.
        """
        self._fence_amount -= 1


class QuoridorGame:
    """
    Represents a QuoridorGame for playing a board game called Quoridor.
    In it's init method, it will communicate with the Player class in order to create two new Player 1 and Player 2.
    """

    def __init__(self):
        """
        Initializes the board with the fences and pawns placed in the correct positions.
        """
        self._player_1 = Player(1)
        self._player_2 = Player(2)
        self._which_turn = 1
        self._game_board = {(0, 0): ['v_fence', 'h_fence']}
        # initialize the fences on the four sides
        for index in range(1, 9):
            self._game_board[(index, 0)] = [0, 'h_fence']  # horizontal line
            self._game_board[(0, index)] = ['v_fence', 0]  # vertical line
        for index in range(0, 9):
            self._game_board[(9, index)] = ['v_fence', 0]  # vertical line
            self._game_board[(index, 9)] = [0, 'h_fence']  # horizontal line

    def _search_player(self, player_id):
        """
        A private method which takes player_id as a parameter and returns the related player object.
        """
        if self._player_1.get_player_id() == player_id:
            return self._player_1
        else:
            return self._player_2

    def move_pawn(self, player_id, pawn_aiming_address):
        """
        Takes following two parameters in order: an integer that represents which player (1 or 2) is making the
        move and a tuple with the coordinates of where the pawn is going to be moved to.
        Returns False if the move is forbidden by the rule or blocked by the fence or if the game has been already won.
        Returns True if the move was successful or if the move makes the player win.
        """
        if self._which_turn != player_id or self._if_winner_exist() is True:
            return False
        if pawn_aiming_address[0] not in range(0, 9) or pawn_aiming_address[1] not in range(0, 9):
            return False
        if self._moving_type_return(player_id, pawn_aiming_address) == "no moving type match":
            return False
        if self._moving_type_return(player_id, pawn_aiming_address) == "horizontally or vertically one cell type":
            return self._implement_h_v_one_cell_moving_type(player_id, pawn_aiming_address)
        if self._moving_type_return(player_id, pawn_aiming_address) == "jump moving two cells type":
            return self._implement_jump_moving_two_cells_moving_type(player_id, pawn_aiming_address)
        if self._moving_type_return(player_id, pawn_aiming_address) == "diagonally move one cell type":
            return self._implement_diagonally_move_one_cell_moving_type(player_id, pawn_aiming_address)

    def _h_v_possible_aiming_address(self, player_id):
        """
        A private method which takes player_id as a parameter and returns the possible position if the player decides
        to move only vertically or horizontally.
        """
        curr_pos = self._search_player(player_id).get_player_position()
        curr_pos_x = curr_pos[0]
        curr_pos_y = curr_pos[1]
        pos_u = (curr_pos_x, curr_pos_y - 1)
        pos_r = (curr_pos_x + 1, curr_pos_y)
        pos_d = (curr_pos_x, curr_pos_y + 1)
        pos_l = (curr_pos_x - 1, curr_pos_y)
        return pos_u, pos_r, pos_d, pos_l

    def _jump_moving_two_cells_aiming_address(self, player_id):
        """
        A private method which takes player_id as a parameter and returns the possible position if the player decides
        to move in the jumping over pawn way.
        """
        curr_pos = self._search_player(player_id).get_player_position()
        curr_pos_x = curr_pos[0]
        curr_pos_y = curr_pos[1]
        pos_u = (curr_pos_x, curr_pos_y - 2)
        pos_r = (curr_pos_x + 2, curr_pos_y)
        pos_d = (curr_pos_x, curr_pos_y + 2)
        pos_l = (curr_pos_x - 2, curr_pos_y)
        return pos_u, pos_r, pos_d, pos_l

    def _diagonally_move_one_cell_aiming_address(self, player_id):
        """
        A private method which takes player_id as a parameter and returns the possible position if the player decides
        to move diagonally.
        """
        curr_pos = self._search_player(player_id).get_player_position()
        curr_pos_x = curr_pos[0]
        curr_pos_y = curr_pos[1]
        pos_ur = (curr_pos_x + 1, curr_pos_y - 1)
        pos_rd = (curr_pos_x + 1, curr_pos_y + 1)
        pos_dl = (curr_pos_x - 1, curr_pos_y + 1)
        pos_lu = (curr_pos_x - 1, curr_pos_y - 1)
        return pos_ur, pos_rd, pos_dl, pos_lu

    def _moving_type_return(self, player_id, pawn_aiming_address):
        """
        A private method which takes player_id and its aiming address tuple and returns what kind of moving type this
        player behaves.
        It contains three moving types: "horizontally or vertically one cell type", "jump moving two cells type", and
        "diagonally move one cell type". If there is no moving type match, returns "no moving type match".
        """
        if pawn_aiming_address in self._h_v_possible_aiming_address(player_id):
            return "horizontally or vertically one cell type"
        if pawn_aiming_address in self._jump_moving_two_cells_aiming_address(player_id):
            return "jump moving two cells type"
        if pawn_aiming_address in self._diagonally_move_one_cell_aiming_address(player_id):
            return "diagonally move one cell type"
        return "no moving type match"

    def _which_direction(self, player_id, pawn_aiming_address):
        """
        A private method which takes player_id and its aiming address tuple and returns what kind of moving direction
        this player behaves. It contains eight kinds of moving directions: 'u', 'r', 'd', 'l', ('u', 'r'), ('r', 'd'),
        ('d', 'l'), ('l', 'u')
        """
        curr_pos = self._search_player(player_id).get_player_position()
        if pawn_aiming_address[1] < curr_pos[1] and pawn_aiming_address[0] == curr_pos[0]:
            return 'u'
        if pawn_aiming_address[0] > curr_pos[0] and pawn_aiming_address[1] == curr_pos[1]:
            return 'r'
        if pawn_aiming_address[1] > curr_pos[1] and pawn_aiming_address[0] == curr_pos[0]:
            return 'd'
        if pawn_aiming_address[0] < curr_pos[0] and pawn_aiming_address[1] == curr_pos[1]:
            return 'l'
        if pawn_aiming_address[0] > curr_pos[0] and pawn_aiming_address[1] < curr_pos[1]:
            return 'u', 'r'
        if pawn_aiming_address[0] > curr_pos[0] and pawn_aiming_address[1] > curr_pos[1]:
            return 'r', 'd'
        if pawn_aiming_address[0] < curr_pos[0] and pawn_aiming_address[1] > curr_pos[1]:
            return 'd', 'l'
        if pawn_aiming_address[0] < curr_pos[0] and pawn_aiming_address[1] < curr_pos[1]:
            return 'l', 'u'

    def _winner_trigger(self, player_id):
        """
        A private method which takes player_id returns whether this player satisfies the winner condition.
        """
        if player_id == 1:
            player_1_pos = self._search_player(player_id).get_player_position()
            if player_1_pos[0] in range(0, 9) and player_1_pos[1] == 8:
                return True
        if player_id == 2:
            player_2_pos = self._search_player(player_id).get_player_position()
            if player_2_pos[0] in range(0, 9) and player_2_pos[1] == 0:
                return True
        return False

    def _implement_h_v_one_cell_moving_type(self, player_id, pawn_aiming_address):
        """
        A private method which takes player_id and its aiming address tuple and implement the returns the
        "horizontally or vertically one cell type" move.
        Returns False if the move is forbidden by the rule or blocked by the fence or if the game has been already won.
        Returns True if the move was successful or if the move makes the player win.
        """
        curr_player = self._search_player(player_id)
        curr_pos = curr_player.get_player_position()
        direction = self._which_direction(player_id, pawn_aiming_address)
        if pawn_aiming_address == self._player_1.get_player_position():
            return False
        if pawn_aiming_address == self._player_2.get_player_position():
            return False
        if direction == 'u':
            if self._if_fence_exist(curr_pos, 'h'):
                return False
        if direction == 'r':
            if self._if_fence_exist(pawn_aiming_address, 'v'):
                return False
        if direction == 'd':
            if self._if_fence_exist(pawn_aiming_address, 'h'):
                return False
        if direction == 'l':
            if self._if_fence_exist(curr_pos, 'v'):
                return False
        curr_player.set_player_position(pawn_aiming_address)
        self._update_player_track()
        if self._winner_trigger(player_id) is True:
            curr_player.set_is_winner()
        return True

    def _oppo_player(self, player_id):
        """
        A private method which takes player_id and returns the opposite player object of said player
        """
        if player_id == 1:
            return self._player_2
        if player_id == 2:
            return self._player_1

    def _one_cell_pos(self, direction, curr_pos):
        """
        A private method which takes a direction and a position and returns the coordinate tuple next to the said
        position (in the given direction).
        """
        pos_x = curr_pos[0]
        pos_y = curr_pos[1]
        if direction == 'u':
            return pos_x, pos_y - 1
        if direction == ('u', 'r'):
            return pos_x + 1, pos_y - 1
        if direction == 'r':
            return pos_x + 1, pos_y
        if direction == ('r', 'd'):
            return pos_x + 1, pos_y + 1
        if direction == 'd':
            return pos_x, pos_y + 1
        if direction == ('d', 'l'):
            return pos_x - 1, pos_y + 1
        if direction == 'l':
            return pos_x - 1, pos_y
        if direction == ('l', 'u'):
            return pos_x - 1, pos_y - 1

    def _implement_jump_moving_two_cells_moving_type(self, player_id, aim_address):
        """
        A private method which takes player_id and its aiming address tuple and implement the returns the
        "jump moving two cells type" move.
        Returns False if the move is forbidden by the rule or blocked by the fence or if the game has been already won.
        Returns True if the move was successful or if the move makes the player win.
        """
        curr_player = self._search_player(player_id)
        oppo_player = self._oppo_player(player_id)
        curr_pos = curr_player.get_player_position()
        direction = self._which_direction(player_id, aim_address)
        if direction == 'u':
            if self._if_fence_exist(curr_pos, 'h') or self._if_fence_exist(self._one_cell_pos('u', curr_pos), 'h'):
                return False
        if direction == 'r':
            if self._if_fence_exist(self._one_cell_pos('r', curr_pos), 'v') or self._if_fence_exist(aim_address, 'v'):
                return False
        if direction == 'd':
            if self._if_fence_exist(self._one_cell_pos('d', curr_pos), 'h') or self._if_fence_exist(aim_address, 'h'):
                return False
        if direction == 'l':
            if self._if_fence_exist(curr_pos, 'v') or self._if_fence_exist(self._one_cell_pos('l', curr_pos), 'v'):
                return False
        if aim_address == oppo_player.get_player_position():
            return False
        if self._one_cell_pos(direction, curr_pos) == oppo_player.get_player_position():
            curr_player.set_player_position(aim_address)
            self._update_player_track()
            if self._winner_trigger(player_id) is True:
                curr_player.set_is_winner()
            return True
        return False

    def _implement_diagonally_move_one_cell_moving_type(self, player_id, pawn_aiming_address):
        """
        A private method which takes player_id and its aiming address tuple and implement the returns the
        "diagonally move one cell type" move.
        Returns False if the move is forbidden by the rule or blocked by the fence or if the game has been already won.
        Returns True if the move was successful or if the move makes the player win.
        """
        curr_player = self._search_player(player_id)
        oppo_player = self._oppo_player(player_id)
        curr_pos = curr_player.get_player_position()
        direction = self._which_direction(player_id, pawn_aiming_address)
        condition_1 = self._one_cell_pos(direction[0], curr_pos) == oppo_player.get_player_position()
        condition_2 = self._one_cell_pos(direction[1], curr_pos) == oppo_player.get_player_position()
        if (condition_1 or condition_2) is not True:
            return False
        if self._which_direction(player_id, oppo_player.get_player_position()) == 'u':
            if not self._if_fence_exist(oppo_player.get_player_position(), 'h'):
                return False
        if self._which_direction(player_id, oppo_player.get_player_position()) == 'r':
            if not self._if_fence_exist(pawn_aiming_address, 'v'):
                return False
        if self._which_direction(player_id, oppo_player.get_player_position()) == 'd':
            if not self._if_fence_exist(pawn_aiming_address, 'h'):
                return False
        if self._which_direction(player_id, oppo_player.get_player_position()) == 'l':
            if not self._if_fence_exist(oppo_player.get_player_position(), 'v'):
                return False
        curr_player.set_player_position(pawn_aiming_address)
        self._update_player_track()
        if self._winner_trigger(player_id) is True:
            curr_player.set_is_winner()
        return True

    def _if_fence_exist(self, address_tuple, v_or_h):
        """
        A private method which takes a certain address and "vertical" or "horizontal" fence and returns whether there
        is a "vertical" or "horizontal" fence exists in that place.
        """
        if address_tuple in self._game_board:
            if v_or_h == 'v':
                if self._game_board[address_tuple][0] == 'v_fence':
                    return True
            elif v_or_h == 'h':
                if self._game_board[address_tuple][1] == 'h_fence':
                    return True
        return False

    def _if_winner_exist(self):
        """
        A private method which returns whether there's a winner exist in current game.
        """
        if self.is_winner(1) is True or self.is_winner(2) is True:
            return True
        return False

    def _update_player_track(self):
        """
        A private method which updates the track to the next player.
        """
        if self._which_turn == 1:
            self._which_turn = 2
        else:
            self._which_turn = 1

    def place_fence(self, player_id, v_or_h, fence_aiming_address):
        """
        Takes following parameters in order: an integer that represents which player (1 or 2) is making the move,
        a letter indicating whether it is vertical (v) or horizontal (h) fence, a tuple of integers that represents
        the position on which the fence is to be placed.
        Returns False if player has no fence left, or if the fence is out of the boundaries of the board,
        or if there is already a fence there and the new fence will overlap or intersect with the existing fence.
        Returns False if the game has been already won.
        Returns True if the fence can be placed.
        Returns exactly the string "breaks the fair play rule" if it breaks the fair-play rule.
        """
        curr_player = self._search_player(player_id)
        if self._which_turn != player_id:
            return False
        if curr_player.get_fence_amount() <= 0 or self._if_winner_exist() is True:
            return False
        if fence_aiming_address[0] not in range(0, 9) or fence_aiming_address[1] not in range(0, 9):
            return False
        if self._if_fence_exist(fence_aiming_address, v_or_h) is True:
            return False
        if self._if_break_fair_play_rule(player_id, v_or_h, fence_aiming_address):
            return 'breaks the fair play rule'
        self._update_player_track()
        curr_player.deduct_fence_amount()
        if fence_aiming_address not in self._game_board:
            if v_or_h == 'v':
                self._game_board[fence_aiming_address] = ['v_fence', 0]
            elif v_or_h == 'h':
                self._game_board[fence_aiming_address] = [0, 'h_fence']
        else:
            if v_or_h == 'v':
                self._game_board[fence_aiming_address][0] = 'v_fence'
            elif v_or_h == 'h':
                self._game_board[fence_aiming_address][1] = 'h_fence'
        return True

    def is_winner(self, player_id):
        """
        Takes a single integer representing the player number as a parameter and returns True if that player has won
        and False if that player has not won.
        """
        if self._search_player(player_id).get_is_winner() is True:
            return True
        else:
            return False

    def print_board(self):
        """
        Prints the board
        """
        for co_y in range(0, 9):
            for co_x in range(0, 9):
                print('+', end='')
                if (co_x, co_y) in self._game_board and self._game_board[(co_x, co_y)][1] == 'h_fence':
                    print('==', end='')
                else:
                    print('  ', end='')
                if (co_x + 1) == 9:
                    print('+')
                    for cell in range(0, 9):
                        if (cell, co_y) in self._game_board and self._game_board[(cell, co_y)][0] == 'v_fence':
                            print('|', end='')
                        else:
                            print(' ', end='')
                        if self._player_1.get_player_position() == (cell, co_y):
                            print('P1', end='')
                        elif self._player_2.get_player_position() == (cell, co_y):
                            print('P2', end='')
                        else:
                            print('  ', end='')
                        if cell + 1 == 9:
                            print('|')
        print("+==+==+==+==+==+==+==+==+==+")

    def _if_break_fair_play_rule(self, player_id, v_or_h, fence_aiming_address):
        """
        Takes following parameters in order: an integer that represents which player (1 or 2) is making the move,
        a letter indicating whether it is vertical (v) or horizontal (h) fence, a tuple of integers that represents
        the position on which the fence is to be placed.
        Returns if this action will result in 'breaks the fair play rule'.
        """
        oppo_player = 2 if player_id == 1 else 1
        if fence_aiming_address not in self._game_board:
            if v_or_h == 'v':
                self._game_board[fence_aiming_address] = ['v_fence', 0]
                if self._if_no_room_left_for_this_player(oppo_player) is True:
                    del self._game_board[fence_aiming_address]
                    return True
                del self._game_board[fence_aiming_address]
                return False
            elif v_or_h == 'h':
                self._game_board[fence_aiming_address] = [0, 'h_fence']
                if self._if_no_room_left_for_this_player(oppo_player) is True:
                    del self._game_board[fence_aiming_address]
                    return True
                del self._game_board[fence_aiming_address]
                return False
        else:
            if v_or_h == 'v':
                self._game_board[fence_aiming_address][0] = 'v_fence'
                if self._if_no_room_left_for_this_player(oppo_player) is True:
                    self._game_board[fence_aiming_address] = [0, 'h_fence']
                    return True
                self._game_board[fence_aiming_address] = [0, 'h_fence']
                return False
            elif v_or_h == 'h':
                self._game_board[fence_aiming_address][1] = 'h_fence'
                if self._if_no_room_left_for_this_player(oppo_player) is True:
                    self._game_board[fence_aiming_address] = ['v_fence', 0]
                    return True
                self._game_board[fence_aiming_address] = ['v_fence', 0]
                return False

    def _remain_invisible_fences_face_to_current_player(self, player_id):
        """
        A private method which takes player_id and returns a list which contains all the horizontal lines in front of
        the current player.
        """
        remain_list = []
        curr_pos = self._search_player(player_id).get_player_position()
        pos_x = curr_pos[0]
        pos_y = curr_pos[1]
        if player_id == 1:
            for remain_y in range(pos_y + 1, 9):
                remain_list.append((pos_x, remain_y))
        if player_id == 2:
            for remain_y in range(pos_y, 0, -1):
                remain_list.append((pos_x, remain_y))
        return remain_list

    def _all_the_fences_address_face_to_current_player(self, player_id):
        """
        A private method which takes player_id and returns a list which contains all the fences address right in front
        of the current player.
        """
        fences_address_list = []
        for fence_address in self._remain_invisible_fences_face_to_current_player(player_id):
            if self._if_fence_exist(fence_address, 'h') is True:
                fences_address_list.append(fence_address)
        return fences_address_list

    def _return_fences_vertices_related_to_fence_address(self, fence_address, left_vertex=None, used_vertex=None):
        """
        A private method which takes fence_address and returns a set contains all the vertices of the fences address
        related to the chosen fence in a recursion way.
        """
        pos_x = fence_address[0]
        pos_y = fence_address[1]
        if used_vertex is None and left_vertex is None:
            left_vertex = [fence_address]
            used_vertex = set()
        if self._if_fence_exist(fence_address, 'h') is True:
            if fence_address[0] in range(0, 9) and fence_address[1] in range(0, 9):
                if (pos_x+1, pos_y) not in left_vertex and (pos_x+1, pos_y) not in used_vertex:
                    left_vertex.append((pos_x+1, pos_y))
        if self._if_fence_exist(fence_address, 'v') is True:
            if fence_address[0] in range(0, 9) and fence_address[1] in range(0, 9):
                if (pos_x, pos_y+1) not in left_vertex and (pos_x, pos_y+1) not in used_vertex:
                    left_vertex.append((pos_x, pos_y+1))
        if self._if_fence_exist((pos_x-1, pos_y), 'h') is True:
            if fence_address[0] in range(0, 9) and fence_address[1] in range(0, 9):
                if (pos_x-1, pos_y) not in left_vertex and (pos_x-1, pos_y) not in used_vertex:
                    left_vertex.append((pos_x-1, pos_y))
        if self._if_fence_exist((pos_x, pos_y-1), 'v') is True:
            if fence_address[0] in range(0, 9) and fence_address[1] in range(0, 9):
                if (pos_x, pos_y-1) not in left_vertex and (pos_x, pos_y-1) not in used_vertex:
                    left_vertex.append((pos_x, pos_y-1))
        left_vertex.remove(fence_address)
        used_vertex.add(fence_address)
        if left_vertex:
            self._return_fences_vertices_related_to_fence_address(left_vertex[0], left_vertex, used_vertex)
        return used_vertex

    def _if_no_room_left_for_this_player(self, player_id):
        """
        A private method which takes player_id and returns if the access to the goal line of current player is
        left open.
        """
        possible_list = [] # [{(), ()....}, {(),(),.....}, {(),(),.....}, {(),(),.....}]
        if player_id == 2:
            remain_fence = self._all_the_fences_address_face_to_current_player(2)
            if not remain_fence:
                return False
            else:
                for fence_address in remain_fence:
                    possible_list.append(self._return_fences_vertices_related_to_fence_address(fence_address))
                for a_set in possible_list:
                    for fence_vertex in a_set:
                        if fence_vertex[0] == 0:
                            return True
            return False
        if player_id == 1:
            remain_fence = self._all_the_fences_address_face_to_current_player(1)
            if not remain_fence:
                return False
            else:
                for fence_address in remain_fence:
                    possible_list.append(self._return_fences_vertices_related_to_fence_address(fence_address))
                for a_set in possible_list:
                    for fence_vertex in a_set:
                        if fence_vertex[0] == 9:
                            return True
            return False

# Unittest, simple display with un-rendered board
game_1 = QuoridorGame()
game_1.place_fence(1,'h',(4,1))
game_1.place_fence(1,'h',(4,2))
game_1.place_fence(2,'v',(4,1))
game_1.place_fence(1,'v',(4,2))
game_1.place_fence(2,'v',(4,9))
game_1.place_fence(2,'h',(8,8))
game_1.move_pawn(1, (3, 0))
game_1.move_pawn(2, (4, 7))
game_1.move_pawn(1, (3, 1))
game_1.move_pawn(2, (4, 6))
game_1.move_pawn(1, (3, 2))
game_1.move_pawn(2, (4, 5))
game_1.place_fence(1, 'v', (3, 3))
game_1.move_pawn(2, (4, 4))
game_1.move_pawn(1, (3, 3))
game_1.place_fence(2, 'h', (4, 3))
game_1.place_fence(1, 'h', (3, 3))
game_1.move_pawn(2, (4, 3))
game_1.move_pawn(1, (5, 3))
game_1.move_pawn(2, (4, 4))
game_1.place_fence(1, 'h', (3, 1))
game_1.place_fence(2, 'h', (2, 1))
game_1.place_fence(1, 'h', (1, 1))
game_1.place_fence(2, 'h', (7, 5))
print(game_1.place_fence(1, 'h', (0, 1)))
game_1.place_fence(1, 'h', (6, 4))
game_1.place_fence(2, 'h', (8, 5))
game_1.move_pawn(1, (6, 3))
game_1.place_fence(2, 'v', (6, 3))
game_1.move_pawn(1, (6, 2))
print(game_1.place_fence(2, 'v', (7, 4)))
print(game_1.move_pawn(2, (4, 3)))
print(game_1.move_pawn(1, (5, 2)))
print(game_1.move_pawn(2, (5, 3)))
print(game_1.place_fence(1, 'h', (5, 2)))
print(game_1.move_pawn(2, (6, 2)))
print(game_1.move_pawn(1, (5, 3)))
print(game_1.move_pawn(2, (6, 1)))
print(game_1.place_fence(1, 'h', (0, 1)))
print(game_1.move_pawn(2, (6, 0)))
print(game_1.move_pawn(1, (5, 4)))

game_1.print_board()
