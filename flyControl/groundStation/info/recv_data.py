#!/usr/bin/python3
# coding=utf-8
'''
UDP-Server
'''
import socket
import groundStation.vars as vars


def working():
    print("[Data_Link]打开飞行数据回传链路...")
    try:
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_server.bind(('0.0.0.0', 13133))

        while True:
            data_bytes, addr = sock_server.recvfrom(1024)
            resolve_data(data_bytes)
    except Exception as e:
        print("[Data_Link]数据回传链路接收数据时发生异常...")


#数据链路服务端
def resolve_data(data_bytes):
    try:
        data = eval(data_bytes.decode("utf-8"))
        #print(data)
        vars.label_2.config(text=data.get('ROLL'))
        vars.label_3.config(text=data.get('PITCH'))
        vars.label_4.config(text=data.get('YAW'))
        vars.label_5.config(text=data.get('Pressure'))
        vars.label_6.config(text=data.get('Temp'))
        vars.label_7.config(text=data.get('Altitude'))
        vars.label_8.config(text=data.get('Altitude'))
        vars.label_9.config(text=data.get('GYRO_X'))
        vars.label_10.config(text=data.get('GYRO_Y'))
        vars.label_11.config(text=data.get('GYRO_Z'))
        vars.label_13.config(text=data.get('LOG'))
        vars.label_14.config(text=data.get('LAT'))
        vars.label_15.config(text=data.get('SPEED'))
    except Exception as e:
        print("data resolve error.")