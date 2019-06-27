from tkinter import messagebox
from groundStation.info import recv_data
import threading
import groundStation.vars as vars



def do_job():
    messagebox.showinfo(title='Info', message='loading..')


'''
打开数据回传链路
显示飞行数据
'''


def show_flydata():
    vars.flydataer = threading.Thread(target=recv_data.working, args=())
    vars.flydataer.setDaemon(True)
    vars.flydataer.start()