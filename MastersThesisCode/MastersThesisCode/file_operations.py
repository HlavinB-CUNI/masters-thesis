import os

def file_existence_check(path):
    print(f"Checking if the .csv exists at the following path: {path}", "\n")
    try:   
        os.remove(path)
        print("File found, replacing with new file...")
    except OSError:
        print("File does not exist. Generating new one...")
        pass

def export_values_to_csv(filename, dataframe):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path_usage = os.path.join(script_dir, 'Data', f'{filename}')
    dataframe.write_csv(path_usage)
    print(f"File {filename} generated.", "\n")