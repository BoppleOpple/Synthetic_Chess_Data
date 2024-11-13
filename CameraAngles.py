import bpy
import math
from mathutils import Vector
from random import random

class RandomCameraPosition(bpy.types.Operator):

    CAMERA_MIN_DISTANCE = 20.0
    CAMERA_MAX_DISTANCE = 50.0
    CAMERA_MIN_PITCH = math.pi/10.0
    CAMERA_MAX_PITCH = math.pi/2.0
    BOARD_HEIGHT = 0.0
    
    bl_idname = "object.datagen_randomize_camera"
    bl_label = "Randomize Camera Position"
    
    def execute(self, context):
        camera = context.scene.camera
        
        camera_distance = random() * (self.CAMERA_MAX_DISTANCE - self.CAMERA_MIN_DISTANCE) + self.CAMERA_MIN_DISTANCE
        camera_pitch = random() * (self.CAMERA_MAX_PITCH - self.CAMERA_MIN_PITCH) + self.CAMERA_MIN_PITCH
        camera_yaw = random() * 2 * math.pi
        
        camera_xy_distance = camera_distance * math.cos(camera_pitch)
        
        camera.location.x = math.cos(camera_yaw) * camera_xy_distance
        camera.location.y = math.sin(camera_yaw) * camera_xy_distance
        camera.location.z = self.BOARD_HEIGHT + camera_distance * math.sin(camera_pitch)
        
        camera.rotation_euler.z = camera_yaw + math.pi/2
        camera.rotation_euler.x = -camera_pitch + math.pi/2
        
        camera.data.dof.focus_distance = camera_distance
        
        return {"FINISHED"}

class LoadPiecesFromFEN(bpy.types.Operator):
    fen_string = "2kr3r/3pb1Qp/R1n5/5N2/1qP5/6P1/1P2PPKP/5R2"
    
    bl_idname = "object.datagen_load_fen"
    bl_label = "Load Pieces From FEN"
    
    def __init__(self):
        self.collection = bpy.data.collections['Pieces']
        
    def clearPieces(self):
        for c in self.collection.objects:
            self.collection.objects.unlink(c)
    
    def loadPiece(self, piece_type, location):
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
        
        piece = bpy.data.collections['PieceReference'].objects[pieceName].copy()
        piece.location.xy = location
        
        piece.material_slots[0].link = 'OBJECT' 
        piece.material_slots[0].material = bpy.data.materials['White_Pieces' if is_white else 'Black_Pieces']
        
        self.collection.objects.link(piece)
    
    def execute(self, context, thing):
        origin = Vector((-3.5,  3.5))
        offset = Vector(( 0.0,  0.0))
        
        print(thing)
        
        self.clearPieces()
        
        for row in self.fen_string.split('/'):
            for char in row: 
                if (char.isdigit()):
                    offset.x += int(char)
                else:
                    self.loadPiece(char, origin + offset)
                    offset.x += 1.0
            offset.x = 0.0
            offset.y -= 1.0
        
        return {"FINISHED"}
    

def register():
    bpy.utils.register_class(RandomCameraPosition)
    bpy.utils.register_class(LoadPiecesFromFEN)

def unregister():
    bpy.utils.unregister_class(RandomCameraPosition)
    bpy.utils.unregister_class(LoadPiecesFromFEN)        

if __name__ == "__main__":
    register()