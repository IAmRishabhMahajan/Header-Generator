import pandas as pd
from collections import Counter
import os
import google.generativeai as genai
import sys

# Configure the Google Generative AI library
genai.configure(api_key="KEY") 

# Detect delimiter
def detect_delimiter(file_path):
    with open(file_path, 'r') as file:
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
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        second_line = file.readline().strip()

    first_line_parts = first_line.split(delimiter)
    second_line_parts = second_line.split(delimiter)

    if all(x.isalpha() for x in first_line_parts if x) and not all(x.isalpha() for x in second_line_parts if x):
        return True
    return False

# Load data, removing headers if present
def load_data(file_path):
    delimiter = detect_delimiter(file_path)
    headers_present = has_headers(file_path, delimiter)

    if headers_present:
        
        return pd.read_csv(file_path, delimiter=delimiter, header=0), delimiter
    else:
        
        return pd.read_csv(file_path, delimiter=delimiter, header=None), delimiter

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
    suggested_headers = [header.strip() for header in suggested_headers.split(',')]  # Split by comma and clean
    
    if len(suggested_headers) == dataframe.shape[1]:
        dataframe.columns = suggested_headers
        return True, dataframe
    else:
        
        return False, dataframe

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
                
                return
        
        # Append the updated data with headers to the original file
        updated_file_path = file_path.replace('.csv', '_with_headers.csv')
        df.to_csv(updated_file_path, index=False, mode='a', header=True)
        print(f"\nHeaders applied and appended to '{updated_file_path}'.")

    except Exception as e:
        print(f"Error processing file: {e}")

# Command-line interface
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python codename.py <file_name.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    if not file_path.endswith('.csv'):
        print(f"Error: File '{file_path}' is not a CSV file.")
        sys.exit(1)

    main(file_path)