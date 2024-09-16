from importlib.machinery import SourceFileLoader
from pathlib import Path


# Loading Modules
from CSV_JSON_handler.handle_json import read_send_data_to_json


def new_phone_no_add(guest_list):

    DIR_LOCATION = str(Path.cwd())

    try:
        if len(guest_list) != 0:
            #json_obj = SourceFileLoader('read_send_data_to_json' , DIR_LOCATION + "/CSV_JSON_handler/handle_json.py").load_module()
            data_of_phone_check_file = read_send_data_to_json("Phone_check_file" , "r")

            print(data_of_phone_check_file)
            for guest in guest_list:
                data_of_phone_check_file[str(guest)] = {}
            
            print(data_of_phone_check_file)
            read_send_data_to_json("Phone_check_file" , "w" , data_of_phone_check_file)
            return True
        else:
            return False
    except Exception as error:
        print(error)
        exit()

