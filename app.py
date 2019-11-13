import tkinter
w = 1280
h = 720
canvas = tkinter.Canvas(width=w,height=h)
canvas.pack()
from random import *
import datetime


entryID=0
buttonPrihlasit=0
entryCardNum=0
entryDateCard=0
entryCVVcard=0
entryAmount=0
buttonPayment=0
buttonBack=0

def menuScreen():
    global w,h,entryID, buttonPrihlasit
    print("MENU SCREEN")
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
    global w,h, entryCardNum, entryDateCard, entryCVVcard,entryAmount,buttonPayment,buttonBack
    print("PAYMENT SCREEN")
    canvas.delete("all")
    entryID.destroy()
    buttonPrihlasit.destroy()
    creditCardImg((w//2)-300,h-0.92*h,(w//2)+300,h-0.42*h)
    canvas.create_text((w//2)-275,h-(0.83*h),text="Číslo karty: " ,font="Arial 19", anchor="w")
    entryCardNum = tkinter.Entry(width=30,font = "Helvetica 15 bold")
    entryCardNum.pack()
    entryCardNum.place(x=(w//2)-275,y=h-(0.78*h),height=30)
    canvas.create_text((w//2)-275,h-(0.7*h),text="Neplatné číslo karty" ,font="Arial 14", anchor="w", fill="red")
    canvas.create_text((w//2)-275,h-(0.65*h),text="Dátum splatnosti: " ,font="Arial 19", anchor="w")
    canvas.create_text((w//2)+75,h-(0.65*h),text="CVV kód: " ,font="Arial 19", anchor="w")
    entryDateCard = tkinter.Entry(width=15,font = "Helvetica 15 bold")
    entryDateCard.pack()
    entryDateCard.place(x=(w//2)-275,y=h-(0.61*h),height=30)
    canvas.create_text((w//2)-275,h-(0.53*h),text="Nesprávny alebo expirovaný dátum" ,font="Arial 14", anchor="w", fill="red")
    entryCVVcard = tkinter.Entry(width=5,font = "Helvetica 15 bold")
    entryCVVcard.pack()
    entryCVVcard.place(x=(w//2)+75,y=h-(0.61*h),height=30)
    canvas.create_text((w//2)+75,h-(0.53*h),text="Nesprávny CVV kód" ,font="Arial 14", anchor="w", fill="red")
    canvas.create_text((w//2)+75,h-(0.48*h),text="Čo je to CVV kód?" ,font="Arial 14 italic underline", anchor="w")
    canvas.create_text((w//2)-100,h-(0.35*h),text="Suma: ",font="Arial 22", anchor="w")
    entryAmount = tkinter.Entry(width=8,font = "Helvetica 15 bold")
    entryAmount.pack()
    entryAmount.place(x=(w//2),y=h-(0.37*h),height=30)
    canvas.create_text((w//2)+100,h-(0.35*h),text="€",font="Arial 22", anchor="w")
    buttonPayment = tkinter.Button(text='VYKONAŤ PLATBU', font="Helvetica 15")
    buttonPayment.pack()
    buttonPayment.place(x=(w//2)-92,y=h-(0.3*h))
    buttonBack = tkinter.Button(text='SPÄŤ', font="Helvetica 15",command=backBtn)
    buttonBack.pack()
    buttonBack.place(x=(w//2)-300,y=h-(0.3*h))
    correctInfoImg((w//2)+80,h-(0.76*h))
    correctInfoImg((w//2)-83,h-(0.59*h))
    correctInfoImg((w//2)+155,h-(0.59*h))
    
def creditCardImg(x1, y1, x2, y2, r=50, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True,outline="black", fill="#e1e5e8")

def correctInfoImg(x,y):
    canvas.create_oval(x-15,y+15,x+15,y-15, fill="white", outline="black")
    canvas.create_line(x-8,y,x,y+8,fill="green",width=4)
    canvas.create_line(x,y+8,x+11,y-11,fill="green",width=4)
    return
    
def backBtn():
    global entryCardNum, entryDateCard, entryCVVcard,entryAmount,buttonPayment
    canvas.delete("all")
    entryCardNum.destroy()
    entryDateCard.destroy()
    entryCVVcard.destroy()
    entryAmount.destroy()
    buttonPayment.destroy()
    buttonBack.destroy()
    menuScreen()
    
menuScreen()

