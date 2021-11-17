from tile import Tile
from bag import Bag


def validate_line(tiles):
    if tiles[0].get_color() == tiles[1].get_color():
        color = tiles[0].get_color()

    elif tiles[0].get_shape() == tiles[1].get_shape():
         shape = tiles[0].get_shape()

    else:
        is_line_valid = True
        return is_line_valid

    for tile in tiles[1:]:
        if tile.get_color() != color and tile.get_shape() != shape:
            is_line_valid = False
            return is_line_valid

        is_line_valid = True
        return is_line_valid


def main():
    bag = Bag()
    tiles = bag.take_tiles(4)
    is_line_valid = validate_line(tiles)
    tiles_list = []
    for tile in tiles:
        tiles_list.append((tile.get_color(), tile.get_shape()))
    print(tiles_list)
    print(is_line_valid)


if __name__ == '__main__':
    main()
