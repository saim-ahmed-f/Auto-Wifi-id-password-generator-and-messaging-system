from CSV_JSON_handler.handle_json import read_or_write_json_data


from message_system.text_msg import message_text
from message_system.whatsapp_msg import whatsapp_msg



def message_system(new_user , pass_dict):
    
    active_system_data = read_or_write_json_data("Active_System_file" , "r")
    
    
    #PHONE_ID = "100718606298262"
    #TOKEN = "TOKEN FROM META" // This is the token to send the whatsapp message 
    
    
    whatsapp_msg_count = 0
    text_msg_count = 0

    for room_no , all_guest_in_room in new_user.items():       

        if active_system_data["whatsapp_msg_system"] == True:
            msg_phone_nos = []

            # Whatsapp Message
            response_from_whatsapp = None
            for phone_no , guest_names in all_guest_in_room.items():
                print(phone_no , guest_names)
                response_from_whatsapp = whatsapp_msg(guest_names , room_no , pass_dict[room_no] , phone_no)
                if response_from_whatsapp != False:
                    whatsapp_msg_count += 1
                    print(response_from_whatsapp)
                else:
                    msg_phone_nos.append(phone_no)

        else:
            msg_phone_nos = list(all_guest_in_room.keys())
        
        if active_system_data["text_msg_system"] == True:
            if len(msg_phone_nos) != 0:
                # Text Message
                response_from_text_msg = None
                response_from_text_msg = message_text(room_no , pass_dict[room_no] , msg_phone_nos)#all_guest_in_room.keys())

                if response_from_text_msg != False:
                    text_msg_count += len(all_guest_in_room.keys())
                    print(response_from_text_msg)


        
        # for lol in final_value:
        #     if len(lol[2]) > 9:
        #         if lol[2] not in check:
        #             check.append(lol[2])
        #             send(lol[1] , final_key , final_value[0][0] , str(lol[2])  , TOKEN)
    return True , whatsapp_msg_count , text_msg_count

if __name__ == "__main__":
    new_u = {"201" : {"7247336070" : "Mr Raj Singh"}}
    pass_d = {'201' : '12345' , '301' : '01234'}
    message_system(new_u , pass_d)
