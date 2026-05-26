import streamlit as st
import os
from modules.input_processing import InputProcessor
from modules.audio_generation import AudioGenerator
from modules.video_animation import VideoAnimator
from modules.output_processing import OutputProcessor
from PIL import Image
import tempfile

st.title('LiveTalk AI: Talking Head Video Generator')

# Sidebar for model paths
dlib_path = st.sidebar.text_input('Path to shape_predictor_68_face_landmarks.dat', 'shape_predictor_68_face_landmarks.dat')
sadtalker_dir = st.sidebar.text_input('Path to SadTalker directory', 'SadTalker')

uploaded_image = st.file_uploader('Upload a portrait image', type=['jpg', 'jpeg', 'png'])

script_option = st.radio('Script Input:', ['Type text', 'Upload .txt file'])
if script_option == 'Type text':
    script_text = st.text_area('Enter the script to speak:')
else:
    uploaded_script = st.file_uploader('Upload script (.txt)', type=['txt'])
    script_text = uploaded_script.read().decode('utf-8') if uploaded_script else ''

if st.button('Generate Talking Head Video'):
    if not uploaded_image or not script_text:
        st.error('Please upload an image and provide a script.')
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save image
            image_path = os.path.join(tmpdir, 'input.png')
            img = Image.open(uploaded_image)
            img.save(image_path)
            # Save script
            script_path = os.path.join(tmpdir, 'script.txt')
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_text)
            # Run pipeline
            inp = InputProcessor(dlib_path)
            face_img = inp.detect_and_align(image_path)
            aligned_img_path = os.path.join(tmpdir, 'aligned_face.png')
            Image.fromarray(face_img).save(aligned_img_path)
            text = inp.process_text(script_path)
            audio_gen = AudioGenerator()
            audio_path = os.path.join(tmpdir, 'tts.wav')
            audio_gen.text_to_speech(text, audio_path)
            animator = VideoAnimator(sadtalker_dir)
            video_path = animator.animate(aligned_img_path, audio_path, tmpdir)
            out_proc = OutputProcessor()
            final_path = out_proc.finalize(video_path, tmpdir)
            st.success('Video generated!')
            with open(final_path, 'rb') as vid_file:
                st.video(vid_file.read())
