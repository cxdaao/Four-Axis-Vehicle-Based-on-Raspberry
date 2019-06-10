import pigpio
import time

class data():
        def __init__(self):
                self.t1h = 0
                self.t1l = 0
                self.t2h = 0
                self.t2l = 0
                self.t3h = 0
                self.t3l = 0
                self.t4h = 0
                self.t4l = 0
                self.t5h = 0
                self.t5l = 0
                self.t6h = 0
                self.t6l = 0
                self.tick0 = None
                self.tick1 = None
                self.tick2 = None
                self.tick3 = None
                self.tick4 = None
                self.tick5 = None
                self.tick6 = None
                self.tick7 = None
                self.tick8 = None
                self.tick9 = None
                self.tick10 = None
                self.tick11 = None
                self.diff1 = None
                self.diff2 = None
                self.diff3 = None
                self.diff4 = None
                self.diff5 = None
                self.diff6 = None

        def get_t1h(self):
                return self.t1h

        def get_t2h(self):
                return self.t2h

        def get_t3h(self):
                return self.t3h

        def get_t4h(self):
                return self.t4h

        def get_t5h(self):
                return self.t5h

        def get_t6h(self):
                return self.t6h

        def mycallback1(self, gpio, level, tick):
                if level == 0:
                        self.tick0 = tick
                        if self.tick1 is not None:
                                self.diff1 = pigpio.tickDiff(self.tick1, tick)
                        self.t1h=self.diff1
                else:
                        self.tick1 = tick
                        if self.tick0 is not None:
                                self.diff1 = pigpio.tickDiff(self.tick0, tick)
                        self.t1l=self.diff1

        def mycallback2(self, gpio, level, tick):
            if level == 0:
                self.tick2 = tick
                if self.tick3 is not None:
                    self.diff2 = pigpio.tickDiff(self.tick3, tick)
                self.t2h=self.diff2
            else:
                self.tick3 = tick
                    if self.tick2 is not None:
                            self.diff2 = pigpio.tickDiff(self.tick2, tick)
                    self.t2l=self.diff2

        def mycallback3(self, gpio, level, tick):
                if level == 0:
                        self.tick4 = tick
                        if self.tick5 is not None:
                                self.diff3 = pigpio.tickDiff(self.tick5, tick)
                        self.t3h=self.diff3
                else:
                        self.tick5 = tick
                        if self.tick4 is not None:
                                self.diff3 = pigpio.tickDiff(self.tick4, tick)
                        self.t3l=self.diff3

        def mycallback4(self, gpio, level, tick):
                if level == 0:
                        self.tick6 = tick
                        if self.tick7 is not None:
                                self.diff4 = pigpio.tickDiff(self.tick7, tick)
                        self.t4h=self.diff4
                else:
                        self.tick7 = tick
                        if self.tick6 is not None:
                                self.diff4 = pigpio.tickDiff(self.tick6, tick)
                        self.t4l=self.diff4

        def mycallback5(self, gpio, level, tick):
                if level == 0:
                        self.tick8 = tick
                        if self.tick9 is not None:
                                self.diff5 = pigpio.tickDiff(self.tick9, tick)
                        self.t5h=self.diff5
                else:
                        self.tick9 = tick
                        if self.tick8 is not None:
                                self.diff5 = pigpio.tickDiff(self.tick8, tick)
                        self.t5l=self.diff5

        def mycallback6(self, gpio, level, tick):
                if level == 0:
                        self.tick10 = tick
                        if self.tick11 is not None:
                                self.diff6 = pigpio.tickDiff(self.tick11, tick)
                        self.t6h=self.diff6
                else:
                        self.tick11 = tick
                        if self.tick10 is not None:
                                self.diff6 = pigpio.tickDiff(self.tick10, tick)
                        self.t6l=self.diff6
