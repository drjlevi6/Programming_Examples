""" Draws an ellipse by tangents. 
	Source: Cundy, Martin, and AP Rollett, Mathematical Models (1960)
	
	20190727: Default focal point added; timing of drawing of the
	construction's component parts adjusted to minimize monotony
	for a user observing the process.
"""

import math, turtle
from turtle import *
import time, random

#############
# functions #
#############

def calcMaxVectors(fx0):
    """ No. vectors needed increases at extremes ( 0 and 4).
        Perhaps try:
        0.5: 60 ok
        1:	40 insuff, 50 OK
        2:	20 insuff, 40 OK, 60 smooth
        3:	40 OK
        3.95:	70 OK
    """
    # Want linear fn y = mx + b   s.t. y(2.25) = 28, y(3.875) = 52, or:
    m, b = [14.77, -5.23]
    return 40
#    return round((m * fx0) + b)

def calcx(theta):			# compute coordinates of vector at angle theta
    tanth = math.tan(theta)
    A = 1 + tanth**2
    B = -2 * fx * tanth**2
    C = (fx**2 * tanth**2) - r**2
    x1, x2 = [(-B + math.sqrt(B**2 - 4 * A * C))/(2*A),
        (-B - math.sqrt(B**2 - 4 * A * C))/(2*A)]
    return max(x1, x2) if ((theta < math.pi/2) or 
        (theta > 3 * math.pi/2)) else min(x1, x2)

def drawBoundingCircle():	# draws circle enclosing ellipse, axis...
    t.pencolor("yellow")
    t.penup()
    t.goto(-r, 0)
    t.pendown()
    t.right(90)
#    t.speed(10)
    s.delay(200)
    t.speed(11)
    t.circle(r)
    s.delay(0)

def drawAxisAndPoints():	# draws axis, center, focus
    t.pencolor("yellow")
    t.penup()
    t.goto(-r, 0)
    t.left(90)
    t.pendown()
    t.goto(0, 0)
    t.dot()
    t.goto(fx, 0)
    t.dot()
    t.goto(r, 0)
    
def drawVector(theta):			# draws vector from f at angle theta
    if theta == 0:			# special cases for theta = 0, pi: no vector
        return (r, 0)
    if theta == math.pi:
        return (-r, 0)
        
    if theta == math.pi/2:	# special cases for theta = pi/2, 3pi/2
        x, y = [fx, math.sqrt(r**2 - fx**2)]
    elif theta == 3 * math.pi/2:
        x, y = [fx, -math.sqrt(r**2 - fx**2)]
    else:
        x = calcx(theta)
        y = (x-fx) * math.tan(theta)
    t.pencolor("yellow")
    t.penup()
    t.goto(fx, 0)
    t.pendown()
    t.speed(11)
    t.goto(x, y)
    t.speed(11)
    return (x, y)

def drawVectors(maxvectors):				# chooses vals of theta, calls drawVector()
    t.speed(11)
    for i in range(maxvectors):
        theta = i/maxvectors * 2 * math.pi
        x, y = drawVector(theta)
        drawTangent(x, y, theta)

def drawTangent(x, y, theta):	# Draws line tangent to ellipse, perp. to ray from focus 
    if theta == 0 or theta == math.pi: return	# no tangent needed
    phi = theta + math.pi/2 if theta < math.pi else theta - math.pi/2
    
    A, B, C = [1, 2*(x * math.cos(phi) + y * math.sin(phi)),
        (x**2 + y**2 - r**2)]
    l1, l2 = [(-B + math.sqrt(B**2 - 4 * A * C))/2,
        (-B + math.sqrt(B**2 - 4 * A * C))/2] # A= 1, so omit from denom  
    l = l2
    dotsize = 1
    t.pencolor("red")
    t.penup()
    t.speed(11)
    t.goto(x, y)
    t.pendown()
    t.goto(x + (l-dotsize)*math.cos(phi), y + (l-dotsize)*math.sin(phi))
    t.speed(11)
    t.pencolor("yellow")
    t.dot(dotsize)

def getRandomFocus():
    """ Returns a random number representing a focus in inches,
        between fx0min and fx0max. """
    fx0min, fx0max = [2, 3.75]
    return fx0min + (fx0max - fx0min)*random.random()

def printElapsedTime(t0):
    t1 = time.monotonic()
    print("Elapsed time (sec):", int(t1-t0))

def printStats(fx0, maxvectors):  # used to name screenshots
    print('fx0=' + str(fx0) + ',maxvectors=' + str(maxvectors))

def getFocalPointFromUser(): # gets focal point, must range from 2.25-3.875
    fxdefault = 3.75
    try:
        fx0 = float(input("Please enter focal point, between 0.5 (near center) and 3.95 (near edge): "))
        if fx0 < 0.05 or fx0 > 3.95:
            raise ValueError
    except ValueError:
        print("Invalid value of focal point: Using default focus " + str(fxdefault)) #, file=sys.stderr, flush=True)
        fx0 = fxdefault
    return fx0
    #return float(fx0)
  
########
# Main #
########
t0 = time.monotonic()
pxlperinch = 72
r0 = 4					# radius in inches
r = r0 * pxlperinch		# radius in pixels
#fx0 = getRandomFocus()
#fx0 = 2.25 #3.75 #1.75, 2, 3.75, 3.875		# focus abscissa in inches
fx0 = getFocalPointFromUser()
fx = fx0 * pxlperinch		# focus abscissa in pixels
maxvectors = calcMaxVectors(fx0)	# 28

s = Screen()
s.bgcolor("#000040")
t = Turtle()
drawBoundingCircle()
drawAxisAndPoints()

drawVectors(maxvectors)
printStats(fx0, maxvectors)
printElapsedTime(t0)

mainloop()