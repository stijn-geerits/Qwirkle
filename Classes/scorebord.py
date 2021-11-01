class Scorebord:
    def __init__(self, spelers):
        self.spelers = spelers
        self.score = [0] * len(self.spelers)

    def change_score(self, speler, value):
        index = self.spelers.index(speler)
        current_score = self.score[index]
        new_score = current_score + value
        self.score[index] = new_score

    def get_score(self):
        return self.score


# test
if __name__ == "__main__":
    deelnemers = ["Stijn", "Laël", "Stan"]
    bord = Scorebord(deelnemers)
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