#!/usr/bin/env wen.py
import math
from time import sleep
from flyControl.lib import PCA9685
from flyControl.lib import rpwm
import threading
import pigpio
from flyControl.motors import angleculc
import multiprocessing
from smbus import SMBus
from flyControl.lib import config as cfg
from flyControl.lib import pid


class Controller():
	'''
	^
	|forward
	m4   m1
	 \ /
	 / \
	m3  m2
	'''

	def __init__(self):
		self.dc1 = 4.2
		self.dc2 = 4.2
		self.dc3 = 4.2
		self.dc4 = 4.2
		self.step = 1
		self.i2c_address = 0x40
		self.bus = SMBus(1)
		self.pwm = PCA9685.PWM(self.bus, self.i2c_address)

		self.channel0 = 0
		self.channel1 = 1
		self.channel2 = 2
		self.channel3 = 3
		self.pwm.setFreq(50)
		self.pwm.setDuty(self.channel0, 4.2)
		self.pwm.setDuty(self.channel1, 4.2)
		self.pwm.setDuty(self.channel2, 4.2)
		self.pwm.setDuty(self.channel3, 4.2)

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
		cfg.ROLL_SET = 0
		cfg.PITCH_SET = -25
		cfg.YAW_SET = 0

	def back(self):
		cfg.ROLL_SET = 0
		cfg.PITCH_SET = +25
		cfg.YAW_SET = 0

	def rollleft(self):
		cfg.ROLL_SET = -15
		cfg.PITCH_SET = 0
		cfg.YAW_SET = 0

	def rollright(self):
		cfg.ROLL_SET = +15
		cfg.PITCH_SET = 0
		cfg.YAW_SET = 0

	def turnleft(self):
		cfg.ROLL_SET = 0
		cfg.PITCH_SET = 0
		cfg.YAW_SET = -45

	def turnright(self):
		cfg.ROLL_SET = 0
		cfg.PITCH_SET = 0
		cfg.YAW_SET = +45

	def motor(self, m1, m2, m3, m4):
		if m1 > 8.5:
			m1 = 8.5
		elif m1 < 4.5:
			m1 = 4.5
		if m2 > 8.5:
			m2 = 8.5
		elif m2 < 4.5:
			m2 = 4.5
		if m3 > 8.5:
			m3 = 8.5
		elif m3 < 4.5:
			m3 = 4.5
		if m4 > 8.5:
			m4 = 8.5
		elif m4 < 4.5:
			m4 = 4.5
		self.dc1 = m1
		self.dc2 = m2
		self.dc3 = m3
		self.dc4 = m4
		#print('m1:', m1)
		self.pwm.setFreq(50)
		self.pwm.setDuty(self.channel0, m1)
		self.pwm.setDuty(self.channel1, m2)
		self.pwm.setDuty(self.channel2, m3)
		self.pwm.setDuty(self.channel3, m4)

	def close(self):
		self.dc1 = 4.2
		self.dc2 = 4.2
		self.dc3 = 4.2
		self.dc4 = 4.2
		cfg.curr_power = 0
		cfg.YAW_SET = 0
		cfg.PITCH_SET = 0
		cfg.YAW_SET = 0
		cfg.motor1_power = 0
		cfg.motor2_power = 0
		cfg.motor3_power = 0
		cfg.motor4_power = 0
		self.motor(self.real_pwm(cfg.motor1_power), self.real_pwm(cfg.motor2_power), self.real_pwm(cfg.motor3_power), self.real_pwm(cfg.motor4_power))

	def limit_power_range(self, power):
		MIN_POWER = 5
		MAX_POWER = 90
		if power > MAX_POWER:
			return MAX_POWER
		if power < MIN_POWER:
			return MIN_POWER
		return power

	def set_power(self, x_pwm, y_pwm, z_pwm):
		if cfg.curr_power < cfg.flight_power:
			x_pwm = 0
			y_pwm = 0
			z_pwm = 0
		if x_pwm > 0 and y_pwm > 0:
			cfg.motor1_power = self.limit_power_range(cfg.motor1_power - x_pwm / 2.0 - y_pwm / 2.0)  # -x -y
			cfg.motor2_power = self.limit_power_range(cfg.motor2_power + x_pwm / 2.0 + y_pwm / 2.0)  # -x +y
			cfg.motor3_power = self.limit_power_range(cfg.motor3_power + x_pwm / 2.0 + y_pwm / 2.0)  # +x +y
			cfg.motor4_power = self.limit_power_range(cfg.motor4_power - x_pwm / 2.0 - y_pwm / 2.0)  # +x -y
		print('m1: %s ; m2: %s ; m3: %s ; m4: %s;' % (cfg.motor1_power, cfg.motor2_power, cfg.motor3_power, cfg.motor4_power))
		self.motor(self.real_pwm(cfg.motor1_power), self.real_pwm(cfg.motor2_power), self.real_pwm(cfg.motor3_power), self.real_pwm(cfg.motor4_power))

	def real_pwm(self, power):
		v = (100 + power) / 20.0
		return v

	def start(self, _233d, _233c):
		if ~_233c.get('lock', 0):
			try:
				self.__init__()
				pc = pid.PID()
				while True:# if _233c.get('t3h', 0) > 1200:
					lift_pwm = _233c.get('t3h', 0)
					# print('lift_pwm: %s ' % lift_pwm)
					cfg.curr_power = (lift_pwm - 1000) / 1000.0 * 100
					t1 = _233c.get('t1h', 0)
					t2 = _233c.get('t2h', 0)
					t3 = _233c.get('t3h', 0)
					t4 = _233c.get('t4h', 0)
					t5 = _233c.get('t5h', 0)
					t6 = _233c.get('t6h', 0)
					if t1 == 0 or t2 == 0 or t3 == 0 or t4 == 0 or t6 == 0:
						continue
					dc1 = ((t3 - 1015.0) + (t4 - 1520.0) + (t1 - t6) / 4.0 + (t1 + t6 - 2.0 * t2) / 2.0) / (
								2020.0 - 1015.0) * 100
					dc2 = ((t3 - 1015.0) - (t4 - 1520.0) + (t1 - t6) / 4.0 - (t1 + t6 - 2.0 * t2) / 2.0) / (
								2020.0 - 1015.0) * 100
					dc3 = ((t3 - 1015.0) + (t4 - 1520.0) - (t1 - t6) / 4.0 - (t1 + t6 - 2.0 * t2) / 2.0) / (
								2020.0 - 1015.0) * 100
					dc4 = ((t3 - 1015.0) - (t4 - 1520.0) - (t1 - t6) / 4.0 + (t1 + t6 - 2.0 * t2) / 2.0) / (
								2020.0 - 1015.0) * 100
					cfg.motor1_power = dc1
					cfg.motor2_power = dc2
					cfg.motor3_power = dc3
					cfg.motor4_power = dc4
					print(cfg.curr_power)
					xs_pwm, ys_pwm, zs_pwm = pc.calculate(_233d)
					self.set_power(xs_pwm, ys_pwm, zs_pwm)
					print('x:', xs_pwm)
					print('y:', ys_pwm)
					# print('z:', zs_pwm)
			except Exception as ex:
				print(ex)
			except KeyboardInterrupt:
				self.close()
			finally:
				self.close()
		else:
			self.close()
			print('no power.')


