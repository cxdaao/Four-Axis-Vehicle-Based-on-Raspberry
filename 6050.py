#!/usr/bin/env 6050.py
import smbus
import numpy

class MPU6050():
	def __init__(self):
		self.count = 0
		self.power_mgmt_1 = 0x6b
		self.power_mgmt_2 = 0x6c
		self.bus = smbus.SMBus(1)
		self.address = 0x68
		self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)
		self.bus.write_byte_data(self.address, 0x19, 0x07)
		sample = 50 / (1 + self.bus.read_byte_data(self.address, 0x19))
		print(sample)
		self.bus.write_byte_data(self.address, 0x1a, 0x06)
		self.bus.write_byte_data(self.address, 0x1b, 0x18)  # 2000o/s
		self.bus.write_byte_data(self.address, 0x1c, 0x18)  # 16g
		whoami = self.bus.read_byte_data(self.address, 0x75)
		print(whoami)
		print("mpu6050 open")
		print("------------")

	def read16bit(self, high, low):
		word = (self.bus.read_byte_data(self.address, high) << 8) | self.bus.read_byte_data(self.address, low)
		return word

	def out_put_acc(self, acc):
		if (acc & 0x8000):
			acc = acc - 0x8000
			acc = acc ^ 0x7fff
			acc = acc & 0x7fff
			data = -(acc / 32768.0 * 16 * 9.8)
		else:
			data = acc / 32768.0 * 16 * 9.8
		return data

	def out_put_gyro(self, gyro):
		if (gyro & 0x8000):
			gyro = gyro - 0x8000
			gyro = gyro ^ 0x7fff
			gyro = gyro & 0x7fff
			data = -(gyro / 32768.0 * 2000.0)
		else:
			data = gyro / 32768.0 * 2000.0
		return data

	def temperature(self):
		tem = (self.read16bit(0x41, 0x42)) / 340 + 36.53
		return tem

	def ax(self):
		self.count = 6
		while self.count > 0:
			ax = []
			ax.append(self.out_put_acc(self.read16bit(0x3b, 0x3c)))
			self.count -= 1
			return ax

	def ay(self):
		self.count = 6
		while self.count > 0:
			ay = []
			ay.append(self.out_put_acc(self.read16bit(0x3d, 0x3e)))
			self.count -= 1
		return ay

	def az(self):
		self.count = 6
		while self.count > 0:
			az = []
			az.append(self.out_put_acc(self.read16bit(0x3f, 0x40)))
			self.count -= 1
		return az

	def gx(self):
		self.count = 6
		while self.count > 0:
			gx = []
			gx.append(self.out_put_gyro(self.read16bit(0x43, 0x44)))
			self.count -= 1
		return gx

	def gy(self):
		self.count = 6
		while self.count > 0:
			gy = []
			gy.append(self.out_put_gyro(self.read16bit(0x45, 0x46)))
			self.count -= 1
		return gy

	def gz(self):
		self.count = 6
		while self.count > 0:
			gz = []
			gz.append(self.out_put_gyro(self.read16bit(0x47, 0x48)))
			self.count -= 1
		return gz
