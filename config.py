from pathlib import Path
import platform
from werkzeug.security import generate_password_hash
import json
import os

global config
config = {}

def load_config(path = None):
    print("path:", path)
    config_path = path if path else input("Enter the path to the config.json file: ")
    try:  
        with open(config_path, "r") as file:
            global config
            config = json.load(file)
        config["login_key"] = generate_password_hash(config["login_key"])
        config["flounder_secret_key"] = generate_password_hash(config["flounder_secret_key"])
    except FileNotFoundError:
        print("Config file not found")
        return load_config()
    except json.JSONDecodeError:
        print("Config file is not a valid JSON file")
        return load_config()
    except Exception as e:
        print(f"An error occurred: {e}")
        return load_config()

paths = {
    "root" : Path(),
    "modelfiles": Path(Path() / "data" / "modelfiles"),
    "logs": Path(Path() / "data" / "serverlog.csv"),
    "modelfilesref": Path(Path() / "data" / "modelfiles.json"),
    "hamachi" : "only needed for windows"
}

if __name__ == "__main__":
    pass
    #load_config()
    #print(config["flounder_secret_key"])