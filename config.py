import math
from mathutils import Vector

# Board configuration
BOARD_HEIGHT = 0.0
WHITE_YAW = -math.pi / 2.0
BLACK_YAW = math.pi / 2.0

# Background settings
BACKGROUND_HDRI_DIR = "./backgrounds/"

# Piece settings
PIECE_MAX_DISTANCE = 0.2
WHITE_PIECE_MATERIAL = "White_Pieces"
BLACK_PIECE_MATERIAL = "Black_Pieces"

# Camera settings
CAMERA_MIN_DISTANCE = 20.0
CAMERA_MAX_DISTANCE = 50.0
CAMERA_MIN_PITCH = math.pi / 10.0
CAMERA_MAX_PITCH = math.pi / 2.0
CAMERA_YAW_RANGE = math.pi / 2.0 # +/- 45 degrees

# Light settings
LIGHT_MIN_DISTANCE = 20.0
LIGHT_MAX_DISTANCE = 50.0
LIGHT_MIN_PITCH = math.pi / 10.0
LIGHT_MAX_PITCH = math.pi / 2.0

# File paths and rendering settings
FEN_FILEPATH = "./positions/PGN2FEN/output/FEN-results.txt"
FEN_PREFIX = "FEN format: "
RENDER_OUTDIR = "./output/"
PROPORTION_POSITIONS_RENDERED = 0.001