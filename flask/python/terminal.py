import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import config, paths
from python.hamachi_manager import HamachiManager
#DANGEROUS: execute commands on server side without care
#hamachi_manager = HamachiManager()

#show current OS:
#map linux to windows commands(cmd)
#auto elevate common tasks (sudo)/runa

def unix_to_win(command):
    #just passes for  now as arguments need to be changed.
    new_command = command
    return new_command

def execute_command(command):
    #cmd parse:
    response = {}
    command_list = command.split(" ")
    type = command_list.pop(0).lower()
    if config["os"] == "Windows":
        command_list = ["powershell.exe"] + command_list
    elif config["os"] == "Linux":
        command_list = command_list
    if type == "help":
        pass
    elif type == "flounder":
        #commands for flounder server
        if command_list[1] == "update":
            pass
        elif command_list[1] == "restart":
            pass
        elif command_list[1] == "stop":
            pass
        elif command_list[1] == "start":
            pass
        else:
            response["error"] = f"Command not found '{command}'"
    elif type == "olm":
        pass
    elif type == "ham":
        response["stdout"] = HamachiManager.command_run(command_list)
    elif type == "cli":
        try:
            #needs to run in the correct cli environment.
            response["stdout"] = subprocess.run(command_list, capture_output=True, text=True).stdout
        except Exception as e:
            response["error"] = f"Error executing command: {e}"
    else:
        response["error"] = f"Command not found '{command}'"
    response["post"] = f"Command executed '{command}'"
    return response
