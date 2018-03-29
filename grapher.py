from tkinter import *
import pygame, math

white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
green = (0,127,0)
colours = [red,green,blue]

pi = math.pi

#_______________________CLASSES___________________#
class tkWindow():
    def __init__(self, master):
        self.label = Label(master, text = "Equation of graph y = f(x)")
        self.label.pack()

        self.eq = StringVar()
        self.e = Entry(master,textvariable=self.eq,width=25)
        self.e.pack()
        self.e.focus_set()
        
        self.label2 = Label(master, text = "Equation of graph r = g(θ)")
        self.label2.pack()

        self.eq2 = StringVar()
        self.e2 = Entry(master,textvariable=self.eq2,width=25)
        self.e2.pack()
        self.e2.focus_set()
        
        self.b = Button(master,text = "Draw",command = lambda: generateCoordinates(self.e.get(),self.e2.get()))
        self.b.pack()

class App():
    def __init__(self):
        self.screenx = 300
        self.screeny = 300
        self.tickspeed = 20
    def begin(self,equation):
        pygame.init()
        pygame.display.set_caption(equation)
        self.screen = pygame.display.set_mode((self.screenx, self.screeny))
        self.clock = pygame.time.Clock()
    def exitGame(self):
        pygame.quit()
        #quit()
    def getTickSpeed(self):
        return self.tickspeed
    def getClock(self):
        return self.clock
    def getScreen(self):
        return self.screen

class Stack():
    def __init__(self):
        self.array = []
    def push(self,item):
        self.array.append(item)
    def pop(self):
        if not self.isEmpty():
            return self.array.pop(-1)
        else:
            return True
    def isEmpty(self):
        return len(self.array) == 0

#__________________________MAIN STUFF____________________________#
def saveImage():
    root = Tk()
    root.withdraw()
    response = messagebox.askyesno("Save Image","Would you like to save an image of the graphs?")
    root.update()
    if response == True:
        pygame.image.save(app.getScreen(),"graphs.png")
    else:
        return

def events():
    direction = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                saveImage()

def addAxis():
    pygame.draw.line(app.getScreen(), black, (0,app.screeny/2), (app.screenx,app.screeny/2),2)
    pygame.draw.line(app.getScreen(), black, (app.screenx/2,0), (app.screenx/2,app.screeny),2)

def generateCoordinates(equation,equationpolar):
    lines = equation.split(";")
    polarlines = equationpolar.split(";")
    if lines == ['']:
        lines = []
    if polarlines == ['']:
        polarlines = []
    coords = [[] for i in range(len(lines)+len(polarlines))]
    if lines != []:
        for eq in range(len(lines)):
            for x in range(app.screenx * -1,app.screenx):
                try:
                    y = app.screeny-round(evaluateRPN(lines[eq],x/25,'x'))
                    y -= round(app.screeny / 2)
                    x += round(app.screenx / 2)
                    coords[eq].append((x,y))
                except:
                    pass
    if polarlines != []:
        for eq in range(len(polarlines)):
            for i in range(0,2000):
                try:
                    theta = i*pi/500
                    r = round(evaluateRPN(polarlines[eq],theta,'theta'))
                    #print(r,theta)
                    y = round((app.screeny / 2) - (r*math.sin(theta)))
                    x = round((app.screenx / 2) + (r*math.cos(theta)))
                    coords[eq+len(lines)].append((x,y))
                except:
                    pass
    drawGraph(coords,equation)
    
def drawGraph(coords,equation):
    app.begin(equation)
    while True:
        app.getScreen().fill(white)
        addAxis()
        for i in range(len(coords)):
            linecol = colours[i%len(colours)]
            pygame.draw.aalines(app.getScreen(),linecol,False,coords[i],2)
        pygame.display.update()
        app.getClock().tick(app.getTickSpeed())
        response = events()
        if response == False:
            pygame.quit()
            return
            
def main():
    root = Tk()
    myTK = tkWindow(root)
    root.mainloop()

#____________________________MATHS_______________________#
def factorial(n):
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)
                
def evaluateRPN(y,x,variable):
    stack = Stack()
    eq = y.split(" ")
    d_operators = ["+","-","*","/","^"]
    s_operators = ["sin","cos","tan","arcsin","arccos","arctan","!"]
    for i in range(len(eq)):
        if eq[i] == variable:
            eq[i] = x 
    for i in eq:
        if i not in d_operators and i not in s_operators:
            stack.push(i)
        else:
            if i in s_operators:
                a = float(stack.pop())
                if i == s_operators[0]:
                    stack.push(math.sin(a))
                elif i == s_operators[1]:
                    stack.push(math.cos(a))
                elif i == s_operators[2]:
                    stack.push(math.tan(a))
                elif i == s_operators[3]:
                    stack.push(math.asin(a))
                elif i == s_operators[4]:
                    stack.push(math.acos(a))
                elif i == s_operators[5]:
                    stack.push(math.atan(a))
                elif i == s_operators[6]:
                    stack.push(factorial(a))
            elif i in d_operators:
                b = float(stack.pop())
                a = float(stack.pop())
                if i == d_operators[0]:
                    stack.push(a+b)
                elif i == d_operators[1]:
                    stack.push(a-b)
                elif i == d_operators[2]:
                    stack.push(a*b)
                elif i == d_operators[3]:
                    stack.push(a/b)
                elif i == d_operators[4]:
                    stack.push(a**b)
    return stack.pop() * 25

######################################################################
if __name__ == "__main__":
    app = App()
    main()
