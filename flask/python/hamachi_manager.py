import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import config, paths
import time
import re


#autostartup for Hamachi server/client via cli.
class HamachiManager:
    def __init__(self):
        self.commands = {
    "status": "",
    "list": "list",
    "login": "login",
    "join": f"join {config["hamachi_network"]} {config["hamachi_password"]}",
    "set-nick": f"set-nick {config["hamachi_name"]}",
    "go-online": "go-online",
    "go-offline": "go-offline",
    "logout": "logout"
    }
        self.hamachi_config()
        self.server_ip = self.get_server_ip()
        
    #should be one time run
    def hamachi_config(self, force=False):
        #enables as service
        if not config["hamachi_enabled"] or force:
            if config["os"] == "Linux":
                process = subprocess.run(["systemctl", "enable", "logmein-hamachi"], capture_output=True, text=True)
                if process.returncode != 0:
                    return f"HamachiManager: Error enabling Hamachi service: {process.stderr}"
                process = subprocess.run(["systemctl", "start", "logmein-hamachi"], capture_output=True, text=True)
                if process.returncode != 0:
                    return f"HamachiManager: Error starting Hamachi service: {process.stderr}"
            elif config["os"] == "Windows":
                process = subprocess.run(["powershell", "-Command", "\"Start-Process hamachi -Verb RunAs\""], capture_output=True, text=True)
                if process.returncode != 0:
                    return f"HamachiManager: Error starting Hamachi service: {process.stderr}"
            elif config["os"] == "Darwin":
                pass
        config["hamachi_enabled"] = True
        return "Hamachi config completed successfully."

    def command_run(self, command: str):
        if command not in self.commands:
            return {"error": f"HamachiManager: Command not found: {command}"}
        command = self.commands[command]
        try:
            if config["os"] == "Linux":
                process = subprocess.run("sudo hamachi " + command, capture_output=True, text=True)
            elif config["os"] == "Windows":
                command = "&" + str(paths["hamachi"]) + " --cli " + command
                process = subprocess.run(command, capture_output=True, powershell=True)
            elif config["os"] == "Darwin":
                pass
        except subprocess.CalledProcessError as e:
            return {"Error": f"HamachiManager: Error running command: {process.stderr}"}
        time.sleep(1)#wait for command to finish
        return {"stdout": process.stdout}

    def get_server_ip(self):
        output = self.command_run("list").stdout.split("\n")
        for line in output[1:]:
            if config["server_name"] in line:
                server_ip = re.search(r'25\.\d+\.\d+\.\d+', line).group(0)
                return server_ip
        return None

    
if __name__ == "__main__":
    hamachi_manager = HamachiManager()
    print("server ip: ", hamachi_manager.get_server_ip())
    input("Press Enter to disconnect")
    hamachi_manager.hamachi_disconnect()