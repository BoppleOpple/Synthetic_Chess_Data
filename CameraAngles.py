import bpy
import math
from random import random

CAMERA_MIN_DISTANCE = 20.0
CAMERA_MAX_DISTANCE = 25.0
CAMERA_MIN_PITCH = math.pi/10.0
CAMERA_MAX_PITCH = math.pi/2.0
BOARD_HEIGHT = 1.5

def randomizeCameraPosition(camera):
    camera_distance = random() * (CAMERA_MAX_DISTANCE - CAMERA_MIN_DISTANCE) + CAMERA_MIN_DISTANCE
    camera_pitch = random() * (CAMERA_MAX_PITCH - CAMERA_MIN_PITCH) + CAMERA_MIN_PITCH
    camera_yaw = random() * 2 * math.pi
    
    camera_xy_distance = camera_distance * math.cos(camera_pitch)
    
    camera.location.x = math.cos(camera_yaw) * camera_xy_distance
    camera.location.y = math.sin(camera_yaw) * camera_xy_distance
    camera.location.z = BOARD_HEIGHT + camera_distance * math.sin(camera_pitch)
    
    camera.rotation_euler.z = camera_yaw + math.pi/2
    camera.rotation_euler.x = -camera_pitch + math.pi/2

if __name__ == "__main__":
    randomizeCameraPosition(bpy.data.objects['Camera'])