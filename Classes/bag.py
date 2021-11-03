import random
from tile import Tile


# Generates all tiles in the game
def generate_tiles():
    tiles = []
    tile_id = 0
    colors = ('red', 'orange', 'yellow', 'green', 'blue', 'purple')
    shapes = ('circle', 'x', 'diamond', 'square', 'star', 'clover')

    for color in colors:
        for shape in shapes:
            tiles.extend([Tile(tile_id + i, color, shape, 0) for i in range(3)])
            tile_id += 3

    return tiles


class Bag:
    def __init__(self):
        self.tiles = generate_tiles()
        self.current_amount = len(self.tiles)

    def __update_current_amount(self):
        self.current_amount = len(self.tiles)

    def __add_tile(self, tile):
        self.tiles.append(tile)
        self.__update_current_amount()

    def __take_tile(self):
        tile_index = self.tiles.index(random.choice(self.tiles))
        tile = self.tiles.pop(tile_index)
        return tile

    def get_current_amount(self):
        return self.current_amount

    def take_tiles(self, amount):
        tiles = [self.__take_tile() for i in range(amount)]

        self.__update_current_amount()
        return tiles

    def trade_tiles(self, old_tiles):
        new_tiles = [self.__take_tile() for i in range(len(old_tiles))]

        for old_tile in old_tiles:
            self.__add_tile(old_tile)

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
