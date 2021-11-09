class Scoreboard:
    def __init__(self, players):
        self.players = players
        self.score = [0] * len(self.players)

    def change_score(self, player, value):
        index = self.players.index(player)
        current_score = self.score[index]
        new_score = current_score + value
        self.score[index] = new_score

    def get_score(self, player):
        index = self.players.index(player)
        current_score = self.score[index]
        return current_score


# test
if __name__ == "__main__":
    deelnemers = ["Stijn", "Laël", "Stan"] # mergen met klasse speler
    bord = Scoreboard(deelnemers)
    print("Begin score: " + str(bord.get_score()))

    # ronde1
    bord.change_score("Stijn", 100)
    bord.change_score("Laël", 200)
    bord.change_score("Stan", 150)
    print("Score na ronde 1: " + str(bord.get_score()))

    # ronde2
    bord.change_score("Stijn", 135)
    bord.change_score("Laël", 115)
    bord.change_score("Stan", 125)
    print("Score na ronde 2: " + str(bord.get_score()))

    # ronde3
    bord.change_score("Stijn", 145)
    bord.change_score("Laël", 105)
    bord.change_score("Stan", 225)
    print("Score na ronde 3: " + str(bord.get_score()))