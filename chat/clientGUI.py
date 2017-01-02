#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
from tkinter.colorchooser import *
from tkinter.font import Font
from functools import partial
from datetime import datetime
import os
# import webbrowser
import re
import threading
import socket
import sys
import json


class ChatGUI(object):

    def __init__(self):
        self.SERVER_IP = '192.168.3.13'
        self.PORT = 21567
        self.ADDR = (self.SERVER_IP, self.PORT)
        self.BUFSIZE = 1024 * 10

        # 设置偏函数
        MyButton = partial(Button,bg='#BFEFFF', fg='black', activeforeground='#EFFAFF',activebackground='#6AD169', width= 10, height = 2)
        # 总体界面
        self.top = Tk()
        self.top.title('移动支付组群聊')
        self.top.geometry('700x480+50+80')
        self.top.resizable(False, False)
        # 增加菜单
        self.addMenu()
        # 消息框
        self.textfm = Frame(self.top)
        self.textsb_v =Scrollbar(self.textfm, orient=VERTICAL)
        self.text = Text(self.textfm, height=30, width=80, relief = 'flat', yscrollcommand=self.textsb_v.set)
        self.text.bind('<KeyPress>', lambda e:"break")
        self.text.tag_configure('color', foreground='blue')
        self.bold_font = Font(family="Consolas", size=11, weight="bold")
        self.text.tag_configure("BOLD", font=self.bold_font)
        self.text.tag_configure("system", font=self.bold_font, foreground='red')
        self.text.pack(side=LEFT, fill=BOTH)
        self.textsb_v.pack(fill=Y,expand=0, side=LEFT, anchor=N)
        #在线人数
        Label(self.textfm,text='群成员').pack(side="top")
        self.online = Text(self.textfm, height = 25, width = 20)
        self.online_font = Font(family="微软雅黑", size=10)
        self.online.tag_configure("oneline_font", font= self.online_font, foreground="red")
        self.online.bind('<KeyPress>', lambda e:"break")
        self.online.pack(side=RIGHT, fill=Y)
        self.textfm.pack()
        # 输入框
        self.chatTextn = Text(self.top, width=80, height=5)
        self.top.bind('<Return>', self.__out)
        self.chatTextn.pack(side=LEFT)
        # 发送
        self.bfm = Frame(self.top)
        self.send = MyButton(self.bfm, text='send', command=self.__out)
        self.send.pack()
        self.bfm.pack(side=LEFT,padx='20')

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.ADDR)
        except (ConnectionRefusedError, ConnectionResetError):
            print("服务端没有启动")
            sys.exit(-1)
        data = json.dumps({"name": os.getlogin()})
        self.socket.send(data.encode())
        threading.Thread(target=self.__in).start()
    def __in(self):
        while True:
            try:
                data = self.socket.recv(self.BUFSIZE).decode()
            except (ConnectionRefusedError,ConnectionResetError):
                print("服务端没有启动")
                sys.exit(-1)
            if not data:
                print('没有从服务端接收到数据')
            data = json.loads(data)
            message = data.get('message')
            online = data.get('online')
            if message:
                self.insertText(message)
            if online:
                self.updateOnline(online)


    def __out(self):
        data = self.getWholeTextMsg(self.chatTextn)
        if not data.strip():
            return
        # if data.endswith('\n'):
        #     data = data[:-1]
        data = json.dumps({"message":data})
        self.socket.send(data.encode())
        self.chatTextn.delete('1.0', 'end')

    def updateOnline(self, online):
        self.online.delete('1.0',END)
        self.online.insert('1.0', online, 'oneline_font')


    def getWholeTextMsg(self, text):
        """
        The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character). END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached. The only issue with this is that it actually adds a newline to our input. So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on.
        """
        return text.get('1.0','end-1c')


    def addMenu(self):
        menu = Menu(self.top)
        menu.add_command(label="历史记录", command=self.check_history)
        menu.add_command(label="选择颜色", command=self.choose_color)
        self.top.config(menu=menu)


    def check_history(self):

        # webbrowser.open("http://localhost:8000")
        self.tl = Toplevel(self.top, width=800)
        self.tl.focus()
        self.tl.title("选择历史纪录日期")
        MODES = []
        
        for f in os.listdir("D://gitdir/pythonTools/chat/history"):
            # 文件名.db去掉.db来显示
            fl = len(f[:-3])
            fv = f[:-3] + " " * (60 - fl)
            MODES.append((fv, f))
        if not MODES:
            self.tl.destroy()
            messagebox.showinfo("温馨提示", "暂无历史记录")
        self.v = StringVar()
        # self.v.set("L") # initialize

        for text, mode in MODES:
            b = Radiobutton(self.tl, text=text,
                            variable=self.v, value=mode,indicatoron=0,command=self.selected)
            b.pack(anchor=W)


    def selected(self):

        self.tl.destroy()
        self.text.delete('1.0', 'end')
        self.insertText(self.v.get())


    def insertText(self, message):
        for _l in message.split('\n'):
            if _l.startswith('【系统提示】'):
                self.text.insert(END, _l + '\n','system')
            elif re.match('【.*】：\s+\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}',_l):
                self.text.insert(END, '\n' + _l + '\n', 'color')
            else:
                self.text.insert(END, _l, 'BOLD')
        self.text.see(END)


    def choose_color(self):

        color = askcolor()
        self.text.tag_configure("BOLD", font=self.bold_font,foreground=color[1])


if __name__ == '__main__':
    ui = ChatGUI() # create main ui
    ui.top.mainloop()