"""
TODO:
- Background image til að gera þetta meira cool?
- Einhverjar skemmtilegar visual breytingar a GUI-inu

- Þriðji leikurinn myndi vera slotmachine leikur, einföld utgáfa
"""

from tkinter import *
from random import randint
import slotmachine

class scoreSystem:

    def __init__(self):
        self.playerScore = 0
        # self.userCreditInsert()

    def updateScore(self, plusMinus):
        if plusMinus == 1:
            self.playerScore += 100
        elif plusMinus == 0 and self.playerScore is not 0:
            self.playerScore -= 100

        self.gameMenu.updateScore()

    def getScore(self):
        return self.playerScore

    def bindGameMenuLabel(self, gameMenu):
        self.gameMenu = gameMenu

    def cashout(self, ammount):
        print('Trying to cash out...')
        if(self.playerScore > 0):
            print('You have successfully cashed out!')
            self.playerScore -= ammount
            self.gameMenu.updateScore()
        elif(self.playerScore == 0):
            print('Not enough credit to cash out...')

    def userCreditInsert(self):
        # Hér verður tekið inn merkið frá Arduino og unnið úr því
        # Hvernig er best að láta RPi hlusta eftir high merki
        print('I received a signlal!')

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
        self.frame.grid(row=0, padx=700, pady=370)

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
                # self.pumpAlcohol(1)
                self.updateScoreLabel()
                self.updateMessageLabel('buy')
            else:
                self.updateMessageLabel('nobuy')
        elif(btn == 'good'):
            if(self.scoreSystem.getScore() >= 200):
                print('You bought good alcohol...')
                self.scoreSystem.cashout(200)
                # self.pumpAlcohol(2)
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
        else:
            print('Could not find button')

    def updateMessageLabel(self, action):
        if(action == 'buy'):
            self.message.set("You have bought a shot!")
        elif(action == 'nobuy'):
            self.message.set("Not enough credit")

    def updateScoreLabel(self):
        self.credit.set(self.scoreSystem.getScore())

    def pumpAlcohol(self, pumpNumber):
        # Hér verður sent út merki til að dæla réttu áfengi
        print('Pump number is: ' + str(pumpNumber))

#------------------------------------------------------------------

class guessTheColor:

    def __init__(self, master, scoreSystem):
        self.master = master
        self.scoreSystem = scoreSystem
        self.currentCredit = self.scoreSystem.getScore()
        self.chosenColor = ''
        self.randomColorGenerator()
        self.createLayout()
        
    def createLayout(self):

        def key(event):
            self.handleKeyboardEvent(event.char)

        self.frame = Frame(self.master, bd=1, width=200, height=200)
        self.frame.bind("<Key>", key)
        self.frame.focus_set()
        self.frame.grid(row=0, padx=700, pady=370)

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
        self.credits = StringVar()
        self.credits.set(self.currentCredit)
        self.stigLabel = Label(self.frame, textvariable=self.credits, font=(20)).grid(row=4, column=1, sticky=W)

        quitButton = Button(self.frame, text="Quit: Press q", command=lambda id_btn='quit': self.btn_click(id_btn), font=(20))
        quitButton.grid(row=5, sticky=W)
        
        self.message = StringVar()
        self.message.set("")
        self.messageLabel = Label(self.frame, textvariable=self.message, font=(20)).grid(row=6, sticky=W)
        
    def randomColorGenerator(self):
        rand = randint(0,2)

        if (rand == 0):
            self.chosenColor = 'red'
            print ('Right color: red')
        elif (rand == 1):
            self.chosenColor = 'blue'
            print ('Right color: blue')
        elif (rand == 2):
            self.chosenColor = 'green'
            print ('Right color: green')
        else:
            print('Error choosing a color!')
        
    
    def btn_click(self, btn):
        if (btn == self.chosenColor):
            print ("You have chosen the right color! Try again.")
            print('------------')
            self.updateMessageLabel('write', 'right')
            self.scoreSystem.updateScore(1)
            self.currentCredit = self.scoreSystem.getScore()
            self.updateScore()
            self.chosenColor = ''
            self.randomColorGenerator()
        elif (btn == 'q'):
            self.updateMessageLabel('clear', None)
            self.master.destroy()
        else:
            print("You chose the wrong color! Try again.")
            print('------------')
            self.updateMessageLabel('write', 'wrong')
            self.scoreSystem.updateScore(0)
            self.currentCredit = self.scoreSystem.getScore()
            self.updateScore()
            self.chosenColor = ''
            self.randomColorGenerator()

    def updateScore(self):
        self.credits.set(str(self.currentCredit))

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
        elif(key == 'c' or key == 'C'):
            self.btn_click("c")
        else:
            print('Could not find button')

#------------------------------------------------------------------

