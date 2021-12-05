# 6 valid colors: red, orange, yellow, green, blue, purple
# 6 valid shapes: circle, x, diamond, square, star, clover

import pygame

class Tile:
    def __init__(self, tile_id, color, shape, position, image=None):
        self.id = tile_id
        self.color = color
        self.shape = shape
        self.position = position
        self.image = image

    def __eq__(self, other):
        return self.id == other.id

    def get_id(self):
        """
        Get function for Tile id
        """
        return self.id

    def get_color(self):
        """
        Get function for Tile color
        """
        return self.color

    def get_shape(self):
        """
        Get function for Tile shape
        """
        return self.shape

    def get_position(self):
        """
        Get function for Tile position
        """
        return self.position

    def set_position(self, position):
        """
        Set function for Tile position
        """
        self.position = position
    
    def get_image(self):
        """
        Get the pygame.Surface object for the tile
        """
        return self.image
    
    def set_image(self, image):
        """
        Set the pygame.Surface object for the tile
        """
        self.image = image
        return
    
    def get_rect(self):
        """
        Get the pygame.Rect object for the tile
        """
        #pygame.Rect objects of pygame.Surface objects are placed at 0x0 by default
        if self.image != None:
            return self.image.get_rect().move(self.position)
        else:
            return pygame.Rect(position + [0, 0])


# Test
if __name__ == "__main__":
    example_tile = Tile(0, 'blue', 'square', (0, 0))

    print("Tile has ID: " + str(example_tile.get_id()))
    print("Tile has Color: " + example_tile.get_color())
    print("Tile has Shape: " + example_tile.get_shape())
    print("Tile has Position: X: " + str(example_tile.get_position()[0]) + " Y: " + str(example_tile.get_position()[1]))

    example_tile.set_position((4, 5))

    print("Tile has Position: X: " + str(example_tile.get_position()[0]) + " Y: " + str(example_tile.get_position()[1]))
