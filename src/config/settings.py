import os
from pathlib import Path
from dotenv import load_dotenv

INPUT_FOLDER = os.getenv('INPUT_FOLDER', Path('resources') / 'files')
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', Path('resources') / 'output' / 'completed')
TMP_FOLDER = os.getenv('TMP_FOLDER',  Path('resources') / 'output' / 'tmp')
MAX_CHUNK_SIZE = os.getenv('MAX_CHUNK_SIZE', 150)
SPEAKER_PATH = os.getenv('SPEAKER_PATH', Path('resources') / 'voices' / '4367.wav')
TTS_LANGUAGE = os.getenv('TTS_LANGUAGE', 'pt')