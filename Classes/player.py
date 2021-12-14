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

    def set_hand(self, hand):
        """
        Set function for player's hand
        This function should only be used for rewind purposes
        """
        self.hand = hand

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
