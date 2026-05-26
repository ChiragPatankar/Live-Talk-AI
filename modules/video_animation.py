# This module assumes SadTalker is installed and its API is available
# For full SadTalker setup, see: https://github.com/OpenTalker/SadTalker
import os
import sys
import subprocess
import tempfile
from pathlib import Path

class VideoAnimator:
    def __init__(self, sadtalker_path):
        """Initialize the video animator with path to SadTalker"""
        self.sadtalker_path = Path(sadtalker_path)
        if not self.sadtalker_path.exists():
            raise ValueError(f"SadTalker directory not found at {sadtalker_path}")
        
        # Verify key files exist
        self.inference_script = self.sadtalker_path / "inference.py"
        if not self.inference_script.exists():
            raise ValueError(f"inference.py not found in {sadtalker_path}")
            
    def animate(self, source_image, audio_path, output_dir):
        """Generate talking head video using SadTalker"""
        # Ensure all input files exist
        if not os.path.exists(source_image):
            raise ValueError(f"Source image not found: {source_image}")
        if not os.path.exists(audio_path):
            raise ValueError(f"Audio file not found: {audio_path}")
            
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Prepare the command
        cmd = [
            sys.executable,
            str(self.inference_script),
            "--driven_audio", audio_path,
            "--source_image", source_image,
            "--result_dir", output_dir,
            "--enhancer", "gfpgan",  # Use GFPGAN for face enhancement
            # Removed unsupported --use_pose_style argument
            "--still",  # Add as a flag if still image input is desired
            "--preprocess", "full"  # Full preprocessing for better quality
        ]
        
        try:
            # Run SadTalker
            process = subprocess.Popen(
                cmd,
                cwd=str(self.sadtalker_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for completion and get output
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"SadTalker failed: {stderr}")
                
            # Find the output video file
            result_files = list(Path(output_dir).glob("*.mp4"))
            if not result_files:
                raise ValueError("No output video file found")
                
            # Return path to the generated video
            return str(result_files[0])
            
        except Exception as e:
            raise RuntimeError(f"Error running SadTalker: {str(e)}")
            
    def cleanup(self, output_dir):
        """Clean up temporary files"""
        try:
            for file in Path(output_dir).glob("*"):
                if file.is_file():
                    file.unlink()
        except Exception as e:
            print(f"Warning: Error during cleanup: {str(e)}")
