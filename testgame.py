from game import Game
from player import Player


def main():
    # Init the game
    speler1 = Player(1, "Stijn")
    speler2 = Player(2, "Laël")
    speler3 = Player(3, "Stan")
    mygame = Game([speler1, speler2, speler3])

    tile_dict = generate_tile_dict()

    board = mygame.get_field()
    for row in board:
        print(row)

    # Kies eerste speler
    mygame.player_on_hand = mygame.players[0]
    current_player = mygame.get_player_on_hand()
    print(f"{current_player.get_name()} is aan de beurt")

    # Toon blokken in hand van speler
    current_hand = current_player.get_hand()
    tiles_info = make_tiles_printable(current_hand)
    print(tiles_info)

    play_tile_ids, play_positions = handle_player_input()
    play_tiles = []
    for tile in current_hand:
        if tile.get_id() in play_tile_ids:
            play_tiles.append(tile)

    play_tiles_p = make_tiles_printable(play_tiles)
    print(f"Je hebt gespeeld: {play_tiles_p}, {play_positions}")

    mygame.play_tiles(play_tiles, play_positions)
    '''
    xylines = mygame.build_line(play_tiles)

    # Remove single tile lines
    for xyline in xylines:
        if len(xyline) == 1:
            xylines.remove(xyline)
    print(f"De xy lijnen zijn: {xylines}")

    line_list = mygame.create_line(xylines)

    for i, line in enumerate(line_list):
        for line2 in line_list[i::]:
            if line.is_equal(line2):
                line_list.remove(line2)

    print(f"De unieke lijnen zijn: {line_list}")
    '''
    p_board = make_board_printable(tile_dict, board)
    for row in p_board:
        for el in row:
            print(el, end=' ')
        print()


def generate_tile_dict():
    tile_dict = {}
    tile_id = 0
    colors = ('red', 'orange', 'yellow', 'green', 'blue', 'purple')
    shapes = ('circle', 'x', 'diamond', 'square', 'star', 'clover')

    for color in colors:
        for shape in shapes:
            for i in range(3):
                tile_dict[tile_id + i] = (color, shape)
            tile_id += 3

    return tile_dict


def make_tiles_printable(tiles):
    printable_tiles = []
    for tile in tiles:
        printable_tiles.append((tile.get_id(), tile.get_color(), tile.get_shape()))
    return printable_tiles


def make_board_printable(tile_dict, board):
    # Color codes
    # 1: Red, 2: Green, 3: Yellow, 4: Blue, 5: Purple, 6: Cyan -> Orange
    colors = {"red": '\x1b[91m', "orange": '\x1b[96m',
              "yellow": '\x1b[93m', "green": '\x1b[92m',
              "blue": '\x1b[94m', "purple": '\x1b[95m'}

    shapes = {"circle": chr(0x25cf), "x": "X",
              "diamond": chr(0x25c6), "square": chr(0x25aa),
              "star": chr(0x2738), "clover": chr(0x2663)}

    printable_board = []
    for row in board:
        printable_row = []
        for el in row:
            if el != 0:
                tile = tile_dict[el]
                color = tile[0]
                shape = tile[1]
                tile_str = colors[color] + shapes[shape] + "\x1b[97m"
                printable_row.append(tile_str)

            else:
                printable_row.append(0)

        printable_board.append(printable_row)

    return printable_board


def handle_player_input():
    print("Geef de id's van de blokjes en hun locaties die je wil plaatsen." + "\n" + "bv: 15;(3,5);25;(6,9)")
    user_input = str(input(':'))
    user_input = user_input.split(";")

    tile_ids = list(map(int, user_input[::2]))

    position_strings = user_input[1::2]
    tmp1 = [el.strip('()') for el in position_strings]
    tmp2 = [el.split(',') for el in tmp1]
    positions = [tuple(int(el2) for el2 in el) for el in tmp2]

    return tile_ids, positions


if __name__ == "__main__":
    main()
