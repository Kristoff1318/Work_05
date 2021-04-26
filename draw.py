from display import *
from matrix import *

  # ====================
  # add the points for a rectagular prism whose 
  # upper-left corner is (x, y, z) with width, 
  # height and depth dimensions.
  # ====================
def add_box( points, x, y, z, width, height, depth ):
    ltf = [x, y, z]
    rtf = [x + width, y, z]

    lbf = [x, y - height, z]
    rbf = [x + width, y - height, z]

    ltb = [x, y, z - depth]
    rtb = [x + width, y, z - depth]

    lbb = [x, y - height, z - depth]
    rbb = [x + width, y - height, z - depth]

    add_edge(points, ltf[0], ltf[1], ltf[2], rtf[0], rtf[1], rtf[2])
    add_edge(points, lbf[0], lbf[1], lbf[2], rbf[0], rbf[1], rbf[2])
    add_edge(points, ltb[0], ltb[1], ltb[2], rtb[0], rtb[1], rtb[2])
    add_edge(points, lbb[0], lbb[1], lbb[2], rbb[0], rbb[1], rbb[2])
    
    add_edge(points, ltf[0], ltf[1], ltf[2], ltb[0], ltb[1], ltb[2])
    add_edge(points, rtf[0], rtf[1], rtf[2], rtb[0], rtb[1], rtb[2])
    add_edge(points, lbf[0], lbf[1], lbf[2], lbb[0], lbb[1], lbb[2])
    add_edge(points, rbf[0], rbf[1], rbf[2], rbb[0], rbb[1], rbb[2])

    add_edge(points, ltf[0], ltf[1], ltf[2], lbf[0], lbf[1], lbf[2])
    add_edge(points, rtf[0], rtf[1], rtf[2], rbf[0], rbf[1], rbf[2])
    add_edge(points, ltb[0], ltb[1], ltb[2], lbb[0], lbb[1], lbb[2])
    add_edge(points, rtb[0], rtb[1], rtb[2], rbb[0], rbb[1], rbb[2])


  # ====================
  # Generates all the points along the surface
  # of a sphere with center (cx, cy, cz) and
  # radius r.
  # Returns a matrix of those points
  # ====================
def generate_sphere( points, cx, cy, cz, r, step ):
    m = new_matrix()
    for rot in range(0, 100, int(100 * step)):
        for circ in range(0, 100, int(100 * step)):
            p = circ/100
            q = rot/100
            x = r * math.cos(math.pi * p) + cx
            y = r * math.sin(math.pi * p) * math.cos(2 * math.pi * q) + cy
            z = r * math.sin(math.pi * p) * math.sin(2 * math.pi * q) + cz

            xn = x + 1
            yn = y + 1
            zn = z + 1
            add_edge(m, x, y, z, xn, yn, zn)
    return m

  # ====================
  # adds all the points for a sphere with center 
  # (cx, cy, cz) and radius r to points
  # should call generate_sphere to create the
  # necessary points
  # ====================
def add_sphere( points, cx, cy, cz, r, step ):
    p = generate_sphere(points, cx, cy, cz, r, step)
    for point in p:
        points.append(point)


  # ====================
  # Generates all the points along the surface
  # of a torus with center (cx, cy, cz) and
  # radii r0 and r1.
  # Returns a matrix of those points
  # ====================
def generate_torus( points, cx, cy, cz, r0, r1, step ):
    m = new_matrix()
    for rot in range(0, 100, int(step * 100)):
        for cir in range(0, 100, int(step * 100)):
            q = rot/100
            p = cir/100
            x = math.cos(2 * math.pi * q) * (r0 * math.cos(2 * math.pi * p) + r1) + cx
            y = r0 * math.sin(2 * math.pi * p) + cy
            z = -math.sin(2 * math.pi * q) * (r0 * math.cos(2 * math.pi * p) + r1) + cz

            xn = x + 1
            yn = y + 1
            zn = z + 1
            add_edge(m, x, y, z, xn, yn, zn)
    return m

  # ====================
  # adds all the points for a torus with center
  # (cx, cy, cz) and radii r0, r1 to points
  # should call generate_torus to create the
  # necessary points
  # ====================
def add_torus( points, cx, cy, cz, r0, r1, step ):
    p = generate_torus(points, cx, cy, cz, r0, r1, step)
    for point in p:
        points.append(point)

def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy

    i = 1
    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
