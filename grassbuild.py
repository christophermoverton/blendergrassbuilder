import random
import math
global NumStrings, Weight
global MaxinflectionangleAC, MaxinflectionangleAB, MaxinflectionangleBC
global MaxradiusAC
NumStrings = 20
Weight = 10
MaxinflectionangleAC = 10 ## in degrees from vertical randomized plus/minus
MaxinflectionangleAB = 25   ## in degrees from vertical
MaxinflectionangleBC = 25  ## in degrees from vertical
## weight is 0 at the top and 2/3 at the bottom
MaxradiusAC = 3

def radians(deg):
    return deg*math.pi/180.0

def polarx(theta,r):
    return (r*math.cos(theta),r*math.sin(theta))
    
def midpoint(A,B):
    Ax,Ay = A
    Bx,By = B
    return ((Ax+Bx)/2.0, (Ay+By)/2.0)

def slope(L1):
    p1,p2 = L1
    p1x,p1y = p1
    p2x,p2y = p2
    return ((p2y-p1y),(p2x-p1x))

def normal(L1):
    p1,p2 = L1
    slp = slope(L1)
    a,b = slp
    return (-b,a)

def norm(vec):
    x,y = vec
    d =(x*x+y*y)**.5
    return (x/d,y/d)

def scale(scale,vec):
    x,y = vec
    return (scale*x,scale*y)

def translate(P,vec):
    x,y = vec
    px,py = P
    return (x+px,y+py)

def opp(vec):
    x,y = vec
    return (-1*x,-1*y)

def lineintersect(L1,L2):
    ## points on the line

    p1,p2 = L1
    p3,p4 = L2
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4
    ipx = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    ipy = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    return (ipx,ipy)

def ParabolicArc(A,B,C):
    segAB = [A,B]
    segBC = [B,C]
    for i in range(NumStrings):
        newseg = []
        for jind,j in enumerate(segAB):
            t1 = j == A
            
            if not jind == len(segAB)-1:
                t2 = segAB[jind+1] == B
                if t1:
                    newseg.append(j)
                newseg.append(midpoint(j,segAB[jind+1]))
                if t2:
                    newseg.append(segAB[jind+1])
        segAB = newseg[0:len(newseg)]
        newseg = []
        for jind,j in enumerate(segBC):
            t1 = j == B
            
            if not jind == len(segBC)-1:
                t2 = segBC[jind+1] == C
                if t1:
                    newseg.append(j)
                newseg.append(midpoint(j,segBC[jind+1]))
                if t2:
                    newseg.append(segBC[jind+1])
        segBC = newseg[0:len(newseg)]

    linepairs = []
    for iind, i in enumerate(segAB):
        linepairs.append((i,segBC[iind]))
    print(linepairs)
    arcpoints = [A]
    for lpind, lp in enumerate(linepairs):
        if lpind != len(linepairs)-1:
            print(linepairs[lpind+1])
            ap = lineintersect(lp,linepairs[lpind+1])
            print(ap)
            arcpoints.append(ap)
    print arcpoints
    return arcpoints

def Skeleton(arcpoints):
    ## arcpoints determine the position of skeleton lines
    ## Normal (slope) determines the general direction of the skeleton
    ## Normed vector
    cpoint = len(arcpoints)/2
    skeletonpositions = {}
    for iid,i in enumerate(arcpoints):
        if iid != len(arcpoints)-1:
            L = (i,arcpoints[iid+1])
            nslope = normal(L)
            ny,nx = nslope
            nvec = (nx,ny)
            nvec = norm(nvec)
            ## skeleton length is determined by desired magnitude for inc
            if iid > cpoint:
                cslope = Weight*(1.0/3.0)/(cpoint-len(arcpoints)-1)
                wght = cslope*(iid - cpoint) + Weight
            else:
                cslope = Weight/(cpoint)
                wght = cslope*(iid - cpoint) + Weight
            svec = scale(wght,nvec)
            pos2 = arcpoints[iid+1]
            skeletonpos1 = translate(pos2,svec)
            skeletonpos2 = opp(skeletonpos1)
            skeletonpositions[i] = (skeletonpos1,skeletonpos2)

    return skeletonpositions

def rPickControlPoints():
    ## get Random control points for the parabolic arc
    ## These are A and B of a three point system (ABC)
    ## Control point A is established by random angle from B off
    ## vertical.
    ## Control point B is a little trickier in this method.
    ## We intersect two randomly generated polar angles from A and C.
    raAC = random.randint(-MaxinflectionangleAC,MaxinflectionangleAC)
    raAB = random.randint(-MaxinflectionangleAB,MaxinflectionangleAB)
    raCB = random.randint(0,MaxinflectionangleBC)
    while abs(raAB) == abs(raCB):
        raCB = random.randint(0,MaxinflectionangleBC)
    if not raAB > 0:
        raCB = -raCB
    raAC = 90 - raAC
    raAC = radians(raAC)
    A = polarx(raAC,MaxradiusAC)
    C = (0.0,0.0)
    raAB = 270 + raAB
    raAB = radians(raAB)
    p1B = polarx(raAB,1.0)
    p1B = translate(p1B, A)
    L1B = (A,p1B)
    raCB = 90 - raCB
    raCB = radians(raCB)
    p2B = polarx(raCB,1.0)
    L2B = (C,p2B)
    B = lineintersect(L1B,L2B)
    return A,B

A,B = rPickControlPoints()
C = (0.0,0.0)
apoints = ParabolicArc(A,B,C)
