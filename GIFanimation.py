import tkinter
w = 1280
h = 720
canvas = tkinter.Canvas(width=w,height=h,bg="#71CAE7")
canvas.pack()
from random import *
import datetime
import time
import os


num = 0
arr = []
subor = open("TRANSAKCIE_PAYWALL.txt", "a+")
subor.seek(0)


num = subor.readline().strip()
for i in range (int(num)):
    riadok = subor.readline()
    arr.append(riadok.strip())



def newfile():
    global num, arr,subor
    subor.close()
    novysubor = open("TRANSAKCIE_PAYWALL.txt", "w+")
    novysubor.write(str(int(num)+1))
    for i in range (len(arr)):
        novysubor.write("\n" + arr[i])
    novysubor.write("\n" + "nieconieconieco")


