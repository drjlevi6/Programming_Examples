""" Animates the spreadsheet 
    "/Users/jonathan/Development/LibreOffice/Lissajous_Video_Project/Lissajous.ods" 
    by filling in the cells needed to draw the line segments approximating 
    a Lissajous curve and a dot at the end of the partially drawn curve, moving 
    the dot to the new end with the addition of each segment.
    
    The data for the graph is arranged in two columns, representing the 
    respective abscissas and the ordinates of the points to be plotted.
    These cells are filled in by copying values from two other columns of
    cells which have been "preloaded", i.e. they constitute a cache of
    data which is copied to the first two columns.
    
    The equations used to generate the cached values of the points to
    be plotted is
    
        (x(t), y(t)) = (3 sin(4t), 4 sin(3t)).
    """

import StartLissajousDocWithRunFunction
#exit()

[localContext, resolver, smgr, desktop, model, current_controller, 
    active_sheet] =  StartLissajousDocWithRunFunction.run()
import time

def named_cell(j_col, i_row):
    """ This function's only purpose is to make the text less cumbersome."""
    return active_sheet.getCellByPosition(j_col, i_row)

nrows = 1000
rowOffset = 3	# first data row (since coordinates are zero-based)

# set first segment (starting point) and endpoint.
[named_cell(1, rowOffset).Formula, named_cell(2, rowOffset).Formula, \
    named_cell(3, rowOffset).Formula, named_cell(4, rowOffset).Formula, ] = \
    [named_cell(5, rowOffset).Formula, named_cell(6, rowOffset).Formula, 
    named_cell(5, rowOffset).Formula, named_cell(6, rowOffset).Formula, ]

# Choose a temporary character to fill in cells while testing
if named_cell(7, 1).Formula == 'a':
    tempchar = 'b'
else:
    tempchar = 'a'
named_cell(7, 1).Formula = tempchar

# Erase any data in rows (rowOffset + 1) thru (rowOffset + 1 + 101), columns 2-5.
#print("animateLissajousDoc: Erasing any leftover segments/endpoints.")

for i in range(rowOffset + nrows, rowOffset, -1):
    for j in range(1,5):
        named_cell(j,i).Formula = tempchar
time.sleep(1)
[named_cell(1, rowOffset).Formula, named_cell(2, rowOffset).Formula, 
    named_cell(3, rowOffset).Formula, named_cell(4, rowOffset).Formula] = \
    [named_cell(5, rowOffset).Formula, named_cell(6, rowOffset).Formula,
    named_cell(5, rowOffset).Formula, named_cell(6, rowOffset).Formula]

time.sleep(0.5)		# let erased graph 'sit' a moment before drawing

"""
# Transfer data from cached-coordinates columns to redraw the figure.
for i in range(rowOffset+1, rowOffset + nrows + 1):
    named_cell(1, i).Formula, named_cell(3, i).Formula = \
        [named_cell(5, i).Formula, named_cell(5, i).Formula]
    named_cell(2, i).Formula, named_cell(4, i).Formula = \
        [named_cell(6, i).Formula, named_cell(6, i).Formula]
    if i > rowOffset:
        [named_cell(3, i-1).Formula, named_cell(4, i-1).Formula] = ['', '']
"""

# Erase first dot.
#print("animateLissajousDoc: Erasing dot", rowOffset)
#[named_cell(3, rowOffset).Formula, named_cell(4, rowOffset).Formula] = ['', '']
#time.sleep(.75)

# Transfer data from cached-coordinates columns, 2 rows at a time, to redraw the figure.
#print("animateLissajousDoc: Drawing new segments/endpoints.")
for i in range(rowOffset, rowOffset + nrows, 2):
    # Draw next 2 segments.
#    print("Drawing segments", i+1, "and", i+2)
    named_cell(1, i+1).Formula, named_cell(2, i+1).Formula = \
        [named_cell(5, i+1).Formula, named_cell(6, i+1).Formula]
    named_cell(1, i+2).Formula, named_cell(2, i+2).Formula = \
        [named_cell(5, i+2).Formula, named_cell(6, i+2).Formula]
    
    # Redraw the endpoint.
    if i > rowOffset:
#        print("Erasing dot row", i)
        [named_cell(3, i).Formula, named_cell(4, i).Formula] = ['', '']
#    print("Drawing dot row", i+2, "\n")
    [named_cell(3, i+2).Formula, named_cell(4, i+2).Formula] = \
        [named_cell(5, i+2).Formula, named_cell(6, i+2).Formula]
    time.sleep(0.2)
