'''
Created on Dec 11, 2014

@author: aditya reddy
'''
import math
from Point2D import Point

class Offset2D:     
    def __init__(self, points, dis):
        
        self.count = len(points)
    
        points1 = self.removeDuplicatePts(points)
        
        self.x = [x for x,y in points1]
        self.y = [y for x,y in points1]
        self.dis = dis
        
        self.npts1 = self.OffsetPts(self.x, self.y, dis);
        self.npts2 = []
        
    
    def getPts(self): 
        if len(self.npts2) == 0:
            return self.npts1
        else:
            return self.joinOffsetCurves(self.npts1, self.npts2)
            
        
          
    def joinOffsetCurves(self, npts1, npts2):
            
        ipt = self.LineXLine(*npts1[-2]+npts1[-1]+npts2[1]+npts2[0])
        return npts1 + [ ipt ] + npts2
        
    
    def LineXLine(self, x1, y1, x2, y2, x3, y3, x4, y4):
        
        A1 = y2-y1;
        B1 = x1-x2;
        C1 = A1*x1+B1*y1;

        A2 = y4-y3;
        B2 = x3-x4;
        C2 = A2*x3+B2*y3;
        
        det = A1*B2 - A2*B1;
        '''Lines are parallel'''
        if det==0: 
            return None  
        else:
            return ((B2*C1 - B1*C2)/det, (A1*C2 - A2*C1)/det)
        
    
    def OffsetPts(self, x, y, dis):
        
        cnt = len(x) 
        
        nor = []
        for i in range(cnt-1):
            dx = x[i+1] - x[i]
            dy = y[i+1] - y[i]
            mag = math.hypot(dx,dy)
            nor += [ [dx/mag, dy/mag] ]
            
        '''For the start point calculate the normal'''
        npts = [ [x[0]-dis*nor[0][1], y[0]+dis*nor[0][0]] ]
        '''For 1 to N-1 calculate the intersection of the offset lines'''
        for i in range(1, cnt-1):
            L = dis / (1 + nor[i][0] * nor[i-1][0] + nor[i][1] * nor[i-1][1])
            npts += [ [x[i] - L * (nor[i][1] + nor[i-1][1]), y[i] + L * (nor[i][0] + nor[i-1][0])] ]
        ''' For the end point use the normal'''  
        npts += [ [x[i] - dis * nor[i - 1][1], y[i] + dis * nor[i - 1][0]] ]
          
        return npts  
    
    
   
    def removeDuplicatePts(self, points):
        
        ds = Point(*points[1]).distance_to(points[0])
        
        for i in range(1, len(points)):
            if Point(*points[i]).distance_to(points[i-1]) <= 0.1:       # distance(points[i], points[i-1]) == 0.0:
                points.remove(points[i])
       
        return points
    
    
       
    def appendNextPtsAry(self, points, dis):
        self.ncount = len(points)
        
        points1 = self.removeDuplicatePts(points)
        
        self.nx = [x for x,y in points1]
        self.ny = [y for x,y in points1]
        self.ndis = dis
        
        self.npts2 = self.OffsetPts(self.nx, self.ny, dis)
        
        
        