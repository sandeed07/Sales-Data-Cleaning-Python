import pandas as pd
import numpy as np
import os

def clean_sales_data(file_path):
    """
    Loads, cleans, and processes sales data from a given CSV/Excel file.

    Args:
        file_path (str): The path to the messy sales data file.

    Returns:
        pandas.DataFrame: A DataFrame containing the cleaned sales data.
    """
    print(f"Loading data from: {file_path}")
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: The file '{file_path}' does not exist. Please check the path.")
            return pd.DataFrame()

        # Load data (assuming CSV for simplicity, can extend to Excel)
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            print("Error: Unsupported file format. Please provide .csv or .xlsx")
            return pd.DataFrame()

    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()

    print(f"\n--- Initial Data Overview ({os.path.basename(file_path)}) ---")
    print(f"Total rows: {len(df)}")
    print("Columns and their data types (before cleaning):")
    df.info()
    print("\nFirst 5 rows (before cleaning):")
    print(df.head().to_string()) # .to_string() for better display in console

    # --- 1. Handle Missing Values ---
    print("\n--- Step 1: Handling Missing Values ---")
    # Identify missing values
    missing_before = df.isnull().sum()
    print("Missing values before cleaning:\n", missing_before[missing_before > 0])

    if 'Quantity' in df.columns:
        # Convert 'Quantity' to numeric, coerce errors to NaN
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        median_quantity = df['Quantity'].median()
        df['Quantity'].fillna(median_quantity, inplace=True)
        print(f"-> Filled missing 'Quantity' with median: {median_quantity}")

    if 'Product Name' in df.columns:
        initial_rows_before_dropping_product = len(df)
        df.dropna(subset=['Product Name'], inplace=True)
        print(f"-> Removed {initial_rows_before_dropping_product - len(df)} rows with missing 'Product Name'.")

    # --- 2. Remove Duplicates ---
    print("\n--- Step 2: Removing Duplicate Entries ---")
    initial_rows_before_duplicates = len(df)
    df.drop_duplicates(inplace=True)
    print(f"-> Removed {initial_rows_before_duplicates - len(df)} duplicate rows.")

    # --- 3. Standardize Date Formats ---
    print("\n--- Step 3: Standardizing Date Formats ---")
    if 'Date' in df.columns:
        # Convert to datetime objects, coercing errors will turn invalid dates into NaT
        initial_invalid_dates = df['Date'].isnull().sum()
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        # Drop rows where date conversion failed (if any critical)
        rows_dropped_due_to_date = df['Date'].isnull().sum() - initial_invalid_dates
        if rows_dropped_due_to_date > 0:
            df.dropna(subset=['Date'], inplace=True)
            print(f"-> Removed {rows_dropped_due_to_date} rows with unparseable date formats.")
        # Format to YYYY-MM-DD
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        print("-> Standardized 'Date' column to YYYY-MM-DD.")

    # --- 4. Normalize Product Names ---
    print("\n--- Step 4: Normalizing Product Names ---")
    if 'Product Name' in df.columns:
        df['Product Name'] = df['Product Name'].astype(str).str.strip().str.title() # Strip whitespace, Title Case
        # Example mapping for common misspellings (expand as needed)
        product_mapping = {
            'Lptop': 'Laptop',
            'Celphone': 'Cellphone',
            'Smartwatch': 'SmartWatch',
            'Keybord': 'Keyboard' # Added one more for demo
        }
        initial_unique_products = df['Product Name'].nunique()
        df['Product Name'] = df['Product Name'].replace(product_mapping)
        print(f"-> Normalized product names. Unique products before mapping: {initial_unique_products}, after mapping: {df['Product Name'].nunique()}")

    print(f"\n--- Cleaning Complete ---")
    print(f"Final rows in cleaned data: {len(df)}")
    print("Cleaned data info:")
    df.info()
    print("\nFirst 5 rows (after cleaning):")
    print(df.head().to_string())

    return df

# --- Main execution block ---
if __name__ == "__main__":
    # Specify the path to your messy data file
    # Make sure this file exists in the same directory as clean_data.py
    input_csv_file = 'messy_sales_data.csv'
    output_csv_file = 'cleaned_sales_data.csv'

    # Perform cleaning
    cleaned_df = clean_sales_data(input_csv_file)

    # Export cleaned data to a new CSV file
    if not cleaned_df.empty:
        cleaned_df.to_csv(output_csv_file, index=False)
        print(f"\nCleaned data saved to: {output_csv_file}")

        # --- Generate data for the Top 5 Products chart ---
        # Assuming 'Quantity' and 'Product Name' columns are now clean
        if 'Product Name' in cleaned_df.columns and 'Quantity' in cleaned_df.columns:
            print("\n--- Generating Top 5 Products Data ---")
            top_5_products = cleaned_df.groupby('Product Name')['Quantity'].sum().nlargest(5).reset_index()
            top_5_products.columns = ['product', 'sales']
            print("\nTop 5 Sold Products:")
            print(top_5_products.to_string(index=False))
        else:
            print("Could not generate top 5 products: 'Product Name' or 'Quantity' columns missing from cleaned data.")
    else:
        print("\nCleaning resulted in an empty DataFrame. No output file generated.")
