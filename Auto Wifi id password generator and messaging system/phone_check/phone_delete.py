from importlib.machinery import SourceFileLoader

from pathlib import Path


# Loading Modules
from CSV_JSON_handler.handle_json import read_send_data_to_json


def phone_delete_scan(deleted_guest_list):

    DIR_LOCATION = str(Path.cwd())

    #json_obj = SourceFileLoader('read_send_data_to_json' , DIR_LOCATION + "/CSV_JSON_handler/handle_json.py").load_module()
    data_from_phone_check = read_send_data_to_json("Phone_check_file" , 'r')



    for guest in deleted_guest_list:
        del data_from_phone_check[guest]

    read_send_data_to_json("Phone_check_file" , 'w' , data_from_phone_check)

    

