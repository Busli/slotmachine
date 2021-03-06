from tkinter import *
from random import randint
import RPi.GPIO as GPIO
import serial
import threading
import queue
from utils import Loop, range1, first, sjoin, nl
from time import sleep
import os

# Heldur utan um credit spilara
class scoreSystem:

    def __init__(self):
        self.playerScore = 0

    def updateScore(self, action):
        if action == 1:
            self.playerScore += 100
        elif action == 2:
            self.playerScore += 600
        elif action == 3:
            self.playerScore -= 200
        elif action == 0 and self.playerScore is not 0:
            self.playerScore -= 100

        self.gameMenu.updateScore()

    def getScore(self):
        return self.playerScore

    def bindGameMenuLabel(self, gameMenu):
        self.gameMenu = gameMenu

    def cashout(self, ammount):
        if(self.playerScore > 0):
            self.playerScore -= ammount
            self.gameMenu.updateScore()
        elif(self.playerScore == 0):
            print('Not enough credit to cash out...')

#------------------------------------------------------------------

# Glugginn þegar notandi er að kaupa sér áfengi
class cashOut:

    def __init__(self, master, scoreSystem, gameMenu):
        self.master = master
        self.scoreSystem = scoreSystem
        self.gameMenu = gameMenu
        self.createLayout()

    def createLayout(self):
        def key(event):
            self.handleKeyboardEvent(event.char)

        # Aðal ramminn
        self.frame = Frame(self.master, bd=1, width=200, height=200)
        self.frame.bind("<Key>", key)
        self.frame.focus_set()
        self.frame.grid(row=0, padx=500, pady=370)

        Label(self.frame, text="You are cashing out, choose your poison", font=(20)).grid(row=0, sticky=W)

        btnBadAlcohol = Button(self.frame, text="Bad alcohol: 100", command=lambda id_btn='bad': self.btn_click(id_btn), font=(20))
        btnBadAlcohol.grid(row=1, sticky=N+S+E+W, columnspan=2)
        btnGoodAlcohol = Button(self.frame, text="Good alcohol: 200", command=lambda id_btn='good': self.btn_click(id_btn), font=(20))
        btnGoodAlcohol.grid(row=2, sticky=N+S+E+W, columnspan=2)

        Label(self.frame, text="Current credit: ", font=(20)).grid(row=3, column=0, sticky=W)
        self.credit = StringVar()
        self.credit.set(self.scoreSystem.getScore())
        self.currentCreditLabel = Label(self.frame, textvariable=self.credit, font=(20))
        self.currentCreditLabel.grid(row=3, column=1, sticky=W)

        quitButton = Button(self.frame, text="Quit: Press q", command=lambda id_btn='q': self.btn_click(id_btn), font=(20))
        quitButton.grid(row=4, sticky=W)

        self.message = StringVar()
        self.message.set("")
        self.messageLabel = Label(self.frame, textvariable=self.message, font=(20)).grid(row=5, sticky=W)

    def btn_click(self, btn):
        if(btn == 'bad'):
            if(self.scoreSystem.getScore() >= 100):
                print('You bought bad alcohol...')
                self.scoreSystem.cashout(100)
                self.pumpAlcohol(1)
                self.updateScoreLabel()
                self.updateMessageLabel('buy')
            else:
                self.updateMessageLabel('nobuy')
        elif(btn == 'good'):
            if(self.scoreSystem.getScore() >= 200):
                print('You bought good alcohol...')
                self.scoreSystem.cashout(200)
                self.pumpAlcohol(2)
                self.updateScoreLabel()
                self.updateMessageLabel('buy')
            else:
                self.updateMessageLabel('nobuy')
        elif(btn == 'q'):
            self.master.destroy()
        
    def handleKeyboardEvent(self, key):
        if(key == '1'):
            self.btn_click('bad')
        elif(key == '2'):
            self.btn_click('good')
        elif(key == 'q' or key == 'Q'):
            self.btn_click('q')

    def updateMessageLabel(self, action):
        if(action == 'buy'):
            self.message.set("You have bought a shot!")
        elif(action == 'nobuy'):
            self.message.set("Not enough credit")

    def updateScoreLabel(self):
        self.credit.set(self.scoreSystem.getScore())

    def pumpAlcohol(self, pumpNumber):
        # Hér verður sent út merki til að dæla réttu áfengi
        if(pumpNumber == 1):
            #self.ser.write('2')
            os.system("python runPump1.py")
        elif(pumpNumber == 2):
            #self.ser.write('4')
            os.system("python runPump2.py")
        else:
            print("Invalid pump")

