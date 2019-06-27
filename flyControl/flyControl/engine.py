#!/usr/bin/python3
# coding=utf-8

import threading
from flyControl.motors import controller

c = controller.Controller()


def start(_233d, _233c):
    threads = []
    try:
        t0 = threading.Thread(target=c.start, args=(_233c, _233d))
        threads.append(t0)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        c.close()
    finally:
        print("shut down power.")


def close():
    c.close()