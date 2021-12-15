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
        tile_id = 1
        self.colors = ('red', 'orange', 'yellow', 'green', 'blue', 'purple')
        self.shapes = ('circle', 'x', 'diamond', 'square', 'star', 'clover')

        # for testing
        # self.colors = ('red', 'orange', 'yellow')
        # self.shapes = ('circle', 'x')

        for color in self.colors:
            for shape in self.shapes:
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

    def get_tile_dictionary(self):
        tile_dict = {}
        for tile in self.tiles:
            tile_dict[tile.get_id()] = tile
        return tile_dict

    def get_current_amount(self):
        """
        Get function for current amount of tiles in the bag.
        """
        return self.current_amount

    def take_tiles(self, amount):
        """
        Takes a given amount of tiles from the bag and returns them in a list.
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
        The old tiles are added back to the bag.
        """
        # Different behaviour if old_tiles is single tile or list
        if isinstance(old_tiles, list):  # new_tiles will be list
            new_tiles = self.take_tiles(len(old_tiles))

            for old_tile in old_tiles:
                self.__add_tile(old_tile)
        else:  # new_tiles will be single tile
            new_tiles = self.take_tiles(1)
            self.__add_tile(old_tiles)

        self.__update_current_amount()
        return new_tiles
