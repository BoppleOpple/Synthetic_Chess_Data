import math

# Board configuration
BOARD_HEIGHT = 0.0

# Camera settings
CAMERA_MIN_DISTANCE = 20.0
CAMERA_MAX_DISTANCE = 50.0
CAMERA_MIN_PITCH = math.pi/10.0
CAMERA_MAX_PITCH = math.pi/2.0

# Light settings
LIGHT_MIN_DISTANCE = 20.0
LIGHT_MAX_DISTANCE = 50.0
LIGHT_MIN_PITCH = math.pi/10.0
LIGHT_MAX_PITCH = math.pi/2.0

# File paths and rendering settings
FEN_FILEPATH = "./positions/PGN2FEN/output/FEN-results.txt"
FEN_PREFIX = "FEN format: "
RENDER_OUTDIR = "./output/"
PROPORTION_POSITIONS_RENDERED = 0.001
RENDERS_PER_POSITION = 2 