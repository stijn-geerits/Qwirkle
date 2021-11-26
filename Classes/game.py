import player
import scoreboard
import bag
import tile
import random
import line


class Game:
    def __init__(self, players):
        self.players = players
        self.scoreboard = scoreboard.Scoreboard(players)
        self.bag = bag.Bag()
        self.field = [[0 for x in range(92)] for y in range(92)]
        magic_hand = random.randint(0, len(players) - 1)
        self.player_on_hand = players[magic_hand]
        self.last_move = None
        for player in players:  # new
            player.add_to_hand(self.bag.take_tiles(6))

    def get_field(self, position=None):
        """
        Get function for field
        """
        if position is None:
            return self.field
        else:
            (x, y) = position
            return self.field[y][x]

    def get_player_on_hand(self):
        """
        Get function for current player on hand
        """
        return self.player_on_hand

    def next_player(self):
        """
        Import the current player on hand
        Add current index by 1 and respect the rules by % !! len(players) = 3 , objects has index: 0, 1, 2 !!
        Determines the new player on hand, return
        """
        current_player = self.player_on_hand
        index = self.players.index(current_player)
        index += 1
        new_player = self.players[index % len(self.players)]
        return new_player

    def play_tiles(self, tiles, positions):
        """
        Take tiles from current players hand, trade them with bag and insert new in hand
        Every tile will be placed on corresponding position on field
        This function has 4 child functions: build_line, validate line, controle, create_line
        """
        self.player_on_hand.take_from_hand(tiles)
        new_tile = self.bag.trade_tiles(tiles)
        self.player_on_hand.add_to_hand(new_tile)
        for i in range(len(tiles)):
            (x, y) = positions[i]
            tile = tiles[i]
            self.field[y][x] = tile.get_id()
            tile.set_position((x, y))

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
            (x, y) = tile.get_position(tile)
            t = x
            while self.get_field((t, y)) != 0:
                tile = self.get_field((t, y))
                xline.append(tile)
                t = t + 1
            t = x -1
            while self.get_field((t, y)) != 0:
                tile = self.get_field((t, y))
                xline.insert(0, tile)
                t = t - 1
            s = y
            while self.get_field((x, s)) != 0:
                tile = self.get_field((x, s))
                yline.append(tile)
                s = s + 1
            s = y-1
            while self.get_field((x, s)) != 0:
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

    def __controle(self, xylines):
        """
        Checks if move is valid, uses above function
        """
        for xyline in xylines:
            if self.__validate_line(xyline) is False:
                print("Move not valid")
                return False
        return True

    def __create_line(self, xylines):
        """
        If move is valid the line will be created by giving the start and end coordinates to the class Tile
        """
        for xyline in xylines:
            start_tile = xyline[0]
            end_tile = xyline[-1]
            start_cord = end_tile.get_position()
            end_cord = start_tile.get_position()
            li = line.Line(start_cord, end_cord)
        return li

    def switch_tiles(self, tiles):
        """
        Take tiles from current players hand, trade them with bag and insert new in hand
        """
        self.player_on_hand.take_from_hand(tiles)
        new_tiles = self.bag.trade_tiles(tiles)
        self.player_on_hand.add_to_hand(new_tiles)

    def cancel(self):
        """
        Re-initial current player on hand
        """
        return self.player_on_hand


if __name__ == "__main__":
    speler1 = player.Player(1, "Stijn")
    speler2 = player.Player(2, "Laël")
    speler3 = player.Player(3, "Stan")
    game = Game([speler1, speler2, speler3])

    while True:
        tiles = []
        for tile in player.Player.get_hand(game.player_on_hand):
            tiles.append(tile.get_id())
        print(player.Player.get_name(game.player_on_hand)+" jij bent aan de beurt."+"\n"+"Dit is jouw hand: "+str(tiles)
              + "\n"+"Maak een keuze:"+"\n"+"1: Aanleggen"+"\n"+"2: Ruilen")

        correct = False
        while not correct:
            keuze = int(input())
            if keuze == 1:
                correct = True
                print("Je koos voor aanleggen.")
                print("Geef de id's van de blokjes en hun locaties die je wil plaatsen."+"\n"+"bv: 15;(3,5);25;(6,9)")
                invoer = str(input())
                invoer = invoer.split(";")
                blokjes = invoer[::2]
                hand = player.Player.get_hand(game.player_on_hand)
                blokken = []
                print(blokjes)
                print(tiles)
                for blokje in blokjes:
                    if blokje in tiles:
                        index = tiles.index(blokje)
                        blokken.append(hand[index])
                locaties = invoer[1::2]
                print(blokken)
                print(locaties)
                game.play_tiles(blokken, locaties)

            elif keuze == 2:
                correct = True
                print("Je koos voor ruilen.")

            else:
                print("Foute invoer.")

        """
        # blokjes leggen op speelveld
        game.player_on_hand = game.players[0]
        print(speler1.get_hand())
        positions = [(5, 3), (8, 9)]
        game.play_tiles(tiles, positions)
        print(speler1.get_hand())
        print(game.get_field((8, 9)))
        """
        """
        # wijzigen speler aan de beurt
        huidige_speler = game.get_player_on_hand()
        nieuwe_speler = game.next_player()
        print(huidige_speler.get_name())
        print(nieuwe_speler.get_name())
        """
        """
        # weergeven van speelveld
        for i in game.get_field():
            print(*i)
        """