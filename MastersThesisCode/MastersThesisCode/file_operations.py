import os
import polars as pl

def file_existence_check(path):
    print(f"Checking if the .csv exists at the following path: {path}", "\n")
    try:   
        os.remove(path)
        print("File found, replacing with new file...")
    except OSError:
        print("File does not exist. Generating new one...")
        pass

def file_to_dataframe_check(path):
    if os.path.isfile(path):
        print(f"Loading in data from {path}")
        dataframe = pl.read_csv(path)
        return dataframe
    else:
        print(f"No file exists for {path}. User will need to run the dataframe generation for this data.")
        return {}

def export_values_to_csv(filename, dataframe):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path_usage = os.path.join(script_dir, 'Data', f'{filename}')
    dataframe.write_csv(path_usage)
    print(f"File {filename} generated.", "\n")

