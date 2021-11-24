from game import Game
from player import Player
from bag import Bag
from tile import Tile


def main():
    # Init the game
    mybag = Bag()

    speler1 = Player(1, "Stijn")
    speler2 = Player(2, "Laël")
    speler3 = Player(3, "Stan")
    mygame = Game([speler1, speler2, speler3])

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

    for row in board:
        print(row)


def make_tiles_printable(tiles):
    printable_tiles = []
    for tile in tiles:
        printable_tiles.append((tile.get_id(), tile.get_color(), tile.get_shape()))
    return printable_tiles


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
