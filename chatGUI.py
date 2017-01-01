#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from tkinter.colorchooser import *
from tkinter.font import Font
from functools import partial as pto
from time import ctime, sleep
from datetime import datetime
from threading import *
import os
import webbrowser

class ChatUI(object):
    def __init__(self):
        # root = Tk()
        # self.top = Toplevel(root)
        self.top = Tk()
        self.top.title('移动支付组群聊')
        self.top.geometry('700x480+50+80')
        self.top.resizable(False, False)
        # self.toAcc = toAcc

        self.addMenu()
        # msg box
        self.textfm = Frame(self.top)
        self.textsb_v =Scrollbar(self.textfm, orient=VERTICAL)
        # self.textsb_h = Scrollbar(self.textfm, orient=HORIZONTAL)
        self.text = Text(self.textfm, height=30, width=80, relief = 'flat', yscrollcommand=self.textsb_v.set)
        self.text.bind('<KeyPress>', lambda e:"break")

        self.text.tag_configure('color', foreground='blue')
        # self.bold_font = Font(family="Helvetica", size=12, weight="bold")
        self.bold_font = Font(family="Consolas", size=11, weight="bold")
        self.text.tag_configure("BOLD", font=self.bold_font)

        self.text.pack(side=LEFT, fill=BOTH)
        # self.textsb_v.config(command=self.text.yview)
        # self.textsb_h.config(command=self.text.xview)
        # self.textsb_h.pack(fill=X,expand=0, side=BOTTOM, anchor=N, before=self.text)
        self.textsb_v.pack(fill=Y,expand=0, side=LEFT, anchor=N)
        Label(self.textfm,text='群成员').pack(side="top")
        #在线人数
        self.online = Text(self.textfm, height = 25, width = 20)
        self.online_font = Font(family="微软雅黑", size=10)
        self.online.tag_configure("oneline_font", font= self.online_font, foreground="red")
        self.getOnline()
        self.online.bind('<KeyPress>', lambda e:"break")
        self.online.pack(side=RIGHT, fill=Y)
        self.textfm.pack()


        # input box
        # self.chatText = StringVar(self.top) #words to send
        # self.chatTextn = Entry(self.top, width=55, textvariable=self.chatText)
        self.chatTextn = Text(self.top, width=80, height=5)

        self.top.bind('<Return>', self.sendMsg)
        self.chatTextn.pack(side=LEFT)

        # buttons
        self.bfm = Frame(self.top)
        # self.clr = MyButton(self.bfm, text='clear', command=self.clrDir)
        self.send = MyButton(self.bfm, text='send', command=self.sendMsg)
        # self.quit = MyButton(self.bfm, text='quit', command=self.top.quit)
        # self.clr.pack(side=LEFT)
        self.send.pack()
        # self.quit.pack(side=LEFT)
        self.bfm.pack(side=LEFT,padx='20')

        # show all msgs cached on msgList
        #msgListLock.acquire()
        #for msg in [msg for msg in msgList if msg.frAcc == self.toAcc]:
        #    self.text.insert(END, ctime()+"  <<"+ msg.frAcc+'\n', 'color')
        #     self.text.insert(END, msg.msg+'\n')
        #     msgList.remove(msg)
        # msgListLock.release()

    # def clrDir(self, ev=None):
    #     self.chatText.set('')
    def getOnline(self):
        msg="☆  陈章\n☆  李玟璟\n☆  刘永涛"
        self.online.insert(END, msg, 'oneline_font')


    def sendMsg(self, ev=None):
        # msg=self.chatText.get()
        msg = self.getWholeTextMsg(self.chatTextn)
        if not msg.strip():
            return
        if msg.endswith('\n'):
            msg = msg[:-1]
        # self.chatText.set(msg+': sending...')
        # self.text.insert(END, ctime()+'  >>' + self.toAcc + '\n', 'color')
        # self.text.config(state = 'normal')
        tagText = '【' + os.getlogin() + '】：    ' + datetime.now().strftime('%Y/%m/%d %X') + '\n'
        self.text.insert(END, tagText, 'color')

        # sock.send1ChatMsg(self.toAcc, msg)
        self.text.insert(END, msg+'\n','BOLD')
        self.text.see(END)
        with open("history/" +datetime.now().strftime('%Y%m%d%p')+".db", 'a',encoding='utf-8') as f:
            f.write(tagText + msg + '\n')

        # self.text.config(state='disabled')
        # self.chatText.set('')
        self.chatTextn.delete('1.0','end')

    def getWholeTextMsg(self, text):
        """
        The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character). END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached. The only issue with this is that it actually adds a newline to our input. So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on.
        """
        return text.get('1.0','end-1c')

    def appendMsg2Text(self, text):
        pass

    def addMenu(self):
        menu = Menu(self.top)
        menu.add_command(label="历史记录", command=self.check_history)
        menu.add_command(label="选择颜色", command=self.choose_color)
        self.top.config(menu=menu)

    def check_history(self):
        def selected():
            self.tl.destroy()
            with open("history/" + self.v.get(), 'r', encoding='utf-8') as f:
                self.text.delete('1.0','end')
                self.text.insert('1.0', f.read())
            self.text.see(END)
        # webbrowser.open("http://localhost:8000")
        self.tl = Toplevel(self.top, width=800)
        self.tl.focus()
        self.tl.title("选择历史纪录日期")
        MODES = []
        for f in os.listdir("D://gitdir/pythonTools/history"):
                fl = len(f[:-3])
                fv = f[:-3] + " " * (60 - fl)
                MODES.append((fv, f))
        if not MODES:
            self.tl.destroy()
            messagebox.showinfo("温馨提示", "暂无历史记录")

        # 文件名.db去掉.db来显示
        self.v = StringVar()
        self.v.set("L") # initialize


        for text, mode in MODES:
            b = Radiobutton(self.tl, text=text,
                            variable=self.v, value=mode,indicatoron=0,command=selected)
            b.pack(anchor=W)


    def choose_color(self):
        color = askcolor()
        self.text.tag_configure("BOLD", font=self.bold_font,foreground=color[1])


MyButton = pto(Button,bg='#BFEFFF', fg='black', activeforeground='#EFFAFF',activebackground='#6AD169', width= 10, height = 2)
showInfo = lambda msg: showinfo('Info', msg)

if __name__ == '__main__':
    ui = ChatUI() # create main ui
    ui.top.mainloop()