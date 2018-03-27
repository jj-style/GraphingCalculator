# GraphingCalculator
Simple 2D graph plotter made in python

How to plot graphs:  
Enter the equation of the line without the 'y =' or 'r =' 
Equation must be in post-fix notation (see below) with spaces in between every operator/operand  
Multiple lines can be drawn, use a semicolon(;) to seperate the equations of the lines  
Variable must be 'x' for y=f(x) lines or 'theta' for r=g(θ) lines. No other letters will work
Press 's' to save an image of the graph! 
    
Post-fix Notation:  
Post-fix notation, also known as Reverse Polish Notation (RPN) is simply a way of writing maths without the need for brackets. It is used as computers can evaluate results more easily in a stack without having to know the rules of BIDMAS.  
In RPN the operator comes after the operand as opposed to inbetween, which is how we usually see it in in-fix.  
  
For example:  
(a+bx)/d in RPN would be 'a b x * + d /'  

The operators which the program currently supports are:  
'+ - * / ^ ! sin cos tan arcsin arccos arctan'  
  
Feel free to make pull requests and get graphing!
<br /><br /><br />
Screenshot of graphs:  
![multigraphs](https://user-images.githubusercontent.com/27488093/37825501-f4d42fc6-2e87-11e8-8196-48cac9590195.png)

Licensed under the [MIT License](LICENSE).
