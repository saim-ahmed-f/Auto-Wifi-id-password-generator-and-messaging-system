import csv

from pathlib import Path

def write_in_csv(final_new_guest_list , file_action_name , action = None):
    
    FILE_DIR = str(Path.cwd())

    fields = ['Name','Username','Password','Email Address','Group' , 'status']
    rows = []
    for key , pass_word in final_new_guest_list.items():            
            rows.append(["Guest",str(key),str(pass_word),"Guest@jnr.com","Guest" , action])

    file_name = FILE_DIR + "/ALL_DATA_FILES/" + file_action_name
    try:
        file = open(file_name , 'w' , newline="")
        write_csv = csv.writer(file)
        write_csv.writerow(fields)
        write_csv.writerows(rows)
    except Exception as error:
        print(error)
        return False
    return True


def activate_record_csv_dump_load(file_name , action , data):
    FILE_DIR = str(Path.cwd())

    try:
        # Reading All Data from th file 
        file_name = FILE_DIR + "/ALL_DATA_FILES/" + file_name
        file = open(file_name , 'r')
        csvFile = csv.reader(file)
        old_data = []
        for lines in csvFile:
            old_data.append(lines)
        file.close()
        
        print(old_data)

        # Taking actions like adding new key or deleting key
        if action == "add":
            for key , value in data.items():
                old_data.append([str(key),str(value)])
        elif action == "remove":
            new_old_data = []
            for key2 in old_data:
                if len(key2) != 0:
                    if int(key2[0]) not in data or str(key2[0]) not in data:
                        new_old_data.append(key2)
            old_data = new_old_data

        print(f"New Old : {old_data}")

        # Writing the updated Key's
        file = open(file_name , 'w' , newline="")
        write_csv = csv.writer(file)
        write_csv.writerows(old_data)

        return True
    
    except Exception as error : 
        print("Error Related to activate_record_csv_dump_load function : " , error)
        exit()



def get_data_from_csv(file_name):

    FILE_DIR = str(Path.cwd())

    file_name = FILE_DIR + "/ALL_DATA_FILES/" + file_name + ".csv"
    file = open(file_name , 'r')
    csv_action = csv.reader(file)
    all_room = {}
    for i in csv_action:
        if len(i) != 0:
            all_room[str(i[0])] = i[1]
    return all_room


if __name__ == "__main__":
    pass