#------------------------------------------------------------------

class guessTheColor:

    def __init__(self, master, scoreSystem):
        self.master = master
        self.scoreSystem = scoreSystem
        self.createLayout()
        
    def createLayout(self):

        def key(event):
            self.handleKeyboardEvent(event.char)

        self.frame = Frame(self.master, bd=1, width=200, height=200)
        self.frame.bind("<Key>", key)
        self.frame.focus_set()
        self.frame.grid(row=0, padx=500, pady=370)

        Label(self.frame, text="I want to play a game", font=(20)).grid(row=0, sticky=W)

        # Colord buttons 
        redButton = Button(self.frame, text="Red: Press 1", command=lambda id_btn='red': self.btn_click(id_btn), background="red", activebackground="#fff", font=(20), fg="white")
        redButton.grid(row=1, sticky=N+S+E+W, columnspan=2)
        blueButton = Button(self.frame, text="Blue: Press 2", command=lambda id_btn='blue': self.btn_click(id_btn), background="blue", activebackground="#fff", font=(20), fg="white")
        blueButton.grid(row=2, sticky=N+S+E+W,columnspan=2)
        greenButton = Button(self.frame, text="Green: Press 3", command=lambda id_btn='green': self.btn_click(id_btn), background="green", activebackground="#fff", font=(20), fg="white")
        greenButton.grid(row=3, sticky=N+S+E+W,columnspan=2)

        self.makeScoreLabel()

    def makeScoreLabel(self):
        self.stigPlaceholder = Label(self.frame, text="Current credit: ", font=(20)).grid(row=4, column=0, sticky=W)

        # StringVar() til að geta update-að label dynamicly
        self.credits = IntVar()
        self.credits.set(self.scoreSystem.getScore())
        self.stigLabel = Label(self.frame, textvariable=self.credits, font=(20)).grid(row=4, column=1, sticky=W)

        quitButton = Button(self.frame, text="Quit: Press q", command=lambda id_btn='quit': self.btn_click(id_btn), font=(20))
        quitButton.grid(row=5, sticky=W)
        
        self.message = StringVar()
        self.message.set("")
        self.messageLabel = Label(self.frame, textvariable=self.message, font=(20)).grid(row=6, sticky=W)
            
    def btn_click(self, btn):
        if(btn == 'm'):
            self.scoreSystem.updateScore(2)
            self.updateScore()
        elif(self.scoreSystem.getScore() is 0):
            self.message.set("Not enough credit")
            return
        odds = randint(1,10)
        if (btn == 'q'):
            self.updateMessageLabel('clear', None)
            self.master.destroy()
        elif(odds < 5):
            # You win
            self.updateMessageLabel('write', 'right')
            self.scoreSystem.updateScore(1)
            self.updateScore()
        elif(odds > 5):
            # You loose
            self.updateMessageLabel('write', 'wrong')
            self.scoreSystem.updateScore(0)
            self.updateScore()

    def updateScore(self):
        self.credits.set(self.scoreSystem.getScore())

    def updateMessageLabel(self, action, msg):
        if(action == 'write'):
            self.message.set("You chose the " + msg + " color!")
        elif(action == 'clear'):
            self.message.set("")
    
    def handleKeyboardEvent(self, key):
        # red
        if(key == '1'):
            self.btn_click('red')
        # blue
        elif(key == '2'):
            self.btn_click('blue')
        # green
        elif(key == '3'):
            self.btn_click('green')
        elif(key == 'q' or key == 'Q'):
            self.btn_click('q')
        elif(key == 'm' or key == 'M'):
            self.btn_click('m')

#------------------------------------------------------------------

