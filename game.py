"""
TODO:
- Láta notanda vita þegar hann er buinn að gera "Cash out"

- Þegar maður gerir cash out kemur pop up gluggi sem leyfir þér að velja áfengistegund
- Mismunandi verð á þeim

- Lækka verðið á drykkjunum
- Setja quit takka
- Hvernig á að meðhöndla þegar viðkomandi er búinn að gera cash out

- Tjekka hvort öll þessi message eru ekki rett logic séð
- Er hægt að birta/taka burt þessi message á betri hátt?

- Taka GUI i gegn

Þriðji leikurinn myndi vera slotmachine leikur, einföld utgáfa
"""

from tkinter import *
from random import randint

class scoreSystem:

    def __init__(self):
        # Hvernig er best að taka við merkinu fra Arduino?
        self.playerScore = 0

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

    def cashout(self):
        print('Trying to cash out...')
        if(self.playerScore > 0):
            print('You have successfully cashed out!')
            self.playerScore = 0
            self.gameMenu.updateScore()
        elif(self.playerScore == 0):
            print('Not enough credit to cash out...')

#------------------------------------------------------------------

class cashOut:

    def __init__(self, master, scoreSystem):
        self.master = master
        self.scoreSystem = scoreSystem
        self.createLayout()

    def createLayout(self):
        def key(event):
            self.handleKeyboardEvent(event.char)

        self.frame = Frame(self.master, height=20, bd=1)
        self.frame.bind("<Key>", key)
        self.frame.focus_set()
        self.frame.place(relx=.5, rely=.5, anchor="c")

        Label(self.frame, text="You are cashing out, choose your poison", font=(20)).pack()

        btnBadAlcohol = Button(self.frame, text="Bad alcohol: 100", command=lambda id_btn='bad': self.btn_click(id_btn), font=(20))
        btnBadAlcohol.pack({'fill': 'x'})
        btnGoodAlcohol = Button(self.frame, text="Good alcohol: 200", command=lambda id_btn='good': self.btn_click(id_btn), font=(20))
        btnGoodAlcohol.pack({'fill': 'x'})

    def btn_click(self, btn):
        # Notandi getur átt efni á slæmu áfengi en ekki góðu
        # gera tjekk svo notanadi geti ekki keypt vitlaust
        if(btn == 'bad'):
            # kostar 300
            # Hér er verið að reyna að kaupa slæmt áfengi
            # Her fer dælan i gang
            print('Bad alcohol...')
        elif(btn == 'good'):
            # kostar 500
            # Hér er verið að reyna að kaupa gott áfengi
            # Hér fer dælan i gang
            print('Good alcohol...')

    def handleKeyboardEvent(self, key):
        if(key == '1'):
            self.btn_click('bad')
        elif(key == '2'):
            self.btn_click('good')
        else:
            print('Could not find button')

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
        
        self.frame = Frame(self.master, height=20, bd=1)
        self.frame.bind("<Key>", key)
        self.frame.focus_set()
        self.frame.place(relx=.5, rely=.5, anchor="c")

        Label(self.frame, text="I want to play a game", font=(20)).pack()

        # Colord buttons 
        redButton = Button(self.frame, text="Red: Press 1", command=lambda id_btn='red': self.btn_click(id_btn), background="red", activebackground="#fff", font=(20), fg="white")
        redButton.pack({'fill': 'x'})
        blueButton = Button(self.frame, text="Blue: Press 2", command=lambda id_btn='blue': self.btn_click(id_btn), background="blue", activebackground="#fff", font=(20), fg="white")
        blueButton.pack({'fill': 'x'})
        greenButton = Button(self.frame, text="Green: Press 3", command=lambda id_btn='green': self.btn_click(id_btn), background="green", activebackground="#fff", font=(20), fg="white")
        greenButton.pack({'fill': 'x'})

        self.makeScoreLabel()

    def makeScoreLabel(self):
        self.stigPlaceholder = Label(self.frame, text="Current credit: ", font=(20)).pack(side=LEFT)

        # StringVar() til að geta update-að label dynamicly
        self.credits = StringVar()
        self.credits.set(self.currentCredit)
        self.stigLabel = Label(self.frame, textvariable=self.credits, font=(20)).pack(side=LEFT)

        quitButton = Button(self.frame, text="Quit: Press q", command=lambda id_btn='quit': self.btn_click(id_btn), font=(20))
        quitButton.pack()
        
        self.message = StringVar()
        self.message.set("")
        self.messageLabel = Label(self.frame, textvariable=self.message, font=(20)).pack(side=LEFT)
        
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
        
        self.frame = Frame(self.master, height=20, bd=1)
        self.frame.bind("<Key>", key)
        self.frame.focus_set()
        self.frame.place(relx=.5, rely=.5, anchor="c")

        Label(self.frame, text="I want to play a game", font=(20)).pack()

        # Colord buttons 
        oneButton = Button(self.frame, text="1: Press 1", command=lambda id_btn='1': self.btn_click(id_btn), font=(20))
        oneButton.pack({'fill': 'x'})
        twoButton = Button(self.frame, text="2: Press 2", command=lambda id_btn='2': self.btn_click(id_btn), font=(20))
        twoButton.pack({'fill': 'x'})
        threeButton = Button(self.frame, text="3: Press 3", command=lambda id_btn='3': self.btn_click(id_btn), font=(20))
        threeButton.pack({'fill': 'x'})

        self.makeScoreLabel()

    def makeScoreLabel(self):
        self.stigPlaceholder = Label(self.frame, text="Current credit: ", font=(20)).pack(side=LEFT)

        # StringVar() til að geta update-að label dynamicly
        self.credits = StringVar()
        self.credits.set(self.currentCredit)
        self.stigLabel = Label(self.frame, textvariable=self.credits, font=(20)).pack(side=LEFT)

        quitButton = Button(self.frame, text="Quit: Press q", command=lambda id_btn="q": self.btn_click(id_btn), font=(20))
        quitButton.pack()

        self.message = StringVar()
        self.message.set("")
        self.messageLabel = Label(self.frame, textvariable=self.message, font=(20)).pack(side=LEFT)

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
        elif(key == 'c' or key == 'C'):
            self.btn_click("c")


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
        
        self.frame = Frame(self.master, bd=1)
        self.frame.bind("<Key>", key)
        # Gefa frame focus til að geta notað lyklaborðið
        self.frame.focus_set()
        self.frame.place(relx=.5, rely=.5, anchor="c")
        Label(self.frame, text="Choose a game", font=(20)).pack()

        btnColorGame = Button(self.frame, text="Play color game: Press 1", command=lambda id_btn="color": self.playGame(id_btn), font=(20))
        btnColorGame.pack({'fill': 'x'})

        btnNumberGame = Button(self.frame, text="Play number game: Press 2", command=lambda id_btn="number": self.playGame(id_btn), font=(20))
        btnNumberGame.pack({'fill': 'x'})

        btnCashOut = Button(self.frame, text="Cash out: Press c", command=lambda id_btn="c": self.playGame(id_btn), font=(20))
        btnCashOut.pack({'fill': 'x'})

        Label(self.frame, text="Current credit: ", font=(20)).pack(side=LEFT)
        self.credit = StringVar()
        self.credit.set(self.score)
        self.currentCreditLabel = Label(self.frame, textvariable=self.credit, font=(20))
        self.currentCreditLabel.pack(side=LEFT)

        self.message = StringVar()
        self.message.set("")
        self.messageLabel = Label(self.frame, textvariable=self.message, font=(20)).pack(side=LEFT)

    def playGame(self, btn):
        if(btn == "color"):
            print('You have chosen the color game!')
            # open color game
            self.colorWindow = Toplevel()
            self.colorWindow.attributes('-fullscreen', True)
            guessTheColor(self.colorWindow, self.scoreSystem)
        elif(btn == "number"):
            print('You have chosen the number game!')
            # open number game
            self.numberWindow = Toplevel()
            self.numberWindow.attributes('-fullscreen', True)
            guessTheNumber(self.numberWindow, self.scoreSystem)
        elif(btn == "c"):
            if(self.scoreSystem.getScore() <= 100):
                self.updateMessageLabel('write')
                return
            elif(self.scoreSystem.getScore() >= 200):
                self.cashoutWindow = Toplevel()
                self.cashoutWindow.attributes('-fullscreen', True)
                cashOut(self.cashoutWindow, self.scoreSystem)
        else:
            print('Error, could not open game')

    def handleKeyboardEvent(self, key):
        print(key)
        if(key == '1'):
            self.playGame("color")
        elif(key == '2'):
            self.playGame("number")
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
    myScoreSystem = scoreSystem()
    root.title('Game of thrones')
    gameMenu = mainMenu(root, myScoreSystem)
    myScoreSystem.bindGameMenuLabel(gameMenu)
    root.mainloop()

if (__name__ == '__main__'):
    main()
