#!/usr/bin/env wen.py
import math
from time import ctime,sleep
import PCA9685
import rpwm
import threading
import pigpio

class controller():
	'''
	^
	|forward
	m4   m1
	 \ /
	 / \
	m3  m2
	'''
	def __init__(self):
		self.dc1 = 42
		self.dc2 = 42
		self.dc3 = 42
		self.dc4 = 42
		self.step = 1
		self.pwm = PCA9685.PWM()

		self.channel0 = 0
		self.channel1 = 1
		self.channel2 = 2
		self.channel3 = 3
		self.pwm.setFreq(50)
		self.pwm.setDuty(self.channel0, 4.2)
		self.pwm.setDuty(self.channel1, 4.2)
		self.pwm.setDuty(self.channel2, 4.2)
		self.pwm.setDuty(self.channel3, 4.2)

	def lift(self, dc):
		self.dc1 += dc
		self.dc2 += dc
		self.dc3 += dc
		self.dc4 += dc
		self.motor(self.dc1, self.dc2, self.dc3, self.dc4)

	def ziwen(self, pitch0, row0, yaw0, pitch, row, yaw):
		if pitch > pitch0:
			self.forward()
		if pitch < pitch0:
			self.back()
		if row > row0:
			self.rollleft()
		if row < row0:
			self.rollright()
		if yaw > yaw0:
			self.turnleft()
		if yaw < yaw0:
			self.turnright()


	def forward(self):
		dc1 = self.dc1 - self.step
		dc4 = self.dc4 - self.step
		dc2 = self.dc2 + self.step
		dc3 = self.dc3 + self.step
		self.motor(dc1, dc2, dc3, dc4)

	def back(self):
		dc2 = self.dc2 - self.step
		dc3 = self.dc3 - self.step
		dc1 = self.dc1 + self.step
		dc4 = self.dc4 + self.step
		self.motor(dc1, dc2, dc3, dc4)

	def rollleft(self):
		dc4 = self.dc4 - self.step
		dc3 = self.dc3 - self.step
		dc1 = self.dc1 - self.step
		dc2 = self.dc2 - self.step
		self.motor(dc1, dc2, dc3, dc4)

	def rollright(self):
		dc1 = self.dc1 - self.step
		dc2 = self.dc2 - self.step
		dc3 = self.dc3 + self.step
		dc4 = self.dc4 + self.step
		self.motor(dc1, dc2, dc3, dc4)

	def turnleft(self):
		dc1 = self.dc1 - self.step
		dc3 = self.dc3 - self.step
		dc2 = self.dc2 + self.step
		dc4 = self.dc4 + self.step
		self.motor(dc1, dc2, dc3, dc4)

	def turnright(self):
		dc2 = self.dc2 - self.step
		dc4 = self.dc4 - self.step
		dc1 = self.dc1 + self.step
		dc3 = self.dc3 + self.step
		self.motor(dc1, dc2, dc3, dc4)

	def motor(self, m1, m2, m3, m4):
		if m1 > 85:
			m1 = 85
		elif m1 < 42:
				m1 = 42
		if m2 > 85:
			m2 = 85
		elif m2 < 42:
			m2 = 42
		if m3 > 85:
			m3 = 85
		elif m3 < 42:
			m3 = 42
		if m4 > 85:
			m4 = 85
		elif m4 < 42:
			m4 = 42
		self.pwm.setFreq(50)
		self.pwm.setDuty(self.channel0, m1 / 10.0)
		self.pwm.setDuty(self.channel1, m2 / 10.0)
		self.pwm.setDuty(self.channel2, m3 / 10.0)
		self.pwm.setDuty(self.channel3, m4 / 10.0)

	def close(self):
		self.dc1 = 42
		self.dc2 = 42
		self.dc3 = 42
		self.dc4 = 42
		self.motor(self.dc1, self.dc2, self.dc3, self.dc4)


if __name__ == '__main__':
	controller = controller()
	rpwm = rpwm.data()
	pi = pigpio.pi()
	threads = []
	t1 = threading.Thread(target=pi.callback, args=(21, pigpio.EITHER_EDGE, rpwm.mycallback3))
	threads.append(t1)
	for t in threads:
		t.setDaemon(True)
		t.start()
	laterlift = rpwm.get_t3h()
	dc = 0
	while True:
		try:
			dc = (laterlift - 1000.0) / (2000.0 - 1000.0) * (85.0 - 42.0)
			controller.lift(dc)
			sleep(0.2)
		except KeyboardInterrupt:
			controller.close()
			print('控制系统关闭')
			break
