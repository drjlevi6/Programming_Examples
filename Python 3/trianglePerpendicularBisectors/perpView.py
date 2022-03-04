""" Handles the View aspect of the Perpendicular Bisectors program, 
using Python's Turtle module. (Another module is planned, to present 
the same view using GhostScript.)"""

import turtle
from turtle import *
import math

global llx, lly, urx, ury
llx, lly = [-45, -230]
urx, ury = [llx + 700, lly + 700]

def open_screen(s):
	""" open the Turtle canvas (screen); set its coordinates"""
	s.setworldcoordinates(llx, lly, urx, ury)

def draw_triangle(t, vertices):
	"""Draw the base triangle"""
	[ [Ax, Ay], [Bx, By], [Cx, Cy] ] = vertices
	t.speed(6)
	t.goto(Ax, Ay)
	t.speed(3)
	t.pendown()
	t.goto(Bx, By)
	t.goto(Cx, Cy)
	t.goto(Ax, Ay)

def draw_bisectors(t, midpoints, circle_data):
	"""Draw base triangle's parpenducular bisectors"""
	[[midABx, midABy], [midBCx, midBCy ], [midCAx, midCAy]] = midpoints
	[[circ_center_x, circ_center_y], circumradius] = circle_data
	
	t.pencolor( "blue" )
	t.penup();		t.goto( circ_center_x, circ_center_y )
	t.pendown();	t.goto( midABx, midABy )
	t.penup();		t.goto( circ_center_x, circ_center_y )
	t.pendown();	t.goto( midBCx, midBCy )
	t.penup();		t.goto( circ_center_x, circ_center_y )
	t.pendown();	t.goto( midCAx, midCAy )

def draw_circumcircle( t, circle_data ):
	"""Draw the base triangle's circumscribing circle"""
	saved_speed = t.speed()
	t.speed(10)
	[[circ_center_x, circ_center_y], 
		circumradius] = circle_data
	t.pencolor( "red" )
	t.penup();
	t.goto( circ_center_x, circ_center_y )
	t.setheading(math.pi )
	t.pendown()
	t.goto( circ_center_x - circumradius, circ_center_y );
	t.setheading(math.pi * 1.5);
	t.speed(3)
	t.circle(circumradius)
	t.speed(saved_speed)

def draw_right_angles(midpoints, slopes):
	""" Draws right angles between triangle's edges & their perp. bisectors"""
	for i in range(2):
		draw_one_right_angle(midpoints[i], slopes[i])

def draw_ticks(s, t, vertices, midpoints, slopes):
	"""Arranges drawing (two) groups of tick-marks on each triangle-edge. """
	saved_width = t.width()
	t.width(5)
	saved_color = t.pencolor()
	t.pencolor("purple")
	for i in range(3):
		draw_one_tick_group(s, t, i, vertices, slopes, 0.25)
		draw_one_tick_group(s, t, i, vertices, slopes, 0.75)
	t.pencolor(saved_color)
	t.width(saved_width)

def draw_one_tick_group(s, t, i, vertices, slopes, displacement):
	"""Draws one group of (i) tick-marks on triangle edge i."""
	""" The group is displaced by (decimal) argument displacement from 
		starting vertex to ending vertex."""
	# small = x if x < y else y
	tick_group_width = 20.0	# width of group on triangle edge
	tick_length = 20		# tick's total length (both sides of triangle edge)
	t.width(1)
	t.pencolor("black")
	start_angle = math.atan(slopes[i]) if i==0 else \
		math.atan(slopes[i]) + math.pi
	t.setheading( start_angle )
	s.delay(1)	# not 1000
	t.penup()
	group_center_x, group_center_y = [ 
		(1.0-displacement) * vertices[i][0] + displacement * vertices[(i+1) % 3][0], 
		(1.0-displacement) * vertices[i][1] + displacement * vertices[(i+1) % 3][1]
		]
	t.speed(6)
	t.setheading(t.towards(group_center_x, group_center_y))
	t.goto( group_center_x, group_center_y )
	t.setheading( start_angle )
	t.speed(3)
	if i==0:
		t.left(math.pi/2)
		t.pendown()
		t.forward(tick_length/2)
		t.left(math.pi)
		t.forward(tick_length)
		t.penup()
		t.left(math.pi)
		t.forward(tick_length/2)
	else:
		t.backward(tick_group_width/i/2)
		for j in range(i+1):
			t.left(math.pi/2)
			t.pendown()
			t.forward(tick_length/2)
			t.backward(tick_length)
			t.penup()
			t.forward(tick_length/2)
			t.right(math.pi/2)
			t.forward(tick_group_width/2)
	
def writeName(t, vertices):
	"""Display author's name"""
	t.pencolor("black")
	t.penup()
	t.speed(3)
	t.setheading(t.towards(urx, lly + 100))
	t.speed(6)
	t.goto(urx, lly + 100)
	t.pendown()
	t.write("J LEVI 2021", True, align="right",
		font=("Arial", 12, "normal"))	
	t.penup()

def draw_right_angles(t, midpoints, slopes):
	""" Manages drawing a right-angle marker at the edges' midpoints"""
	reverse_direction = [False, True, True]
	saved_color = t.pencolor()
	saved_speed = t.speed()
	t.pencolor("green")
	t.speed("slowest")
	for i in range(3):
		draw_one_right_angle(t, midpoints[i], slopes[i], 
			reverse_direction[i])	
	t.pencolor(saved_color)
	t.speed(saved_speed)
		
def draw_one_right_angle(t, midpoint, slope, reverse_direction):
	"""Draw a right-angle signs at the intersection of one of the triangle's 
		edges and its perpendicular bisector."""
	angle_side = 20 	# length of the right angle's sides
	t.penup()
	t.setheading(t.towards(midpoint[0], midpoint[1]))
	t.speed(6)
	t.goto(midpoint)
	direction = math.atan(slope) if  not reverse_direction  else \
		math.atan(slope) + math.pi
	t.speed(3)
	t.setheading(direction)	
	t.forward(angle_side)
	t.left(math.pi/2)
	t.pendown()
	t.forward(angle_side)
	t.left(math.pi/2)
	t.forward(angle_side)
	t.penup()
	

### Main ######################################################################
	
def show_view_with_turtle(vertices, midpoints, slopes, circle_data):
	""" Main function; calls others to draw the specific items """

	turtle.setup( width=800, height=800 )
	turtle.title("Perpendicular Bisectors of a Triangle")
	t, s = [ Turtle(), Screen() ]
	t.radians()
	open_screen( s )
	draw_triangle( t, vertices )
	draw_bisectors( t, midpoints, circle_data )
	draw_right_angles(t, midpoints, slopes)
	draw_ticks(s, t, vertices, midpoints, slopes)
	draw_circumcircle( t, circle_data )
	writeName(t, vertices)