class guessTheNumber:

    def __init__(self, master, scoreSystem):
        self.master = master
        self.scoreSystem = scoreSystem
        self.createLayout()
        
    def createLayout(self):

        def key(event):
            self.handleKeyboardEvent(event.char)
        
        self.frame = Frame(self.master, bd=1, width=200, height=200)
        self.frame.bind("<Key>", key)
        self.frame.focus_set()
        self.frame.grid(row=0, padx=500, pady=370)

        Label(self.frame, text="I want to play a game", font=(20)).grid(row=0, sticky=W)

        # Number buttons 
        oneButton = Button(self.frame, text="1: Press 1", command=lambda id_btn='1': self.btn_click(id_btn), font=(20))
        oneButton.grid(row=1, sticky=N+S+E+W, columnspan=2)
        twoButton = Button(self.frame, text="2: Press 2", command=lambda id_btn='2': self.btn_click(id_btn), font=(20))
        twoButton.grid(row=2, sticky=N+S+E+W, columnspan=2)
        threeButton = Button(self.frame, text="3: Press 3", command=lambda id_btn='3': self.btn_click(id_btn), font=(20))
        threeButton.grid(row=3, sticky=N+S+E+W, columnspan=2)

        self.makeScoreLabel()

    def makeScoreLabel(self):
        self.stigPlaceholder = Label(self.frame, text="Current credit: ", font=(20)).grid(row=4, column=0, sticky=W)

        # StringVar() til að geta update-að label dynamicly
        self.credits = IntVar()
        self.credits.set(self.scoreSystem.getScore())
        self.stigLabel = Label(self.frame, textvariable=self.credits, font=(20)).grid(row=4, column=1, sticky=W)

        quitButton = Button(self.frame, text="Quit: Press q", command=lambda id_btn="q": self.btn_click(id_btn), font=(20))
        quitButton.grid(row=5, sticky=W)

        self.message = StringVar()
        self.message.set("")
        self.messageLabel = Label(self.frame, textvariable=self.message, font=(20)).grid(row=6, sticky=W)
    
    def btn_click(self, btn):
        if(btn == 'm'):
            self.scoreSystem.updateScore(2)
            self.updateScore()
        elif(self.scoreSystem.getScore() is 0):
            self.message.set("Not enough credit")
            return
        odds = randint(1,10)
        if (btn == 'q'):
            self.master.destroy()
        elif(odds < 5):
            # You win
            self.updateMessageLabel('write', 'right')
            self.scoreSystem.updateScore(1)
            self.updateScore()
        elif(odds > 5):
            # You loose
            self.updateMessageLabel('write', 'wrong')
            self.scoreSystem.updateScore(0)
            self.updateScore()

    def updateScore(self):
        self.credits.set(self.scoreSystem.getScore())

    def updateMessageLabel(self, action, msg):
        if(action == 'write'):
            self.message.set("You chose the " + msg + " number!")
        elif(action == 'clear'):
            self.message.set("")

    def handleKeyboardEvent(self, key):
        if(key == '1'):
            self.btn_click('1')
        elif(key == '2'):
            self.btn_click('2')
        elif(key == '3'):
            self.btn_click('3')
        elif(key == 'q' or key == 'Q'):
            self.btn_click('q')
        elif(key == 'm' or key == 'M'):
            self.btn_click('m')
            
#----------------------------------------------------------------------------------------

class Reel(object):
    def __init__(self, rotations, max_cycle, symbols):
        self.reel      = Loop(symbols.keys(), name="symbol")
        self.rotations = rotations
        self.max_cycle = max_cycle

    def symbol(self, cycle=0):
        if cycle and cycle <= self.max_cycle:
            self.rotate()
        return self.reel.symbol

    def rotate(self): self.reel.next(self.rotations)

#------------------------------------------------------------------

