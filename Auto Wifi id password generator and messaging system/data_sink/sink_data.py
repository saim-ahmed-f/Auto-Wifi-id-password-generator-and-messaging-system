from datetime import date , datetime

# Loading Modules

from CSV_JSON_handler.handle_json import read_or_write_json_data


def reset_day_or_month(file_data):

    date_extract = datetime.strptime(file_data['date'] , '%Y-%m-%d').date()


    if date_extract.month != date.today().month:
        
        return {
            "date": str(date.today()), 
            "whatsapp_msg_sended_today": 0, 
            "whatsapp_msg_sended_month": 0, 
            "text_msg_sended_today": 0,
            "text_msg_sended_month": 0
        }
    elif date_extract.day != date.today().day:
        
        return {
            "date": str(date.today()),
            "whatsapp_msg_sended_today": 0, 
            "whatsapp_msg_sended_month": file_data["whatsapp_msg_sended_month"], 
            "text_msg_sended_today": 0,
            "text_msg_sended_month": file_data['text_msg_sended_month']
        }
    else:
        
        return file_data
        

def data_sink_system(total_whatsapp_msg = 0 , total_text_msg = 0):

    try:

        
        data = read_or_write_json_data('data_sink_file' , 'r')
        formated_file_data = reset_day_or_month(data)

        # Adding Whatsapp msg data
        formated_file_data["whatsapp_msg_sended_today"] += total_whatsapp_msg
        formated_file_data["whatsapp_msg_sended_month"] += total_whatsapp_msg

        # Adding Text msg data
        formated_file_data["text_msg_sended_today"] += total_text_msg
        formated_file_data["text_msg_sended_month"] += total_text_msg
        
        read_or_write_json_data('data_sink_file' , 'w' , formated_file_data)
        
    except Exception as error:
        print(error)


