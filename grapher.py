from tkinter import *
import tkinter.messagebox
import pygame, math

white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
green = (0,127,0)
colours = [red,green,blue]

pi = math.pi
e = math.e

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

        self.label3 = Label(master, text = "Parametric equation of graph x = f(t) y = f(t)")
        self.label3.pack()
        self.eq3a = StringVar()
        self.e3a = Entry(master,textvariable=self.eq3a,width=25)
        self.e3a.pack()
        self.eq3b = StringVar()
        self.e3b = Entry(master,textvariable=self.eq3b,width=25)
        self.e3b.pack()
        
        self.b = Button(master,text = "Draw",command = lambda: drawGraph(self.e.get(),self.e2.get(),self.e3a.get(),self.e3b.get()))
        self.b.pack()

class App():
    def __init__(self):
        self.screenx = 300
        self.screeny = 300
        self.tickspeed = 20
    def begin(self,equation):
        pygame.init()
        pygame.mixer.quit()
        pygame.display.set_caption(equation)
        self.screen = pygame.display.set_mode((self.screenx, self.screeny))
        self.clock = pygame.time.Clock()
        self.xscale = 25
        self.yscale = 25
    def exitGame(self):
        pygame.quit()
        #quit()
    def getTickSpeed(self):
        return self.tickspeed
    def getClock(self):
        return self.clock
    def getScreen(self):
        return self.screen
    def getXScale(self):
        return self.xscale
    def getYScale(self):
        return self.yscale
    def setXScale(self,n):
        if self.xscale+n > 0:
            self.xscale += n
    def setYScale(self,n):
        if self.yscale+n > 0:
            self.yscale += n

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
    response = tkinter.messagebox.askyesno("Save Image","Would you like to save an image of the graphs?")
    root.update()
    if response == True:
        pygame.image.save(app.getScreen(),"graphs.png")
    else:
        return

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                saveImage()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                app.setXScale(-2)
                app.setYScale(-2)
                return "scale" 
            elif event.button == 5:
                app.setXScale(2)
                app.setYScale(2)
                return "scale"

def addAxis():
    pygame.draw.line(app.getScreen(), black, (0,app.screeny/2), (app.screenx,app.screeny/2),2)
    pygame.draw.line(app.getScreen(), black, (app.screenx/2,0), (app.screenx/2,app.screeny),2)

def generateCoordinates(equation,equationpolar,equationparaX,equationparaY):
    lines = equation.split(";")
    polarlines = equationpolar.split(";")
    paraXlines = equationparaX.split(";")
    paraYlines = equationparaY.split(";")
    paralines = [paraXlines,paraYlines]
    if lines == ['']:
        lines = []
    if polarlines == ['']:
        polarlines = []
    if (len(paralines[0]) != len(paralines[1])) or (paralines[0] == [''] and paralines[1] == ['']):
        paralines[0] = []
        paralines[1] = []
    coords = [[] for i in range(len(lines)+len(polarlines)+len(paralines[0]))]
    if lines != []:
        for eq in range(len(lines)):
            for x in range(app.screenx * -1,app.screenx):
                try:
                    y = app.screeny-round(evaluateRPN(lines[eq],x/app.getXScale(),'x'))
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
                    y = round((app.screeny / 2) - (r*math.sin(theta)))
                    x = round((app.screenx / 2) + (r*math.cos(theta)))
                    coords[eq+len(lines)].append((x,y))
                except:
                    pass
    if paralines[0] != []:
        for eq in range(len(paralines[0])):
            for t in range(app.screenx * -1,app.screenx):
                try:
                    x = round(evaluateRPN(paralines[0][eq],t/app.getXScale(),'t'))
                    x += round(app.screenx / 2)
                    y = app.screeny-round(evaluateRPN(paralines[1][eq],t/app.getYScale(),'t'))
                    y -= round(app.screeny / 2)
                    coords[eq+len(lines)+len(polarlines)].append((x,y))
                except:
                    pass
    return coords
    
def drawGraph(equation,polarequation,equationparaX,equationparaY):
    title = "y=("+";".join(equation.split(";"))+"), r=("+";".join(polarequation.split(";"))+"), (x=("+";".join(equationparaX.split(";"))+"),y=("+";".join(equationparaY.split(";"))+"))"
    app.begin(title)
    coords = generateCoordinates(equation,polarequation,equationparaX,equationparaY)
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
        elif response == "scale":
            coords = generateCoordinates(equation,polarequation,equationparaX,equationparaY)
            
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
    eq = [x for x in eq if x]
    d_operators = ["+","-","*","/","^"]
    #add logs --> math.log(x,base)
    s_operators = ["sin","cos","tan","arcsin","arccos","arctan","!","sqrt","cosec","sec","cot"]
    for i in range(len(eq)):
        if eq[i] == variable:
            eq[i] = x
        elif eq[i] == 'e':
            eq[i] = e
        elif eq[i] == 'pi':
            eq[i] = pi
    for i in eq:
        if i not in d_operators and i not in s_operators:
            stack.push(float(i))
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
                elif i == s_operators[7]:
                    stack.push(math.sqrt(a))
                elif i == s_operators[8]:
                    stack.push(1/(math.sin(a)))
                elif i == s_operators[9]:
                    stack.push(1/(math.cos(a)))
                elif i == s_operators[10]:
                    stack.push(1/(math.tan(a)))
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
    return stack.pop() * app.getYScale()

######################################################################
if __name__ == "__main__":
    app = App()
    main()
