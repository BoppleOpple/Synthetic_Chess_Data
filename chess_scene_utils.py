import bpy
from mathutils import Vector
from random import random
import math
from config import BOARD_HEIGHT

def randomize_object_position(object, r_min, r_max, pitch_min, pitch_max, is_camera=False):
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

def clear_collection(collection):
    for c in collection.objects:
        collection.objects.unlink(c)

def load_piece(piece_type, location, piece_collection, reference_collection):
    piece_name = ""
    is_white = piece_type.isupper()
    
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
    
    piece = reference_collection.objects[piece_name].copy()
    piece.location.xy = location
    
    piece.material_slots[0].link = 'OBJECT' 
    piece.material_slots[0].material = bpy.data.materials['White_Pieces' if is_white else 'Black_Pieces']
    
    piece_collection.objects.link(piece)

def load_position(fen_string, destination_collection, reference_collection):
    origin = Vector((-3.5,  3.5))
    offset = Vector(( 0.0,  0.0))
    
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
                    reference_collection
                )
                offset.x += 1.0
        offset.x = 0.0
        offset.y -= 1.0 