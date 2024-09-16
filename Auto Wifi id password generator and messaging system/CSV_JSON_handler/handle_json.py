from pathlib import Path
from json import load  ,dump


def read_send_data_to_json(file_name , action , data = None):
    
    File_DIR = str(Path.cwd())
    
    file_name = File_DIR + "/ALL_DATA_FILES/" + file_name + ".json"
    file = open(file_name , action)
    if action == "w":
        dump(data , file)
        file.close()
        return True
    elif action == 'r':
        all_data = dict(load(file))
        file.close()
        return all_data
    return False

def read_or_write_json_data(file_name , action , data=None):
    File_DIR = str(Path.cwd())

    file_path = File_DIR+ "/ALL_DATA_FILES/" + file_name +".json"
    if action == 'w':
        file = open(file_path , 'w')
        dump(data , file)
        file.close()
        return True
    elif action == 'r':
        file = open(file_path , 'r')
        file_data = load(file)
        file.close()
        return file_data
    else:
        return False