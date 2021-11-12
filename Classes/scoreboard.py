import player


class Scoreboard:
    def __init__(self, players):
        self.scoreboard = {}
        for i in players:
            self.scoreboard[i.get_id()] = 0

    def change_score(self, id, value):
        """
        Add given VALUE to player's score
        """
        current_score = self.scoreboard[id]
        new_score = current_score + value
        self.scoreboard[id] = new_score

    def get_score(self, id):
        """
        Get function for given PLAYER's score
        """
        return self.scoreboard[id]

    def get_score_all(self):
        """
        Get function for all players
        """
        return self.scoreboard


# test
if __name__ == "__main__":
    speler1 = player.Player(1, "Stijn")
    speler2 = player.Player(2, "Laël")
    speler3 = player.Player(3, "Stan")

    spelers = [speler1, speler2, speler3]
    bord = Scoreboard(spelers)

    print("Beginscore: " + str(bord.get_score_all()))

    # ronde1
    bord.change_score(1, 100)
    bord.change_score(2, 200)
    bord.change_score(3, 150)
    print("Score van " + speler1.get_name() + " na ronde 1: " + str(bord.get_score(1)))
    print("Score van " + speler2.get_name() + " na ronde 1: " + str(bord.get_score(2)))
    print("Score van " + speler3.get_name() + " na ronde 1: " + str(bord.get_score(3)))

    # ronde2
    bord.change_score(1, 135)
    bord.change_score(2, 115)
    bord.change_score(3, 125)
    print("Score van " + speler1.get_name() + " na ronde 2: " + str(bord.get_score(1)))
    print("Score van " + speler2.get_name() + " na ronde 2: " + str(bord.get_score(2)))
    print("Score van " + speler3.get_name() + " na ronde 2: " + str(bord.get_score(3)))

    # ronde3
    bord.change_score(1, 145)
    bord.change_score(2, 105)
    bord.change_score(3, 225)
    print("Score van " + speler1.get_name() + " na ronde 3: " + str(bord.get_score(1)))
    print("Score van " + speler2.get_name() + " na ronde 3: " + str(bord.get_score(2)))
    print("Score van " + speler3.get_name() + " na ronde 3: " + str(bord.get_score(3)))

    print("Eindscore: " + str(bord.get_score_all()))
