import player
import scoreboard
import bag
import random


class Game:
    def __init__(self, players):
        self.players = players
        self.scoreboard = scoreboard.Scoreboard(players)
        self.bag = bag.Bag
        w, h = 92, 92
        self.field = [[0 for x in range(w)] for x in range(h)]

    def get_field(self):
        return self.field

    #def build(self):
    #def switch(self):


if __name__ == "__main__":
    speler1 = player.Player(1, "Stijn")
    speler2 = player.Player(2, "Laël")
    speler3 = player.Player(3, "Stan")

    spelers = [speler1, speler2, speler3]
    game = Game(spelers)

    for i in game.get_field():
        for j in i:
            print(j, end=" ")
        print()
