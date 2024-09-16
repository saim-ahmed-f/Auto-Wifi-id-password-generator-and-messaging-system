from importlib.machinery import SourceFileLoader

from pathlib import Path


# Loading Modules
from CSV_JSON_handler.handle_json import read_or_write_json_data
from sql_connector.sql_connect import extarct_data
from CSV_JSON_handler.handle_csv import activate_record_csv_dump_load



def delete_user(query):

    try:

        DIR_LOCATION = str(Path.cwd())

        # Loading Modules
        # json_obj = SourceFileLoader('read_or_write_json_data' , DIR_LOCATION+"/CSV_JSON_handler/handle_json.py").load_module()
        # sql_obj = SourceFileLoader('extarct_data' , DIR_LOCATION+"/sql_connector/sql_connect.py").load_module()
        # active_key_csv_obj = SourceFileLoader('activate_record_csv_dump_load' , DIR_LOCATION+"/CSV_JSON_handler/handle_csv.py").load_module()
        


        print("Delete Function --> Starting Searching Deleting User")
        track_file_data = read_or_write_json_data('Guest_file' , 'r')
        database_data = extarct_data(query)

        delete_user_id = set(track_file_data).difference(database_data.keys())

        
        
        if len(delete_user_id) != 0:    
            print("Delete Function --> All Deleted record Founded")


            # Removing The activate Key csv File
            activate_record_csv_dump_load("Active_Guest_Credential.csv" , "remove" , list(delete_user_id))
            print("Delete Function --> Updating the active key file")

            
            saving_old_records = set(database_data.keys()).intersection(track_file_data)
            read_or_write_json_data('Guest_file' , 'w' , list(saving_old_records))
            print("Delete Function --> Updated Data Track File for Deleted User")
            
            return True , list(delete_user_id)
        
        print("Delete Function --> No User Found to be Deleted")
        return False , []

    except Exception as error :
        print(error)
        exit()


        

if __name__ == "__main__":
    pass
