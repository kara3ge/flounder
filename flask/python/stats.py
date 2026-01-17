import psutil
import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def get_cpu_usage():
    cpu = psutil.cpu_percent(interval=1)
    return cpu

def get_gpu_usage():
    #is specific to setup
    return 0

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent

def get_network_usage():
    old_sent = psutil.net_io_counters().bytes_sent
    time.sleep(1)
    new_sent = psutil.net_io_counters().bytes_sent
    speed = abs(old_sent - new_sent) / 1024 / 1024 # convert to MB/s
    return speed

def get_temperature():
    temperature = psutil.sensors_temperatures()
    return temperature['coretemp'][0].current