#!/usr/bin/python3

# A logger for SBT904 based pressure sensor

import datetime
import os
from pathlib import Path
import serial
import time

def get_hex(port, cmd):
    """
    Collect hex data from serial after serial.write
    """
    with serial.Serial(port, 9600, timeout=0.5) as ser:
        ser.write(cmd)
        x = ser.read(10).hex() # require 10, larger than output
    return x

def pressure_logger(file_path, output_hex):
    """
    Convert hex output from SBT904 to decimal and append to target file
    """
    try:
        pressure = int(output_hex[7: 14], 16)
    except ValueError:
        print("Empty string, skipped")
    try:
        with open(file_path, 'a') as fp:
            fp.write("{}, {}, {}\n".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                                           output_hex, 
                                           pressure))
    except PermissionError:
        print("Permission denied when writing to log file.")

    print("{}: {}".format(datetime.datetime.now(), pressure))    

def main(time_interval, serial_port, task_name='pressure_logger'):
    """
    Collect data from serial and write to csv file (in current directory).
    """
    print("LOGGER START")
    log_path = Path("./"+task_name+".csv")
    print("Sampling period: {} s,  log file: {}, good luck.".format(time_interval,
                                                                  str(log_path)))
    record_cmd = bytes.fromhex("010300500002C41A")
    # Common ports on both Linux & Win platforms
    while True:
        output_hex = get_hex(port=serial_port, cmd=record_cmd)
        pressure_logger((log_path), output_hex)
        time.sleep(time_interval)


if __name__ == '__main__':
    task_name = input("Task name: ")
    time_interval = int(input("Sampling period (s): "))
    serial_port = input("Serial port for sensor (e.g. COM3): ")

    main(time_interval, serial_port, task_name)
