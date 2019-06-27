#!/usr/bin/python3
# coding=utf-8

import threading
from flyControl.sensors import MPU6050


def start(_233d):
    thread_list = []
    try:
        t1 = threading.Thread(target=MPU6050.start, args=(_233d,))
        thread_list.append(t1)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for t in thread_list:
            t.join()
    except Exception as e:
        print(e)
    finally:
        print("sensors stop.")