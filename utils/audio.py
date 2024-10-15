# A/utils/audio.py

"""
File: audio.py
Path: A/utils/audio.py
Author: Benoit Desrosiers
Date: 06-04-23
Description: Utility module for audio processing using in-memory audio streams.
"""

import io
from gtts import gTTS


class AudioUtils:
    """
    Utility class for audio processing.
    """

    @staticmethod
    def generate_audio(text):
        """
        Generate audio from text using TTS and return an in-memory audio stream.

        Args:
            text (str): The text to convert into audio.

        Returns:
            io.BytesIO or None: An in-memory bytes buffer containing the audio data, or None on failure.
        """
        try:
            tts = gTTS(text=text)
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)  # Reset pointer to the beginning
            return audio_fp
        except Exception as e:
            print(f"Error generating audio: {e}")
            return None
