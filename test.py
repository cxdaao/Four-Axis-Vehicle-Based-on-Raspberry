# Servo PCA9685.py
# PCA9685

from smbus import SMBus
from PCA9685 import PWM #from PCA9685 put in PWM
import time


i2c_address = 0x40 # (standard) base on motor interface set I2C address
channel0 = 0 #control channel
channel1 = 1
channel2 = 2
channel3 = 3

def setup():
    try:
        global pwm
        bus = SMBus(1)# Raspberry Pi revision 2
        pwm = PWM(bus, i2c_address)
        pwm.setFreq(50)
        pwm.setDuty(channel0, 4.2)
        pwm.setDuty(channel1, 4.2)
        pwm.setDuty(channel2, 4.2)
        pwm.setDuty(channel3, 4.2)
    except KeyboardInterrupt:
        pwm.setDuty(channel0, 4.2)
        pwm.setDuty(channel1, 4.2)
        pwm.setDuty(channel2, 4.2)
        pwm.setDuty(channel3, 4.2)

print('starting')
try:
    setup()
    now = 42
    while True:
        num = int(input("duty:"))
        if num > now:
            for i in range(now, num, 1):
                i = i / 10.0
                pwm.setDuty(channel0, i)
                pwm.setDuty(channel1, i)
                pwm.setDuty(channel2, i)
                pwm.setDuty(channel3, i)
        if num < now:
            for i in range(now, num, -1):
                i = i / 10.0
                pwm.setDuty(channel0, i)
                pwm.setDuty(channel1, i)
                pwm.setDuty(channel2, i)
                pwm.setDuty(channel3, i)
        now = num


except KeyboardInterrupt:
    pwm.setDuty(channel0, 4.2)
    pwm.setDuty(channel1, 4.2)
    pwm.setDuty(channel2, 4.2)
    pwm.setDuty(channel3, 4.2)
print("done")
