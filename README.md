# README

## Overview
This Python script processes a CSV file by detecting its delimiter, determining if it has headers, and using Google Generative AI to suggest appropriate headers for the file. The generated headers are applied to the data and appended to a new file named `<original_filename>_with_headers.csv`. If the generated headers do not match the required number of columns, the script retries up to 5 times to generate valid headers.

## Features
- Automatically detects the delimiter used in the CSV file.
- Checks if the file has headers and handles them appropriately.
- Uses Google Generative AI to suggest specific and relevant headers.
- Retries header generation up to 5 times if the headers do not match the number of columns.
- Saves the processed file with the applied headers as `<original_filename>_with_headers.csv`.

## Requirements
- Python 3.7 or higher
- Pandas library
- Google Generative AI Python SDK (`google-generativeai`)

## Installation
1. Install Python 3.7 or higher if not already installed.
2. Install the required Python packages:
   ```bash
   pip install pandas google-generativeai
   ```
3. Configure the Google Generative AI library with your API key. Replace `"KEY"` in the script with your actual API key.

## Usage
### Command-Line Interface
To use the script, run it from the command line with the following syntax:
```bash
python codename.py <file_name.csv>
```
- `<file_name.csv>`: Path to the CSV file to be processed.

### Example
```bash
python codename.py data.csv
```
- If `data.csv` does not have headers, the script will suggest and apply new headers.
- If `data.csv` has headers, it will use the existing structure to process the file.
- The processed file will be saved as `data_with_headers.csv`.

## Error Handling
- If the file does not exist, the script prints an error message and exits.
- If the file is not a CSV file, it prints an error message and exits.
- If the headers cannot be successfully generated after 5 attempts, the script terminates with a failure message.

## File Output
- The script appends the processed data with headers to a new file named `<original_filename>_with_headers.csv`.

## Limitations
- The script assumes that the input file is well-formed and can be read by Pandas.
- If the file contains complex or ambiguous data, the Generative AI may not always suggest accurate headers.

## Future Enhancements
- Add support for other file formats like TSV or Excel.
- Include more robust error handling for corrupted or malformed input files.
- Provide a verbose mode for detailed logs during execution.

## Author
This script was designed for users who require automated header generation and CSV processing with minimal manual intervention. For questions or improvements, feel free to contribute!

