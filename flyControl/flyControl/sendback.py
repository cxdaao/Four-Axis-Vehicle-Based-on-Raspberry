#!/usr/bin/python3
# coding=utf-8
from flyControl.sensors import send_data
import threading


def start(_233d):
    thread_list = []
    try:
        t1 = threading.Thread(target=send_data.start, args=(_233d,))
        thread_list.append(t1)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for t in thread_list:
            t.join()
    except Exception as e:
        print(e)
    finally:
        print("community thread close!")