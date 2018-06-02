#encoding=utf-8  
#!/usr/bin/python  
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.  
# See LICENSE for details.  

from tkinter import messagebox
from tkinter import *
import time,random,threading
import beijing_pk10 as pk


class MyThread(threading.Thread):
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args
    def run(self):
        self.result = self.func(*self.args)
    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

class Updata_Excel(Frame):
    up_time = 0
    def __init__(self, parent=None,**kw):
        Frame.__init__(self, parent, kw)
        # self.notice = StringVar()
        self.makeWidgets()
    def makeWidgets(self):
        self.text1 = Text(self,width=100,height=30)
        self.text1.pack()
        # l1 = Label(self,textvariable=self.notice).pack()
    def _update(self):
        self._settime()
        self.timer = self.after(1000, self._update)
    def _settime(self):
        if self.up_time <= 100:
            self.up_time += random.randint(5,15)
            x = min(self.up_time,100)
            notice1 = '正在更新中....[%s/100]\n'%(x)
            time.sleep(1)
            self.text1.insert(END,notice1)
        else:
            self.dialog()
    def start(self):
        self._update()
        self.pack()
    def refresh_(self):
        self.start()
        t1 = MyThread(pk.start_all)
        t1.setDaemon(True)
        t1.start()
        time.sleep(1)
        if threading.activeCount() < 2:
            self.up_time = 100
        # print(threading.activeCount())
    def dialog(self):
        messagebox.showwarning('确定','数据已更新完毕!')
        self.quit()

class Watch(Frame):
    def __init__(self, parent=None, **kw):
            Frame.__init__(self, parent, kw)
            self.timestr1 = StringVar()
            self.timestr2 = StringVar()
            self.pk10 = StringVar()
            self.makeWidgets()
    def makeWidgets(self):
        l1 = Label(self, textvariable = self.timestr1).pack()
        l2 = Label(self, textvariable = self.timestr2).pack()
        l3 = Label(self,text='最新开奖号',font=('宋体',12,'bold')).pack()
        l4 = Label(self,textvariable = self.pk10,
                    fg="yellow",
                    bg='dark green',
                    font=("黑体", 14, "bold"),
                    relief='sunken',
                    borderwidth=5,
                    padx=20,
                    pady=5
                ).pack()
    def _update(self,refresh=0):
        self._settime(refresh)
        self.timer = self.after(1000, self._update)
    def _settime(self,refresh=0):
        today1 = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        time1 = str(time.strftime('%H:%M:%S', time.localtime(time.time())))
        # 9:07分开奖
        if refresh==1:
            if (int(time1.split(':')[0]) == 9 and int(time1.split(':')[1]) >= 7) or (int(time1.split(':')[0]) > 9):
                pk10 = pk.find_now_data()
            else:
                pk10 = '暂未开奖'
            self.pk10.set(pk10)
        self.timestr1.set(today1)
        self.timestr2.set(time1)
    def start(self):
        self._update(refresh=1)
        self.pack(side = TOP)



if __name__ == '__main__':
    def main():
        root = Tk()
        root.title(u'北京PK10') 
        root.geometry('400x250')
        frame1 = Frame(root)
        frame1.pack(side = BOTTOM)
        mw = Watch(root)
        ue = Updata_Excel(root)
        mywatch1 = Button(frame1, text = '刷新开奖', command = mw.start).grid(row = 3, column = 0, sticky = NW, pady = 8, padx = 20)
        mywatch2 = Button(frame1, text = '更新Excel数据', command = ue.refresh_).grid(row = 3, column = 3, sticky = NW, pady = 8, padx = 20)
        root.mainloop()
    main()