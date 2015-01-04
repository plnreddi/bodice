'''
Created on Nov 30, 2014

@author: aditya reddy
'''
import math

class Point(object):
    ''' 
    classdocs
    '''

    def __init__(self, x, y):
        '''Constructor'''
        self.x = x
        self.y = y
        
    def __str__(self):
        #return "(%s, %s)" % (self.x, self.y)
        #return ', '.join('[{:.3f}, {:.3f}]'.format(self.x, self.y) )
        return ( '({:.1f}, {:.1f})'.format(self.x, self.y) )   
        
   
    def __repr__(self):
        #return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y) 
        return (   'pt({:.1f}, {:.1f})'.format(self.x, self.y)   )    
        
        
    def getxy(self):   
        return (self.x, self.y) 
    
    
    def getx(self):   
        return self.x 
    
    
    def gety(self):   
        return self.y 
     
       
    def __add__(self, p):
        """Point(x1+x2, y1+y2)"""
        return Point(self.x+p.x, self.y+p.y)
       
       
    def __sub__(self, p):
        """Point(x1-x2, y1-y2)"""
        return Point(self.x-p.x, self.y-p.y)
      
      
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    
    def distance_to(self, p):
        """Calculate the distance between two points."""
        
        if type(p) is list or type(p) is tuple:
            pt = Point(*p)
        else:
            pt = p
            
        return (self - pt).length()
        
    
    def move_by_xy(self, dx, dy):
        '''Move to new (x+dx,y+dy)'''
        return Point(self.x + dx, self.y + dy)
    
    
    def angle_to (self, pt):  
        return math.atan2(pt.y-self.y, pt.x-self.x)
    
    
    def mid_pt(self, pt): 
        return Point((self.x + pt.x)/2.0, (self.y + pt.y)/2.0 )
    
    
    def polar_pt(self, ang, dis):
        return Point(self.x + dis*math.cos(ang), self.y + dis*math.sin(ang))
    
    
    def pol_Rt(self, dis):
        return self.polar_pt(0., dis)
    def pol_Up(self, dis):
        return self.polar_pt(0.5*math.pi, dis)
    def pol_Lt(self, dis):
        return self.polar_pt(math.pi, dis)
    def pol_Dn(self, dis):
        return self.polar_pt(1.5*math.pi, dis)
    
    
    def __del__(self):
        class_name = self.__class__.__name__
        #print (class_name, "destroyed")
        
###############################################################################

if __name__ == "__main__":
    
    p1 = Point(1,2)
    p2 = Point(3,4)
    p3 = p1-p2
    
    print (p3)
    print('distance', p1.distance_to(p2))