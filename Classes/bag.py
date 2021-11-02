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

    def get_current_amount(self):
        return self.current_amount

    def add_tile(self, tile):
        self.tiles.append(tile)
        self.__update_current_amount()

    def take_tile(self, tile):
        return
        # TODO add functionality to remove tiles from the list


# Test
if __name__ == "__main__":
    bag = Bag()
    print(bag.tiles[0].get_id())
