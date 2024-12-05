import bpy
import time
import sys
import os
from random import sample

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from config import *
from chess_scene_utils import randomize_object_position, load_position



def main():
    camera = bpy.context.scene.camera
    active_pieces = bpy.data.collections['Pieces']
    reference_pieces = bpy.data.collections['PieceReference']
    
    current_time = time.localtime()
    outdir = RENDER_OUTDIR + f"data_{current_time.tm_mon}-{current_time.tm_mday}-{current_time.tm_year}_{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}/"
    
    os.makedirs(outdir)
    with open(FEN_FILEPATH, 'r') as fen_file:
        lines = list(filter(lambda line: line.startswith(FEN_PREFIX), fen_file.readlines()))
        lines = [line[len(FEN_PREFIX):] for line in sample(lines, k=int(len(lines) * PROPORTION_POSITIONS_RENDERED))]
        
        print(f"Rendering {len(lines)} positions")
        
        with open(outdir+"labels.txt", 'w') as label_file:
            label_file.write('\n'.join(lines))

        position = 0
        for line in lines:
            for i in range(RENDERS_PER_POSITION):
                position_string = line.split(' ')[0]
                
                print(position_string)
                load_position(
                    position_string,
                    active_pieces,
                    reference_pieces
                )
                
                randomize_object_position(
                    camera,
                    CAMERA_MIN_DISTANCE,
                    CAMERA_MAX_DISTANCE,
                    CAMERA_MIN_PITCH,
                    CAMERA_MAX_PITCH,
                    True
                )
                
                randomize_object_position(
                    bpy.data.objects['Light'],
                    LIGHT_MIN_DISTANCE,
                    LIGHT_MAX_DISTANCE,
                    LIGHT_MIN_PITCH,
                    LIGHT_MAX_PITCH
                )
                
                bpy.context.scene.render.filepath = outdir + f"position_{position}_{i}"
                bpy.ops.render.render(write_still=True)
            position += 1
    
if __name__ == "__main__":
    main()
