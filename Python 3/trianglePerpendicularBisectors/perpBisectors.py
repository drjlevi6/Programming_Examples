""" Draws a triangle, its sides' perpendicular bisectors and circumcircle """

import math, sys
import turtle
import perpView

# Point-slope equation for BC perpendicular bisector
def get_bisector_BC(x):
	return slope_perp_BC * (x - midBCx) + midBCy

# Compute triangle data:
# vertices
Ax, Ay = [0.0, 0.0]
Bx, By = [600.0, 1.0]	# Make ordinate By a tiny pos int so that slope of normal != ∞
Cx, Cy = [150, 400.0]
vertices = [ [Ax, Ay], [Bx, By], [Cx, Cy] ]

# Midpoints:
midABx, midABy = [ (Ax+Bx)/2, (Ay+By)/2]
midBCx, midBCy = [ (Bx+Cx)/2, (By+Cy)/2]
midCAx, midCAy = [ (Cx+Ax)/2, (Cy+Ay)/2]
midpoints = [[midABx, midABy], [midBCx, midBCy ], [midCAx, midCAy]]

# Slope of BC and its perpendicular bisector:
slope_BC = (Cy-By)/(Cx-Bx)
slope_perp_BC = -1/slope_BC


# Make a different definition of slopes of both triangle's edges and their normals:
slopes = []

for i in range(3):
	slopes.append( 
		( vertices[ (i+1)%3 ][1] - vertices[i][1] ) / 
			( vertices[ (i+1)%3 ][0] - vertices[i][0] )
	)
	"""
	print("i =", i)
	print("Ordinates:", vertices[ (i+1)%3 ][1], vertices[i][1], ":", 
		( vertices[ (i+1)%3 ][1] - vertices[i][1] ) )
	print("Abcissas:", vertices[ (i+1)%3 ][0], vertices[i][0], ":", 
		( vertices[ (i+1)%3 ][0] - vertices[i][0] ) )
		"""

# Circumcenter, calculated using get_bisector_BC():
circ_center_x, circ_center_y = [ midABx, get_bisector_BC(midABx) ]
circumradius = math.sqrt(circ_center_x**2 + circ_center_y**2)
circle_data = [[circ_center_x, circ_center_y], circumradius]

# VIEW: Use module turtle; also plan an alternative display using Ghostscript.
perpView.show_view_with_turtle(vertices, midpoints, slopes, circle_data)
while True:
  pass
