import os
import subprocess
from pathlib import Path
import shutil

class OutputProcessor:
    def __init__(self):
        """Initialize the output processor"""
        # Verify ffmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
        except FileNotFoundError:
            raise RuntimeError("FFmpeg not found. Please install FFmpeg to use this module.")

    def finalize(self, video_path, output_dir):
        """Process and enhance the output video"""
        if not os.path.exists(video_path):
            raise ValueError(f"Input video not found: {video_path}")

        # Create output path
        output_path = os.path.join(output_dir, 'final_output.mp4')
        
        try:
            # Enhance video quality and ensure web compatibility
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-c:v', 'libx264',  # Use H.264 codec
                '-preset', 'medium',  # Balance between quality and encoding speed
                '-crf', '23',  # Constant Rate Factor (18-28 is visually lossless)
                '-c:a', 'aac',  # Use AAC audio codec
                '-b:a', '192k',  # Audio bitrate
                '-movflags', '+faststart',  # Enable fast start for web playback
                '-y',  # Overwrite output file if it exists
                output_path
            ]
            
            # Run ffmpeg
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if process.returncode != 0:
                raise RuntimeError(f"FFmpeg processing failed: {process.stderr}")
                
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"Error processing video: {str(e)}")
            
    def compress_for_web(self, video_path, target_size_mb=10):
        """Compress video to target size while maintaining quality"""
        if not os.path.exists(video_path):
            raise ValueError(f"Input video not found: {video_path}")
            
        output_path = str(Path(video_path).with_name('compressed_output.mp4'))
        
        try:
            # Get video duration
            probe_cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video_path
            ]
            duration = float(subprocess.check_output(probe_cmd).decode().strip())
            
            # Calculate target bitrate (in bits per second)
            target_size_bits = target_size_mb * 8 * 1024 * 1024
            bitrate = int(target_size_bits / duration)
            
            # Compress video
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-c:v', 'libx264',
                '-b:v', f'{bitrate}',
                '-pass', '1',
                '-f', 'null',
                '/dev/null'
            ]
            
            # Two-pass encoding for better quality
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-c:v', 'libx264',
                '-b:v', f'{bitrate}',
                '-pass', '2',
                '-c:a', 'aac',
                '-b:a', '128k',
                output_path
            ]
            
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"Error compressing video: {str(e)}")
            
    def cleanup_temp_files(self, directory):
        """Clean up temporary files and directories"""
        try:
            # Remove FFmpeg pass log files
            for file in Path(directory).glob('ffmpeg2pass*'):
                file.unlink()
            
            # Remove any other temporary files
            for file in Path(directory).glob('temp_*'):
                if file.is_file():
                    file.unlink()
                elif file.is_dir():
                    shutil.rmtree(file)
                    
        except Exception as e:
            print(f"Warning: Error during cleanup: {str(e)}")
