import json
import threading
from ruamel.yaml import YAML




lock = threading.Lock()
yaml = YAML()

def save_line(filename: str, data: list | str):
    if isinstance(data, list):
        data = '\n'.join(data)
    
    with lock:
        with open(filename, 'a') as file:
            file.write(f"\n{str(data)}")

def remove_line(filename: str, line: str):
    with open(filename, 'r') as file:
        lines = file.readlines()
        
    with open(filename, 'w') as file:
        for line in lines:
            if not line.startswith(line):
                with lock:
                    file.write(line)
    

def replace(filename: str, old_line: str, new_line: str):
    with open(filename, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip() == old_line:
            lines[i] = new_line + '\n'
            break
    
    with lock:
        with open(filename, 'w') as file:
            file.writelines(lines)

def load_json(filename):
    try:
        with open(filename, 'r') as file:
            with lock:
                return json.load(file)
    except:
        return None
    

def save_json(filename, data):
    with open(filename, 'w') as file:
        with lock: json.dump(data, file, indent=4)


def load_yaml(filename: str):
    with open(filename, 'r') as file:
        data = yaml.load(file)
    
    return data

def read_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file]
    except:
        return None
