import bpy
import math
import time
from mathutils import Vector
from random import random, sample

BOARD_HEIGHT = 0.0
CAMERA_MIN_DISTANCE = 20.0
CAMERA_MAX_DISTANCE = 50.0
CAMERA_MIN_PITCH = math.pi/10.0
CAMERA_MAX_PITCH = math.pi/2.0
FEN_FILEPATH = "./positions/PGN2FEN/output/FEN-results.txt"
FEN_PREFIX = "FEN format: "
LIGHT_MIN_DISTANCE = 20.0
LIGHT_MAX_DISTANCE = 50.0
LIGHT_MIN_PITCH = math.pi/10.0
LIGHT_MAX_PITCH = math.pi/2.0
PROPORTION_POSITIONS_RENDERED = 0.5
RENDER_OUTDIR = "./output/"
RENDERS_PER_POSITION = 2


def randomizeObjectPosition(object, r_min, r_max, pitch_min, pitch_max, is_camera = False):
    object_distance = random() * (r_max - r_min) + r_min
    object_pitch = random() * (pitch_max - pitch_min) + pitch_min
    object_yaw = random() * 2 * math.pi
    
    object_xy_distance = object_distance * math.cos(object_pitch)
    
    object.location.x = math.cos(object_yaw) * object_xy_distance
    object.location.y = math.sin(object_yaw) * object_xy_distance
    object.location.z = BOARD_HEIGHT + object_distance * math.sin(object_pitch)
    
    object.rotation_euler.z = object_yaw + math.pi/2
    object.rotation_euler.x = -object_pitch + math.pi/2
    
    if is_camera:
        object.data.dof.focus_distance = object_distance

def clearCollection(collection):
    for c in collection.objects:
        collection.objects.unlink(c)

def loadPiece(piece_type, location, piece_collection, reference_collection):
    pieceName = ""
    is_white = piece_type.isupper()
    
    match piece_type.lower():
        case 'k':
            pieceName = "King"
        case 'q':
            pieceName = "Queen"
        case 'r':
            pieceName = "Rook"
        case 'b':
            pieceName = "Bishop"
        case 'n':
            pieceName = "Knight"
        case 'p':
            pieceName = "Pawn"
        case _:
            return
    
    piece = reference_collection.objects[pieceName].copy()
    piece.location.xy = location
    
    piece.material_slots[0].link = 'OBJECT' 
    piece.material_slots[0].material = bpy.data.materials['White_Pieces' if is_white else 'Black_Pieces']
    
    piece_collection.objects.link(piece)

def loadPosition(fen_string, destination_collection, reference_collection):
    # could make these global vars at some point
    origin = Vector((-3.5,  3.5))
    offset = Vector(( 0.0,  0.0))
    
    clearCollection(destination_collection)
    
    for row in fen_string.split('/'):
        for char in row: 
            if (char.isdigit()):
                offset.x += int(char)
            else:
                loadPiece(
                    char,
                    origin + offset,
                    destination_collection,
                    reference_collection
                )
                offset.x += 1.0
        offset.x = 0.0
        offset.y -= 1.0
        
def main():
    camera = bpy.context.scene.camera
    activePieces = bpy.data.collections['Pieces']
    referencePieces = bpy.data.collections['PieceReference']
    
    current_time = time.localtime()
    outdir = RENDER_OUTDIR + f"data_{current_time.tm_mon}-{current_time.tm_mday}-{current_time.tm_year}_{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}/"
    
    with open(FEN_FILEPATH, 'r') as fen_file:
        
        lines = list(filter(lambda line: line.startswith(FEN_PREFIX), fen_file.readlines()))
        lines = [line[len(FEN_PREFIX):] for line in sample(lines, k=int(len(lines) * PROPORTION_POSITIONS_RENDERED))]
        
        print(f"Rendering {len(lines)} positions")
        
        position = 0
        for line in lines:
            for i in range(RENDERS_PER_POSITION):
                position_string = line.split(' ')[0]
                
                print(position_string)
                loadPosition(
                    position_string,
                    activePieces,
                    referencePieces
                )
                
                randomizeObjectPosition(
                    camera,
                    CAMERA_MIN_DISTANCE,
                    CAMERA_MAX_DISTANCE,
                    CAMERA_MIN_PITCH,
                    CAMERA_MAX_PITCH,
                    True
                )
                
                randomizeObjectPosition(
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