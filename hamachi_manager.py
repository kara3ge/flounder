import psutil
import subprocess
from config import config
import time
import re

#autostartup for Hamachi server/client via cli.
class HamachiManager:
    def __init__(self):
        self.hamachi_config()
        self.hamachi_connect()
        self.self_ip = self.get_self_ip()
        self.server_ip = self.get_server_ip()
        if (not self.self_ip == self.server_ip) or self.server_ip is None:
            print(f"Client: accessing server on {self.server_ip}:{config["server_port"]}...")
            self.hamachi_disconnect()

    def hamachi_config(self):
        subprocess.run(["sudo","systemctl","enable","logmein-hamachi"], check=True)
        print("Hamachi service starting")
        subprocess.run(["sudo","systemctl","start","logmein-hamachi"], check=True)
        time.sleep(5)
        subprocess.run(["sudo","hamachi", "login"])
        time.sleep(1)
        subprocess.run(["sudo","hamachi", "join", config["hamachi_network"], config["hamachi_password"]])
        time.sleep(1)
        subprocess.run(["sudo","hamachi", "set-nick", config["hamachi_name"]])
        time.sleep(1)

    def hamachi_connect(self):
        subprocess.run(["sudo","hamachi", "go-online", config["hamachi_network"]])
        
    def get_self_ip(self):
        print(len(psutil.net_if_addrs()))
        for iface, addrs in psutil.net_if_addrs().items():
            if "ham0" in iface.lower():
                for addr in addrs:
                    if addr.family.name == "AF_INET":
                        return addr.address
        raise Exception("Hamachi IP not found")

    def hamachi_disconnect(self):
        time.sleep(1)
        subprocess.run(["sudo","hamachi", "logout"])
        time.sleep(1)
        subprocess.run(["sudo","systemctl","stop","logmein-hamachi"])
        print("Hamachi disconnected")

    def get_server_ip(self):
        output = subprocess.run(["sudo","hamachi", "list"], capture_output=True, text=True).stdout.split("\n")
        for line in output[1:]:
            if config["server_name"] in line:
                server_ip = re.search(r'25\.\d+\.\d+\.\d+', line).group(0)
                return server_ip
        return None

if __name__ == "__main__":
    hamachi_manager = HamachiManager()
    print("hamachi ip: ", hamachi_manager.self_ip)
    print("server ip: ", hamachi_manager.get_server_ip())
    input("Press Enter to disconnect")
    hamachi_manager.hamachi_disconnect()