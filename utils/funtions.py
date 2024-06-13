import ctypes
import queue
import os
import json
import time
import base64
import traceback
import psutil
import threading
import functools
import requests

from tqdm import tqdm
from datetime import datetime

from colorama import Fore





def encode_base64(text):
    encoded_bytes = base64.b64encode(text.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def decode_base64(encoded_text):
    try:
        decoded_bytes = base64.b64decode(encoded_text.encode('utf-8'))
        decoded_string = decoded_bytes.decode('utf-8')
    except:
        decoded_string = None
        
    return decoded_string

def get_queue(name) -> str:
    if not name.empty():
        return name.get()


def create_queue(filename):
    items = open(filename, "r").readlines()

    items = [link for link in items if link.strip()]
    my_queue = queue.Queue()
    for item in items:
        my_queue.put(item.strip())
    return my_queue



def safe_int(val):
    try:
        return int(val)
    except:
        return None


def safe_float(val):
    try:
        return float(val)
    except:
        return None


def safe_json(val):
    try:
        json_data = json.loads(val)
        return json.dumps(json_data, indent=4)
    except:
        return None


def safe_str(val):
    try:
        return str(val)
    except:
        return None


# system_operations.py
def update_title(title):
    kernel32 = ctypes.WinDLL('kernel32')
    kernel32.SetConsoleTitleW(title)


def os_exit():
    os._exit(0)


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def time_taken(go):
    return round(time.time() - go, 6)


def report_unhandled_error(error):
    error_str = traceback.format_exc()
    print(error_str)

def get_current_datetime():
    now = datetime.now()
    formatted_datetime = now.strftime("%d-%m-%Y [%H-%M-%S]")
    return formatted_datetime

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return True


def get_hardware_usage(interval=1):
        """
        Get CPU and RAM usage.

        :return: Tuple of float, representing CPU percent and memory usage in MB.
        """
        process = psutil.Process()
        cpu_percent = psutil.cpu_percent(interval=interval)
        memory_info = process.memory_full_info()
        memory_usage = round(memory_info.uss / 1024 / 1024, 1)
        return cpu_percent, memory_usage

def thread_safe(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        def run():
            try:
                func(*args, **kwargs)
            except Exception as e:
                traceback_str = traceback.format_exc()
                print(f"Error occurred in {func.__name__}: {e}")
                print(traceback_str)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    return wrapper

def show_error_popup(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Error", 0x10)


def is_tool(name):
    from distutils.spawn import find_executable

    return find_executable(name) is not None




def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        print(Fore.GREEN)
        with open(save_path, 'wb') as file, tqdm(
            desc=os.path.basename(save_path),
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                # Write data to file
                file.write(data)
                # Update the progress bar
                bar.update(len(data))

    except Exception as e:
        Exception(f"Error downloading file: {e}")
    print(Fore.RESET)
    return True

