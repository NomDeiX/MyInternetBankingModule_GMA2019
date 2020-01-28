import tkinter
w = 1280
h = 720
canvas = tkinter.Canvas(width=w,height=h,bg="#71CAE7")
canvas.pack()
from random import *
import datetime
import time
import os

## Velmi neelegantne, no najjednoduchsie riesenie, widgety (type==int) musia byt globalne, aby sa mohli widget.destroy() v inych definiciach
entryID=0
buttonPrihlasit=0
entryCardNum=0
entryDateCard=0
entryCVVcard=0
entryAmount=0
buttonPayment=0
buttonBack=0
labelMenuImg=0
cvvLabel=0
newroot = 0
CVVinfoLabel=0
sv = tkinter.StringVar()
creditCardType=""
labelCreditCardImg=0
cvvSwitch = False
CardNumber=""
dateCard=""
CVV=""
Amount=0
IDobchodnik = 0
casGIF = 0
timer=0
continueProcess=0


kartyriadok = 0
kartyLockSubor = 0
uctyriadok=0
uctyLockSubor=0
notEnoughFunds=False

##data  potrebne do suborov
obchodnikID = 0
successfulPayment=0
cardID = 0
ucetID = 0
klientID = 0
obchodnikUcet=0
receiverDebetKredit=""
senderDebetKredit=""

##Paths to files
pathUcty = "UCTY.txt"
pathUctyLock = "UCTY_LOCK.txt"
pathKarty = "KARTY.txt"
pathKartyLock = "KARTY_LOCK.txt"
pathTransakciePaywall = "TRANSAKCIE_PAYWALL.txt"
pathTransakciePaywallLock = "TRANSAKCIE_PAYWALL_LOCK.txt"
pathTransakcieKarty = "TRANSAKCIE_KARTY.txt"
pathTransakcieKartyLock = "TRANSAKCIE_KARTY_LOCK.txt"
pathTransakcieUcty = "TRANSAKCIE_UCTY.txt"
pathTransakcieUctyLock = "TRANSAKCIE_UCTY_LOCK.txt"
pathTransakciePaywallVerzia = "TRANSAKCIE_PAYWALL_VERZIA.txt"
pathTransakcieUctyVerzia = "TRANSAKCIE_UCTY_VERZIA.txt"
pathTransakcieKartyVerzia = "TRANSAKCIE_KARTY_VERZIA.txt"
pathUctyVerzia = "UCTY_VERZIA.txt"
pathKartyVerzia = "KARTY_VERZIA.txt"


def menuScreen():
    global w,h,entryID, buttonPrihlasit,menuImg,labelMenuImg
    print("MENU SCREEN")
    uctovnyDen = datetime.datetime.now()
    canvas.create_text((1/2)*w,h-(0.8*h),text="Internet Banking Prihlásenie" ,font="Arial 30", anchor="w")
    canvas.create_text((1/2*w,h-(0.72*h)),text="Aktuálny účtovný deň: " + uctovnyDen.strftime("%d. %b. %Y"),font="Arial 16", anchor="w")
    canvas.create_text((1/2*w,h-(0.60*h)),text="ID obchodníka: ",font="Arial 20", anchor="w")
    entryID = tkinter.Entry(width=30,font = "Helvetica 15 bold")
    entryID.pack()
    entryID.place(x=1/2*w + 200,y=h-(0.62*h),height=30)
    buttonPrihlasit = tkinter.Button(text='PRIHLÁSIŤ', font="Helvetica 15",command=getObchodnikID)
    buttonPrihlasit.pack()
    buttonPrihlasit.place(x=1/2*w,y=h-(0.4*h))
    menuImg = tkinter.PhotoImage(master=canvas,file='obrazky/menu.png')
    labelMenuImg = tkinter.Label(image = menuImg,borderwidth=0)
    labelMenuImgimage = menuImg
    labelMenuImg.pack()
    labelMenuImg.place(x=0.03*w,y=h-(0.55*h), anchor="w")
    canvas.delete("correctInfoTag")

def getObchodnikID():
    global entryID,uctyLockSubor,uctyriadok,obchodnikID, obchodnikUcet
    if(entryID.get()==""):
        print("wooong")
    elif(len(entryID.get())>0 and entryID.get().isdigit()==True):
        obchodnikID=int(entryID.get())
        if(os.path.exists(pathUctyLock)):
            canvas.after(2000,getObchodnikID)
        elif(os.path.exists(pathUctyLock)==False):
            uctyLockSubor = open(pathUctyLock, "w+")
            uctySubor=open(pathUcty, "r+")
            uctyriadok=uctySubor.readline()
            for i in range(int(uctyriadok)):
                uctyriadok=uctySubor.readline()
                print(int(uctyriadok.split(";")[0]))
                if(obchodnikID==int(uctyriadok.split(";")[0])):
                    obchodnikUcet=int(uctyriadok.split(";")[1])
                    print("found a match, obchodnik ID ("+str(obchodnikID)+") is registerred, obchodnikUcet is" + str(obchodnikUcet))
                    paymentScreen()
                    uctySubor.close()
                    uctyLockSubor.close()
                    os.remove(pathUctyLock)   
                    return
                else:
                    print("not found")
                    canvas.create_text((1/2*w,h-(0.55*h)),text="ID obchodnika nie je v databaze",font="Arial  14",fill="red", anchor="w")
            uctySubor.close()
            uctyLockSubor.close()
            os.remove(pathUctyLock)     
                