class slotmachineGame:

    def __init__(self, master, scoreSystem):
        self.master = master
        self.scoreSystem = scoreSystem
        self.setupGame()
        self.createLayout()

    def setupGame(self):
        self.num_reels  = 3
        self.pause_time = 0.05
        self.first_stop = 10     # stop first reel
        self.reel_delay = 15     # range of delay to stop each reel
        self.winmsg     = "You've won!! Collect your prize : %d"

        self.symbols = {
            '✿': 500,
            '❖': 1000,
            '✬': 2500,
         }
    
    def createLayout(self):
        def key(event):
            self.handleKeyboardEvent(event.char)
        
        self.frame = Frame(self.master, bd=1, width=200, height=200)
        self.frame.bind("<Key>", key)
        # Gefa frame focus til að geta notað lyklaborðið
        self.frame.focus_set()
        self.frame.grid(row=0, padx=500, pady=370)

        Label(self.frame, text="Welcome to the slotmachine!", font=(20)).grid(row=0, sticky=W)

        btnSpinTheWheel = Button(self.frame, text="Spin the wheel! : Press 1", command=lambda: self.spinTheWheel(), font=(20))
        btnSpinTheWheel.grid(row=1, sticky=N+S+E+W, columnspan=2)

        self.displayText = Text(self.frame, height=1, width=2)
        self.displayText.grid(row=2, sticky=N+S+E+W, columnspan=2)

        self.stigPlaceholder = Label(self.frame, text="Current credit: ", font=(20)).grid(row=3, column=0, sticky=W)
        # StringVar() til að geta update-að label dynamicly
        self.credits = IntVar()
        self.credits.set(self.scoreSystem.getScore())
        self.stigLabel = Label(self.frame, textvariable=self.credits, font=(20)).grid(row=3, column=1, sticky=W)

        quitButton = Button(self.frame, text="Quit: Press q", command=lambda: self.master.destroy(), font=(20))
        quitButton.grid(row=4, sticky=W)

        self.message = StringVar()
        self.message.set("")
        self.messageLabel = Label(self.frame, textvariable=self.message, font=(20)).grid(row=5, sticky=W)

    def spinTheWheel(self):
        if(self.scoreSystem.getScore() == 0):
            self.message.set("Not enough credit")
        else:
            # Message-ið er prentað eftir að buið er að keyra leikinn
            # þarf kannski að gera thread
            self.updateMessageLabel('write', "The wheel has stopped!")
            output = self.run(self.pause_time)
            self.insertText(output[0])
            self.checkForVictory(output[1])

    def checkForVictory(self, fromSlot):
        if(fromSlot == 0):
            self.updateMessageLabel('write', "You lost! Try again")
            self.scoreSystem.updateScore(3)
            self.updateScoreLabel()
        elif(fromSlot > 0):
            self.updateMessageLabel('write', "You won!!!")
            self.scoreSystem.updateScore(2)
            self.updateScoreLabel()

    def run(self, pause_time, display=True):
        rotations    = [randint(1,4) for _ in range(self.num_reels)]    # reel rotations per cycle
        rd           = self.reel_delay
        total_cycles = [randint(x, x+rd) for x in range(self.first_stop, self.first_stop + rd*self.num_reels, rd)]

        reels        = [Reel(rotations, max_cycle, self.symbols) for rotations, max_cycle in zip(rotations, total_cycles)]

        for cycle in range1(max(total_cycles)):
            line = sjoin( [reel.symbol(cycle) for reel in reels] )
            # hér er verið að reyna að prenta
            self.insertText(line)
            if display: (nl*5, line)
            sleep(pause_time)

        return self.done(reels, display, line)

    def done(self, reels, display, line):
        # Hér þarf kannski að gefa vinning fyrir 2 rétta
        # Þá myndir 2 rettir vera upphæðin sem var bettað, 3 rettir væri eitthvað meira
        S      = [r.symbol() for r in reels]
        won    = bool(len(set(S)) == 1)
        amount = self.symbols[first(S)] if won else 0
        
        if won and display:
            #if won:
            print(self.winmsg % self.symbols[first(S)])
        return line, amount

    def handleKeyboardEvent(self, key):
        if(key == '1'):
            self.spinTheWheel()
        elif(key == 'q' or key == 'Q'):
            self.master.destroy()
        elif(key == 'm' or key == 'M'):
            self.scoreSystem.updateScore(2)
            self.updateScoreLabel()

    def updateScoreLabel(self):
        self.credits.set(self.scoreSystem.getScore())

    def updateMessageLabel(self, action, msg):
        if(action == 'write'):
            self.message.set(msg)
        elif(action == 'clear'):
            self.message.set("")

    def insertText(self, text):
        self.displayText.delete(1.0, END)
        self.displayText.insert(END, text)

#------------------------------------------------------------------

