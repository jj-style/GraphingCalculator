import math, pygame
pi = math.pi
e = math.e

white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
green = (0,127,0)
colours = [red,green,blue]

class PygameApp():
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
        self.shade = False
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
    def getShade(self):
        return self.shade
    def toggleShade(self):
        self.shade ^= True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #self.exitGame()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    pass
                    #saveImage()
                elif event.key == pygame.K_r:
                    return "shade"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.setXScale(-2)
                    self.setYScale(-2)
                    return "scale"
                elif event.button == 5:
                    self.setXScale(2)
                    self.setYScale(2)
                    return "scale"

    def generateCoordinates(self, equation,equationpolar,equationparaX,equationparaY):
        lines = equation.split(";")
        polarlines = equationpolar.split(";")
        paraXlines = equationparaX.split(";")
        paraYlines = equationparaY.split(";")
        paralines = [paraXlines,paraYlines]
        lines = [x for x in lines if x]
        polarlines = [x for x in polarlines if x]
        if (len(paralines[0]) != len(paralines[1])) or (paralines[0] == [''] and paralines[1] == ['']):
            paralines[0] = []
            paralines[1] = []
        coords = [[] for i in range(len(lines)+len(polarlines)+len(paralines[0]))]
        if lines != []:
            for eq in range(len(lines)):
                for x in range(self.screenx * -1,self.screenx):
                    try:
                        y = self.screeny - round(evaluateRPN(lines[eq],x/self.xscale,'x')*self.yscale)
                        y -= round(self.screeny / 2)
                        x += round(self.screenx / 2)
                        coords[eq].append((x,y))
                    except Exception as e:
                        pass
        if polarlines != []:
            for eq in range(len(polarlines)):
                for i in range(0,2000):
                    try:
                        theta = i*pi/500
                        r = round(evaluateRPN(polarlines[eq],theta,'theta') * self.yscale)
                        y = round((self.screeny / 2) - (r*math.sin(theta)))
                        x = round((self.screenx / 2) + (r*math.cos(theta)))
                        coords[eq+len(lines)].append((x,y))
                    except:
                        pass
        if paralines[0] != []:
            for eq in range(len(paralines[0])):
                for t in range(self.screenx * -1,self.screenx):
                    try:
                        x = round(evaluateRPN(paralines[0][eq],t/self.xscale,'t') * self.yscale)
                        x += round(self.screenx / 2)
                        y = self.screeny - round(evaluateRPN(paralines[1][eq],t/self.yscale,'t') * self.yscale)
                        y -= round(self.screeny / 2)
                        coords[eq+len(lines)+len(polarlines)].append((x,y))
                    except:
                        pass
        return coords

    def drawGraph(self, equation,polarequation,equationparaX,equationparaY):
        title = "y=("+";".join(equation.split(";"))+"), r=("+";".join(polarequation.split(";"))+"), (x=("+";".join(equationparaX.split(";"))+"),y=("+";".join(equationparaY.split(";"))+"))"
        self.begin(title)
        coords = self.generateCoordinates(equation,polarequation,equationparaX,equationparaY)
        while True:
            self.getScreen().fill(white)
            self.addAxis()
            for i in range(len(coords)):
                linecol = colours[i%len(colours)]
                pygame.draw.aalines(self.getScreen(),linecol,False,coords[i],2)
                if self.getShade() == True:
                    for j in range(0,len(coords[i]),10):
                        pygame.draw.line(self.getScreen(), black, coords[i][j], (coords[i][j][0],self.screeny/2),1)
            pygame.display.update()
            self.getClock().tick(self.getTickSpeed())
            response = self.events()
            if response == False:
                pygame.quit()
                return
            elif response == "scale":
                coords = self.generateCoordinates(equation,polarequation,equationparaX,equationparaY)
            elif response == "shade":
                self.toggleShade()

    def addAxis(self):
        pygame.draw.line(self.getScreen(), black, (0,self.screeny/2), (self.screenx,self.screeny/2),2)
        pygame.draw.line(self.getScreen(), black, (self.screenx/2,0), (self.screenx/2,self.screeny),2)

#_______________________MATHS_______________________#

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

def evaluateRPN(y,x,variable):
    stack = Stack()
    eq = y.split(" ")
    eq = [x for x in eq if x]
    d_operators = ["+","-","*","/","^","log"]
    s_operators = ["sin","cos","tan",
                   "arcsin","arccos","arctan",
                   "cosec","sec","cot",
                   "!","sqrt","|",
                   "ln"]
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
                    stack.push(1/(math.sin(a)))
                elif i == s_operators[7]:
                    stack.push(1/(math.cos(a)))
                elif i == s_operators[8]:
                    stack.push(1/(math.tan(a)))
                elif i == s_operators[10]:
                    stack.push(math.sqrt(a))
                elif i == s_operators[11]:
                    stack.push(abs(a))
                elif i == s_operators[12]:
                    stack.push(math.log(a,e))
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
                elif i == d_operators[5]:
                    stack.push(math.log(a,b))
    return stack.pop()