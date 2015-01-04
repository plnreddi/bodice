'''
Created on Nov 30, 2014

@author: aditya reddy
'''
import math
from Point2D import Point

class Spline2D(object):
    '''
    classdocs
    '''


    def __init__(self, points):
        '''
        Constructor
        '''
        self.count = len(points)
        #self.x = self.calcCurve([x for x,y in points])
        #self.y = self.calcCurve([y for x,y in points])
        self.x = self.calcCurve([pt.getx() for pt in points])
        self.y = self.calcCurve([pt.gety() for pt in points])
            
    def calcCurve(self, axis):
        
        n = self.count - 1
        
        ''' gama '''
        gama = [0.5]
        for i in range(1, n):                       
            gama += [ 1.0 / (4.0 - gama[i-1]) ]
        gama += [ 1.0 / (2.0 - gama[n-1]) ]
        
        ''' delta '''
        delta = [ 3.0 * (axis[1] - axis[0]) * gama[0] ]
        for i in range(1, n):
            delta += [ (3.0 * (axis[i+1] - axis[i-1]) - delta[i-1]) * gama[i] ]
        delta += [ (3.0 * (axis[n] - axis[n-1]) - delta[n-1]) * gama[n] ]

        ''' d '''
        '''
        d[n] = delta[n];
        for (int i = n - 1; i >= 0; i--)
            d[i] = delta[i] - gamma[i] * d[i + 1];
        '''
        d = (n+1)*[None]
        d[-1] = delta[-1]
        for i in range(2, n+2):
            d[-i] = delta[-i] - gama[-i] * d[-i+1];
            
        c = []
        for i in range(n):
            x0 = axis[i]
            x1 = axis[i+1]
            d0 = d[i]
            d1 = d[i+1]
            #tmp = Cubic(x0, d0,   3.0 * (x1 - x0) - 2.0 * d0 - d1,   2.0 * (x0 - x1) + d0 + d1)
            c += [Cubic(x0, d0,   3.0 * (x1 - x0) - 2.0 * d0 - d1,   2.0 * (x0 - x1) + d0 + d1)]
         
        return c     
    
    
    def getPositionAt(self, param):   
        ''' clamp '''
        if (param < 0.0):
            param = 0.0
            
        ''' split '''
        ti = math.trunc(param)
        tf = param - ti
        
        ''' eval '''
        return Point(self.x[ti].evaluate(tf), self.y[ti].evaluate(tf))
    
    '''
    private void getSplineSegments(float[][] cnpts, float[][][] splines, int bas) {
        
        Spline2D  splin = new Spline2D(cnpts);
        
        float inc = 0.1f;
        float d = 0.05f;
         
        for (int i=0, j=0; d < cnpts.length-1; j++)
        { 
           float[] at = splin.getPositionAt(d);
           
           if (d > i) { i++; j=0;}
           splines[bas+i-1][j][0] = at[0];
           splines[bas+i-1][j][1] = at[1];
           
           d += inc;
        } 
        
    }//end
    
     '''
   
    def  getSpline(self, inc=0.1, d=0.05):
        
        n = self.count-1
        splin = []
        pts = []
        i = 1
        
        while(d < n):
            
            if d > i:
                i += 1
                splin += [ pts ]
                pts = []
                
            pts += [ self.getPositionAt(d) ]
                         
            d += inc
            
        return splin + [ pts ]
     
     
    def printCoefs(self): 
        
        for x in self.x:
            print('X', x)
            
        for y in self.y:
            print('Y', y) 
              
              
    def printSpline(self): 
        splin = self.getSpline()
        
        for pts in splin:
            print (', '.join('({:.3f}, {:.3f})'.format(x, y) for x,y in pts ) ) 
        
            
        '''
        print ( '[' + ', '.join('(%s, %s)' % x,y) + ']' )
        print ( ['%5.3f, %5.3f',  x,y for x,y in pts] )
        #print( '(%8.3f, %8.3f)'.format(x,y) for x,y in pts  )  
        '''
    def printAll(self):   
        self.printCoefs() 
        self.printSpline()    
            
            
class Cubic:
    
    def __init__(self, a,b,c,d):
        self.a, self.b, self.c, self.d = a,b,c,d
      
    def evaluate(self, u):  
        return (((self.d * u) + self.c) * u + self.b) * u + self.a
        
    def __str__(self):
        return 'Coefs(%8.3f, %8.3f, %8.3f, %8.3f)' % (self.a, self.b, self.c, self.d) 
    
    def __repr__(self):
        return 'Coefs(%8.3f, %8.3f, %8.3f, %8.3f)' % (self.a, self.b, self.c, self.d) 
    
    '''
    Offset2D(float[][] points, float dis) {

        this.count = points.length;

        float[][] points1 = removeDuplicatePts(points);

        x = new float[count];
        y = new float[count];

        for (int i = 0; i < count; i++) {
            x[i] = points1[i][0];
            y[i] = points1[i][1];
        }

        this.dis = dis;

        npts1 = OffsetPts(x, y, dis);
        
    }
    '''
###############################################################################

if __name__ == "__main__":
    
    pts = [(12, 56), (20, 94), (33, 98)]
    segs = Spline2D(pts).printAll()
    