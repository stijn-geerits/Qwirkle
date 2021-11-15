import player
import scoreboard
import bag
import tile
import random


class Game:
    def __init__(self, players):
        self.players = players
        self.scoreboard = scoreboard.Scoreboard(players)
        self.bag = bag.Bag
        w, h = 92, 92
        self.field = [[0 for x in range(w)] for y in range(h)]
        magic_hand = random.randint(0, len(players)-1)
        self.player_on_hand = players[magic_hand]
        self.last_move = None

    def get_field(self):
        """
        Get function for field
        """
        return self.field

    def get_player_on_hand(self):
        """
        Get function for current player on hand
        """
        return self.player_on_hand

    def next_player(self):
        """
        Import the current player on hand
        Add current index by 1 and respect the rules !! len(players) = 3 , objects has index: 0, 1, 2 !!
        Determines the new player on hand, return
        """
        current_player = self.player_on_hand
        index = self.players.index(current_player)
        index += 1
        if index >= len(self.players):
            index = 0
        new_player = self.players[index]
        return new_player

    def build(self, tile, position):
        self.player_on_hand.take_from_hand(tile)

    def switch(self, tile):
        new_tile = self.bag.trade_tiles(tile)
        self.player_on_hand.take_from_hand(tile)
        self.player_on_hand.add_to_hand(new_tile)

    #def cancel(self):
    #def confirm(self):


if __name__ == "__main__":
    speler1 = player.Player(1, "Stijn")
    speler2 = player.Player(2, "Laël")
    speler3 = player.Player(3, "Stan")

    spelers = [speler1, speler2, speler3]
    game = Game(spelers)

    tile = tile.Tile(0, 'blue', 'square', (0, 0))
    game.switch(tile)

    #wijzigen speler aan de beurt
    """
    huidige_speler = game.get_player_on_hand()
    nieuwe_speler = game.next_player()
    print(huidige_speler.get_name())
    print(nieuwe_speler.get_name())
    """

    #weergeven van speelveld
    """
    for i in game.get_field():
        for j in i:
            print(j, end=" ")
        print()
    """