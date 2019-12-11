import math

pi = math.pi
e = math.e

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

def generateCoordinates(equation,equationpolar,equationparaX,equationparaY, width, height):
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
            for x in range(width * -1,width):
                try:
                    y = round(evaluateRPN(lines[eq],x,'x'))
                    coords[eq].append((x,y))
                except:
                    pass
    if polarlines != []:
        for eq in range(len(polarlines)):
            for i in range(0,2000):
                try:
                    theta = i*pi/500
                    r = round(evaluateRPN(polarlines[eq],theta,'theta'))
                    coords[eq+len(lines)].append((x,y))
                except:
                    pass
    if paralines[0] != []:
        for eq in range(len(paralines[0])):
            for t in range(width * -1,width):
                try:
                    x = round(evaluateRPN(paralines[0][eq],t,'t'))
                    y = round(evaluateRPN(paralines[1][eq],t,'t'))
                    coords[eq+len(lines)+len(polarlines)].append((x,y))
                except:
                    pass
    return coords

#_______________________MATHS_______________________#
def factorial(n):
    result = 1
    for i in range(1,n+1):
        result *= i
    return result

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
                elif i == s_operators[9]:
                    stack.push(factorial(a))
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
