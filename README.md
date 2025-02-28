# PDF Vocabulary Extractor

This repository extracts words from a PDF file, provided that the PDF is in text format (not scanned images).

## Features
- Extracts text from PDF files.
- Filters words based on the NGSL model.
- Uses SFI (Standard Frequency Index) scores for ranking words.
  - **Lower SFI values indicate more advanced vocabulary.**
- Built with Flask and Python.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/amirzack/pdf-vocab-extractor.git
   cd pdf-vocab-extractor
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```sh
   python app.py
   ```

## Usage

- Upload a PDF file via the provided API or UI.
- Extracted words will be processed and filtered based on their SFI scores.

## Technologies Used
- **Python** for backend processing
- **Flask** for API and server
- **PyPDF2** or **pdfplumber** for text extraction
- **NGSL word list** for vocabulary filtering

## Contributing
Feel free to submit pull requests or report issues.

## License
[MIT License](LICENSE)
