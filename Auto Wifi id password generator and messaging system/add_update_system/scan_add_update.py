from importlib.machinery import SourceFileLoader

from pathlib import Path

# Loading Modules
from CSV_JSON_handler.handle_json import read_or_write_json_data
from CSV_JSON_handler.handle_csv import write_in_csv
from sql_connector.sql_connect import extarct_data
from CSV_JSON_handler.handle_csv import activate_record_csv_dump_load


# Loading Command Module
from CMD_command_system.cmd_command import cmd_executer


def add_or_update():
    query_for_room = "SELECT  cast([ROMNUB] as varchar(50)) , cast([REGNUB] as varchar(50)) FROM [NEXT70].[PMS].[FMOCCTBL];"
    
    try:

        DIR_LOCATION = str(Path.cwd())

        # Loading Modules
        # json_obj = SourceFileLoader('read_or_write_json_data' , DIR_LOCATION+"/CSV_JSON_handler/handle_json.py").load_module()
        # csv_obj = SourceFileLoader('write_in_csv' , DIR_LOCATION+"/CSV_JSON_handler/handle_csv.py").load_module()
        # sql_obj = SourceFileLoader('extarct_data' , DIR_LOCATION+"/sql_connector/sql_connect.py").load_module()

        # active_key_csv_obj = SourceFileLoader('activate_record_csv_dump_load' , DIR_LOCATION+"/CSV_JSON_handler/handle_csv.py").load_module()



        print("Add OR Update Function --> Starting Searching Updated User")
        track_file_data = read_or_write_json_data('Guest_file' , 'r')
        database_data = extarct_data(query_for_room)

        

        new_added = set(database_data.keys()).difference(set(track_file_data))
        print(track_file_data)
        print(database_data)
        print("set" , new_added)
        
        print(f"Add OR Update Function --> {str(len(new_added))} New Entry Found")

        
        if len(new_added) != 0:
            final_new_guest_list = {}
            for room in new_added:
                final_new_guest_list[room] = database_data[room]

            # writeing in csv to generate XG user
            write_in_csv(final_new_guest_list , "wifi.csv" , 'Active')
            print("Add OR Update Function --> CSV File is Create with New User")


            # Sending Command to XG server
            #cmd_ex('python Userimport.py -f 192.168.1.1 -i wifi2.csv -u admin -p Admin_nimda0 -a -n')
            cmd_executer()
            print("Add OR Update Function --> Command is sended to XG WI-Fi")

            # Editing The activate Key csv File
            activate_record_csv_dump_load("Active_Guest_Credential.csv" , "add" , final_new_guest_list)
            print("Add OR Update Function --> Updating the active key file")


            saving_new_data = list(set(track_file_data).union(final_new_guest_list.keys()))
            read_or_write_json_data('Guest_file' , 'w' , saving_new_data)
            print("Add OR Update Function --> Updated Data Track File")

            return True , final_new_guest_list.keys()
        
        else:
            print("Add OR Update Function --> No New User Founded")
            return False , []
        
    except Exception as error:
        print(error)
        exit()

if __name__ == "__main__":
    pass
