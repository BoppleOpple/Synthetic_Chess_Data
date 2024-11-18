import chess
import chess.pgn
import chess.svg
import cairosvg

# File paths
pgn_path = "/home/arman/Downloads/COS573/Project/master_games.pgn"
image_output_path = "/home/arman/Downloads/COS573/Project/chess_position.png"

# Load the PGN file
with open(pgn_path) as pgn_file:
    game = chess.pgn.read_game(pgn_file)  # Read the first game in the PGN file
    board = game.board()

    # Play through all moves to reach the final position
    for move in game.mainline_moves():
        board.push(move)

    # Get the FEN string of the final position
    fen_string = board.fen()
    print("FEN format:", fen_string)

    # Generate SVG representation of the chessboard position
    board_svg = chess.svg.board(board=board)

    # Convert SVG to PNG and save the image
    png_data = cairosvg.svg2png(bytestring=board_svg)
    with open(image_output_path, "wb") as output_file:
        output_file.write(png_data)

print(f"Chess board position image saved at: {image_output_path}")
