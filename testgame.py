#!/usr/bin/env python3
import sys

# Add classes folder to path
CLASSESDIR = "Classes/"
sys.path.insert(1, CLASSESDIR)

# Import classes
from game import Game
from player import Player


def main():
    # Init the game
    print("Welkom bij Qwirkle!")
    continu = False
    player_id = 0
    spelers = []
    while not continu:
        print("Maak u keuze:"+"\n"+"1:Speler toevoegen"+"\n"+"2:Spel starten")
        keuze = int(input())
        if keuze == 1:
            player_id += 1
            na = "Speler"+str(player_id)
            speler = Player(player_id, na)
            print("Geef de naam van speler " + str(player_id) + ":")
            naam = input()
            if naam !="":
                speler.change_name(naam)
            spelers.append(speler)

        if keuze == 2:
            mygame = Game(spelers)
            continu = True

    board = make_board_printable(mygame.get_field())
    for row in board:
        print(row)

    while True:
        # Kies eerste speler
        current_player = mygame.next_player()
        print(f"{current_player.get_name()} is aan de beurt")

        # Toon blokken in hand van speler
        current_hand = current_player.get_hand()
        tiles_info = make_tiles_printable(current_hand)
        print(tiles_info)

        play_tile_ids, play_positions = handle_player_input()
        play_tiles = []
        for tile_id in play_tile_ids:
            for tile in current_hand:
                if tile.get_id() == tile_id:
                    play_tiles.append(tile)

        play_tiles_p = make_tiles_printable(play_tiles)
        print(f"Je hebt gespeeld: {play_tiles_p}, {play_positions}")

        mygame.play_tiles(play_tiles, play_positions)
        # TODO: Line validation

        xylines = mygame.build_line(play_tiles)

        # Remove single tile lines
        for xyline in xylines:
            if len(xyline) == 1:
                xylines.remove(xyline)
        print(f"De xy lijnen zijn: {xylines}")

        is_move_valid = mygame.controle(xylines)
        if is_move_valid:
            print("De gespeelde blokjes zijn geldig")
        else:
            print("De gespeelde blokjes zijn ongeldig")

        line_list = mygame.create_line(xylines)

        for i, line in enumerate(line_list):
            for line2 in line_list[i+1::]:
                if line.is_equal(line2):
                    line_list.remove(line2)

        print(f"De unieke lijnen zijn: {line_list}")

        added_score = 0
        for line in line_list:
            added_score += line.get_length()
        mygame.scoreboard.change_score(current_player.get_id(), added_score)
        print("De huidige score is:")
        print(mygame.scoreboard.get_score_all())

        p_board = make_board_printable(mygame.get_field())
        for row in p_board:
            for el in row:
                print(el, end=' ')
            print()


def make_tiles_printable(tiles):
    printable_tiles = []
    for tile in tiles:
        printable_tiles.append((tile.get_id(), tile.get_color(), tile.get_shape()))
    return printable_tiles


def make_board_printable(board):
    # Color codes
    # 38;2;r;g;b
    colors = {"red": '\x1b[38;2;192;32;32m', 
              "orange": '\x1b[38;2;192;96;32m',
              "yellow": '\x1b[38;2;192;192;32m', 
              "green": '\x1b[38;2;32;144;32m',
              "blue": '\x1b[38;2;32;32;192m',
              "purple": '\x1b[38;2;128;32;144m'}

    shapes = {"circle": chr(0x25cf), "x": "X",
              "diamond": chr(0x25c6), "square": chr(0x25aa),
              "star": chr(0x2738), "clover": chr(0x2663)}

    printable_board = []
    for row in board:
        printable_row = []
        for tile in row:
            if tile.get_id() != 0:
                color = tile.get_color()
                shape = tile.get_shape()
                tile_str = colors[color] + shapes[shape] + "\x1b[00m"
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
