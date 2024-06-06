import os

# Delete files

def delete_files(paths):
    working_directory = os.getcwd()
    try:
        for path in paths:
            os.remove(working_directory+path)
            print(F"file deleted= {path}")
        return True
    except Exception as e:
        print(e)
        return False
