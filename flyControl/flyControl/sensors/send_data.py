#!/usr/bin/python3
# coding=utf-8
'''
    数据链路  飞行器端  UDP-CLIENT
'''

import time
import socket


def start(_233d):
    sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_ipaddr = '192.168.137.1'
    server_port = 13133
    try:
        while True:
            bytes_1553b = str(_233d).encode("utf-8")
            sock_client.sendto(bytes_1553b, (server_ipaddr, server_port))
            time.sleep(0.5)
    except Exception as e:
        print(e)
        print("[Data_Link] send back has exception...")
    finally:
        sock_client.close()