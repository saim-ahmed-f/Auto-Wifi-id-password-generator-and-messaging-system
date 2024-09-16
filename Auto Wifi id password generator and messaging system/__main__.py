from time import sleep
from os import system

# Add new Guest
from add_update_system.scan_add_update import add_or_update

# Delete checkout Guest's
from delete_system.scan_delete import delete_user


# Phone no Add or Update of Guest

from phone_check.new_phone_add import new_phone_no_add
from phone_check.phone_update import check_update_or_add
from phone_check.phone_delete import phone_delete_scan


# Messaging System
from message_system.message_sys_intialize import message_system

# Data Sink System
from data_sink.sink_data import data_sink_system


# sql Functions for reset function
from sql_connector.sql_connect import extarct_data
from CSV_JSON_handler.handle_json import read_or_write_json_data
from phone_check.phone_reset import reset_phone_check_file


def reset_to_start():
    database_data = extarct_data("SELECT  cast([ROMNUB] as varchar(50)) , cast([REGNUB] as varchar(50)) FROM [NEXT70].[PMS].[FMOCCTBL];")
    read_or_write_json_data('data_track_file' , 'w' , list(database_data.keys()))
    reset_phone_check_file()




def run():
    # Delete Guest
    action , delete_list =  delete_user()
    if action == True:
        phone_delete_scan(delete_list)
    
    # Add new Guest
    add_action , new_guest_list = add_or_update()
    if add_action == True:
        new_phone_no_add(new_guest_list)
    
    check_action_from_phone , update_phone_no_list , key_pass_list =check_update_or_add()
    if check_action_from_phone == True:
        response_from_msg , whatsapp_msg_count , test_msg_count = message_system(update_phone_no_list , key_pass_list)

    if response_from_msg == True:
        print("Total No. of whatsapp Msg Sended : " , whatsapp_msg_count)
        print("Total No. of Text Msg Sended : " , test_msg_count)
        data_sink_system(whatsapp_msg_count , test_msg_count)




# Action's

def startup():
    
    reset_to_start()

    while True:
        run()
        sleep(2)
        system('cls')




if __name__ == "__main__":
    startup()