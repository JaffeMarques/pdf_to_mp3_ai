import os
import re
from pydub import AudioSegment
from moviepy.editor import concatenate_audioclips, AudioFileClip
from src.providers.coqui import Coqui
from pathlib import Path
import math
from itertools import islice

class AudioProcessor:
    def __init__(self, value=None):
        self.value = value
        self.Coqui = Coqui()

    def natural_sort_key(self, file_name):
        return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', file_name)]

    def convert_chunks_to_audio(self, chunks, output_folder, reprocess=0):
        audio_files = []
        if reprocess > 0:
            chunks = islice(chunks, reprocess - 1, None)

        for i, chunk in enumerate(chunks, start=reprocess if reprocess > 0 else 1):
            print(f"[INFO] Processing chunk {i+1}")
            output_file = output_folder / f"chunk_{i+1}.mp3"
            self.Coqui.text_to_speech(chunk, output_file)
            audio_files.append(output_file)

        return audio_files
    
    
    
    def combine_audio_with_moviepy(self, folder_path):
        files = sorted(os.listdir(folder_path), key=self.natural_sort_key)
        thousands = math.ceil(len(files) / 1000)
        count = 0

        while count < thousands:
            audio_clips = []  # Reset clips for each chunk
            start_chunk = count * 1000
            max_chunk = (count + 1) * 1000
            print(f"Processing chunk {start_chunk} to {max_chunk}")

            for i, file_name in enumerate(files[start_chunk:max_chunk]):
                if file_name.endswith('.mp3'):
                    file_path = os.path.join(folder_path, file_name)
                    print(f"[INFO] Processing file: {file_path}")
                    try:
                        clip = AudioFileClip(file_path)
                        audio_clips.append(clip)
                    except Exception as e:
                        print(f"[ERROR] Error processing file {file_path}: {e}")

            output_preprocessed = Path('resources') / 'output' / 'tmp' / 'preprocessed' / f'{count}.mp3'
            if audio_clips:
                final_clip = concatenate_audioclips(audio_clips)
                final_clip.write_audiofile(output_preprocessed)
                print(f"[SUCCESS] Combined audio saved to {output_preprocessed}")
                
                # Clean up to free memory
                final_clip.close()
                for clip in audio_clips:
                    clip.close()
            else:
                print("[INFO] No audio clips to combine.")
            
            count += 1

    def combine_audio_from_folder(self, folder_path, pdf_name):
        audio_clips = []
        files = sorted(os.listdir(folder_path), key=self.natural_sort_key)

        for i, file_name in enumerate(files):
            if file_name.endswith('.mp3'):
                file_path = os.path.join(folder_path, file_name)
                print(f"[INFO] Processing file: {file_path}")
                try:
                    clip = AudioFileClip(file_path)
                    audio_clips.append(clip)
                except Exception as e:
                    print(f"[ERROR] Error processing file {file_path}: {e}")

        output_folder = Path('resources') / 'output' / 'completed' / f'{pdf_name}.mp3'
        if audio_clips:
            final_clip = concatenate_audioclips(audio_clips)
            final_clip.write_audiofile(output_folder)
            print(f"[SUCCESS] Combined audio saved to {output_folder}")
            
            final_clip.close()
            for clip in audio_clips:
                clip.close()
        else:
            print("[INFO] No audio clips to combine.")
        
        count += 1