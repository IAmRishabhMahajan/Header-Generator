import pandas as pd
from collections import Counter
import os
import google.generativeai as genai
import sys
import chardet
from fake_data import apply_fake_data

# Configure the Google Generative AI library
genai.configure(api_key="AIzaSyAdMFyDKFKD8yk0qLZ5dnrJ1XDL0CoWHXQ")

# Detect file encoding
def detect_encoding(file_path):
    with open(file_path, "rb") as file:
        result = chardet.detect(file.read(10000))  # Read a sample of the file
        print(f"Detected encoding: {result['encoding']}")
        return result["encoding"]

# Convert the file to UTF-8 (optional)
def convert_to_utf8(file_path, detected_encoding):
    utf8_file_path = file_path.replace(".csv", "_utf8.csv")
    try:
        with open(file_path, "r", encoding=detected_encoding, errors="replace") as file:
            content = file.read()
        with open(utf8_file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"File converted to UTF-8 and saved as: {utf8_file_path}")
        return utf8_file_path
    except Exception as e:
        print(f"Error converting file to UTF-8: {e}")
        return file_path  # Return the original file path if conversion fails

# Detect delimiter
def detect_delimiter(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        first_line = file.readline()

        # Common delimiters to check for
        delimiters = [',', '\t', '|', ';', ' ']

        # Count occurrences of each delimiter in the first line
        delimiter_counts = {d: first_line.count(d) for d in delimiters}

        # Find the most common delimiter
        most_common_delimiter = max(delimiter_counts, key=delimiter_counts.get)
        print(f"Detected delimiter: '{most_common_delimiter}'")
        return most_common_delimiter

# Check if the file has headers
def has_headers(file_path, delimiter):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        first_line = file.readline().strip()
        second_line = file.readline().strip()

    first_line_parts = first_line.split(delimiter)
    second_line_parts = second_line.split(delimiter)

    if all(x.isalpha() for x in first_line_parts if x) and not all(x.isalpha() for x in second_line_parts if x):
        return True
    return False

# Load data, ensuring UTF-8 only if necessary
def load_data(file_path):
    try:
        # Try to load the file with UTF-8 encoding first
        print(f"Attempting to open file with UTF-8 encoding...")
        df = pd.read_csv(file_path, encoding='utf-8')
        print("File opened successfully with UTF-8 encoding.")
        return df, ','  # Assuming default delimiter as ',' for now
    except UnicodeDecodeError:
        # If UTF-8 fails, detect encoding and convert
        print(f"Error: Unable to open file with UTF-8 encoding. Attempting to detect encoding...")
        detected_encoding = detect_encoding(file_path)
        file_path = convert_to_utf8(file_path, detected_encoding)
        
        # After conversion, reload the file with UTF-8 encoding
        df = pd.read_csv(file_path, encoding='utf-8')
        return df, ','  # Assuming default delimiter as ',' for now

import google.generativeai as genai

def append_personal_to_columns(suggested_columns, dataframe):
    # Get 5 rows of data from the DataFrame for context
    sample_data = dataframe.head(5).to_string(index=False)
    
    # Generate the prompt for genai
    prompt = f"""Based on the following data sample, append '_personal' to any column names that relate to personal data (e.g., names, phone numbers, addresses, credit card numbers). 
    The number of column names must remain the same, and you should return the same number of columns as in the dataset. 
    Data sample (first 5 rows): {sample_data}
    Suggested column names (without '_personal' suffix): {suggested_columns}
    Please provide the result as a comma-separated list of column names. Ensure the output has the same number of column names as the input and append '_personal' to the relevant ones."""
    
    # Call the Google Generative AI API
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    # Extract the updated column names
    updated_columns = response.text.strip()
    
    # Return the updated column names
    return updated_columns


# Use the Generative AI model to suggest headers
def suggest_headers(dataframe):
    # Convert a sample of the DataFrame to string
    
    sample_data = dataframe.head(10).to_string(index=False)

    # Generate headers using the Google Generative AI library
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""Based on the following data sample, suggest appropriate headers for the columns. Ensure the number of headers matches the number of columns in the data that is {len(dataframe.columns)} here (no more, no less). The headers should be relevant and informative. The headers should be specific and not generic. Provide the result in the format: header1,header2,...,headerN. Do not include any additional text or explanations in the response. Data sample:{sample_data}"""


    response = model.generate_content(prompt)
    
    # Extract the headers and ensure proper formatting
    suggested_headers = response.text.strip()
    return suggested_headers

# Apply suggested headers to the DataFrame
def apply_headers(dataframe, suggested_headers):
    suggested_headers = append_personal_to_columns(suggested_headers, dataframe)
    suggested_headers = [header.strip() for header in suggested_headers.split(',')]  # Split by comma and clean

    if len(suggested_headers) == dataframe.shape[1]:
        dataframe.columns = suggested_headers
        return True, dataframe
    else:
        return False, dataframe

import pandas as pd

def remove_personal_suffix(file_path):
    # Read only the header (first row) of the CSV file
    headers = pd.read_csv(file_path, nrows=0).columns
    
    # Modify the column names by removing '_personal' suffix
    updated_columns = [col.replace('_personal', '') if col.endswith('_personal') else col for col in headers]
    
    # Read the entire file with updated column names
    df = pd.read_csv(file_path, names=updated_columns, header=0)
    
    # Overwrite the original file with the updated DataFrame
    df.to_csv(file_path, index=False)
    print(f"Original file updated with new column names: {file_path}")
    
    

# Main function
def main(file_path):
    try:
        # Load the data
        df, delimiter = load_data(file_path)

        # Retry logic for generating headers
        retries = 5
        for attempt in range(retries):
            suggested_headers = suggest_headers(df)

            success, df = apply_headers(df, suggested_headers)
            if success:
                break
            elif attempt == retries - 1:
                print("Failed to apply suggested headers after multiple attempts.")
                return

        # Append the updated data with headers to the original file
        updated_file_path = file_path.replace('.csv', '_with_headers.csv')
        df.to_csv(updated_file_path, index=False, mode='a', header=True)
        print(f"\nHeaders applied and appended to '{updated_file_path}'.")
        file_with_fake_data = apply_fake_data(updated_file_path)
        remove_personal_suffix(file_with_fake_data)


    except Exception as e:
        print(f"Error processing file: {e}")

# Command-line interface
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_name.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    if not file_path.endswith('.csv'):
        print(f"Error: File '{file_path}' is not a CSV file.")
        sys.exit(1)

    main(file_path)