def paymentScreen():
    global w,h, entryCardNum, entryDateCard, entryCVVcard,entryAmount,buttonPayment,buttonBack, labelMenuImg, cvvLabel, sv
    checkObchodnik()
    if (IDobchodnik!="" and IDobchodnik!=0 and str(IDobchodnik).isdigit()==True):
        print("PAYMENT SCREEN")
        canvas.delete("all")
        entryID.destroy()
        buttonPrihlasit.destroy()
        labelMenuImg.config(image='')
        labelMenuImg.destroy()
        creditCardBackgroundImg((w//2)-300,h-0.92*h,(w//2)+300,h-0.42*h)
        canvas.create_text((w//2)-275,h-(0.83*h),text="Číslo karty: " ,font="Arial 19", anchor="w")
        cardTypeSV=tkinter.StringVar()
        cardTypeSV.trace("w", lambda name, index, mode, sv=cardTypeSV: cardTypeChecker())
        entryCardNum = tkinter.Entry(width=30,font = "Helvetica 15 bold",textvariable=cardTypeSV)
        entryCardNum.pack()
        entryCardNum.place(x=(w//2)-275,y=h-(0.78*h),height=30)
        canvas.create_text((w//2)-275,h-(0.65*h),text="Dátum splatnosti: " ,font="Arial 19", anchor="w")
        canvas.create_text((w//2)+75,h-(0.65*h),text="CVV kód: " ,font="Arial 19", anchor="w")
        cardDateSV=tkinter.StringVar()
        cardDateSV.trace("w", lambda name, index, mode, sv=cardDateSV: validateDate())
        entryDateCard = tkinter.Entry(width=15,font = "Helvetica 15 bold",textvariable=cardDateSV)
        entryDateCard.pack()
        entryDateCard.place(x=(w//2)-275,y=h-(0.61*h),height=30)
        entryCVVcard = tkinter.Entry(width=5,font = "Helvetica 15 bold", textvariable=sv)
        entryCVVcard.pack()
        entryCVVcard.place(x=(w//2)+75,y=h-(0.61*h),height=30)
        sv.trace("w", lambda name, index, mode, sv=sv: validateCVV())
        cvvLabel = tkinter.Label(text="Kde nájdem CVV kód?", font="Arial 14 italic underline",anchor="w",background="#e1e5e8")
        cvvLabel.pack()
        cvvLabel.place(x=(w//2)+73,y=h-(0.49*h))
        cvvLabel.bind("<Button-1>",whatsCVVScreen)
        canvas.create_text((w//2)-100,h-(0.35*h),text="Suma: ",font="Arial 22", anchor="w")
        entryAmount = tkinter.Entry(width=8,font = "Helvetica 15 bold")
        entryAmount.pack()
        entryAmount.place(x=(w//2),y=h-(0.37*h),height=30)
        canvas.create_text((w//2)+100,h-(0.35*h),text="€",font="Arial 22", anchor="w")
        buttonPayment = tkinter.Button(text='VYKONAŤ PLATBU', font="Helvetica 15", command=transactionValidation)
        buttonPayment.pack()
        buttonPayment.place(x=(w//2)-92,y=h-(0.3*h))
        buttonBack = tkinter.Button(text='SPÄŤ', font="Helvetica 15",command=backBtn)
        buttonBack.pack()
        buttonBack.place(x=(w//2)-300,y=h-(0.3*h))
        errorCreditInfo() 
        cardTypeChecker()
        entryAmount.bind('<Button-1>', validateAll)
        entryCardNum.bind('<Button-1>', validateAll)
        entryCVVcard.bind('<Button-1>', validateAll)
        entryDateCard.bind('<Button-1>', validateAll)
    
    

def checkObchodnik():
    global IDobchodnik,entryID
    IDobchodnik = entryID.get()


def creditCardBackgroundImg(x1, y1, x2, y2, r=50, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True,outline="black", fill="#e1e5e8")

def correctInfoImg(x,y):
    canvas.create_oval(x-15,y+15,x+15,y-15, fill="white", outline="black",tags="correctInfoTag")
    canvas.create_line(x-8,y,x,y+8,fill="green",width=4,tags="correctInfoTag")
    canvas.create_line(x,y+8,x+11,y-11,fill="green",width=4,tags="correctInfoTag")
    return

def whatsCVVScreen(event):
    global w,h,newroot,CVVinfoLabel,newrootActive,cvvSwitch
    if (cvvSwitch == False):
        newroot = tkinter.Tk()
        CVVinfoLabel=tkinter.Label(newroot, text="CVV/CVC kód nájdete na zadnej strane karty napravo od vášho podpisového vzoru." + "\n" + "Keď platíte kartou cez internet, potrebujete zadať tento údaj ako verifikaciu.")
        CVVinfoLabel.config(font=("Courier", 15))
        CVVinfoLabel.pack()
        cvvSwitch = True
    elif(cvvSwitch == True):
        newroot.destroy()
        cvvSwitch = False

def backBtn():
    global entryCardNum, entryDateCard, entryCVVcard,entryAmount,buttonPayment,cvvLabel,labelCreditCardImg,creditCardImg,IDobchodnik,CVV,dateCard,CardNumber
    canvas.delete("all")
    entryCardNum.destroy()
    entryDateCard.destroy()
    entryCVVcard.delete(0,"end")
    entryCVVcard.destroy()
    entryAmount.destroy()
    buttonPayment.destroy()
    buttonBack.destroy()
    cvvLabel.destroy()
    labelCreditCardImg.place(x=0,y=0, anchor="w")
    labelCreditCardImg.config(image='',width=1)
    labelCreditCardImg.destroy()
    IDobchodnik = ""
    CardNumber=""
    dateCard=""
    CVV=""
    menuScreen()


def validateAll(event):
    print("click")
    global IDobchodnik
    if (IDobchodnik!="" and IDobchodnik!=0):
        global correctInfoImg,CVV,CardNumber,entryCVVcard,dateCard,CardNumber,correctnessOfData
        canvas.create_rectangle((w//2)+155-15,h-(0.59*h)+15,(w//2)+155+15,(h-(0.59*h)-15),fill="#e1e5e8",outline='#e1e5e8',tags="correctInfoTag")
        canvas.create_rectangle((w//2)+80-15,(h-(0.76*h))+15,(w//2)+80+15,(h-(0.76*h))-15,fill="#e1e5e8",outline='#e1e5e8',tags="correctInfoTag")
        canvas.create_rectangle(((w//2)-83)-15,(h-(0.59*h))+15,((w//2)-83)+15,(h-(0.59*h))-15,fill="#e1e5e8",outline='#e1e5e8',tags="correctInfoTag")
        correctnessOfData=0
        if (len(CVV)==3 and entryCVVcard.get().isdigit()==True ):
            correctInfoImg((w//2)+155,h-(0.59*h))
        if (len(CardNumber.replace(" ", ""))==16 and CardNumber.replace(" ", "").isdigit()==True):
            correctInfoImg((w//2)+80,h-(0.76*h))
        if(len(dateCard.replace("/",""))==4) and (int(dateCard.replace("/","")[0])==0 or int(dateCard.replace("/","")[0])==1) and (int(dateCard.replace("/","")[0:2])<=13) and (2<=int(dateCard.replace("/","")[2])<=3) and dateCard.replace("/","").isdigit()==True:    
            correctInfoImg((w//2)-83,h-(0.59*h))


def transactionValidation():
    global continueProcess
    continueProcess = 0
    if (len(CVV)==3 and entryCVVcard.get().isdigit()==True ):
        canvas.create_rectangle((w//2)+155-15,h-(0.59*h)+15,(w//2)+155+15,(h-(0.59*h)-15),fill="#e1e5e8",outline='#e1e5e8',tags="correctInfoTag")
        canvas.create_rectangle((w//2)+75,h-(0.53*h)-15,(w//2)+250,h-(0.53*h)+10,fill="#e1e5e8",outline='#e1e5e8',tags="incorrectInfoTag")
        correctInfoImg((w//2)+155,h-(0.59*h))
        continueProcess+=1
    elif (len(CVV)!=3 or entryCVVcard.get().isdigit()==False ):
        canvas.create_rectangle((w//2)+155-15,h-(0.59*h)+15,(w//2)+155+15,(h-(0.59*h)-15),fill="#e1e5e8",outline='#e1e5e8',tags="correctInfoTag")
        canvas.create_text((w//2)+75,h-(0.53*h),text="Nesprávny CVV kod" ,font="Arial 14", anchor="w", fill="red")
    if (len(CardNumber.replace(" ", ""))==16 and CardNumber.replace(" ", "").isdigit()==True):
        canvas.create_rectangle((w//2)+80-15,(h-(0.76*h))+15,(w//2)+80+15,(h-(0.76*h))-15,fill="#e1e5e8",outline='#e1e5e8',tags="correctInfoTag")
        canvas.create_rectangle((w//2)-275,h-(0.7*h)-15,(w//2)+100,h-(0.7*h)+10,fill="#e1e5e8",outline='#e1e5e8',tags="incorrectInfoTag")
        correctInfoImg((w//2)+80,h-(0.76*h))
        continueProcess+=1
    elif(len(CardNumber.replace(" ", ""))!=16 or CardNumber.replace(" ", "").isdigit()==False):
        canvas.create_rectangle((w//2)+80-15,(h-(0.76*h))+15,(w//2)+80+15,(h-(0.76*h))-15,fill="#e1e5e8",outline='#e1e5e8',tags="correctInfoTag")
        canvas.create_text((w//2)-275,h-(0.7*h),text="Neplatné číslo karty" ,font="Arial 14", anchor="w", fill="red")
    if(len(dateCard.replace("/",""))==4) and (int(dateCard.replace("/","")[0])==0 or int(dateCard.replace("/","")[0])==1) and (int(dateCard.replace("/","")[0:2])<=13) and (2<=int(dateCard.replace("/","")[2])<=3) and (dateCard.replace("/","").isdigit()==True):
        canvas.create_rectangle(((w//2)-83)-15,(h-(0.59*h))+15,((w//2)-83)+15,(h-(0.59*h))-15,fill="#e1e5e8",outline='#e1e5e8',tags="correctInfoTag")
        canvas.create_rectangle((w//2)-275,h-(0.53*h)-15,(w//2)+50,h-(0.53*h)+10,fill="#e1e5e8",outline='#e1e5e8',tags="incorrectInfoTag")
        correctInfoImg((w//2)-83,h-(0.59*h))
        continueProcess+=1
    elif(len(dateCard.replace("/",""))!=4) or (int(dateCard.replace("/","")[0])!=0 and int(dateCard.replace("/","")[0])!=1) or (int(dateCard.replace("/","")[0:2])>=13) or (0<=int(dateCard.replace("/","")[2])<=1 or 4<=int(dateCard.replace("/","")[2])) or (dateCard.replace("/","").isdigit()==False):
        canvas.create_rectangle(((w//2)-83)-15,(h-(0.59*h))+15,((w//2)-83)+15,(h-(0.59*h))-15,fill="#e1e5e8",outline='#e1e5e8',tags="correctInfoTag")
        canvas.create_text((w//2)-275,h-(0.53*h),text="Nesprávny alebo expirovaný dátum" ,font="Arial 14", anchor="w", fill="red")
    if (continueProcess==3):
        print("calling transaction")
        transaction()

        
def validateCVV():
    global entryCVVcard,CVV
    CVV = str(entryCVVcard.get())
    if (len(str(entryCVVcard.get()))>3):
        print("The CVV entry widget has maximum of 3 characters")
        entryCVVcard.delete(0,"end")
        entryCVVcard.insert(0,CVV[:3])
        print("First 3 characters: " + CVV[:3])
        print("Characters you are trying to put in: " + CVV)
        CVV =entryCVVcard.get()
           
    
def validateCardNumber():
    global entryCardNum,CardNumber
    CardNumber=str(entryCardNum.get())
    if (len(CardNumber)>0):
        if (len(CardNumber)==4):
            entryCardNum.insert(4," ")
        elif(len(CardNumber)==9):
             entryCardNum.insert(9," ")
        elif(len(CardNumber)==14):
             entryCardNum.insert(14," ")
    if (len(str(entryCardNum.get().replace(" ", "")))>16):
        print("The card number maximum of 16 characters")
        helpStringCardNum = CardNumber.replace(" ", "")
        CardNumber=entryCardNum.get().replace(" ", "")[:16]
        entryCardNum.delete(0,"end")
        entryCardNum.insert(0,helpStringCardNum[:4]+" "+helpStringCardNum[4:8]+" "+helpStringCardNum[8:12]+" "+helpStringCardNum[12:16])

def validateDate():
    global entryDateCard,dateCard
    if (len(entryDateCard.get())==5):
        print("")
##        entryDateCard.insert(0,dateCard)
    dateCard = entryDateCard.get()
    if (2<=len(entryDateCard.get())<=4 and (entryDateCard.get().find("/")!=2) and ("/" not in entryDateCard.get())):  ## NEFUNGUJE KURNIIIIK
        dateCard.replace("/","")
        entryDateCard.delete(0,"end")
        entryDateCard.insert(0,dateCard)
        entryDateCard.insert(2,"/")
    if(len(entryDateCard.get())>5):
        entryDateCard.delete(0,"end")
        entryDateCard.insert(0,dateCard[:5])
        dateCard = dateCard[:5]
    if(entryDateCard.get()[:2].isdigit() == True and "/" in entryDateCard.get()):
        print("no more change")
        
        

    
def errorCreditInfo():
    if (False):
        canvas.create_text((w//2)-275,h-(0.7*h),text="Neplatné číslo karty" ,font="Arial 14", anchor="w", fill="red")
        canvas.create_text((w//2)-275,h-(0.53*h),text="Nesprávny alebo expirovaný dátum" ,font="Arial 14", anchor="w", fill="red")
        canvas.create_text((w//2)+75,h-(0.53*h),text="Nesprávny CVV kod" ,font="Arial 14", anchor="w", fill="red")

def CreditTypePicker():
    global labelCreditCardImg, creditCardImg, creditCardType
    if (creditCardType==""):
        creditCardImg = tkinter.PhotoImage(master=canvas,file='obrazky/defaultLogo.png')
    elif (creditCardType=="Visa"):
        creditCardImg = tkinter.PhotoImage(master=canvas,file='obrazky/VisaLogo.png')
    elif (creditCardType=="MasterCard"):
        creditCardImg = tkinter.PhotoImage(master=canvas,file='obrazky/MasterCardLogo.png')
    elif (creditCardType=="AmericanExpress"):
        creditCardImg = tkinter.PhotoImage(master=canvas,file='obrazky/AmericanExpressLogo.png')
    elif (creditCardType=="Other"):
        creditCardImg = tkinter.PhotoImage(master=canvas,file='obrazky/OtherLogo.png')
    labelCreditCardImg = tkinter.Label(image = creditCardImg,borderwidth=0)
    labelCreditCardImgimage = creditCardImg
    labelCreditCardImg.pack()
    labelCreditCardImg.place(x=0.6*w,y=h-(0.77*h), anchor="w")
    canvas.create_window(0.63*w, h-(0.77*h), window=labelCreditCardImg) 


def cardTypeChecker():
    global entryCardNum,creditCardType
    validateCardNumber()
    CardNumber = str(entryCardNum.get())
    if(len(CardNumber)>=1):
        firstNumber = CardNumber[0]
        if (int(firstNumber)==4):
            creditCardType="Visa"
        elif(int(firstNumber)==5):
            creditCardType="MasterCard"
        elif(int(firstNumber)==3):
            creditCardType="AmericanExpress"
        else:
            creditCardType="Other"
    elif(len(CardNumber)==0):
        creditCardType=""
    CreditTypePicker()  


def transaction():
    global Amount,entryAmount, CardNumber,dateCard,CVV
    print("gg")
    if (len(entryAmount.get())>0 and float(entryAmount.get())>0.00):
        canvas.create_rectangle(350,700,950,575,fill="#71CAE7")
        canvas.create_text(650,670,text="Transakcia sa spracúvava",font="Helvetica 18")
        loadingGIF()
        disableEntries()
        print("starting transaction")
        Amount = float(entryAmount.get())
        Amount = float(str(Amount)[:str(Amount).find(".")+3])
        print("Amount: " + str(Amount))
        getCardID()
        #transactionSuccessful()
    elif(len(entryAmount.get())==0):
        print("transcation failed")
        canvas.create_text((w//2)+130,h-(0.35*h),text="Zadajte sumu v tvare 100.50 €" ,font="Arial 14", anchor="w", fill="red")
     


def loadingGIF():
    global casGIF,timer
    canvas.create_rectangle(420+100*casGIF,600-20,420+100*casGIF+20,600+20,fill="gray",tags="casovanie")
    timer = canvas.after(1000,loadingGIF)
    casGIF+=1
    if (casGIF==6):
        canvas.delete("casovanie")
        casGIF=0


def disableEntries():
    entryAmount.config(state='disabled')
    entryCardNum.config(state='disabled')
    entryDateCard.config(state='disabled')
    entryCVVcard.config(state='disabled')
    buttonBack.config(state='disabled')
    buttonPayment.config(state='disabled')

def enableEntries():
    canvas.create_rectangle(350,700,950,575,fill="#71CAE7",outline="#71CAE7")
    entryAmount.config(state='normal')
    entryCardNum.config(state='normal')
    entryDateCard.config(state='normal')
    entryCVVcard.config(state='normal')
    buttonBack.config(state='normal')
    buttonPayment.config(state='normal')

def everythingIsDone():
    global dateCard
    enableEntries()
    entryCVVcard.delete(0,"end")
    canvas.delete("correctInfoTag")
    dateCard = ""
    resetPaywallVariables()
    backBtn()
    
def transactionSuccessful():
    global timer
    canvas.after_cancel(timer)
    canvas.delete("casovanie")
    canvas.create_rectangle(250,700,1050,575,fill="#71CAE7")
    canvas.create_text(650,630,text="Transakcia bola úspešná.",font="Helvetica 18")
    canvas.create_text(650,660,text="Budete presmerovaný na hlavnú stránku.",font="Helvetica 18")
    canvas.after(4000,everythingIsDone)
    
def getCardID():
    global cardID, kartyriadok, kartyLockSubor,notEnoughFunds,successfulPayment, ucetID
    if (os.path.exists(pathKartyLock)):
        canvas.after(2000,getCardID)
    elif(os.path.exists(pathKartyLock)==False):
        kartyLockSubor = open(pathKartyLock,"w+")
        kartySubor = open(pathKarty,"r+")
        kartyriadok = kartySubor.readline()
        print(kartyriadok)
        for i in range (int(kartyriadok)):
            print("test for loop")
            kartyriadok = kartySubor.readline()
            if (int(kartyriadok.split(";")[3])==int(CardNumber.replace(" ",""))):
                print("Found a match, checking CVV and date")
                if (int(kartyriadok.split(";")[4])==int(dateCard.replace("/","")[:4])):
                    print("Card number and expiry date are correct")
                    if (int(kartyriadok.split(";")[5])==int(CVV)):
                        if (int(kartyriadok.split(";")[8])==0):
                            ucetID = int(kartyriadok.split(";")[6])
                            creditOrDebet()
                            if (notEnoughFunds==False):
                                print("Everything is correct")
                                cardID = int(kartyriadok.split(";")[0])
                                kartySubor.close()
                                kartyLockSubor.close()
                                successfulPayment=1
                                transakciePaywall()     
                                try:
                                    os.remove(pathKartyLock)
                                except OSError:
                                    print("probably already deleted")
                                transactionSuccessful()
                                return True
                            notEnoughFunds = False
                        elif(int(kartyriadok.split(";")[8])==1):
                            print("blocked card")
                            enableEntries()
                            transakciePaywall()
                            canvas.create_text(650,630,text="Vaša karta je zablokovaná.",font="Arial 14",fill="red")
                            canvas.after_cancel(timer)
                            kartySubor.close()
                            kartyLockSubor.close()
                            os.remove(pathKartyLock)
                            return
                            

                    else:
                        print("wrong CVV")
                        enableEntries()
                        transakciePaywall()
                        canvas.create_text((w//2)+75,h-(0.53*h),text="Nesprávny CVV kod" ,font="Arial 14", anchor="w", fill="red")
                        canvas.after_cancel(timer)
                        kartySubor.close()
                        kartyLockSubor.close()
                        os.remove(pathKartyLock)
                        return
                        


                else:
                    print("wrong expiry date")
                    enableEntries()
                    transakciePaywall()
                    canvas.create_text((w//2)-275,h-(0.53*h),text="Nesprávny alebo expirovaný dátum" ,font="Arial 14", anchor="w", fill="red")
                    canvas.after_cancel(timer)
                    kartySubor.close()
                    kartyLockSubor.close()
                    os.remove(pathKartyLock)
                    return
                    
                    
        

        try:    
            kartySubor.close() 
            kartyLockSubor.close()
            os.remove(pathKartyLock)
            print("wrong number")
            enableEntries()
            transakciePaywall()
            canvas.create_text((w//2)-275,h-(0.7*h),text="Neplatné číslo karty" ,font="Arial 14", anchor="w", fill="red")
            canvas.after_cancel(timer)
        except OSError:
            print("probably already done")
        
def creditOrDebet():
    global kartyriadok, Amount,kartyLockSubor,notEnoughFunds, ucetID, klientID, uctyriadok, obchodnikUcet, senderDebetKredit
    if (kartyriadok.split(";")[2]=="D"):
        print("debet card")
        senderDebetKredit="Debet"
        if (os.path.exists(pathUctyLock)):
            canvas.after(2000,creditOrDebet)
        elif(os.path.exists(pathUctyLock)==False):
            uctyLockSubor = open(pathUctyLock,"w+")
            uctySubor = open(pathUcty,"r+")
            uctyriadok = uctySubor.readline()
            for i in range (int(uctyriadok)):
                uctyriadok = uctySubor.readline()
                if(kartyriadok.split(";")[6]==uctyriadok.split(";")[0]):
                    if (Amount<=float(uctyriadok.split(";")[4]) and Amount<=float(kartyriadok.split(";")[10])):
                        print("Suma je mensia ako zostatok")
                        print("nasiel som klient ID: " + uctyriadok.split(";")[1])
                        klientID = uctyriadok.split(";")[1]
                    elif(Amount>float(kartyriadok.split(";")[10]) or Amount>float(uctyriadok.split(";")[4])):
                        #print ("Amount: " + str(Amount) + " + kartyriadoksplit10 " + str(kartyriadok.split(";")[10]) + " is less/more")
                        print("Nemate dostatok penazi na ucte")
                        notEnoughFunds=True
                        enableEntries()
                        transakciePaywall()
                        canvas.create_text(650,630,text="Na Vašom účte sa nenachádza dostatok finančných prostriedkov alebo nizky limit.",font="Arial 14",fill="red")
                        canvas.after_cancel(timer)
                        break          
            uctySubor.close()
            uctyLockSubor.close()
            os.remove(pathUctyLock)
            try:
                kartyLockSubor.close()
                os.remove(pathKartyLock)
            except :
                print("karty lock was probably already deleted")
    elif(kartyriadok.split(";")[2]=="K"):
        print("credit card")
        senderDebetKredit = "Kredit"
        if (os.path.exists(pathUctyLock)):
            canvas.after(2000,creditOrDebet)
        elif(os.path.exists(pathUctyLock)==False):
            uctyLockSubor = open(pathUctyLock,"w+")
            uctySubor = open(pathUcty,"r+")
            uctyriadok = uctySubor.readline()
            for i in range (int(uctyriadok)):
                uctyriadok = uctySubor.readline()
                if(kartyriadok.split(";")[6]==uctyriadok.split(";")[0]):
                    if(Amount+float(kartyriadok.split(";")[7])<=float(kartyriadok.split(";")[10])):
                        print("Sedi")
                        print("nasiel som klient ID: " + uctyriadok.split(";")[1])
                        klientID = uctyriadok.split(";")[1]
                    elif(Amount+float(kartyriadok.split(";")[7])>float(kartyriadok.split(";")[10])):
                        print("Nizky limit")
                        notEnoughFunds=True
                        enableEntries()
                        transakciePaywall()
                        canvas.create_text(650,630,text="Na Vašom účte je nizky limit",font="Arial 14",fill="red")
                        canvas.after_cancel(timer)
                        break
            uctySubor.close()
            uctyLockSubor.close()
            os.remove(pathUctyLock)
            try:
                kartyLockSubor.close()
                os.remove(pathKartyLock)
            except :
                print("karty lock was probably already deleted")

    


def transakciePaywall():
    global Amount, successfulPayment, obchodnikID, klientID, cardID, idtransakcie
    transakcieKarty()
    num = 0
    arr = []
    datum = datetime.date.today().strftime('%d%m%Y')
    najvacsiecisloTP = 0
    if (os.path.exists(pathTransakciePaywallLock)):
            canvas.after(2000,creditOrDebet)
    elif(os.path.exists(pathTransakciePaywallLock)==False):
        locksubor = open(pathTransakciePaywallLock,"w+")
        starysubor = open(pathTransakciePaywall, "a+")
        starysubor.seek(0)
        num = starysubor.readline().strip()
        for i in range (int(num)):
            riadok = starysubor.readline()
            arr.append(riadok.strip())
            if(najvacsiecisloTP<int(riadok.split(";")[0])):
                najvacsiecisloTP=int(riadok.split(";")[0])
        starysubor.close()
        novysubor = open(pathTransakciePaywall, "w+")
        novysubor.write(str(int(num)+1))
        for i in range (len(arr)):
            novysubor.write("\n" + arr[i])
        if (os.path.exists(pathTransakcieUctyLock)):
            canvas.after(2000,transakciePaywall)
        elif(os.path.exists(pathTransakcieUctyLock)==False):
            docasnyFile = open(pathTransakcieUcty, "r")
            docasnyLockFile = open(pathTransakcieUctyLock, "w")
            if (successfulPayment==1):
                riadkyid = docasnyFile.readlines()
                riadokid = riadkyid[len(riadkyid)-1]
                idtransakcie = int(int(riadokid.split(";")[0])+1)
            elif(successfulPayment!=1):
                idtransakcie = 0
            novysubor.write("\n" + str(int(najvacsiecisloTP)+1)+";"+ str(cardID) +";"+str(Amount)+";"+str(klientID)+";"+str(idtransakcie)+";"+str(obchodnikID)+";"+CardNumber+";"+str(successfulPayment)+";"+datum)
            docasnyFile.close()
            docasnyLockFile.close()
            os.remove(pathTransakcieUctyLock)   
        if (successfulPayment==1):
            transakcieUcty()
            successfulPayment=0
        increasePaywallVer()
        novysubor.close()
        locksubor.close()
        os.remove(pathTransakciePaywallLock)
        

def resetPaywallVariables():
    global ucetID, obchodnikID, successfulPayment, cardID, obchodnikUcet,senderDebetKredit,receiverDebetKredit
    obchodnikID = 0
    successfulPayment=0
    cardID = 0
    ucetID = 0
    klientID = 0
    obchodnikUcet=0
    receiverDebetKredit=""
    senderDebetKredit=""

    

def transakcieKarty():
    global cardID, Amount, obchodnikID
    numTK = 0
    arrTK = []
    najvacsiecisloTK = 0
    datum = datetime.date.today().strftime('%d%m%Y')
    if (os.path.exists(pathTransakcieKartyLock)):
            canvas.after(2000,creditOrDebet)
    elif(os.path.exists(pathTransakcieKartyLock)==False):
        lockTKsubor = open(pathTransakcieKartyLock,"w+")
        staryTKsubor = open(pathTransakcieKarty, "a+")
        staryTKsubor.seek(0)
        numTK = staryTKsubor.readline().strip()
        for i in range (int(numTK)):
            riadokTK=staryTKsubor.readline()
            arrTK.append(riadokTK.strip())
            if (int(riadokTK.split(";")[0])>najvacsiecisloTK):
                najvacsiecisloTK = int(riadokTK.split(";")[0])
        staryTKsubor.close()
        novyTKsubor = open(pathTransakcieKarty, "w+")
        novyTKsubor.write(str(int(numTK)+1))
        print("najvacsie cislo je : " + str(riadokTK.split(";")[0]))
        for i in range (len(arrTK)):
            novyTKsubor.write("\n" + arrTK[i])
        novyTKsubor.write("\n" + str(int(najvacsiecisloTK)+1)+";"+str(cardID)+";"+str(Amount)+";"+str(obchodnikID)+";"+str(datum))
        increaseTransakcieKartyVer()
        novyTKsubor.close()
        lockTKsubor.close()
        os.remove(pathTransakcieKartyLock)

def transakcieUcty():
    global Amount, successfulPayment, obchodnikID, klientID, cardID, ucetID, obchodnikID, obchodnikUcet
    moneyTransfer()
    numTU = 0
    arrTU = []
    datum = datetime.date.today().strftime('%d%m%Y')
    najvacsiecisloTU = 0
    if (os.path.exists(pathTransakcieUctyLock)):
            canvas.after(2000,creditOrDebet)
    elif(os.path.exists(pathTransakcieUctyLock)==False):
        lockTUsubor = open(pathTransakcieUctyLock,"w+")
        staryTUsubor = open(pathTransakcieUcty, "a+")
        staryTUsubor.seek(0)
        numTU = staryTUsubor.readline().strip()
        for i in range (int(numTU)):
            riadokTU = staryTUsubor.readline()
            arrTU.append(riadokTU.strip())
            if (najvacsiecisloTU<int(riadokTU.split(";")[0])):
                najvacsiecisloTU = int(riadokTU.split(";")[0])
        staryTUsubor.close()
        novyTUsubor = open(pathTransakcieUcty, "w+")
        novyTUsubor.write(str(int(numTU)+2))
        for i in range (len(arrTU)):
            novyTUsubor.write("\n" + arrTU[i])
        novyTUsubor.write("\n" + str(int(najvacsiecisloTU)+1)+";"+ "C" +";"+"P"+";"+str(klientID)+";"+str(ucetID)+";"+"-"+str(Amount)+";"+str(int(numTU)+2)+";"+str(datum))
        novyTUsubor.write("\n" + str(int(najvacsiecisloTU)+2)+";"+ "D" +";"+"P"+";"+str(obchodnikID)+";"+str(obchodnikUcet)+";"+"+"+str(Amount)+";"+str(int(numTU)+1)+";"+str(datum))
        increaseTransakcieUctyVer()
        novyTUsubor.close()
        lockTUsubor.close()
        os.remove(pathTransakcieUctyLock)
    

def moneyTransfer():
    global senderDebetKredit, Amount, klientID, obchodnikID, CardNumber
    arrDebet=[]
    if (senderDebetKredit=="Debet"):
        print("removing " + str(Amount) + " from his account")
        if (os.path.exists(pathUctyLock)):
            canvas.after(2000,creditOrDebet)
        elif(os.path.exists(pathUctyLock)==False):
            uctyLockSubor = open(pathUctyLock,"w+")
            uctySubor = open(pathUcty,"r+")
            uctyriadok = uctySubor.readline()
            pocetriadkov = int(uctyriadok)
            for i in range (int(uctyriadok)):
                uctyriadok = uctySubor.readline()
                arrDebet.append(uctyriadok)
            uctySubor.seek(0)
            uctySubor.truncate()
            uctySubor.write(str(pocetriadkov)+"\n")
            for i in range(len(arrDebet)):
                if(int(arrDebet[i].split(";")[1])==int(klientID)):
                    print("it is this one")
                    oldSuma = arrDebet[i].split(";")[4].strip()
                    newSuma = str(float(float(oldSuma)-float(Amount)))
                    print("before: " + str(arrDebet[i].split(";")[4]))
                    lengthPomocna = len(arrDebet[i].split(";")[4])
                    if (i!=pocetriadkov):
                        uctySubor.write(arrDebet[i][:len(arrDebet[i])-int(lengthPomocna)]+newSuma+"\n")
                    else:
                        uctySubor.write(arrDebet[i][:len(arrDebet[i])-int(lengthPomocna)]+newSuma)
                    print("old suma : " + str(oldSuma) + " and new suma: " + str(newSuma))
                    print("after: " + arrDebet[i][:len(arrDebet[i])-int(lengthPomocna)]+newSuma)
                elif(int(arrDebet[i].split(";")[1])==int(obchodnikID)):
                    oldSuma2 = arrDebet[i].split(";")[4].strip()
                    newSuma2=str(float(float(oldSuma2)+float(Amount)))
                    print("before2: " + str(arrDebet[i].split(";")[4]))
                    lengthPomocna2 = len(arrDebet[i].split(";")[4])
                    if (i!=pocetriadkov):
                        uctySubor.write(arrDebet[i][:len(arrDebet[i])-int(lengthPomocna2)]+newSuma2+"\n")
                    else:
                        uctySubor.write(arrDebet[i][:len(arrDebet[i])-int(lengthPomocna2)]+newSuma2)
                    print("old suma2 : " + str(oldSuma2) + " and new suma2: " + str(newSuma2))
                    print("after2: " + arrDebet[i][:len(arrDebet[i])-int(lengthPomocna2)]+newSuma2)
                else:
                    uctySubor.write(arrDebet[i])

            increaseUctyVer()        
            uctySubor.close()
            uctyLockSubor.close()
            os.remove(pathUctyLock)
            
    elif (senderDebetKredit=="Kredit"):
        arrKredit=[]
        print("adding" + str(Amount) + " to his credit")
        if (os.path.exists(pathKartyLock)):
            canvas.after(2000,creditOrDebet)
        elif(os.path.exists(pathKartyLock)==False):   
            kartyLockSuborMoneyTransfer = open(pathKartyLock,"w+")
            kartySuborMoneyTransfer = open(pathKarty,"r+")
            kartyriadokMoneyTransfer = kartySuborMoneyTransfer.readline()
            pocetriadkovkredit = int(kartyriadokMoneyTransfer)
            for i in range(int(kartyriadokMoneyTransfer)):
                kartyriadokMoneyTransfer = kartySuborMoneyTransfer.readline()
                arrKredit.append(kartyriadokMoneyTransfer)

            kartySuborMoneyTransfer.seek(0)
            kartySuborMoneyTransfer.truncate()
            kartySuborMoneyTransfer.write(str(pocetriadkovkredit)+"\n")
            for i in range(len(arrKredit)):
                if (int(CardNumber)==int(arrKredit[i].split(";")[3])):
                    print("it is this one kredit")
                    old = float(arrKredit[i].split(";")[7].strip())
                    new = old + float(Amount)
                    arrKredit[i] = ';'.join(v if i != 7 else str(new) for i, v in enumerate(arrKredit[i].split(';')))
                    kartySuborMoneyTransfer.write(arrKredit[i])
                else:
                    kartySuborMoneyTransfer.write(arrKredit[i])

            increaseKartyVer()
            kartySuborMoneyTransfer.close()
            kartyLockSuborMoneyTransfer.close()
            os.remove(pathKartyLock)

            if (os.path.exists(pathUctyLock)):
                canvas.after(2000,creditOrDebet)
            elif(os.path.exists(pathUctyLock)==False):
                arrKreditUcty=[]
                uctyLockSuborK = open(pathUctyLock,"w+")
                uctySuborK = open(pathUcty,"r+")
                uctyriadokK = uctySuborK.readline()
                pocetriadkovK = int(uctyriadokK)
                for i in range (int(uctyriadokK)):
                    uctyriadokK = uctySuborK.readline()
                    arrKreditUcty.append(uctyriadokK)
                uctySuborK.seek(0)
                uctySuborK.truncate()
                uctySuborK.write(str(pocetriadkovK)+"\n")
                for i in range(len(arrKreditUcty)):
                    if(int(arrKreditUcty[i].split(";")[1])==int(obchodnikID)):
                        old2 = arrKreditUcty[i].split(";")[4].strip()
                        new2=str(float(float(old2)+float(Amount)))
                        print("before2: " + str(arrKreditUcty[i].split(";")[4]))
                        lengthPomocna2K = len(arrKreditUcty[i].split(";")[4])
                        if (i!=pocetriadkovK):
                            uctySuborK.write(arrKreditUcty[i][:len(arrKreditUcty[i])-int(lengthPomocna2K)]+new2+"\n")
                        else:
                            uctySuborK.write(arrKreditUcty[i][:len(arrKreditUcty[i])-int(lengthPomocna2K)]+new2)
                        print("old suma2 : " + str(old2) + " and new suma2: " + str(new2))
                        print("after2: " + arrKreditUcty[i][:len(arrKreditUcty[i])-int(lengthPomocna2K)]+new2)
                    else:
                        uctySuborK.write(arrKreditUcty[i])
                increaseUctyVer()
                uctySuborK.close()
                uctyLockSuborK.close()
                os.remove(pathUctyLock)     

def increasePaywallVer():
    tempFilePayVer = open(pathTransakciePaywallVerzia, "r+")
    tempNum = int(tempFilePayVer.readline().strip())
    tempFilePayVer.seek(0)
    tempFilePayVer.truncate()
    tempFilePayVer.write(str(tempNum+1))
    tempFilePayVer.close()

def increaseTransakcieUctyVer():
    tempFileTUVer = open(pathTransakcieUctyVerzia, "r+")
    tempNum2 = int(tempFileTUVer.readline().strip())
    tempFileTUVer.seek(0)
    tempFileTUVer.truncate()
    tempFileTUVer.write(str(tempNum2+1))
    tempFileTUVer.close()

def increaseTransakcieKartyVer():
    tempFileTKVer = open(pathTransakcieKartyVerzia, "r+")
    tempNum3 = int(tempFileTKVer.readline().strip())
    tempFileTKVer.seek(0)
    tempFileTKVer.truncate()
    tempFileTKVer.write(str(tempNum3+1))
    tempFileTKVer.close()

def increaseUctyVer():
    tempFileUctyVer = open(pathUctyVerzia, "r+")
    tempNum4 = int(tempFileUctyVer.readline().strip())
    tempFileUctyVer.seek(0)
    tempFileUctyVer.truncate()
    tempFileUctyVer.write(str(tempNum4+1))
    tempFileUctyVer.close()
    
def increaseKartyVer():
    tempFileKartyVer = open(pathKartyVerzia,"r+")
    tempNum5 = int(tempFileKartyVer.readline().strip())
    tempFileKartyVer.seek(0)
    tempFileKartyVer.truncate()
    tempFileKartyVer.write(str(tempNum5+1))
    tempFileKartyVer.close()
    
canvas.bind('<Button-1>', validateAll)
menuScreen()
