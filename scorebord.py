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

# vertaling van namen naar id's?
