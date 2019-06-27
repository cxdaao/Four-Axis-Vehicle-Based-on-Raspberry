#!/usr/bin/python3
# coding=utf-8
from flyControl import _233d
from flyControl import _233c
from flyControl import engine
from flyControl import sendback
from flyControl import sensor
from flyControl import receiver
from multiprocessing import Process
import os
if __name__ == "__main__":
    try:
        val = os.system('ps -ef | grep -w pigpiod | grep -v \'grep\'')
        if val == 256:
            os.system('sudo pigpiod')
        else:
            os.system('echo \"pigpiod has started.\"')
        _233c['lock'] = False
        p1 = Process(target=sensor.start, args=(_233d,), name='p1')
        p2 = Process(target=engine.start, args=(_233c, _233d), name='p2')
        p3 = Process(target=receiver.start, args=(_233c, _233d), name='p3')
        p4 = Process(target=sendback.start, args=(_233c, _233d), name='p3')

        p1.daemon = True
        p2.daemon = True
        p3.daemon = True
        p4.daemon = True

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        # os.sched_setaffinity(p1.pid, [0x00])
        # os.sched_setaffinity(p2.pid, [0x01])

        p1.join()
        p2.join()
        p3.join()
        p4.join()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        _233c['lock'] = True
    finally:
        print("system stop...")