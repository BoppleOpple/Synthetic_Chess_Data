import bpy # type: ignore
import time
import sys
import os
from random import sample

# Add the parent directory to the system path to allow imports from the root directory
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from config import *
from chess_scene_utils import get_hdri_files, process_pgn_file, randomize_background, randomize_object_position, load_position


def main():
    """
    Main function to render chess positions from a FEN file.
    """

    # Setup scene objects and collections
    white_camera = bpy.data.objects['White_Camera']
    black_camera = bpy.data.objects['Black_Camera']
    active_pieces = bpy.data.collections['Pieces']
    reference_pieces = bpy.data.collections['PieceReference']
    
    # Setup output directory
    current_time = time.localtime()
    outdir = OUTDIR + f"data_{current_time.tm_mon}-{current_time.tm_mday}-{current_time.tm_year}_{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}/"
    
    os.makedirs(outdir)

    # if FEN_FILEPATH:
    #     # Read FEN file and sample positions to render
    #     with open(FEN_FILEPATH, 'r') as fen_file:
    #         # Read all lines and filter for FEN positions
    #         all_lines = fen_file.readlines()
    #         fen_positions = [line for line in all_lines if line.startswith(FEN_PREFIX)]
    # else:

    # Get all PGN files in directory
    pgn_files = [f for f in os.listdir(PGN_DIR) if f.endswith('.pgn')]


    # Get HDRI files
    hdri_files = get_hdri_files(BACKGROUND_HDRI_DIR)
    
    for pgn_file in pgn_files:
        pgn_path = os.path.join(PGN_DIR, pgn_file)

        # Create output directories and copy PGN file
        pgn_filename = os.path.splitext(os.path.basename(pgn_path))[0]
        pgn_outdir = os.path.join(outdir, RENDER_OUTDIR.strip("/"), pgn_filename, PGN_OUTDIR.strip("/"))
        os.makedirs(pgn_outdir, exist_ok=True)
        
        # Copy PGN file to output directory
        with open(pgn_path, 'r') as src, open(os.path.join(pgn_outdir, os.path.basename(pgn_path)), 'w') as dst:
            dst.write(src.read())
        
        
        # Process the PGN file
        fen_positions = process_pgn_file(pgn_path)[1:]
        
        # Calculate number of positions to sample
        # num_positions = int(len(fen_positions) * PROPORTION_POSITIONS_RENDERED)
        
        # Sample random positions and remove prefix
        # sampled_lines = sample(fen_positions, k=num_positions) 
        # lines = [line[len(FEN_PREFIX):] for line in sampled_lines]
        
        print(f"Rendering {len(fen_positions)} positions")
        
        # Write labels to file
        # with open(outdir+"labels.txt", 'w') as label_file:
        #     label_file.write(''.join(lines))

        randomize_background(hdri_files)

        position_tally = 1
        for line in fen_positions:
            position_string = line.split(' ')[0]
                
            print(position_string)
            
            # Load position
            load_position(
                position_string,
                active_pieces,
                reference_pieces,
                PIECE_MAX_DISTANCE,
                WHITE_PIECE_MATERIAL,
                BLACK_PIECE_MATERIAL
            )

            # Randomize white camera position
            randomize_object_position(
                white_camera,
                BOARD_HEIGHT,
                CAMERA_MIN_DISTANCE,
                CAMERA_MAX_DISTANCE,
                CAMERA_MIN_PITCH,
                CAMERA_MAX_PITCH,
                CAMERA_YAW_RANGE,
                WHITE_YAW,
                True
            )
            
            # Randomize black camera position
            randomize_object_position(
                black_camera,
                BOARD_HEIGHT,
                CAMERA_MIN_DISTANCE,
                CAMERA_MAX_DISTANCE,
                CAMERA_MIN_PITCH,
                CAMERA_MAX_PITCH,
                CAMERA_YAW_RANGE,
                BLACK_YAW,
                True
            )
            
            # Randomize light position
            randomize_object_position(
                bpy.data.objects['Light'],
                BOARD_HEIGHT,
                LIGHT_MIN_DISTANCE,
                LIGHT_MAX_DISTANCE,
                LIGHT_MIN_PITCH,
                LIGHT_MAX_PITCH,
                False
            )
            
            # Render white's perspective
            bpy.context.scene.render.filepath = os.path.join(outdir, RENDER_OUTDIR.strip("/"), pgn_filename, RENDER_OUTDIR_WHITE.strip("/"), f"{position_tally}")
            bpy.context.scene.camera = white_camera
            bpy.ops.render.render(write_still=True)

            # Render black's perspective
            bpy.context.scene.render.filepath = os.path.join(outdir, RENDER_OUTDIR.strip("/"), pgn_filename, RENDER_OUTDIR_BLACK.strip("/"), f"{position_tally}")
            bpy.context.scene.camera = black_camera
            bpy.ops.render.render(write_still=True)
                
            position_tally += 1
    
if __name__ == "__main__":
    main()
