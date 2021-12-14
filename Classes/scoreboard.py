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
