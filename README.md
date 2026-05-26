# LiveTalk AI: Talking Head Video Generator

Generate realistic talking head videos from a single image and a text script.

## Features
- Lip-syncing, eye blinking, facial expressions
- Input: Portrait image (.jpg/.png) + text script (.txt)
- Output: Video of the person speaking the script

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Download required models:
   - dlib shape predictor: [Download link](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
   - SadTalker: [Follow official instructions](https://github.com/OpenTalker/SadTalker)

3. Place the models in the appropriate folders (see comments in code).

## Usage
```bash
python main.py --image path/to/image.jpg --text path/to/script.txt --output output_dir
```

## Project Structure
- `main.py`: Pipeline entry point
- `modules/`: Implementation modules

## Notes
- For best results, use a clear, frontal portrait image.
- SadTalker setup may require additional steps (see their repo).
