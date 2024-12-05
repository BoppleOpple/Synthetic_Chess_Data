import bpy
import time
import sys
import os
from random import sample

# Add the parent directory to the system path to allow imports from the root directory
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from config import *
from chess_scene_utils import get_hdri_files, randomize_background, randomize_object_position, load_position



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
    outdir = RENDER_OUTDIR + f"data_{current_time.tm_mon}-{current_time.tm_mday}-{current_time.tm_year}_{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}/"
    
    os.makedirs(outdir)
    
    # Read FEN file and sample positions to render
    with open(FEN_FILEPATH, 'r') as fen_file:
        # Read all lines and filter for FEN positions
        all_lines = fen_file.readlines()
        fen_lines = [line for line in all_lines if line.startswith(FEN_PREFIX)]
        
        # Calculate number of positions to sample
        num_positions = int(len(fen_lines) * PROPORTION_POSITIONS_RENDERED)
        
        # Sample random positions and remove prefix
        sampled_lines = sample(fen_lines, k=num_positions) 
        lines = [line[len(FEN_PREFIX):] for line in sampled_lines]
        
        print(f"Rendering {len(lines)} positions")
        
        # Write labels to file
        with open(outdir+"labels.txt", 'w') as label_file:
            label_file.write(''.join(lines))

        # Get HDRI files
        hdri_files = get_hdri_files(BACKGROUND_HDRI_DIR)

        # Render each position multiple times
        position = 0
        for line in lines:
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

            randomize_background(hdri_files)

            # Render white's perspective
            bpy.context.scene.render.filepath = outdir + f"position_{position}_white"
            bpy.context.scene.camera = white_camera
            bpy.ops.render.render(write_still=True)

            # Render black's perspective
            bpy.context.scene.render.filepath = outdir + f"position_{position}_black"
            bpy.context.scene.camera = black_camera
            bpy.ops.render.render(write_still=True)
                
            position += 1
    
if __name__ == "__main__":
    main()
