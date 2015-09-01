import random
global NumStrings
NumStrings = 20


def midpoint(A,B):
    Ax,Ay = A
    Bx,By = B
    return ((Ax+Bx)/2.0, (Ay+By)/2.0)

def lineintersect(L1,L2):
    ## points on the line
    p1,p2 = L1
    p3,p4 = L2
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4
    return (((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)),
            ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)))

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
    arcpoints = [A]
    for lpind, lp in linepairs:
        if lpind != len(linepairs)-1
        arcpoints.append(lineintersect(lp,linepairs[lpind+1]))
