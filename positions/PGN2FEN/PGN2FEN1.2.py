import chess
import chess.pgn
import chess.svg
import cairosvg
import os

# File paths
pgn_path = "./master_games.pgn"
output_directory = "./output/"

# Load the PGN file and process all games
with open(pgn_path) as pgn_file:
    game_number = 1
    while True:
        game = chess.pgn.read_game(pgn_file)
        if game is None:
            break  # No more games in the file
        board = game.board()

        # Play through all moves to reach the final position
        for move in game.mainline_moves():
            board.push(move)

            # Get the FEN string of the position
            fen_string = board.fen()
            print("FEN format:", fen_string)

        # Generate SVG representation of the chessboard position
        board_svg = chess.svg.board(board=board)

        # Convert SVG to PNG and save the image
        image_output_path = os.path.join(output_directory, f"chess_position_game_{game_number}.png")
        png_data = cairosvg.svg2png(bytestring=board_svg)
        with open(image_output_path, "wb") as output_file:
            output_file.write(png_data)

        print(f"Chess board position image for game {game_number} saved at: {image_output_path}")
        game_number += 1
