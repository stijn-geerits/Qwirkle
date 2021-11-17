import random
from tile import Tile


class Bag:
    def __init__(self):
        self.tiles = self.__generate_tiles()
        self.current_amount = len(self.tiles)

    def __generate_tiles(self):
        """
        Generates a list of 108 tiles.\n
        Every possible combination of color and shape appears 3 times.
        """
        tiles = []
        tile_id = 0
        colors = ('red', 'orange', 'yellow', 'green', 'blue', 'purple')
        shapes = ('circle', 'x', 'diamond', 'square', 'star', 'clover')

        for color in colors:
            for shape in shapes:
                tiles.extend([Tile(tile_id + i, color, shape, 0) for i in range(3)])
                tile_id += 3

        return tiles

    def __update_current_amount(self):
        """
        Private method of Bag.\n
        Updates the current_amount of Bag to match length of tiles list
        """
        self.current_amount = len(self.tiles)

    def __add_tile(self, tile):
        """
        Private method of Bag.\n
        Adds a Tile object to the tiles list.
        """
        self.tiles.append(tile)
        self.__update_current_amount()

    def get_current_amount(self):
        """
        Get function for current amount of tiles in the bag.\n
        """
        return self.current_amount

    def take_tiles(self, amount):
        """
        Takes a given amount of tiles from the bag and returns them in a list.\n
        """
        tiles = []
        for _ in range(amount):
            tile_index = self.tiles.index(random.choice(self.tiles))
            tile = self.tiles.pop(tile_index)
            tiles.append(tile)

        self.__update_current_amount()

        if len(tiles) == 1:
            tiles = tiles[0]

        return tiles

    def trade_tiles(self, old_tiles):
        """
        Takes a list of Tile objects. An amount equal to the amount of old tiles is taken from the tiles list.
        The old tiles are added back to the bag. \n
        """
        # Different behaviour if old_tiles is single tile or list
        if type(old_tiles) == list:  # new_tiles will be list
            new_tiles = self.take_tiles(len(old_tiles))

            for old_tile in old_tiles:
                self.__add_tile(old_tile)
        else:  # new_tiles will be single tile
            new_tiles = self.take_tiles(1)
            self.__add_tile(old_tiles)

        self.__update_current_amount()
        return new_tiles


# Test
if __name__ == "__main__":
    # Create new bag
    bag = Bag()
    print("Current amount in bag " + str(bag.get_current_amount()) + "\n")

    # Take 6 tiles from the bag
    hand = bag.take_tiles(6)
    print("Took 6 tiles from the bag")
    print("IDs of tiles taken: " + str([hand[i].get_id() for i in range(0, 5)]))
    print("Current amount in bag " + str(bag.get_current_amount()) + "\n")

    # Trade tiles 0 and 2
    old_tiles1 = []
    old_tile_indexes = [0, 2]
    for i in old_tile_indexes:
        old_tiles1.append(hand[i])

    new_tiles1 = bag.trade_tiles(old_tiles1)

    i = 0
    for j in old_tile_indexes:
        hand[j] = new_tiles1[i]
        i += 1

    print("Traded 2 tiles")
    print("IDs of tiles in hand: " + str([hand[i].get_id() for i in range(0, 5)]))
    print("Current amount in bag " + str(bag.get_current_amount()) + "\n")
