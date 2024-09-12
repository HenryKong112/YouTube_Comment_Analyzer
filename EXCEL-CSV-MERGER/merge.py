import pandas as pd
from datetime import date
import os

today_date = date.today()

def merge(filetype):
    # Specify the directory path where the files are located
    directory_path = input("Enter your file path: ")

    # Initialize a list to store individual DataFrames
    merge_df_list = []

    # Iterate over files in the specified directory
    for file in os.listdir(directory_path):
        # For CSV files
        if filetype == 2 and file.endswith('.csv'):
            # Construct the full file path
            file_path = os.path.join(directory_path, file)
            # Read each CSV file
            df = pd.read_csv(file_path, header=0)
            merge_df_list.append(df)
        
        # For Excel files
        elif filetype == 1 and file.endswith('.xlsx'):
            file_path = os.path.join(directory_path, file)
            # Read each Excel file
            df = pd.read_excel(file_path, header=0)
            merge_df_list.append(df)

    # Concatenate all DataFrames in the list into a single DataFrame
    merge_df = pd.concat(merge_df_list, ignore_index=True)

    # Save the merged DataFrame to a new file based on the file type
    if filetype == 1:
        output_path = os.path.join(directory_path, f'Merged_{today_date}.xlsx')
        merge_df.to_excel(output_path, index=False)
    elif filetype == 2:
        output_path = os.path.join(directory_path, f'Merged_{today_date}.csv')
        merge_df.to_csv(output_path, index=False)

def main():
# Main logic to select file type and call merge function
    while True:
        print("Enter the file type you want to merge")
        FILE_TYPE = int(input("1. xlsx\n2. csv\nEnter the number: "))

        if FILE_TYPE == 1 or FILE_TYPE == 2:
            merge(FILE_TYPE)
            print("Merged file is created successfully!")
            
        else:
            print("Please enter 1 for xlsx or 2 for csv.")

if __name__ == "__main__":
    main()