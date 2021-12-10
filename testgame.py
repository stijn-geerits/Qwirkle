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

    first_move = True
    # TODO: Check op overlappende plaatsing van tegels (input + board)
    #       Zoek manier om ongeldige beurt terug te draaien
    while True:
        # Kies speler
        current_player = mygame.next_player()
        print("--------------------------------------------")
        print(f"{current_player.get_name()} is aan de beurt")

        # Toon blokken in hand van speler
        current_hand = current_player.get_hand()
        tiles_info = make_tiles_printable(current_hand)
        print(tiles_info)

        # Save unchanged state of the board and hand, for rewind purposes
        prev_board = mygame.get_field()
        prev_hand = current_hand
        choice = ""
        while choice != "1" and choice != "2":
            print("Kies je actie:\t1. Aanleggen\t2. Ruilen")
            choice = str(input(":"))
        if choice == "1":
            # Handle player input with option play
            play_tile_ids, play_positions = handle_player_input("play")
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
                is_move_valid = False
            else:
                # Build lines
                xylines = mygame.build_line(play_tiles)

                # Remove single tile lines
                for xyline in xylines:
                    if len(xyline) == 1:
                        xylines.remove(xyline)
                print(f"De xy lijnen zijn: {xylines}")

                # Controle lines
                is_move_valid = mygame.controle(xylines, first_move, play_tiles)

            if is_move_valid:  # If move is valid, create lines and count score
                print("De gespeelde blokjes zijn geldig")
                # Create lines
                line_list = mygame.create_line(xylines)

                # Delete equal lines
                for i, line in enumerate(line_list):
                    for line2 in line_list[i + 1::]:
                        if line.is_equal(line2):
                            line_list.remove(line2)

                print(f"De unieke lijnen zijn: {line_list}")
                # Calculate score by length of unique lines
                added_score = 0
                for line in line_list:
                    added_score += line.get_length()
                mygame.scoreboard.change_score(current_player.get_id(), added_score)
                print("De huidige score is:")
                print(mygame.scoreboard.get_score_all())
                # Print the new state of the board
                p_board = make_board_printable(mygame.get_field())
                for row in p_board:
                    for el in row:
                        print(el, end=' ')
                    print()
            else:  # If move is not valid, restart players turn
                print("De gespeelde blokjes zijn ongeldig")
                current_player = mygame.previous_player()

        elif choice == "2":
            # Handle the player input with option trade
            trade_tile_ids = handle_player_input("trade")
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
            mygame.switch_tiles(trade_tiles)
            # Show players new hand
            current_hand = current_player.get_hand()
            tiles_info = make_tiles_printable(current_hand)
            print(f"{current_player.get_name()}, dit is je nieuwe hand")
            print(tiles_info)

        first_move = False


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


def handle_player_input(action):
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
