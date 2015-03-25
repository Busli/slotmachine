from tkinter import *
from random import randint

class guessTheColor:

    def __init__(self, master):
        self.master = master
        # Stig leikmanns i leiknum
        self.currentCredit = 0
        self.chosenColor = ''
        self.randomColorGenerator()
        self.createLayout()
        
    def createLayout(self):
        Label(self.master, text="I want to play a game").pack()

        self.frame = Frame(self.master, height=20, bd=1)
        self.frame.pack(fill=X,padx=5, pady=5)

        # Colord buttons 
        redButton = Button(self.frame, text="Red", command=lambda id_btn='red': self.btn_click(id_btn), background="red", activebackground="#fff")
        redButton.pack({'fill': 'x'})
        blueButton = Button(self.frame, text="Blue", command=lambda id_btn='blue': self.btn_click(id_btn), background="blue", activebackground="#fff")
        blueButton.pack({'fill': 'x'})
        greenButton = Button(self.frame, text="Green", command=lambda id_btn='green': self.btn_click(id_btn), background="green", activebackground="#fff")
        greenButton.pack({'fill': 'x'})

        self.makeScoreLabel()

    def makeScoreLabel(self):
        self.variable = StringVar()
        self.variable.set('Stig: ')
        self.stigPlaceholder = Label(self.frame, textvariable=self.variable).pack()

        # StringVar() til að geta update-að label dynamicly
        self.credits = StringVar()
        self.credits.set(self.currentCredit)
        self.stigLabel = Label(self.frame, textvariable=self.credits).pack()

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
        print('------------')
        print('Button has been clicked')
        print('Current color is: ' + self.chosenColor)
        print('User clicked the ' + btn + ' button.')
        if (btn == self.chosenColor):
            print ("You have chosen the right color! Try again.")
            print('------------')
            self.currentCredit += 10
            self.updateScore()
            self.chosenColor = ''
            self.randomColorGenerator()
        else:
            print("You chose the wrong color! Try again.")
            print('------------')
            if(self.currentCredit is not 0):
                self.currentCredit -= 10
            self.updateScore()
            self.chosenColor = ''
            self.randomColorGenerator()

    def updateScore(self):
        self.credits.set(str(self.currentCredit))

#------------------------------------------------------------------

class guessTheNumber:

    def __init__(self, master):
        self.master = master
        self.currentCredit = 0
        self.chosenNumber = ''
        self.randomNumberGenerator()
        self.createLayout()
        
    def createLayout(self):
        Label(self.master, text="I want to play a game").pack()

        self.frame = Frame(self.master, height=20, bd=1)
        self.frame.pack(fill=X,padx=5, pady=5)

        # Colord buttons 
        oneButton = Button(self.frame, text="1", command=lambda id_btn='1': self.btn_click(id_btn))
        oneButton.pack({'fill': 'x'})
        twoButton = Button(self.frame, text="2", command=lambda id_btn='2': self.btn_click(id_btn))
        twoButton.pack({'fill': 'x'})
        threeButton = Button(self.frame, text="3", command=lambda id_btn='3': self.btn_click(id_btn))
        threeButton.pack({'fill': 'x'})

        self.makeScoreLabel()

    def makeScoreLabel(self):
        self.variable = StringVar()
        self.variable.set('Stig: ')
        self.stigPlaceholder = Label(self.frame, textvariable=self.variable).pack(side=LEFT)

        # StringVar() til að geta update-að label dynamicly
        self.credits = StringVar()
        self.credits.set(self.currentCredit)
        self.stigLabel = Label(self.frame, textvariable=self.credits).pack(side=LEFT)

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
        print('------------')
        print('Button has been clicked')
        print('Current color is: ' + self.chosenNumber)
        print('User clicked the ' + btn + ' button.')
        if (btn == self.chosenNumber):
            print ("You have chosen the right number! Try again.")
            print('------------')
            self.currentCredit += 10
            self.updateScore()
            self.chosenNumber = ''
            self.randomNumberGenerator()
        else:
            print("You chose the wrong number! Try again.")
            print('------------')
            if(self.currentCredit is not 0):
                self.currentCredit -= 10
            self.updateScore()
            self.chosenNumber = ''
            self.randomNumberGenerator()

    def updateScore(self):
        self.credits.set(str(self.currentCredit))


#------------------------------------------------------------------

class mainMenu:

    def __init__(self,master):
        self.master = master
        # Spurning um að gera currentCredit hérna til að hægt sé að uppfæra á milli skjáa
        self.createLayout()

    def createLayout(self):
        self.frame = Frame(self.master, height=20, bd=1)
        self.frame.pack(fill=X)
        Label(self.frame, text="Choose a game").pack()

        btnColorGame = Button(self.frame, text="Play color game", command=lambda id_btn="color": self.playGame(id_btn))
        btnColorGame.pack()

        btnNumberGame = Button(self.frame, text="Play number game", command=lambda id_btn="number": self.playGame(id_btn))
        btnNumberGame.pack()

    def playGame(self, btn):
        if(btn == "color"):
            print('You have chosen the color game!')
            # open color game
            self.colorWindow = Toplevel()
            self.colorWindow.title("The color game!")
            guessTheColor(self.colorWindow)
        elif(btn == "number"):
            print('You have chosen the number game!')
            # open number game
            self.numberWindow = Toplevel()
            self.numberWindow.title("The number game!")
            guessTheNumber(self.numberWindow)
        else:
            print('Error, could not open game')

#------------------------------------------------------------------

def main():
    root = Tk()
    root.title('Game of thrones')
    gameMenu = mainMenu(root)
    #myGame = guessTheColor(root)
    #myGame = guessTheNumber(root)
    # Ekki viss um að það þurfi að gera þetta
    # Þetta startar forritinu samt
    root.mainloop()

if (__name__ == '__main__'):
    main()
