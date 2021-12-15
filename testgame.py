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
        print("Maak u keuze:" + "\n" + "1:Speler toevoegen" + "\n" + "2:Spel starten")
        error = False
        while not error:
            try:
                keuze = int(input())
                error = True
            except Exception:
                error = False
        if keuze == 1:
            player_id += 1
            na = "Speler" + str(player_id)
            speler = Player(player_id, na)
            print("Geef de naam van speler " + str(player_id) + ":")
            naam = input()
            if naam != "":
                speler.change_name(naam)
            spelers.append(speler)

        if keuze == 2:
            mygame = Game(spelers)
            continu = True

    board = make_board_printable(mygame.get_field())
    for row in board:
        for el in row:
            print(el, end=' ')
        print()

    while True:
        # Kies speler
        current_player = mygame.get_player_on_hand()
        print("--------------------------------------------")
        print(f"{current_player.get_name()} is aan de beurt")

        # Toon blokken in hand van speler
        current_hand = current_player.get_hand()
        tiles_info = make_tiles_printable(current_hand)
        print(tiles_info)

        choice = ""
        while choice != "1" and choice != "2":
            print("Kies je actie:\t1. Aanleggen\t2. Ruilen")
            choice = str(input(":"))
        if choice == "1":
            # Handle player input with option play
            error = False
            while not error:
                try:
                    play_tile_ids, play_positions = handle_player_input("play")
                    error = True
                except Exception:
                    error = False
            # Get the tiles from the players hand by ID
            play_tiles = []
            for tile_id in play_tile_ids:
                for tile in current_hand:
                    if tile.get_id() == tile_id:
                        play_tiles.append(tile)

            # Show the played tiles and positions
            play_tiles_p = make_tiles_printable(play_tiles)
            print(f"Je hebt gespeeld: {play_tiles_p}, {play_positions}")

            # Play the tiles
            # If the function does not succeed, rewind the players turn
            # The function does not update players hand unless it succeeds
            if mygame.play_tiles(play_tiles, play_positions):
                continue

            print("De huidige score is:")
            print(mygame.scoreboard.get_score_all())
            # Print the new state of the board
            p_board = make_board_printable(mygame.get_field())
            for row in p_board:
                for el in row:
                    print(el, end=' ')
                print()

        elif choice == "2":
            # Handle the player input with option trade
            error = False
            while not error:
                try:
                    trade_tile_ids = handle_player_input("trade")
                    error = True
                except Exception:
                    error = False

            # Get the tiles from players hand by ID
            trade_tiles = []
            for tile_id in trade_tile_ids:
                for tile in current_hand:
                    if tile.get_id() == tile_id:
                        trade_tiles.append(tile)
            # Print the traded tiles
            trade_tiles_p = make_tiles_printable(trade_tiles)
            print(f"Je hebt geruild: {trade_tiles_p}")
            # Trade the tiles
            if mygame.switch_tiles(trade_tiles):
                continue
            # Show players new hand
            current_hand = current_player.get_hand()
            tiles_info = make_tiles_printable(current_hand)
            print(f"{current_player.get_name()}, dit is je nieuwe hand")
            print(tiles_info)

            # Print the new state of the board
            p_board = make_board_printable(mygame.get_field())
            for row in p_board:
                for el in row:
                    print(el, end=' ')
                print()


def make_tiles_printable(tiles):
    """
    Returns console printable combinations of ids, colors and shapes made from a list of tiles.
    :param tiles: list of tile objects that needs to be printed
    :return: printable_tiles: list of combinations of id, color and shape that can be printed
    """
    printable_tiles = []
    for tile in tiles:
        printable_tiles.append((tile.get_id(), tile.get_color(), tile.get_shape()))
    return printable_tiles


def make_board_printable(board):
    """
    Makes a board that can be printed line-by-line to the console. The function takes tile objects in the given board
    and adds the correct unicode character and color code to the printable board
    :param board: 2D-array containing tile objects
    :return: printable_board: 2D-array with strings containing color codes and unicode characters to be displayed
    """
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


def handle_player_input(action):
    """
    Handles tile selection and board position entry on the command line. Has different behaviour for playing and
    trading tiles, which is selected with the action parameter.\n
    :param action: string containing either "play" or "trade"
    :return: None
    """
    if action == "play":
        while True:
            print("Geef de id's van de blokjes en hun locaties die je wil plaatsen." + "\n" + "bv: 15;(3,5);25;(6,9)")
            user_input = str(input(':'))
            user_input = user_input.split(";")

            tile_ids = list(map(int, user_input[::2]))

            position_strings = user_input[1::2]
            tmp1 = [el.strip('()') for el in position_strings]
            tmp2 = [el.split(',') for el in tmp1]
            positions = [tuple(int(el2) for el2 in el) for el in tmp2]

            if len(tile_ids) == len(set(tile_ids)) and len(positions) == len(set(positions)):
                return tile_ids, positions
            else:
                print("Deze invoer is ongeldig, probeer opnieuw")

    elif action == "trade":
        while True:
            print("Geef de id's van de blokjes die je wil ruilen." + "\n" + "bv: 15;25")
            user_input = str(input(':'))
            user_input = user_input.split(";")

            tile_ids = list(map(int, user_input))
            if len(tile_ids) == len(set(tile_ids)):
                return tile_ids
            else:
                print("Deze invoer is ongeldig, probeer opnieuw")


if __name__ == "__main__":
    main()
