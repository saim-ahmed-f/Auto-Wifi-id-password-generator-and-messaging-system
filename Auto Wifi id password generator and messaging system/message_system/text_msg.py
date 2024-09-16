import requests


def phone_no_check_for_text(phone): # -- UPDATED
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


def message_text(id , pass_word , phone_num):

    result_phone = ""
    for phone in phone_num:
        result_phone += phone_no_check_for_text(phone) + ','

    text = "Dear Guest, \nWelcome to Jehan Numa Retreat, Here is your Wi-Fi login credential \nUser: "+ str(id) +" \nPassword: "+ str(pass_word) +" \nValidity: Checkout \nDevice: 4 \nHave a nice day"
    url = "http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms"
    data = {
        "AUTH_KEY": "Authentication Key from Message Provider",
        "message" : text,
        "smsContentType" : "english",
        "senderId" : "Sender ID",
        "routeId": "1",
        "mobileNos" : result_phone
    }
    response = requests.get(url  , params=data)
    if str(response.status_code) != '200':
        return False
    
    print(response.status_code) 
    return True

if __name__ == "__main__":
    print(message_text('201' , '12345' , ['+37247336070']))
