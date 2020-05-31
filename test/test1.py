from threading import Thread
from queue import Queue

import time

from tkinter import *

def t(s:str):
    window = Tk()

    window.title("Welcome to LikeGeeks app")

    def call_back(s):
        print(s)

    b = Button(window, text='click', command=call_back(s))
    b.pack()
    window.mainloop()


def gui_collect(q:Queue, q1:Queue):
    count = 0
    while True:
        count += 1
        try:
            a = q.get(block=True, timeout=0.1)
            s = "[GUI]" + str(int(time.time()*1000)) + " get message: "+a
            print(s)
            q1.put(s)
        except Exception:
            print("[GUI]" + str(int(time.time()*1000)) + " time out.")

def listen(q1:Queue,window):
    while True:
        try:
            s = q1.get(block=True, timeout=0.1)
            Label(window, text=s).pack()
        except Exception:
            pass

q = Queue()
q1 = Queue()
t2 = Thread(target=gui_collect, args=(q,q1,))
t2.start()
window = Tk()

window.title("Welcome to LikeGeeks app")


def call_back():
    q.put("click")

def call_listen():
    t3 = Thread(target=listen, args=(q1,window,))
    t3.start()


b = Button(window, text='click', command=call_back)
c = Button(window, text='listen', command=call_listen)
b.pack()
c.pack()
window.mainloop()

#t("123")

