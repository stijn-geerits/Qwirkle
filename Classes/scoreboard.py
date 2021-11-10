class Scoreboard:
    def __init__(self, player):
        self.player = player
        self.score = 0

    def change_score(self, value):
        """
        Add given VALUE to player's score
        """
        current_score = self.score
        new_score = current_score + value
        self.score = new_score

    def get_score(self):
        """
        Get function for player's score
        """
        return self.score


# test
if __name__ == "__main__":
    import player
    speler1 = player.Player(1, "Stijn")
    speler2 = player.Player(2, "Laël")
    speler3 = player.Player(3, "Stan")

    bord1 = Scoreboard(speler1)
    bord2 = Scoreboard(speler2)
    bord3 = Scoreboard(speler3)
    print("Begin score van " + speler1.get_name() + " : " + str(bord1.get_score()))
    print("Begin score van " + speler2.get_name() + " : " + str(bord2.get_score()))
    print("Begin score van " + speler3.get_name() + " : " + str(bord3.get_score()))

    # ronde1
    bord1.change_score(100)
    bord2.change_score(200)
    bord3.change_score(150)
    print("Score van " + speler1.get_name() + " na ronde 1: " + str(bord1.get_score()))
    print("Score van " + speler2.get_name() + " na ronde 1: " + str(bord2.get_score()))
    print("Score van " + speler3.get_name() + " na ronde 1: " + str(bord3.get_score()))

    # ronde2
    bord1.change_score(135)
    bord2.change_score(115)
    bord3.change_score(125)
    print("Score van " + speler1.get_name() + " na ronde 2: " + str(bord1.get_score()))
    print("Score van " + speler2.get_name() + " na ronde 2: " + str(bord2.get_score()))
    print("Score van " + speler3.get_name() + " na ronde 2: " + str(bord3.get_score()))

    # ronde3
    bord1.change_score(145)
    bord2.change_score(105)
    bord3.change_score(225)
    print("Score van " + speler1.get_name() + " na ronde 3: " + str(bord1.get_score()))
    print("Score van " + speler2.get_name() + " na ronde 3: " + str(bord2.get_score()))
    print("Score van " + speler3.get_name() + " na ronde 3: " + str(bord3.get_score()))
