import argparse
import os
from modules.input_processing import InputProcessor
from modules.audio_generation import AudioGenerator
from modules.video_animation import VideoAnimator
from modules.output_processing import OutputProcessor

def main():
    parser = argparse.ArgumentParser(description='LiveTalk AI - Generate talking head videos')
    parser.add_argument('--image', required=True, help='Path to the input image')
    parser.add_argument('--text', required=True, help='Path to the text script')
    parser.add_argument('--output', default='output', help='Output directory')
    parser.add_argument('--shape_predictor', default='shape_predictor_68_face_landmarks.dat', help='Path to dlib shape predictor')
    parser.add_argument('--sadtalker_dir', default='SadTalker', help='Path to SadTalker directory')
    args = parser.parse_args()

    # Step 1: Input Processing
    inp = InputProcessor(args.shape_predictor)
    face_img = inp.detect_and_align(args.image)
    aligned_img_path = os.path.join(args.output, 'aligned_face.png')
    os.makedirs(args.output, exist_ok=True)
    from PIL import Image
    Image.fromarray(face_img).save(aligned_img_path)
    text = inp.process_text(args.text)

    # Step 2: Audio Generation
    audio_gen = AudioGenerator()
    audio_path = os.path.join(args.output, 'tts.wav')
    audio_gen.text_to_speech(text, audio_path)

    # Step 3: Video Animation
    animator = VideoAnimator(args.sadtalker_dir)
    video_path = animator.animate(aligned_img_path, audio_path, args.output)

    # Step 4: Output Processing
    out_proc = OutputProcessor()
    final_path = out_proc.finalize(video_path, args.output)
    print(f'Final video saved at: {final_path}')

if __name__ == '__main__':
    main()
