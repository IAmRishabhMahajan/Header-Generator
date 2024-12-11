import pandas as pd
from faker import Faker

# Initialize the Faker object
fake = Faker()

# Generate fake data based on the value type and ensure the length remains the same
# Generate fake data based on the value type and ensure the length remains the same
def generate_fake_data(value):
    # Check for empty values (None, NaN, or empty string)
    if not value or pd.isna(value):
        return value  # Return the value unchanged if it's empty or NaN

    # First, check if the value is numeric (either int or float)
    if isinstance(value, (int, float)):
        # For numbers, generate a fake number that has the same number of digits as the original value
        fake_data = fake.random_number(digits=len(str(abs(int(value)))), fix_len=True)
        return fake_data
    
    # If it's not a number, then check if it's a string
    elif isinstance(value, str):
        # If it's a string, generate a fake name or other string
        fake_data = fake.name()  # You can replace this with any other fake data generator (like fake.address())
        # Adjust the length of the fake data to match the original string length
        if len(fake_data) != len(value):
            # Truncate or pad to match the length of the original value
            return fake_data[:len(value)] if len(fake_data) >= len(value) else fake_data.ljust(len(value))
        return fake_data

    # For other types of data (like dates), return the original value (you can customize this for other data types)
    else:
        return value 

# Function to process the dataframe
def process_dataframe(df):
    # Iterate over each column in the dataframe
    for column in df.columns:
        # Check if the column name ends with 'a'
        if column.endswith('_personal'):
            # Replace values in this column with fake data, maintaining the original length
            df[column] = df[column].apply(lambda x: generate_fake_data(x))
    
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
    

    # Check if the file exists and process it
    try:
        output_file = load_and_process_csv(file_path)
    except Exception as e:
        print(f"Error processing file: {e}")
    return output_file


