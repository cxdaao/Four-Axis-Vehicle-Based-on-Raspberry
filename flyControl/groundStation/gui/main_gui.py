import tkinter as tk
import groundStation.gui.function as fun
import groundStation.vars as vars

window = tk.Tk()
window.geometry('1000x450')
window.resizable(0, 0)

x0 = 0
y0 = 0
x1 = 800
y1 = 450

# 菜单栏-----------
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Exit', menu=filemenu)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=window.quit)
#

offsetY = 40
offsetX = 20
# 显示欧拉角
l = tk.Label(window, text="欧拉角",
             anchor="w",
             font=('Arial',14),
             width=100, height=2)
l.place(x=offsetX, y=offsetY, anchor='nw')
l = tk.Label(window, text="ROLL",
             anchor="w",
             font=('Arial',10),
             width=100, height=2)
l.place(x=offsetX, y=offsetY+40, anchor='nw')
vars.label_2 = tk.Label(window, text="N/A",
             anchor ="w",
             foreground ='blue',
             font = ('Arial', 12),
             width=100, height=2)
vars.label_2.place(x=offsetX+100, y=offsetY+40, anchor='nw')

l = tk.Label(window, text="PITCH",
             anchor="w",
             font=('Arial',10),
             width=100, height=2)
l.place(x=offsetX, y=offsetY+80, anchor='nw')
vars.label_3 = tk.Label(window, text="N/A",
             anchor ="w",
             foreground ='red',
             font = ('Arial',12),
             width=100, height=2)
vars.label_3.place(x=offsetX+100, y=offsetY+80, anchor='nw')

l = tk.Label(window, text="YAW",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
l.place(x=offsetX, y=offsetY+120, anchor='nw')
vars.label_4 = tk.Label(window, text="N/A",
             anchor ="w",
             foreground ='green',
             font = ('Arial',12),
             width=100, height=2)
vars.label_4.place(x=offsetX+100, y=offsetY+120, anchor='nw')


l = tk.Label(window, text="海拔高度",
             anchor="w",
             font=('Arial', 14),
             width=100, height=2)
l.place(x=offsetX+240, y=offsetY+80, anchor='nw')
vars.label_7 = tk.Label(window, text="N/A",
             anchor = "w",
             foreground = 'red',
             font = ('Arial',12),
             width=100, height=2)
vars.label_7.place(x=offsetX+360, y=offsetY+80, anchor='nw')

l = tk.Label(window, text="离地高度",
             anchor="w",
             font=('Arial',14),
             width=100, height=2)
l.place(x=offsetX+240, y=offsetY+120, anchor='nw')
vars.label_8 = tk.Label(window, text="N/A",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100, height=2)
vars.label_8.place(x=offsetX+360, y=offsetY+120, anchor='nw')

#显示加速度
l = tk.Label(window, text="角速度GYRO",
             anchor="w",
             font=('Arial',14),
             width=100, height=2)
l.place(x=offsetX, y=offsetY+160, anchor='nw')

l = tk.Label(window, text="X轴",
             anchor="w",
             font=('Arial',10),
             width=100, height=2)
l.place(x=offsetX, y=offsetY+200, anchor='nw')
vars.label_9 = tk.Label(window, text="N/A",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100, height=2)
vars.label_9.place(x=offsetX+100, y=offsetY+200, anchor='nw')

l = tk.Label(window, text="Y轴",
             anchor="w",
             font=('Arial',10),
             width=100, height=2)
l.place(x=offsetX, y=offsetY+240, anchor='nw')
vars.label_10 = tk.Label(window, text="N/A",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100, height=2)
vars.label_10.place(x=offsetX+100, y=offsetY+240, anchor='nw')

l = tk.Label(window, text="Z轴",
             anchor="w",
             font=('Arial',10),
             width=100, height=2)
l.place(x=offsetX,y=offsetY+280, anchor='nw')
vars.label_11 = tk.Label(window, text="N/A",
             anchor="w",
             foreground='red',
             font=('Arial', 12),
             width=100,height=2)
vars.label_11.place(x=offsetX+100, y=offsetY+280, anchor='nw')

#---经度、纬度
l = tk.Label(window, text="GPS经度",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240, y=offsetY+160, anchor='nw')
vars.label_13 = tk.Label(window, text="N/A",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_13.place(x=offsetX+360, y=offsetY+160, anchor='nw')

l = tk.Label(window, text="GPS纬度",
             anchor="w",
             font=('Arial',14),
             width=100, height=2)
l.place(x=offsetX+240, y=offsetY+200, anchor='nw')
vars.label_14 = tk.Label(window, text="N/A",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100, height=2)
vars.label_14.place(x=offsetX+360, y=offsetY+200, anchor='nw')

offsetY = 50

vars.but_2 = tk.Button(window,
    text='显示飞行数据',
    activeforeground='red',
    width=25, height=2,
    command=fun.show_flydata)
vars.but_2.place(x=offsetX+540, y=offsetY+50, anchor='nw')


window.mainloop()