class guessTheNumber:

    def __init__(self, master, scoreSystem):
        self.master = master
        self.scoreSystem = scoreSystem
        self.currentCredit = self.scoreSystem.getScore()
        self.chosenNumber = ''
        self.randomNumberGenerator()
        self.createLayout()
        
    def createLayout(self):

        def key(event):
            self.handleKeyboardEvent(event.char)
        
        self.frame = Frame(self.master, bd=1, width=200, height=200)
        self.frame.bind("<Key>", key)
        self.frame.focus_set()
        self.frame.grid(row=0, padx=700, pady=370)

        Label(self.frame, text="I want to play a game", font=(20)).grid(row=0, sticky=W)

        # Colord buttons 
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
        self.credits = StringVar()
        self.credits.set(self.currentCredit)
        self.stigLabel = Label(self.frame, textvariable=self.credits, font=(20)).grid(row=4, column=1, sticky=W)

        quitButton = Button(self.frame, text="Quit: Press q", command=lambda id_btn="q": self.btn_click(id_btn), font=(20))
        quitButton.grid(row=5, sticky=W)

        self.message = StringVar()
        self.message.set("")
        self.messageLabel = Label(self.frame, textvariable=self.message, font=(20)).grid(row=6, sticky=W)

    def randomNumberGenerator(self):
        rand = randint(1,3)

        if (rand == 1):
            self.chosenNumber = '1'
            print ('Right number: 1')
        elif (rand == 2):
            self.chosenNumber = '2'
            print ('Right number: 2')
        elif (rand == 3):
            self.chosenNumber = '3'
            print ('Right number: 3')
        else:
            print('Error choosing a number!')
        
    
    def btn_click(self, btn):
        if (btn == self.chosenNumber):
            print ("You have chosen the right number! Try again.")
            print('------------')
            self.updateMessageLabel('write', 'right')
            self.scoreSystem.updateScore(1)
            self.currentCredit = self.scoreSystem.getScore()
            self.updateScore()
            self.chosenNumber = ''
            self.randomNumberGenerator()
        elif (btn == 'q'):
            self.master.destroy()
        else:
            print("You chose the wrong number! Try again.")
            print('------------')
            self.updateMessageLabel('write', 'wrong')
            self.scoreSystem.updateScore(0)
            self.currentCredit = self.scoreSystem.getScore()
            self.updateScore()
            self.chosenNumber = ''
            self.randomNumberGenerator()

    def updateScore(self):
        self.credits.set(str(self.currentCredit))

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

#------------------------------------------------------------------

class slotmachineGame:
#- Þarf að meðhöndla keyboard event
#- Þarf að starta leiknum
#- Þarf að breyta symbols
#- Þarf að hugsa hvernig a að gera þetta GUI
#- Breyta stigagjöf þannig þetta gefi lika þegar 2 réttir

    def __init__(self, master, scoreSystem):
        self.master = master
        self.scoreSystem = scoreSystem
        self.createLayout()

    def createLayout(self):
        def key(event):
            self.handleKeyboardEvent(event.char)
        
        self.frame = Frame(self.master, bd=1, width=200, height=200)
        self.frame.bind("<Key>", key)
        # Gefa frame focus til að geta notað lyklaborðið
        self.frame.focus_set()
        self.frame.grid(row=0, padx=700, pady=370)

        Label(self.frame, text="Welcome to the slotmachine!", font=(20)).grid(row=0, sticky=W)

        btnSpinTheWheel = Button(self.frame, text="Spin the wheel! : Press 1", command=lambda: self.spinTheWheel(), font=(20))
        btnSpinTheWheel.grid(row=1, sticky=N+S+E+W, columnspan=2)

        self.displayText = Text(self.frame, height=1, width=2)
        self.displayText.grid(row=2, sticky=N+S+E+W, columnspan=2)

        self.stigPlaceholder = Label(self.frame, text="Current credit: ", font=(20)).grid(row=3, column=0, sticky=W)
        # StringVar() til að geta update-að label dynamicly
        self.credits = StringVar()
        self.credits.set(self.scoreSystem.getScore())
        self.stigLabel = Label(self.frame, textvariable=self.credits, font=(20)).grid(row=3, column=1, sticky=W)

        quitButton = Button(self.frame, text="Quit: Press q", command=lambda: self.master.destroy(), font=(20))
        quitButton.grid(row=4, sticky=W)

        self.message = StringVar()
        self.message.set("")
        self.messageLabel = Label(self.frame, textvariable=self.message, font=(20)).grid(row=5, sticky=W)

    def spinTheWheel(self):
        #slotmachine.main()
        self.updateMessageLabel(None)

    def handleKeyboardEvent(self, key):
        if(key == '1'):
            self.spinTheWheel()
        elif(key == 'q' or key == 'Q'):
            self.master.destroy()

    def updateScoreLabel(self):
        self.credits.set(self.scoreSystem.getScore())

    def updateMessageLabel(self, action):
        #self.message.set(<myMessage>)
        if(action == None):
            self.message.set("You are spinning the wheel!")
            self.insertText("You are spinning the wheel!")

    def insertText(self, text):
        self.displayText.insert(END, text)

#------------------------------------------------------------------

class mainMenu:

    def __init__(self, master, scoreSystem):
        self.master = master
        self.scoreSystem = scoreSystem
        self.score = self.scoreSystem.getScore()
        self.createLayout()

    def createLayout(self):
        # Keyboard listener
        def key(event):
            self.handleKeyboardEvent(event.char)
        
        self.frame = Frame(self.master, bd=1, width=200, height=200)
        self.frame.bind("<Key>", key)
        # Gefa frame focus til að geta notað lyklaborðið
        self.frame.focus_set()
        self.frame.grid(row=0, padx=700, pady=370)
        
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
        self.credit = StringVar()
        self.credit.set(self.score)
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
        else:
            print('Error, could not open game')

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
        else:
            print('Failed to load game...')

    def updateScore(self):
        self.score = self.scoreSystem.getScore()
        self.credit.set(self.score)

    def updateMessageLabel(self, action):
        if(action == 'write'):
            self.message.set("Not enough credit")
        elif(action == 'clear'):
            self.message.set("")

#------------------------------------------------------------------

def main():
    root = Tk()
    root.attributes('-fullscreen', True)
    root.title('Game of thrones')
    myScoreSystem = scoreSystem()
    gameMenu = mainMenu(root, myScoreSystem)
    myScoreSystem.bindGameMenuLabel(gameMenu)
    root.mainloop()

if (__name__ == '__main__'):
    main()
