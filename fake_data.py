import pandas as pd
from faker import Faker
import re
from datetime import datetime

# Initialize the Faker object
fake = Faker()

# Function to generate fake data based on the value type and patterns
def generate_fake_data(value, column_name):
    # Check for empty values (None, NaN, or empty string)
    if not value or pd.isna(value):
        return value  # Return the value unchanged if it's empty or NaN

    column_name_lower = column_name.lower()

    # Handle phone numbers
    if any(key in column_name_lower.lower() for key in ['phone', 'mobile']) or re.match(r"^\+?\d{7,15}$", str(value)):
        return fake.phone_number()

    # Handle addresses
    if "address" in column_name_lower:
        return fake.address().replace("\n", "")

    # Handle dates (assuming dob is a date)
    if any(key in column_name_lower for key in ['dob', 'date']) or (isinstance(value, str) and re.match(r"\d{4}-\d{2}-\d{2}", value)):
        try:
            original_date = datetime.strptime(value, "%Y-%m-%d")
            # Generate a fake date within the same range
            fake_date = fake.date_of_birth(minimum_age=18, maximum_age=100)
            return fake_date.strftime("%Y-%m-%d")
        except ValueError:
            return value  # If it doesn't parse as a date, return the original value

    # Handle numeric data
    if isinstance(value, (int, float)):
        # Generate a fake number with the same number of digits
        fake_data = fake.random_number(digits=len(str(abs(int(value)))), fix_len=True)
        return fake_data

    # Handle generic strings (like names)
    if isinstance(value, str):
        fake_data = fake.name()  # Default to generating a fake name
        # Adjust the length of the fake data to match the original string length
        if len(fake_data) != len(value):
            return fake_data[:len(value)] if len(fake_data) >= len(value) else fake_data.ljust(len(value))
        return fake_data

    # For other types of data, return the original value
    return value 

# Function to process the dataframe
def process_dataframe(df):
    # Iterate over each column in the dataframe
    for column in df.columns:
        column_lower = column.lower()  # Convert column name to lowercase for case-insensitive matching
        # Check if the column matches specific patterns
        if column_lower.endswith('_personal'):
            # Replace values in this column with fake data
            df[column] = df[column].apply(lambda x: generate_fake_data(x, column))
    
    return df

# Function to load the dataframe and process it
def load_and_process_csv(file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Process the DataFrame to generate fake data for appropriate columns
    processed_df = process_dataframe(df)

    # Save the processed DataFrame to a new file
    output_file = file_path.replace(".csv", "_with_fake_data.csv")
    processed_df.to_csv(output_file, index=False)
    print(f"Processed file saved as: {output_file}")

    return output_file

# Main function to run the process
def apply_fake_data(file_path):
    try:
        # Process the file
        output_file = load_and_process_csv(file_path)
    except Exception as e:
        print(f"Error processing file: {e}")
    return output_file
