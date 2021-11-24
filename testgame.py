from game import Game
from player import Player
from bag import Bag
from tile import Tile


def main():
    mybag = Bag()

    speler1 = Player(1, "Stijn")
    speler2 = Player(2, "Laël")
    speler3 = Player(3, "Stan")
    mygame = Game([speler1, speler2, speler3])

    board = mygame.get_field()
    for row in board:
        print(row)

    mygame.player_on_hand = mygame.players[0]
    print(f"{mygame.get_player_on_hand().get_name()} is aan de beurt")

    tiles = mybag.take_tiles(6)
    speler1.add_to_hand(tiles)

    tiles_info = make_tiles_printable(speler1.get_hand())

    print(tiles_info)
    play_tiles, play_positions = handle_player_input(speler1)
    play_tiles_p = make_tiles_printable(play_tiles)
    print(f"Je hebt gespeeld: {play_tiles_p}, {play_positions}")

    mygame.play_tiles(play_tiles, play_positions)

    for row in board:
        print(row)


def make_tiles_printable(tiles):
    printable_tiles = []
    for tile in tiles:
        printable_tiles.append((tile.get_id(), tile.get_color(), tile.get_shape()))
    return printable_tiles


def handle_player_input(speler):
    tile_index_str = ''
    tiles = []
    while tile_index_str != 'x':
        tile_index_str = input("Geef ID van tile: ")
        if tile_index_str.isdigit():
            tiles.append(speler.take_from_hand(int(tile_index_str)))

    position_str_y = ''
    position_str_x = ''
    positions = []
    while position_str_y != 'x' or position_str_x != 'x':
        position_str_y = input("Geef positie in (y): ")
        position_str_x = input("Geef positie in (x): ")
        if position_str_y.isdigit():
            if position_str_x.isdigit():
                positions.append((position_str_y, position_str_x))

    return tiles, positions


if __name__ == "__main__":
    main()
