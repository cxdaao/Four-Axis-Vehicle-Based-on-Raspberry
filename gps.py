import serial
import pynmea2
import threading
import time


class gps(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ser = serial.Serial("/dev/ttyAMA0", 9600)
        self.thread_stop = False

    def get_lat(self):
        while True:
            line = self.ser.readline()
            if line.startswith('$GNRMC'):
                rmc = pynmea2.parse(line)
                print("Latitude:  ", float(rmc.lat)/100)
                return (float)(rmc.lat/100)

    def get_lon(self):
        line = self.ser.readline()
        if line.startswith('$GNRMC'):
            rmc = pynmea2.parse(line)
            print("Longitude: ", float(rmc.lon)/100)
            return (float)(rmc.lon / 100)

gps = gps()
gps.get_lat()
gps.get_lon()


