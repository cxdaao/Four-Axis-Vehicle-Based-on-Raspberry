# coding=utf-8
"""
双环串级PID反馈控制：
                外环输入：欧拉角（X，Y，Z）
                外环输出：期望角速度
                内环输入：期望角速度-当前陀螺仪测量的角速度（X，Y，Z）
                内环输出：PWM信号补偿控制电机
"""
from flyControl.lib import config as cfg


class PID(object):
    # 外环输入：欧拉角的上一次误差
    x_last = 0.0
    y_last = 0.0
    z_last = 0.0
    # 外环输入：欧拉角的积分变量  累计误差
    x_sum = [0.0]
    y_sum = [0.0]
    z_sum = [0.0]
    # 外环输出：角速度期望值
    xv_et = 0.0
    yv_et = 0.0
    zv_et = 0.0
    # 内环输入：角速度的上一次误差
    xv_last = 0.0
    yv_last = 0.0
    zv_last = 0.0
    # 内环输入：角速度的积分变量  累计误差
    xv_sum = [0.0]
    yv_sum = [0.0]
    zv_sum = [0.0]

    def __init__(self):
        # 外环pid参数   外环只做P，不做I和D
        self.kp = 30.0
        self.ki = 0.05  # 外环不做I
        self.kd = 0.01  # 外环不做D
        # 内环pid参数   内环要做P+I+D
        self.v_kp = 0.3    # 经测试0.29~0.15之间比较合适
        self.v_ki = 0.01
        self.v_kd = 0.001

    # 外环角速度限幅
    def engine_limit_palstance(self, val):
        MAX_PALSTANCE = 35  # 允许的最大角速度（度/秒）
        if val > MAX_PALSTANCE:
            return MAX_PALSTANCE
        elif val < -MAX_PALSTANCE:
            return -MAX_PALSTANCE
        return val

    # 内环PWM限幅
    # 油门调整限幅不超过7%
    def engine_limit_pwm(self, pwm):
        MAX_PWM = cfg.curr_power * 20.0   # 对油门的调整幅度不能超过当前油门的一半
        if pwm > MAX_PWM:
            return MAX_PWM
        elif pwm < -MAX_PWM:
            return -MAX_PWM
        return pwm

    '''
    外环PID输入角度输出角速度
    et:当前角度误差
    et2:上一次角度误差
    输出：期望角速度
    '''
    def engine_outside_pid(self, et, et2, sum):
        # 输出期望角速度
        palstance = 0.0
        if sum is None:
            # Z轴PID中只做P和D
            palstance = self.kp * et + self.kd * (et - et2)
            palstance = self.engine_limit_palstance(palstance)
            return palstance
        sum[0] += self.ki * et * 0.01
        # 积分限幅
        sum[0] = self.engine_limit_palstance(sum[0])
        # XY轴PID反馈控制
        palstance = self.kp * et + sum[0] + self.kd * (et - et2)
        # 输出限幅
        palstance = self.engine_limit_palstance(palstance)
        return round(palstance, 2)

    '''
    内环PID输入角速度输出PWM
    et:当前角速度误差
    et2:上一次角速度误差
    输出：PWM调整值
    '''
    def engine_inside_pid(self, et, et2, sum):
        # 输出期望PWM值
        pwm = 0.0
        if sum is None:
            pwm = self.v_kp * et + self.v_kd * (et - et2)
            pwm = self.engine_limit_pwm(pwm)
            return pwm
        sum[0] += self.v_ki * et * 0.01
        sum[0] = self.engine_limit_pwm(sum[0])
        pwm = self.v_kp * et + sum[0] + self.v_kd * (et - et2)
        pwm = self.engine_limit_pwm(pwm)
        return round(pwm, 2)

    '''
       飞控核心自平衡算法 计算x,y,z三个向量上得PWM调整幅度，
       输入：传感器数据队列_233d
       输出：
    '''
    def calculate(self, _233d):
        x = int(_233d.get('ROLL', 0))  # X  -180~+180
        y = int(_233d.get('PITCH', 0))  # Y  -90~+90
        z = int(_233d.get('YAW', 0))  # Z  -180~+180
        gx = int(_233d.get('sGYRO_X', 0))
        gy = int(_233d.get('sGYRO_Y', 0))
        gz = int(_233d.get('sGYRO_Z', 0))
        x_et = cfg.ROLL_SET - x
        y_et = cfg.PITCH_SET - y
        z_et = cfg.YAW_SET - z

        xv = gx
        yv = gy
        zv = gz

        xv_et = self.engine_outside_pid(x_et, self.x_last, self.x_sum)
        yv_et = self.engine_outside_pid(y_et, self.y_last, self.y_sum)
        zv_et = self.engine_outside_pid(z_et, self.z_last, None)

        xv_et -= xv
        yv_et -= yv
        zv_et -= zv

        x_pwm = self.engine_inside_pid(xv_et, self.xv_last, self.xv_sum)
        y_pwm = self.engine_inside_pid(yv_et, self.yv_last, self.yv_sum)
        z_pwm = self.engine_inside_pid(zv_et, self.zv_last, None)

        self.x_last = x_et
        self.y_last = y_et
        self.z_last = z_et

        self.xv_last = xv_et
        self.yv_last = yv_et
        self.zv_last = zv_et

        return x_pwm, y_pwm, z_pwm

