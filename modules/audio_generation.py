import edge_tts
import asyncio
import os

class AudioGenerator:
    def __init__(self, voice="en-US-ChristopherNeural"):
        """Initialize the audio generator with a default voice"""
        self.voice = voice
        
    def text_to_speech(self, text, output_path):
        """Convert text to speech using Edge TTS"""
        async def _generate():
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(output_path)
            
        # Run the async function
        asyncio.run(_generate())
        
        if not os.path.exists(output_path):
            raise ValueError("Failed to generate audio file")
            
        return output_path
        
    def set_voice(self, voice):
        """Change the TTS voice"""
        self.voice = voice
        
    @staticmethod
    async def get_available_voices():
        """Get list of available voices"""
        voices = await edge_tts.list_voices()
        return [voice["ShortName"] for voice in voices]

# For advanced TTS (e.g., edge-tts), add methods or swap implementation as needed
