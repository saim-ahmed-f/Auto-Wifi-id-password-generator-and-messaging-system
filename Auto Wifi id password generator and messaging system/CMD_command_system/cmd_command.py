from os import system
from  pathlib import Path


def cmd_executer():
    BASE_DIR = str(Path.cwd()) + "/ALL_DATA_FILES/wifi.csv"
    final_command = f"python Userimport.py -f 192.168.1.1 -i '{BASE_DIR}' -u admin -p Admin_nimda0 -n"
    system(final_command)
    #system("python Userimport.py -f 192.168.1.1 -i wifi.csv -u admin -p Admin_nimda0 -a -n")
    print("Add OR Update Function --> Command is sended to XG WI-Fi")


