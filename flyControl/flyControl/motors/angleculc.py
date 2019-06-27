from flyControl.sensors import filter
import math
import time
from flyControl.lib import config as cfg


class Culc():
    def __init__(self):
        # self.mpu = mpu6050.MPU6050()
        self.filter = filter.filter()
        self.data = [0] * 6
        self.Kp = 100
        self.Ki = 0.002
        self.halfT = 0.0008

        self.q0 = 1
        self.q1 = 0
        self.q2 = 0
        self.q3 = 0

        self.exint = 0
        self.eyint = 0
        self.ezint = 0

    def culdata(self, _233d):
        ax = _233d.get('ACC_X', 0)
        ay = _233d.get('ACC_Y', 0)
        az = _233d.get('ACC_Z', 0)
        gx = _233d.get('GYRO_X', 0)
        gy = _233d.get('GYRO_Y', 0)
        gz = _233d.get('GYRO_Z', 0)
        self.data[0] = self.filter.circuit(ax)
        self.data[1] = self.filter.circuit(ay)
        self.data[2] = self.filter.circuit(az)
        self.data[3] = self.filter.circuit(gx)
        self.data[4] = self.filter.circuit(gy)
        self.data[5] = self.filter.circuit(gz)
        _233d['sGYRO_X'] = self.data[3]
        _233d['sGYRO_Y'] = self.data[4]
        _233d['sGYRO_Z'] = self.data[5]
        print('ax:', self.data[0])
        print('ay:', self.data[1])
        print('az:', self.data[2])
        print('grx:', self.data[3])
        print('gry:', self.data[4])
        print('grz:', self.data[5])
        print('azo:', _233d.get('ACC_Z', 0)[0])


    def update_imu(self, data):
        # print(q0)
        accx = int(data[0])
        accy = int(data[1])
        accz = int(data[2])
        grx = int(data[3])
        gry = int(data[4])
        grz = int(data[5])

        norm = math.sqrt(accx * accx + accy * accy + accz * accz)
        if norm == 0:
            norm = 1
        accx = accx / norm
        accy = accy / norm
        accz = accz / norm

        vx = 2 * (self.q1 * self.q3 - self.q0 * self.q2)
        vy = 2 * (self.q0 * self.q1 - self.q2 * self.q3)
        vz = self.q0 * self.q0 - self.q1 * self.q1 - self.q2 * self.q2 + self.q3 * self.q3

        ex = (accy * vz - accz * vy)
        ey = (accz * vx - accx * vz)
        ez = (accx * vy - accy * vx)

        self.exint += ex * self.Ki
        self.eyint += ey * self.Ki
        self.ezint += ez * self.Ki

        grx += self.Kp * ex + self.exint
        gry += self.Kp * ey + self.eyint
        grz += self.Kp * ez + self.ezint
        self.q0 += (-self.q1 * grx - self.q2 * gry - self.q3 * grz) * self.halfT
        self.q1 += (self.q0 * grx + self.q2 * grz - self.q3 * gry) * self.halfT
        self.q2 += (self.q0 * gry - self.q1 * grz + self.q3 * grx) * self.halfT
        self.q3 += (self.q0 * grz + self.q1 * gry - self.q2 * grx) * self.halfT

        norm = math.sqrt(self.q0 * self.q0 + self.q1 * self.q1 + self.q2 * self.q2 + self.q3 * self.q3)
        self.q0 /= norm
        self.q1 /= norm
        self.q2 /= norm
        self.q3 /= norm

        pitch = math.asin(-2 * self.q1 * self.q3 + 2 * self.q0 * self.q2) * 57.3
        roll = math.atan2(2 * self.q2 * self.q3 + 2 * self.q0 * self.q1, -2 * self.q1 * self.q1 - 2 * self.q2 * self.q2 + 1) * 57.3
        yaw = math.atan2(2 * (self.q1 * self.q2 + self.q0 * self.q3), self.q0 * self.q0 + self.q1 * self.q1 - self.q2 * self.q2 - self.q3 * self.q3) * 57.3
        return pitch, roll, yaw

    def stand(self, _233d):
        # p = pid.PID()
        self.culdata(_233d)
        pitch, roll, yaw = self.update_imu(self.data)
        _233d['PITCH'] = pitch
        _233d['ROLL'] = roll
        _233d['YAW'] = yaw
        # axx = _233d.get['ACC_X']
        # ayy = _233d.get['ACC_Y']
        # azz = _233d.get['ACC_Z']
        # grx = _233d.get['GYRO_X']
        # gry = _233d.get['GYRO_Y']
        # grz = _233d.get['GYRO_Z']
        # print(axx)
        cfg.pitch = _233d.get('PITCH', 0)
        cfg.roll = _233d.get('ROLL', 0)
        cfg.yaw = _233d.get('YAW', 0)

