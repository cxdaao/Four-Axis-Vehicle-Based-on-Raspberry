import smbus
from flyControl.motors import angleculc


class MPU6050():
    def __init__(self):
        self.count = 0
        self.n_iter = 20
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
        print(str(whoami) + 'is working')
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
        self.count = self.n_iter
        ax = [0] * self.n_iter
        while self.count > 0:
            ax[self.n_iter - self.count] = self.out_put_acc(self.read16bit(0x3b, 0x3c))
            self.count -= 1
        return ax

    def ay(self):
        self.count = self.n_iter
        ay = [0.0] * self.n_iter
        while self.count > 0:
            ay[self.n_iter - self.count] = self.out_put_acc(self.read16bit(0x3d, 0x3e))
            self.count -= 1
        return ay

    def az(self):
        self.count = self.n_iter
        az = [0] * self.n_iter
        while self.count > 0:
            az[self.n_iter - self.count] = self.out_put_acc(self.read16bit(0x3f, 0x40))
            self.count -= 1
        return az

    def gx(self):
        self.count = self.n_iter
        gx = [0] * self.n_iter
        while self.count > 0:
            gx[self.n_iter - self.count] = self.out_put_gyro(self.read16bit(0x43, 0x44))
            self.count -= 1
        return gx

    def gy(self):
        self.count = self.n_iter
        gy = [0] * self.n_iter
        while self.count > 0:
            gy[self.n_iter - self.count] = self.out_put_gyro(self.read16bit(0x45, 0x46))
            self.count -= 1
        return gy

    def gz(self):
        self.count = self.n_iter
        gz = [0] * self.n_iter
        while self.count > 0:
            gz[self.n_iter - self.count] = self.out_put_gyro(self.read16bit(0x47, 0x48))
            self.count -= 1
        return gz


def start(_233d):
    try:
        mpu = MPU6050()
        angle = angleculc.Culc()
        while True:
            __resolve_data(mpu, _233d)
            angle.stand(_233d)
    except Exception as ex:
        print(ex)
        print('MPU6050 has exception and stop.')
    finally:
        pass


def __resolve_data(data, _233d):
    _233d['ACC_X'] = data.ax()
    _233d['ACC_Y'] = data.ay()
    _233d['ACC_Z'] = data.az()
    _233d['GYRO_X'] = data.gx()
    _233d['GYRO_Y'] = data.gy()
    _233d['GYRO_Z'] = data.gz()
    #print(_233d)