if __name__ == '__main__':
	controller = Controller()
	rpwm = rpwm.data()
	selfstand = angleculc.Culc()
	pi = pigpio.pi()
	process = []
	p1 = multiprocessing.Process(target=selfstand.stand, args=())
	process.append(p1)
	for p in process:
		# t.setDaemon(True)
		p.start()

	threads = []
	t1 = threading.Thread(target=pi.callback, args=(25, pigpio.EITHER_EDGE, rpwm.mycallback1))
	t2 = threading.Thread(target=pi.callback, args=(12, pigpio.EITHER_EDGE, rpwm.mycallback2))
	t3 = threading.Thread(target=pi.callback, args=(16, pigpio.EITHER_EDGE, rpwm.mycallback3))
	t4 = threading.Thread(target=pi.callback, args=(20, pigpio.EITHER_EDGE, rpwm.mycallback4))
	t5 = threading.Thread(target=pi.callback, args=(21, pigpio.EITHER_EDGE, rpwm.mycallback5))
	t6 = threading.Thread(target=pi.callback, args=(26, pigpio.EITHER_EDGE, rpwm.mycallback6))
	threads.append(t1)
	threads.append(t2)
	threads.append(t3)
	threads.append(t4)
	threads.append(t5)
	threads.append(t6)
	for t in threads:
		t.setDaemon(True)
		t.start()
	pi = pid.PID()
	dc = 0
	for p in multiprocessing.active_children():
		print("child   p.name:" + p.name + "\tp.id" + str(p.pid))
	print("The number of CPU is:" + str(multiprocessing.cpu_count()))
	while True:
		try:

			laterlift = rpwm.get_t3h()
			if laterlift < 1000:
				laterlift = 1000
			elif laterlift > 1850:
				laterlift = 1850
			print('lift:', laterlift)
			cfg.curr_power = (laterlift - 1000) / 1000 * 100
			dc = (100 + cfg.curr_power) / 20

			print('curr_power:', dc)
			x_pwm, y_pwm, z_pwm = pi.calculate(cfg.grx)
			print(x_pwm)
			controller.set_power(x_pwm, y_pwm, z_pwm)
			controller.motor(cfg.motor1_power, cfg.motor2_power, cfg.motor3_power, cfg.motor4_power)
			print(cfg.motor1_power)
			sleep(1)
		except KeyboardInterrupt:
			controller.close()
			print('control system close!!')
			break
