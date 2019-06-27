#!/usr/bin/python3
# coding=utf-8

import threading
from flyControl.lib import rpwm


def start(_233c, _233d):
    thread_list = []
    try:
        r = rpwm.data()
        t1 = threading.Thread(target=r.start, args=(_233c,))
        # t2 = threading.Thread(target=Data_Link.working, args=(_233d,))
        thread_list.append(t1)
        # thread_list.append(t2)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for t in thread_list:
            t.join()
    except Exception as e:
        print(e)
    finally:
        print("receiver close!")