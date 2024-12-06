import os
import bpy # type: ignore
from mathutils import Vector
from random import random, choice
import math
import chess
import chess.pgn
import chess.svg

def randomize_object_position(object, board_height, r_min, r_max, pitch_min, pitch_max, yaw_range = 2.0 * math.pi, center_yaw = 0.0, is_camera=False):
    """
    Randomize the position of an object in the scene.
    """
    
    # Randomize distance, pitch, and yaw
    object_distance = random() * (r_max - r_min) + r_min
    object_pitch = random() * (pitch_max - pitch_min) + pitch_min
    object_yaw = center_yaw + random() * yaw_range - yaw_range / 2.0
    
    # Convert pitch and yaw to Cartesian coordinates
    object_xy_distance = object_distance * math.cos(object_pitch)
    
    object.location.x = math.cos(object_yaw) * object_xy_distance
    object.location.y = math.sin(object_yaw) * object_xy_distance
    object.location.z = board_height + object_distance * math.sin(object_pitch)
    
    # Set rotation based on pitch and yaw
    object.rotation_euler.z = object_yaw + math.pi/2
    object.rotation_euler.x = -object_pitch + math.pi/2
    
    if is_camera:
        object.data.dof.focus_distance = object_distance

def clear_collection(collection):
    """
    Clear all objects from a collection.
    """
    
    for c in collection.objects:
        collection.objects.unlink(c)

def load_piece(piece_type, location, piece_collection, reference_collection, piece_max_offset, white_piece_material, black_piece_material):
    """
    Load a piece into the scene.
    """
    
    piece_name = ""
    is_white = piece_type.isupper()
    
    # Convert piece type to piece name
    match piece_type.lower():
        case 'k':
            piece_name = "King"
        case 'q':
            piece_name = "Queen"
        case 'r':
            piece_name = "Rook"
        case 'b':
            piece_name = "Bishop"
        case 'n':
            piece_name = "Knight"
        case 'p':
            piece_name = "Pawn"
        case _:
            return
    
    # Copy piece from reference collection and set location
    piece = reference_collection.objects[piece_name].copy()
    piece.location.xy = location + Vector((random() * piece_max_offset * 2.0 - piece_max_offset, random() * piece_max_offset * 2.0 - piece_max_offset))

    # Randomize rotation
    piece.rotation_euler.z = random() * math.pi * 2.0
    
    # Link material to piece
    piece.material_slots[0].link = 'OBJECT' 
    piece.material_slots[0].material = bpy.data.materials[white_piece_material if is_white else black_piece_material]
    
    # Link piece to piece collection
    piece_collection.objects.link(piece)

def load_position(fen_string, destination_collection, reference_collection, piece_max_offset, white_piece_material, black_piece_material):
    """
    Load a chess position into the scene.
    """
    
    # Setup origin and offset
    origin = Vector((-3.5,  3.5))
    offset = Vector(( 0.0,  0.0))
    
    # Clear destination collection
    clear_collection(destination_collection)
    
    for row in fen_string.split('/'):
        for char in row: 
            if (char.isdigit()):
                offset.x += int(char)
            else:
                load_piece(
                    char,
                    origin + offset,
                    destination_collection,
                    reference_collection,
                    piece_max_offset,
                    white_piece_material,
                    black_piece_material
                )
                offset.x += 1.0
        offset.x = 0.0
        offset.y -= 1.0


def get_hdri_files(background_hdri_dir):
    """
    Get all HDRI files in a directory.
    """
    
    return [os.path.join(background_hdri_dir, f) for f in os.listdir(background_hdri_dir) if f.endswith('.hdr') or f.endswith('.exr')]

def setup_background_node():
    """
    Setup the background node.
    """

    # Get the environment node tree of the current scene
    node_tree = bpy.context.scene.world.node_tree
    tree_nodes = node_tree.nodes

    # Clear all nodes
    tree_nodes.clear()

    # Add Background node
    node_background = tree_nodes.new('Background', type='ShaderNodeBackground')

    # Add Environment Texture node
    node_environment = tree_nodes.new('Environment Texture', type='ShaderNodeTexEnvironment')

    # Add Output node
    node_output = tree_nodes.new('World Output', type='ShaderNodeOutputWorld')

    # Link all nodes
    links = node_tree.links
    links.new(node_environment.outputs["Color"], node_background.inputs["Color"])
    links.new(node_background.outputs["Background"], node_output.inputs["Surface"])

def randomize_background(background_hdri_list):
    """
    Randomize the background of the scene.
    """
    hdri = choice(background_hdri_list)

    # Get the environment node tree of the current scene
    node_tree = bpy.context.scene.world.node_tree
    tree_nodes = node_tree.nodes

    # Get the Background node
    node_background = tree_nodes.get('Background')

    # Get the Environment Texture node
    node_environment = tree_nodes.get('Environment Texture')

    # Get the Output node
    node_output = tree_nodes.get('World Output')

    # Load and assign the image to the node property
    node_environment.image = bpy.data.images.load(hdri)

    # Link all nodes
    links = node_tree.links
    links.new(node_environment.outputs["Color"], node_background.inputs["Color"])
    links.new(node_background.outputs["Background"], node_output.inputs["Surface"])

def process_pgn_file(pgn_path, output_directory=None):
    """
    Process a PGN file and return a list of FEN strings.
    Optionally save FEN strings to text files if output_directory is provided.
    """
    fen_positions = []
    
    with open(pgn_path) as pgn_file:
        game_number = 1
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
                
            board = game.board()
            game_positions = []
            
            # Store initial position
            game_positions.append(board.fen())
            
            # Store position after each move
            for move in game.mainline_moves():
                board.push(move)
                game_positions.append(board.fen())
            
            fen_positions.extend(game_positions)
            game_number += 1
        
            if output_directory:
                # Create output directory if it doesn't exist
                os.makedirs(output_directory, exist_ok=True)
                
                # Save FEN string to text file
                pgn_filename = os.path.splitext(os.path.basename(pgn_path))[0]
                fen_file_path = os.path.join(output_directory, f"{pgn_filename}_game_{game_number}.fen")
                with open(fen_file_path, 'w') as f:
                    f.write('\n'.join(game_positions))
    
    return fen_positions

def get_random_position(pgn_path):
    """
    Get a random FEN position from a PGN file.
    """
    positions = process_pgn_file(pgn_path)
    return choice(positions) if positions else None

def process_pgn_directory(pgn_directory, output_directory=None):
    """
    Process all PGN files in a directory and return a list of FEN strings.
    Optionally save FEN strings to text files if output_directory is provided.
    """
    
    all_positions = []
    
    # Get all PGN files in directory
    pgn_files = [f for f in os.listdir(pgn_directory) if f.endswith('.pgn')]
    
    for pgn_file in pgn_files:
        pgn_path = os.path.join(pgn_directory, pgn_file)
        
        # Create subdirectory for this PGN file's images if needed
        file_output_dir = None
        if output_directory:
            os.makedirs(output_directory, exist_ok=True)
        
        # Process the PGN file
        positions = process_pgn_file(pgn_path, output_directory)
        all_positions.extend(positions)
    
    return all_positions