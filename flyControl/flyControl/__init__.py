#!/usr/bin/python3
# coding=utf-8

from multiprocessing import Manager
m = Manager()
# data bus
_233d = m.dict()
# control bus
_233c = m.dict()
# init status
_233d['p1_status'] = 0
_233d['p2_status'] = 0
_233d['p3_status'] = 0
_233c['lock'] = False

