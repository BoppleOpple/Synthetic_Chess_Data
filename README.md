# Chess Scene Generator
This is a Blender script that generates chess scenes from PGN files. There are several options for the camera, lighting, and board/piece appearance located in the config.py file.

## Setup
1. Install Blender

## Usage
1. Run PGN2FEN code to generate FEN strings from PGN files.
2. Run CameraAngles.py on Chess_Board.blend to generate images uint the following command:
```bash
blender -b Chess_Board.blend -P CameraAngles.py
```

## TODO
- [ ] render multiple camera angles simultaneously
- [ ] *maybe* do a better job of threading it
- [ ] maybe add more material options
- [ ] maybe add more background options
- [ ] maybe add more light options
- [ ] maybe add a requirements.txt

## DONE
- [x] dont reload board for each image if the position hasnt changed
- [x] rotate pieces you fool
- [x] slight offsets from centers (for datagen)
- [x] maybe add a README.md
- [x] include PGN2FEN code in chess_scene_utils
    - [x] rename chess_scene_utils.py to helpers.py
