import player
import scoreboard
import bag
from tile import Tile
import random
import line


class Game:
    def __init__(self, players, tileset=None):
        self.players = players
        self.scoreboard = scoreboard.Scoreboard(players)
        self.bag = bag.Bag()
        self.tile_dict = self.bag.get_tile_dictionary()
        if tileset is not None:
            for tile in self.tile_dict:
                self.tile_dict[tile].set_image(tileset.get_tile(self.tile_dict[tile].get_shape() + self.tile_dict[tile].get_color()))
            self.empty_tile = Tile(0, '', "empty", 0, tileset.get_tile("empty"))
        else:
            self.empty_tile = Tile(0, '', '', 0)
        self.field = [[self.empty_tile for x in range(92)] for y in range(92)]
        magic_hand = random.randint(0, len(players) - 1)
        self.player_on_hand = players[magic_hand]
        self.last_move = None
        for player in players:  # new
            player.add_to_hand(self.bag.take_tiles(6))
        self.first_move = True
        self.skip_counter = 0
        self.is_game_over = False

    def get_tile_dictionary(self):
        return self.tile_dict

    def get_players(self):
        """
        Get the player objects
        """
        return self.players

    def get_player_score(self, playerID):
        """
        Get the score for the player with ID playerID
        """
        return self.scoreboard.get_score(playerID)

    def get_tiles_left(self):
        """
        Get the amount of tiles that are left in the bag
        """
        return self.bag.get_current_amount()

    def get_field(self, position=None):
        """
        Get function for field
        """
        if position is None:
            return self.field
        else:
            (x, y) = position
            return self.field[y][x]

    def set_field(self, field):
        """
        Set the gameboard to the given state
        This function should only be used for rewind purposes
        """
        self.field = field

    def get_player_on_hand(self):
        """
        Get function for current player on hand
        """
        return self.player_on_hand

    def get_game_over(self):
        """
        Get function for game over boolean
        """
        return self.is_game_over

    def get_winning_player(self):
        scores = [self.get_player_score(p.get_id()) for p in self.players]
        winner = self.players[scores.index(max(scores))]
        return winner

    def next_player(self, skip=False):
        """
        Import the current player on hand
        Add current index by 1 and respect the rules by % !! len(players) = 3 , objects has index: 0, 1, 2 !!
        Determines the new player on hand, return
        """
        if skip:
            self.skip_counter += 1
            if self.skip_counter >= len(self.players):
                self.is_game_over = True
        else:
            self.skip_counter = 0

        current_player = self.player_on_hand
        if current_player.get_hand() == []:
            self.scoreboard.change_score(current_player.get_id(), 6)  # Give six bonus points to player who finishes first
            self.is_game_over = True

        index = self.players.index(current_player)
        index += 1
        new_player = self.players[index % len(self.players)]
        self.player_on_hand = new_player
        return new_player

    def play_tiles(self, tiles, positions):
        """
        Take tiles from current players hand, trade them with bag and insert new in hand
        Every tile will be placed on corresponding position on field
        This function has 4 child functions: build_line, validate line, controle, create_line
        """
        # Save unchanged state of the board and hand, for rewind purposes
        # Needs to be COPIES of field and hand, otherwise they will change along
        # with the original and rewind will have no effect
        prev_board = [[self.get_field((x, y)) for x in range(92)] for y in range(92)]
        prev_hand = self.player_on_hand.get_hand().copy()
        prev_positions = [tile.get_position() for tile in prev_hand]

        for position, tile in zip(positions, tiles):
            (x, y) = position
            # If there is no tile already on played position
            if self.field[y][x] == self.empty_tile:
                # Place tile on position
                self.field[y][x] = tile
                tile.set_position((x, y))
            else:  # Return True if function did not succeed
                print("De gespeelde blokjes zijn ongeldig")
                self.__rewind(prev_hand, prev_board, prev_positions)
                return True

        # Build lines
        xylines = self.__build_line(tiles)

        # Remove single tile lines
        for xyline in xylines:
            if len(xyline) == 1:
                xylines.remove(xyline)
        print(f"De xy lijnen zijn: {xylines}")

        # Controle lines
        is_move_valid = self.__controle(xylines, self.first_move, tiles)

        if is_move_valid:
            print("De gespeelde blokjes zijn geldig")
            # Create lines
            line_list = self.__create_line(xylines)

            # Delete equal lines
            for i, line in enumerate(line_list):
                for line2 in line_list[i + 1::]:
                    if line.is_equal(line2):
                        line_list.remove(line2)

            print(f"De unieke lijnen zijn: {line_list}")
            # Calculate score by length of unique lines
            added_score = 0
            for line in line_list:
                added_score += line.get_length()
                if line.get_length() == 6:
                    added_score += 6
            self.scoreboard.change_score(self.player_on_hand.get_id(), added_score)

            # Update player hand
            self.player_on_hand.take_from_hand(tiles)
            amount = self.bag.get_current_amount()
            if len(tiles) <= amount:
                new_tile = self.bag.take_tiles(len(tiles))
                self.player_on_hand.add_to_hand(new_tile)
            else:
                new_tile = self.bag.take_tiles(amount)
                self.player_on_hand.add_to_hand(new_tile)

            self.player_on_hand = self.next_player()
            self.first_move = False
            # Return False if function succeeded
            return False

        else:  # If move is not valid, restart players turn
            print("De gespeelde blokjes zijn ongeldig")
            self.__rewind(prev_hand, prev_board, prev_positions)
            # Return True if function did not succeed
            return True

    def __rewind(self, prev_hand, prev_board, prev_positions):
        """
        Internal function to turn back the board and hand state en restart the players turn
        Args:
            prev_hand: Hand state to rewind to
            prev_board: Board state to rewind to
        """
        for tile, position in zip(prev_hand, prev_positions):
            tile.set_position(position)
        self.player_on_hand.set_hand(prev_hand)
        self.set_field(prev_board)

    def __build_line(self, tiles):
        """
        Build a line for every tile that will be placed on the field
        xline creates a horizontal line trough every tile
        yline creates a vertical line through every tile
        """
        xylines = []
        for tile in tiles:
            xline = []
            yline = []
            (x, y) = tile.get_position()
            t = x
            while self.get_field((t, y)) != self.empty_tile:
                tile = self.get_field((t, y))
                xline.append(tile)
                t = t + 1
            t = x -1
            while self.get_field((t, y)) != self.empty_tile:
                tile = self.get_field((t, y))
                xline.insert(0, tile)
                t = t - 1
            s = y
            while self.get_field((x, s)) != self.empty_tile:
                tile = self.get_field((x, s))
                yline.append(tile)
                s = s + 1
            s = y-1
            while self.get_field((x, s)) != self.empty_tile:
                tile = self.get_field((x, s))
                yline.insert(0, tile)
                s = s - 1
            xylines.append(xline)
            xylines.append(yline)
        return xylines

    def __validate_line(self, tiles):
        """
        Checks if a line is valid by checking their colors and shapes.
        Returns True if line is valid, False if line is invalid.
        """
        if len(tiles) > 6:  # Check if line is longer than 6 tiles
            return False  # Line is invalid
        tile_colors = [tile.get_color() for tile in tiles]  # Get lists of all colors and shapes in the line
        tile_shapes = [tile.get_shape() for tile in tiles]
        # If all colors are the same, all shapes must be unique and vice versa
        # Check if every color is unique and shape different
        if len(set(tile_colors)) == 1 and len(set(tile_shapes)) == len(
                tile_shapes):  # Based on unique elements property of set
            return True  # Line is valid
        # Check if every color is different and shape is unique
        elif len(set(tile_colors)) == len(tile_colors) and len(set(tile_shapes)) == 1:
            return True
        else:
            return False

    def __controle(self, xylines, first_move, play_tiles):
        """
        Checks if move is valid, uses above function
        """
        tile_in_board = False
        found_line = False
        for xyline in xylines:
            for tile in xyline:  # controle op minstens 1 bestaand blokje in xy lijnen
                if tile not in play_tiles:
                    tile_in_board = True
                if first_move is True:
                    tile_in_board = True
            if self.__validate_line(xyline) is False:
                print("Move not valid")
                return False

            #control if one line contains all played tiles
            i = 0
            for tile in play_tiles:
                if tile in xyline:
                    i += 1
            if i == len(play_tiles):
                found_line = True

        if tile_in_board and found_line:
            return True
        else:
            return False

    def __create_line(self, xylines):
        """
        If move is valid the line will be created by giving the start and end coordinates to the class Tile
        """
        li = []
        for xyline in xylines:
            start_tile = xyline[0]
            end_tile = xyline[-1]
            start_cord = end_tile.get_position()
            end_cord = start_tile.get_position()
            li.append( line.Line(start_cord, end_cord) )
        return li

    def switch_tiles(self, tiles):
        """
        Take tiles from current players hand, trade them with bag and insert new in hand
        """
        valid_move = False
        amount = self.bag.get_current_amount()
        if len(tiles) <= amount:
            valid_move = True
        else:
            valid_move = False

        if valid_move:
            self.player_on_hand.take_from_hand(tiles)
            new_tiles = self.bag.trade_tiles(tiles)
            self.player_on_hand.add_to_hand(new_tiles)
            self.player_on_hand = self.next_player()
            return False

        else:  # If move is not valid, restart players turn
            print("De gespeelde blokjes zijn ongeldig")
            self.player_on_hand.add_to_hand(tiles)
            return True

    def cancel(self):
        """
        Re-initial current player on hand
        """
        return self.player_on_hand
