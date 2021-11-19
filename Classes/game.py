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

    def get_field(self,position=None):
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
        """
        self.player_on_hand.take_from_hand(tiles)
        new_tile = self.bag.trade_tiles(tiles)
        self.player_on_hand.add_to_hand(new_tile)
        for i in range(len(tiles)):
            (x, y) = positions[i]
            tile = tiles[i]
            self.field[y][x] = tile.get_id()
            tile.set_position((x, y))

    def build_line(self, tiles):
        for tile in tiles:
            (x, y) = tile.get_position()


    #def controle(self)

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

    tile1 = tile.Tile(3, 'bleu', 'star', (0, 0))
    tile2 = tile.Tile(8, 'yellow', 'circle', (0, 0))
    tiles = [tile1, tile2]
    speler1.add_to_hand(tiles)

    spelers = [speler1, speler2, speler3]
    game = Game(spelers)

    game.player_on_hand = game.players[0]
    print(speler1.get_hand())
    positions = [(5, 3), (8, 9)]
    game.play_tiles(tiles, positions)
    print(speler1.get_hand())

    print(game.get_field((8, 9)))

    # wijzigen speler aan de beurt
    """
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