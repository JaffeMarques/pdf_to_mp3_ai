# pdf_to_mp3_ai

A lightweight tool that transforms PDF documents into audiobooks using Coqui TTS technology.

## Features
- PDF text extraction
- High-quality text-to-speech conversion using Coqui TTS
- Simple and user-friendly interface
- Support for long-form content

## Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JaffeMarques/pdf_to_mp3_ai.git
cd pdf_to_mp3_ai
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Project Structure
```
pdf_to_mp3_ai/
├── resources/
│   ├── files/     # Place your PDF files here
│   └── voices/    # Place your custom voice models (.wav) here
├── src/
│   └── ...
├── requirements.txt
└── README.md
```

## Usage

1. Place your PDF file in the `resources/files` directory
2. If using custom voices, place the .wav file in the `resources/voices` directory
3. Run the conversion:
```bash
python main.py process
```

## Important Notes
- Only PDF files placed in `resources/files` will be detected by the program
- Custom voice models must be placed in `resources/voices` directory
- Make sure your PDF files are text-based and not scanned images

## License
This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Coqui TTS](https://github.com/coqui-ai/TTS) for the text-to-speech technology
- All contributors to this project

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Support
If you encounter any problems, please file an issue along with a detailed description.
