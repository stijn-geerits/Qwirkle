class Speler:
    def __init__(self,id, naam, hand):
        self.id = id
        self.naam = naam
        self.hand = hand

    def change_hand(self, new_hand):
        self.hand = new_hand

    def get_hand(self):
        return self.hand

    def get_id(self):
        return self.id

    def get_naam(self):
        return self.naam


# test
if __name__ == "__main__":
    H1 = [11, 12, 13, 14, 15, 16]
    H2 = [21, 22, 23, 24, 25, 26]
    H3 = [31, 32, 33, 34, 35, 36]

    speler1 = Speler(1, "Stijn", H1)
    speler2 = Speler(2, "Laël", H2)
    speler3 = Speler(3, "Stan", H3)

    print("Hand van speler 1: "+str(speler1.get_hand()))
    print("ID van speler 2: "+str(speler2.get_id()))
    print("Naam van speler 3: "+str(speler3.get_naam()))

    H4 = [41, 42, 43, 44, 45, 46]

    print("Hand van speler 2 voor wijziging: "+str(speler2.get_hand()))
    speler2.change_hand(H4)
    print("Hand van speler 2 na wijziging: "+str(speler2.get_hand()))