from importlib.machinery import SourceFileLoader

from pathlib import Path

# Loading Modules
from CSV_JSON_handler.handle_json import read_send_data_to_json
from sql_connector.sql_connect import extarct_data , extarct_data_from_sql_for_phone_check

def reset_phone_check_file():

    DIR_LOCATION = str(Path.cwd())
    
    ALL_ROOM_QUERY = "SELECT  cast([ROMNUB] as varchar(50)) , cast([REGNUB] as varchar(50)) FROM [NEXT70].[PMS].[FMOCCTBL];"

    phone_no_per_room = "SELECT [FAXNUB] , [GSTTIT] + ' ' + [FSTNAM] + ' ' + [LSTNAM] AS 'Full Name' FROM [NEXT6I].[PMS].[FMOCCTBL] WHERE cast([ROMNUB] as varchar(50)) = "


    # json_obj = SourceFileLoader('read_send_data_to_json' , DIR_LOCATION + "/CSV_JSON_handler/handle_json.py").load_module()
    
    # sql_obj_for_room = SourceFileLoader('extarct_data' , DIR_LOCATION + "/sql_connector/sql_connect.py").load_module()
    # sql_obj_for_phone_no = SourceFileLoader('extarct_data_from_sql_for_phone_check' , DIR_LOCATION + "/sql_connector/sql_connect.py").load_module()
    
    
    getting_all_rooms = extarct_data(ALL_ROOM_QUERY)
    
    final_data = {}

    for key in getting_all_rooms.keys():

        getting_all_phone_per_room = extarct_data_from_sql_for_phone_check(phone_no_per_room , 'room' , room = str(key))
        print(getting_all_phone_per_room)
        final_data[key] = getting_all_phone_per_room
    


    read_send_data_to_json("Phone_check_file" , 'w' , final_data)

