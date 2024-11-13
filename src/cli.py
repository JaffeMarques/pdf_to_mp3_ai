import os
import sys
import logging
import argparse
from typing import List, Optional
from pathlib import Path
from src.config import settings
from src.processors.file_processor import FileProcessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PDFToAudioConverter:
    DEFAULT_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"
    DEFAULT_INPUT_DIR = settings.INPUT_FOLDER
    DEFAULT_OUTPUT_DIR = settings.OUTPUT_FOLDER

    def __init__(self, value=None):
        self.value = value
        self.input_dir = Path(self.DEFAULT_INPUT_DIR)
        self.output_dir = Path(self.DEFAULT_OUTPUT_DIR)
        self._ensure_directories()
        self.FileProcessor = FileProcessor(value)

    def _ensure_directories(self) -> None:
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def list_available_files(self) -> List[Path]:
        return sorted(self.input_dir.glob("*.pdf"))

    def get_available_models(self) -> List[str]:
        return [self.DEFAULT_MODEL]

    def process_file(self, filename: Path, model_name: str) -> None:
        """Process a single PDF file to convert it to audio."""
        logger.info(f"Processing file: {filename}")
        logger.info(f"Using model: {model_name}")
        self.FileProcessor.process_file(filename)
        pass

    def download_voice(self, voice_name: str) -> None:
        """Download a new voice model."""
        logger.info(f"Downloading voice: {voice_name}")
        # TODO: Implement voice download logic
        pass

    def merge_voices(self, voice1: str, voice2: str) -> None:
        """Merge two voice models."""
        logger.info(f"Merging voices: {voice1} and {voice2}")
        # TODO: Implement voice merging logic
        pass

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Convert PDF files to audio using TTS models",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Process command
    process_parser = subparsers.add_parser("process", help="Process PDF files")
    process_parser.add_argument(
        "-f", "--file",
        help="Specific PDF file to process (optional)"
    )
    process_parser.add_argument(
        "-m", "--model",
        default=PDFToAudioConverter.DEFAULT_MODEL,
        help="TTS model to use"
    )

    # Voice management commands
    voice_parser = subparsers.add_parser("voice", help="Voice management commands")
    voice_subparsers = voice_parser.add_subparsers(dest="voice_command")

    # Download voice command
    download_parser = voice_subparsers.add_parser("download", help="Download a voice model")
    download_parser.add_argument("name", help="Name of the voice to download")

    # Merge voices command
    merge_parser = voice_subparsers.add_parser("merge", help="Merge two voice models")
    merge_parser.add_argument("voice1", help="First voice model")
    merge_parser.add_argument("voice2", help="Second voice model")

    # List command
    subparsers.add_parser("list", help="List available PDF files")

    return parser

def interactive_file_selection(converter: PDFToAudioConverter) -> Optional[Path]:
    """Interactive file selection from available PDFs."""
    files = converter.list_available_files()
    if not files:
        logger.error("No PDF files found in the input directory")
        return None

    print("\nAvailable files:")
    for idx, file in enumerate(files, 1):
        print(f"[{idx}] {file.name}")

    while True:
        try:
            choice = int(input("\nChoose a file number (0 to cancel): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(files):
                return files[choice - 1]
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def entry_point():
    parser = create_parser()
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    converter = PDFToAudioConverter()

    try:
        if args.command == "process":
            file_path = None
            if args.file:
                file_path = Path(args.file)
            else:
                file_path = interactive_file_selection(converter)
            
            if file_path:
                converter.process_file(file_path, args.model)

        elif args.command == "voice":
            if args.voice_command == "download":
                converter.download_voice(args.name)
            elif args.voice_command == "merge":
                converter.merge_voices(args.voice1, args.voice2)

        elif args.command == "list":
            files = converter.list_available_files()
            if not files:
                print("No PDF files found in the input directory")
            else:
                print("\nAvailable PDF files:")
                for file in files:
                    print(f"- {file.name}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)
