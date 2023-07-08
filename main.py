import psutil
import csv
import time
import sys
from py3nvml import py3nvml
import shutil
import os


def move_file_with_backup(filename):
    if os.path.isfile(filename):
        # Construct the new filename with a "old_" prefix
        new_filename = "old_" + filename

        # Move the file to the new location
        shutil.move(filename, new_filename)

        print(f"File '{filename}' moved to '{new_filename}'")
    else:
        print(f"File '{filename}' does not exist")


def detect_gpu():
    py3nvml.nvmlInit()
    return py3nvml.nvmlDeviceGetCount() > 0


def get_gpu_usage():
    py3nvml.nvmlInit()
    device_count = py3nvml.nvmlDeviceGetCount()
    usage = 0
    total = 0
    for i in range(device_count):
        handle = py3nvml.nvmlDeviceGetHandleByIndex(i)
        info = py3nvml.nvmlDeviceGetUtilizationRates(handle)
        if info.gpu > 0:
            usage += info.gpu
            total += 1

    return usage / max(1, total)


def bytes_to_kilobytes(bytes):
    return bytes / 1024


def log_system_usage(duration):
    start_time = time.time()
    if duration > 0:
        end_time = start_time + duration
    move_file_with_backup('system_usage_log.csv')
    with open('system_usage_log.csv', 'w', newline='') as log_file:
        writer = csv.writer(log_file)
        columns = ['Time',  'Sent (KB/s)', 'Received (KB/s)',
                   'CPU Usage (%)', 'Memory Usage (%)', "Disk Read (Kb/s)", "Disk Write (Kb/s)"]
        if detect_gpu():
            columns.append('GPU Usage (%)')
        writer.writerow(columns)

    prev_disk_io = psutil.disk_io_counters()
    prev_net_io = psutil.net_io_counters()
    while duration < 0 or time.time() < end_time:
        with open('system_usage_log.csv', 'a+', newline='') as log_file:
            writer = csv.writer(log_file)
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            gpu_percent = get_gpu_usage()
            current_net_io = psutil.net_io_counters()
            time_diff = time.time() - start_time
            sent_rate = bytes_to_kilobytes(
                current_net_io.bytes_sent - prev_net_io.bytes_sent) / time_diff
            received_rate = bytes_to_kilobytes(
                current_net_io.bytes_recv - prev_net_io.bytes_recv) / time_diff
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            disk_io = psutil.disk_io_counters()
            disk_read_bytes = bytes_to_kilobytes(
                disk_io.read_bytes - prev_disk_io.read_bytes) / time_diff
            disk_write_bytes = bytes_to_kilobytes(
                disk_io.write_bytes - prev_disk_io.write_bytes) / time_diff

            writer.writerow([current_time, sent_rate, received_rate,
                            cpu_percent, memory_percent, disk_read_bytes, disk_write_bytes, gpu_percent])
            prev_disk_io = disk_io
            prev_net_io = current_net_io
            time.sleep(1)

    print('System usage log saved to system_usage_log.csv')


# Specify the duration in seconds for which you want to log system usage
if __name__ == '__main__':
    if len(sys.argv):
        log_duration = int(sys.argv[1])
    else:
        log_duration = 300  # 5 minutes

    log_system_usage(log_duration)
