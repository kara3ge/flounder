import subprocess
from config import config, paths
import time
import glob
import re
import os

#OllamaManager class !!!!only for serverside!!!!
#Easy ollama API for Flask server.
class OllamaManager:
    def __init__(self,server_ip):
        self.server_ip = server_ip
        if not os.environ.get("OLLAMA_PORT"):
            os.environ["OLLAMA_PORT"] = str(config["ollama_port"])
        self.old_port = os.environ["OLLAMA_PORT"]
        os.environ["OLLAMA_HOST"] = str(self.server_ip)
        self.server_process = None
        self.models = self.ollama_list()

    def ollama_serve(self):
        print("Ollama service starting")
        try:
            self.server_process = subprocess.run(["ollama","serve"], check=True)
        except subprocess.CalledProcessError as e:
            return f"Error starting ollama server: Check if the port is already in use."
        return f"Started ollama server on {self.ip}:{config["ollama_port"]} successfully."
            

    def ollama_list(self):
        print("Listing models...")
        output = subprocess.run(["ollama","list"], capture_output=True, text=True).stdout.split("\n")
        output = [line.split(" ",1)[0] for line in output[1:-1]]
        self.models = output
        return self.models

    def ollama_list_modelfiles(self):
        print("Listing modelfiles...")
        self.models_files = glob.glob(str(paths["modelfiles"]) + "/*.model")
        return self.models_files
    
    def ollama_pull(self, model_name):
        print(f"Pulling model {model_name}...")
        try:
            subprocess.run(["ollama","pull", model_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error pulling model {model_name}: {e}")
            return f"Error pulling model {model_name}."
        return f"Model {model_name} pulled successfully."
    
    def ollama_remove(self, model_name):
        print(f"Deleting model {model_name}...")
        try:
            subprocess.run(["ollama","rm", model_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error deleting model {model_name}.")
            return f"Error deleting model {model_name}."
        return f"Model {model_name} deleted successfully."

    def ollama_create(self, model_name, model_file):
        print(f"Creating model {model_name} with file {model_file}...")
        model_file_path = paths["modelfiles"] / model_file
        print(model_file_path)
        if not model_file_path.exists():
            return f"Error: Model file {model_file} not found."
        try:
            subprocess.run(["ollama","create", model_name, "-f", str(model_file_path)], check=True)
            return f"Model {model_name} created successfully."
        except subprocess.CalledProcessError as e:
            print(f"Error creating model {model_name}: {e}")
            return f"Error creating model {model_name}."

    def ollama_close(self):
        #Doesnt actually close the server, just changes the port
        os.environ["OLLAMA_PORT"] = self.old_port
        return "Ollama closed successfully."

if __name__ == "__main__":
    ollama_manager = OllamaManager("0.0.0.0")
    print(ollama_manager.ollama_serve())
    print(ollama_manager.ollama_list())
    print(ollama_manager.ollama_remove("test-llama"))
    print(ollama_manager.ollama_list())
    print(ollama_manager.ollama_close())
    