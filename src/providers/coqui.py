from TTS.api import TTS
import re
import torch
from src.config import settings

class Coqui():
    def __init__(self, value=None):
        self.value = value
        self.tts = self.initialize_tts()

    def initialize_tts(self, model_name="tts_models/multilingual/multi-dataset/xtts_v2"):
        try:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            tts = TTS(model_name=model_name)
            tts.to(device)

            print("[SUCCESS] Model loaded successfully.")
            print(f"[INFO] Available languages: {tts.languages if hasattr(tts, 'languages') else 'Not specified'}")

            return tts
        except Exception as e:
            print(f"[ERROR] Failed to initialize TTS: {str(e)}")
            return None
        
    def preprocess_text(self, text):
        abbreviations = {
            'Dr.': 'Doutor',
            'Sr.': 'Senhor',
            'Sra.': 'Senhora',
            'Prof.': 'Professor',
            'etc.': 'etcetera',
            'Ex.': 'Exemplo',
            'Gov.': 'Governador',
            'Av.': 'Avenida',
            'St.': 'Santo',
            'Sta.': 'Santa'
        }
        
        for abbr, full in abbreviations.items():
            text = text.replace(abbr, full)
        
        text = re.sub(r'(\d)\.(\d)', r'\1@\2', text)
        
        text = text.replace('.', ' ')
        
        text = text.replace('@', '.')
        
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
        
    def text_to_speech(self, chunk, output_path):
        print("[INFO] Starting text-to-speech conversion...")
        tts = self.tts

        if tts is None:
            print("[ERROR] TTS model was not initialized successfully.")
        else:
            try:
                print(f"[INFO] Generating audio file at '{output_path}'...")
                tts.tts_to_file(
                    text=self.preprocess_text(chunk),
                    file_path=output_path,
                    speaker_wav=settings.SPEAKER_PATH,
                    language=settings.TTS_LANGUAGE
                )
                print(f"[SUCCESS] Audio file created at '{output_path}'.")
            except Exception as e:
                print(f"[ERROR] Failed to create audio file: {str(e)}")
