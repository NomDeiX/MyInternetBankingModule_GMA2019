import tkinter
w = 1280
h = 720
canvas = tkinter.Canvas(width=w,height=h)
canvas.pack()
from random import *
import datetime


entryID=0
buttonPrihlasit=0

def menuScreen():
    global w,h,entryID, buttonPrihlasit
    uctovnyDen = datetime.datetime.now()
    canvas.create_text((1/2)*w,h-(0.8*h),text="Internet Banking Prihlásenie" ,font="Arial 30", anchor="w")
    canvas.create_text((1/2*w,h-(0.72*h)),text="Aktuálny účtovný deň: " + uctovnyDen.strftime("%d. %b. %Y"),font="Arial 16", anchor="w")
    canvas.create_text((1/2*w,h-(0.60*h)),text="ID obchodníka: ",font="Arial 20", anchor="w")
    entryID = tkinter.Entry(width=30,font = "Helvetica 15 bold")
    entryID.pack()
    entryID.place(x=1/2*w + 200,y=h-(0.62*h),height=30)
    buttonPrihlasit = tkinter.Button(text='PRIHLÁSIŤ', font="Helvetica 15",command=paymentScreen)
    buttonPrihlasit.pack()
    buttonPrihlasit.place(x=1/2*w,y=h-(0.4*h))


def paymentScreen():
    global w,h
    print("d")
    canvas.delete("all")
    entryID.destroy()
    buttonPrihlasit.destroy()
    creditCardImg((w//2)-300,h-0.92*h,(w//2)+300,h-0.42*h) 
    
def creditCardImg(x1, y1, x2, y2, r=50, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True,outline="black", fill="#e1e5e8")
    
menuScreen()
