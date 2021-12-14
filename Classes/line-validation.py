from tile import Tile


# Deze functie controleert niet of de posities van de start- en eindblokjes correct zijn,
# enkel of de kleuren en vormen kloppen.
def validate_line(tiles):
    """
    Checks if a line is valid by checking their colors and shapes.
    Returns True if line is valid, False if line is invalid.
    """
    # Check if line is longer than 6 tiles
    if len(tiles) < 6:
        return False  # Line is invalid
    # Get lists of all colors and shapes in the line
    tile_colors = [tile.get_color() for tile in tiles]
    tile_shapes = [tile.get_shape() for tile in tiles]

    # If all colors are the same, all shapes must be unique and vice versa
    # Check if every color is unique and shape different
    if len(set(tile_colors)) == 1 and len(set(tile_shapes)) == len(tile_shapes):  # Based on unique elements property of set
        return True  # Line is valid
    # Check if every color is different and shape is unique
    elif len(set(tile_colors)) == len(tile_colors) and len(set(tile_shapes)) == 1:
        return True
    else:
        return False
