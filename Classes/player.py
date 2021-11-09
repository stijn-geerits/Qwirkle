class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.hand = []

    def change_name(self, new_name): #new
        self.name = new_name

    def add_to_hand(self, tile, index): #new
        self.hand = self.hand.insert(index, tile)

    def take_from_hand(self, index): #new
        self.hand = self.hand.pop(index)

    def get_index_hand(self, tile): #new
        index = self.hand.index(tile)
        return index

    def get_hand(self):
        return self.hand

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name


# test
if __name__ == "__main__":
    H1 = [11, 12, 13, 14, 15, 16]
    H2 = [21, 22, 23, 24, 25, 26]
    H3 = [31, 32, 33, 34, 35, 36]

    speler1 = Player(1, "Stijn")
    speler2 = Player(2, "Laël")
    speler3 = Player(3, "Stan")

    for i in range(1,7):
        speler1.add_to_hand(i, H1[i])
        speler2.add_to_hand(i, H2[i])
        speler3.add_to_hand(i, H3[i])

    print("Hand van speler 1: "+str(speler1.get_hand()))
    print("Hand van speler 2: " + str(speler2.get_hand()))
    print("Hand van speler 3: " + str(speler3.get_hand()))
    print("ID van speler 1: "+str(speler1.get_id()))
    print("ID van speler 2: " + str(speler2.get_id()))
    print("ID van speler 3: " + str(speler3.get_id()))
    print("Naam van speler 1: " + str(speler1.get_name()))
    print("Naam van speler 2: " + str(speler2.get_name()))
    print("Naam van speler 3: "+str(speler3.get_name()))

    steen_leggen = 23
    steen_krijgen = 43

    print("Hand van speler 2 voor wijziging: "+str(speler2.get_hand()))
    ind = speler2.get_index_hand(23)
    speler2.take_from_hand(ind)
    speler2.add_to_hand(43, ind)
    print("Hand van speler 2 na wijziging: "+str(speler2.get_hand()))