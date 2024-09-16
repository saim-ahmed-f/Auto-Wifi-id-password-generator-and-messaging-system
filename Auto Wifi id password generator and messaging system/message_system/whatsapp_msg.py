from json import dumps
import requests
from time import sleep

def phone_no_check_for_whatsapp(phone): # -- UPDATED
    phone = str(phone).strip()
    phone_len = len(phone)
    if phone_len == 13:
        return phone[3:]
    elif phone_len == 12:
        return phone[2:]
    elif phone_len == 11:
        return phone[1:]
    else:
        return phone 


def MSG_generator(username , Id , pass_word):

        MESSAGE = {
            "name": "checkin",
            "language": { "code": "en_gb"},
            "components" : [
                {
                "type": "header",
                "parameters": [
                    {
                        "type": "text",
                        "text": str(username)
                    }
                ]
            },
            {
                "type": "body",
                "parameters": [
                    {
                        "type": "text",
                        "text": str(Id)
                    },
                    {
                        "type": "text",
                        "text": str(pass_word)
                    },
                ]
            },
            ]
        }

        return MESSAGE

def whatsapp_msg(username , Id , pass_word , send_to):
    send_to = phone_no_check_for_whatsapp(send_to)
    TOKEN = "EAB0WREi08Y0BAPRohg2ixjE9GoIZB9yd4EvlmIwweYq8KJlNHT96w5Jkj6o800tTlCNpwZBA99e5Ihy5IJcV98FmINUDDivsuNz2zM8n1qMPYSJU3KUvlYZCDCvzax8HJyGXAfDylS4tsZBZBkJJhA7Ur1Xw4qfL9urewwlfRDIwgiR22okz7i2tkx00f58a5ZChv3ZAr5dTAZDZD"
    try:
        MESSEGE = MSG_generator(username , Id ,pass_word)
        URL = 'https://graph.facebook.com/v16.0/100718606298262/messages'
        headers = {
            "Authorization": "Bearer "+TOKEN, 
            "Content-Type": "application/json"
        }
        data = { 
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to":  str('+91') + send_to, 
            "type": "template", 
            "template": dumps(MESSEGE)
        }
        response = requests.post(URL, headers=headers, data=data)
        response_json = response.json()
        
        if 'error' in response_json.keys():
            return False
        
        print("Whatsapp Message Sended to : " ,send_to)
        print("\n\n")
        sleep(1)
        return response_json
        # data_sink(0,0,0,1,1)
        
    except Exception as error:
        print(error , " IN Phone No. : ", str(send_to))


if __name__ == "__main__":
    whatsapp_msg("saim ahmed" , "201" , "12345" , "+27247336070" )#, "EAB0WREi08Y0BAPRohg2ixjE9GoIZB9yd4EvlmIwweYq8KJlNHT96w5Jkj6o800tTlCNpwZBA99e5Ihy5IJcV98FmINUDDivsuNz2zM8n1qMPYSJU3KUvlYZCDCvzax8HJyGXAfDylS4tsZBZBkJJhA7Ur1Xw4qfL9urewwlfRDIwgiR22okz7i2tkx00f58a5ZChv3ZAr5dTAZDZD")
