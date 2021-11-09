# 6 valid colors: red, orange, yellow, green, blue, purple
# 6 valid shapes: circle, x, diamond, square, star, clover


class Tile:
    def __init__(self, id, color, shape, position):
        self.id = id
        self.color = color
        self.shape = shape
        self.position = position

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


# Test
if __name__ == "__main__":
    example_tile = Tile(0, 'blue', 'square', (0, 0))

    print("Tile has ID: " + str(example_tile.get_id()))
    print("Tile has Color: " + example_tile.get_color())
    print("Tile has Shape: " + example_tile.get_shape())
    print("Tile has Position: X: " + str(example_tile.get_position()[0]) + " Y: " + str(example_tile.get_position()[1]))

    example_tile.set_position((4, 5))

    print("Tile has Position: X: " + str(example_tile.get_position()[0]) + " Y: " + str(example_tile.get_position()[1]))
