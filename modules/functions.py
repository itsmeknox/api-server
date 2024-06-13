import time

def validate_time_stamp(timestamp, threshold=20):
    current_timestamp = time.time()
    if current_timestamp == timestamp or (timestamp < current_timestamp and timestamp > current_timestamp - threshold):
        return True
    else:
        return False