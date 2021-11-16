class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.hand = []

    def change_name(self, new_name):
        """
        Change player's name by given NEW_NAME
        """
        self.name = new_name

    def add_to_hand(self, tiles, indexes=0):#adjust
        """
        Add given TILE to given INDEX in player's hand
        """
        hand = self.hand
        if type(tiles) == list:
            if indexes == 0:
                indexes = [0, 1, 2, 3, 4, 5]
            for i in range(len(tiles)):
                hand.insert(indexes[i], tiles[i])
        else:
            hand.insert(indexes, tiles)
        self.hand = hand

    def take_from_hand(self, tiles):#adjust
        """
        Delete given TILE from player's hand
        """
        hand = self.hand
        if type(tiles) == list:
            for tile in tiles:
                hand.remove(tile)
        else:
            hand.remove(tiles)
        self.hand = hand

    def get_index_hand(self, tiles):#adjust
        """
        Get index from given TILE in player's hand
        """
        indexes = []
        if type(tiles) == list:
            for tile in tiles:
                index = self.hand.index(tile)
                indexes.append(index)
        else:
            indexes = self.hand.index(tiles)
        return indexes

    def get_hand(self):
        """
        Get function for player's hand
        """
        return self.hand

    def get_id(self):
        """
        Get function for player's id
        """
        return self.id

    def get_name(self):
        """
        Get function for player's name
        """
        return self.name


# test
if __name__ == "__main__":

    H1 = [11, 12, 13, 14, 15, 16]
    H2 = [21, 22, 23, 24, 25, 26]
    H3 = [31, 32, 33, 34, 35, 36]

    speler1 = Player(1, "Stijn")
    speler2 = Player(2, "Laël")
    speler3 = Player(3, "Stan")

    speler1.add_to_hand(H1)
    speler2.add_to_hand(H2)
    speler3.add_to_hand(H3)

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
    print(ind)
    speler2.take_from_hand(steen_leggen)
    print(str(speler2.get_hand()))
    speler2.add_to_hand(43, ind)
    print("Hand van speler 2 na wijziging: "+str(speler2.get_hand()))
