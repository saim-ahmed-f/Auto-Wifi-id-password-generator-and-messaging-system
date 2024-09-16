from importlib.machinery import SourceFileLoader

from pathlib import Path


# Loading Modules
from CSV_JSON_handler.handle_json import read_send_data_to_json
from CSV_JSON_handler.handle_csv import get_data_from_csv
from sql_connector.sql_connect import extarct_data_from_sql_for_phone_check



def check_update_or_add():

    DIR_LOCATION = str(Path.cwd())

    ROOM_QUERY = "SELECT [FAXNUB] , [GSTTIT] + ' ' + [FSTNAM] + ' ' + [LSTNAM] AS 'Full Name' FROM [NEXT70].[PMS].[FMOCCTBL] WHERE cast([ROMNUB] as varchar(50)) = "
    PHONE_QUERY = "SELECT [FAXNUB] , [GSTTIT] + ' ' + [FSTNAM] + ' ' + [LSTNAM] AS 'Full Name' FROM [NEXT70].[PMS].[FMOCCTBL] WHERE cast([ROMNUB] as varchar(50)) = "


    # Loading Modules 
    # json_obj = SourceFileLoader('read_send_data_to_json' , DIR_LOCATION + "/CSV_JSON_handler/handle_json.py").load_module()
    # csv_obj = SourceFileLoader('get_data_from_csv' , DIR_LOCATION + "/CSV_JSON_handler/handle_csv.py").load_module()
    # sql_obj = SourceFileLoader('extarct_data_from_sql_for_phone_check' , DIR_LOCATION + "/sql_connector/sql_connect.py").load_module()


    data_from_phone_check = read_send_data_to_json("Phone_check_file" , 'r')
    data_from_csv = get_data_from_csv("Active_Guest_Credential")

    

    main_data = {}
    for key in data_from_csv.keys():
        if len(data_from_phone_check[key]) != 0 :
            getting_all_updated_no = extarct_data_from_sql_for_phone_check(PHONE_QUERY , 'phone' , str(key) , data_from_phone_check[key].keys())
        else:
            getting_all_updated_no = extarct_data_from_sql_for_phone_check(PHONE_QUERY , 'phone' , str(key) , [''])
        
        if len(getting_all_updated_no) != 0 :
            main_data[key] = getting_all_updated_no
            data_from_phone_check[key].update(getting_all_updated_no)
            read_send_data_to_json("Phone_check_file" , 'w' , data_from_phone_check)    

    return True , main_data , data_from_csv

        #     #final_data = final_dict_provider(data_from_csv[key] , key , getting_all_updated_no)
        #     #main_data.update(final_data)
        #     print(getting_all_updated_no)
        #     data_from_phone_check[key].update(getting_all_updated_no)
        # else:
        #     room_phone_no = sql_obj.extarct_data_from_sql_for_phone_check(ROOM_QUERY , 'room' , str(key))
        #     getting_all_updated_no = sql_obj.extarct_data_from_sql_for_phone_check(PHONE_QUERY , 'phone' , str(key) , room_phone_no)
            
        #     #final_data = final_dict_provider(data_from_csv[key] , key , room_phone_no)
        #     #main_data.update(final_data)
        #     data_from_phone_check[key] = room_phone_no
    
    # print("Main Data : ",main_data)
    # print("Phone : " , data_from_phone_check)
    