class mainMenu:

    def __init__(self, master, scoreSystem, queue):
        self.master = master
        self.queue = queue
        self.scoreSystem = scoreSystem
        self.createLayout()

    def createLayout(self):
        # Keyboard listener
        def key(event):
            self.handleKeyboardEvent(event.char)
        
        self.frame = Frame(self.master, bd=1, width=200, height=200)
        self.frame.bind("<Key>", key)
        # Gefa frame focus til að geta notað lyklaborðið
        self.frame.focus_set()
        self.frame.grid(row=0, padx=500, pady=370)
        
        Label(self.frame, text="Choose a game", font=(20)).grid(row=0, sticky=W)

        btnColorGame = Button(self.frame, text="Play color game: Press 1", command=lambda id_btn="color": self.playGame(id_btn), font=(20))
        btnColorGame.grid(row=1, sticky=N+S+E+W, columnspan=2)
        btnNumberGame = Button(self.frame, text="Play number game: Press 2", command=lambda id_btn="number": self.playGame(id_btn), font=(20))
        btnNumberGame.grid(row=2, sticky=N+S+E+W, columnspan=2)
        btnSlotMachineGame = Button(self.frame, text="Play slotmachine game: Press 3", command=lambda id_btn="slotmachine": self.playGame(id_btn), font=(20))
        btnSlotMachineGame.grid(row=3, sticky=N+S+E+W, columnspan=2)
        
        btnCashOut = Button(self.frame, text="Cash out: Press c", command=lambda id_btn="c": self.playGame(id_btn), font=(20))
        btnCashOut.grid(row=4, sticky=N+S+E+W, columnspan=2)

        Label(self.frame, text="Current credit: ", font=(20)).grid(row=5, column=0, sticky=W)
        self.credit = IntVar()
        self.credit.set(self.scoreSystem.getScore())
        self.currentCreditLabel = Label(self.frame, textvariable=self.credit, font=(20))
        self.currentCreditLabel.grid(row=5, column=1, sticky=W)

        self.message = StringVar()
        self.message.set("")
        self.messageLabel = Label(self.frame, textvariable=self.message, font=(20)).grid(row=6, sticky=W)

    def playGame(self, btn):
        if(btn == "color"):
            print('You have chosen the color game!')
            # open color game
            self.colorWindow = Toplevel()
            self.colorWindow.attributes('-fullscreen', True)
            guessTheColor(self.colorWindow, self.scoreSystem)
            self.updateMessageLabel('clear')
        elif(btn == "number"):
            print('You have chosen the number game!')
            # open number game
            self.numberWindow = Toplevel()
            self.numberWindow.attributes('-fullscreen', True)
            guessTheNumber(self.numberWindow, self.scoreSystem)
            self.updateMessageLabel('clear')
        elif(btn == "slotmachine"):
            print('You have chosen the slotmachine game!')
            # open number game
            self.slotmachineWindow = Toplevel()
            self.slotmachineWindow.attributes('-fullscreen', True)
            slotmachineGame(self.slotmachineWindow, self.scoreSystem)
            self.updateMessageLabel('clear')
        elif(btn == "c"):
            # cash outs
            if(self.scoreSystem.getScore() < 100):
                self.updateMessageLabel('write')
                return
            elif(self.scoreSystem.getScore() >= 100):
                self.cashoutWindow = Toplevel()
                self.cashoutWindow.attributes('-fullscreen', True)
                cashOut(self.cashoutWindow, self.scoreSystem, self)

    def handleKeyboardEvent(self, key):
        print(key)
        if(key == '1'):
            self.playGame("color")
        elif(key == '2'):
            self.playGame("number")
        elif(key == '3'):
            self.playGame("slotmachine")
        elif(key == 'c' or key == 'C'):
            self.playGame("c")
        elif(key == 'm' or key == 'M'):
            self.scoreSystem.updateScore(2)
            self.updateScore()

    def updateScore(self):
        self.score = self.scoreSystem.getScore()
        self.credit.set(self.score)

    def updateMessageLabel(self, action):
        if(action == 'write'):
            self.message.set("Not enough credit")
        elif(action == 'clear'):
            self.message.set("")

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        #print("gameMenu: Checking in game queue")
        while self.queue.qsize():
            try:
                print("Trying to update score")
                #print("gameMenu: I iz gunna update teh score")
                #print("gameMenu: queue size is: " + str(self.queue.qsize()))
                self.scoreSystem.updateScore(1)
                self.updateScore()
                self.queue.get()
            except Queue.Empty:
                pass

#------------------------------------------------------------------

class ThreadedClient:

    def __init__(self, master):
        self.master = master
        self.queue = queue.Queue()
        
        # Setup GUI part
        self.myScoreSystem = scoreSystem()
        self.gameMenu = mainMenu(self.master, self.myScoreSystem, self.queue)
        self.myScoreSystem.bindGameMenuLabel(self.gameMenu)
        
        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()
        #self.thread2 = threading.Thread(target=self.workerThread2)
        #self.thread2.start()
        
        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gameMenu.processIncoming()
        if not self.running:
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def workerThread1(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        input = GPIO.input(7)
        while self.running:
            try:
                GPIO.wait_for_edge(7, GPIO.FALLING)
                self.queue.put(1)
            except KeyboardInterrupt:
                GPIO.cleanup

    #def workerThread2(self):
        #self.ser = serial.Serial('/dev/ttyACM0', 9600)
        #while self.running:
            #answer = self.ser.readline()
            #if(answer):
                #self.queue.put(1)

    def endApplication(self):
        self.running = 0
        
#------------------------------------------------------------------

def main():
    root = Tk()
    root.attributes('-fullscreen', True)
    client = ThreadedClient(root) 
    root.mainloop()

if (__name__ == '__main__'):
    main()
