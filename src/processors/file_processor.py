import os
import re
import time
import logging
import pdfplumber
from src.config import settings
from pathlib import Path
from src.processors.audio_processor import AudioProcessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FileProcessor:
    def __init__(self, value=None):
        self.value = value
        self.AudioProcessor = AudioProcessor()

    def pdf_to_markdown(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            markdown_content = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    markdown_page = text.replace('\n', '\n\n')
                    markdown_content += markdown_page + '\n\n---\n\n'

            return markdown_content
        
    def markdown_to_plain_text(self, markdown_text):
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', markdown_text)

        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold with **
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic with *
        text = re.sub(r'\_\_([^_]+)\_\_', r'\1', text)  # Bold with __
        text = re.sub(r'\_([^_]+)\_', r'\1', text)      # Italic with _

        text = re.sub(r'#+\s?', '', text)  # Headers
        text = re.sub(r'-\s?', '', text)   # List items
        text = re.sub(r'>\s?', '', text)   # Blockquotes
        return text
    
    def split_text(self, text, max_chunk_size=settings.MAX_CHUNK_SIZE):
        chunks = []
        current_chunk = ""

        for sentence in text.split('.'):
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
                current_chunk += sentence + "."
            else:
                chunks.append(current_chunk)
                current_chunk = sentence + "."

        if current_chunk:
            chunks.append(current_chunk)

        return chunks
    
    def process_file(self, filename: Path):
        pdf_path = f'{filename}'
        markdown_text = self.pdf_to_markdown(pdf_path)
        print('[SUCCESS] Marked ready')

        plain_text = self.markdown_to_plain_text(markdown_text)
        print('[SUCCESS] Plain text ready')

        chunks = self.split_text(plain_text)
        print('[SUCCESS] Splited text ready')

        output_folder = Path('resources') / 'output' / 'tmp'

        # reprocess = 4767
        # self.AudioProcessor.convert_chunks_to_audio(chunks, output_folder, reprocess)

        self.AudioProcessor.convert_chunks_to_audio(chunks, output_folder)
        print('[SUCCESS] Chunks ready')

        # self.AudioProcessor.combine_audio_with_moviepy(output_folder, Path('resources') / 'output' / 'completed' / f'{filename}.mp3')
        self.AudioProcessor.combine_audio_from_folder(Path('resources') / 'output' / 'tmp' / 'preprocessed', 'completed')
        #combine_audio_with_pydub('chunks', f'output/{filename}.mp3')
        print('[SUCCESS] Audio ready')