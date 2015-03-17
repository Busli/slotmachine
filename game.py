from tkinter import *
from random import randint

class game:

    def __init__(self, master):
        self.master = master
        self.chosenColor = ''
        self.points = 0
        self.createLayout()
        self.randomColorGenerator()

    def createLayout(self):
        Label(self.master, text="I want to play a game").pack()

        self.frame = Frame(self.master, height=20, bd=1)
        self.frame.pack(fill=X, padx=5, pady=5)

        redButton = Button(self.frame, text="red", command=lambda id_btn='red': self.btn_click(id_btn), background="red", activebackground="#fff")
        redButton.pack({'fill': 'x'})
        blueButton = Button(self.frame, text="Blue", command=lambda id_btn='blue': self.btn_click(id_btn), background="blue", activebackground="#fff")
        blueButton.pack({'fill': 'x'})
        greenButton = Button(self.frame, text="green", command=lambda id_btn='green': self.btn_click(id_btn), background="green", activebackground="#fff")
        greenButton.pack({'fill': 'x'})

        self.makeScoreLabel(self.points)

    def makeScoreLabel(self, score):
        self.variable = StringVar()
        self.variable.set('Stig: ')
        self.stigPlaceholder = Label(self.frame, textvariable=self.variable).pack()
        
        self.stig = StringVar()
        self.stig.set(str(self.points))
        self.stigLabel = Label(self.frame, textvariable=self.stig).pack()

    def randomColorGenerator(self):
        rand = randint(0,2)

        if (rand == 0):
            self.chosenColor = 'red'
            print ('Right color: red')
        elif (rand == 1):
            self.choseColor = 'blue'
            print ('Right color: blue')
        elif (rand == 2):
            self.chosenColor = 'green'
            print ('Right color: green')
        else:
            print('Error choosing a color!')
    
    def btn_click(self, id_btn):
        if (id_btn == self.chosenColor):
            print ("You have chosen the right color! Try again.")
            self.chosenColor = ''
            self.randomColorGenerator()
        else:
            print("You chose the wrong color! Try again.")
            self.chosenColor = ''
            self.randomColorGenerator()

def main():
    root = Tk()
    root.title('Game of thrones')
    myGame = game(root)
    root.mainloop()

if (__name__ == '__main__'):
    main()
