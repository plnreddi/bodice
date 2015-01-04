
from tkinter import *

from ValidateEntry import FloatEntry
from Spline2D import Spline2D
from BasicBodice import BasicBodice

class Application():
    '''           '''
    def __init__(self, data=[]):
        
        self.data = data
        self.entry = []
        
        self.app = Tk()
        #self.app.wm_iconbitmap('.\data\spider.ico')
        
        self.app.wm_title("Basic Bodice")
        self.app.minsize(width=1000, height=800)    #(width=614, height=631)
        self.app.maxsize(width=1000, height=800)
        
        
        ''' left frame '''
        leftFrame = Frame(self.app, width=32)
        
        self.getInput(leftFrame)   
        
        bt = Button(leftFrame, text = 'RUN', width=12, padx=50, command = self.saveInput)
        bt.pack(side=RIGHT)
        
        leftFrame.pack(side=LEFT)
        
       
        ''' Right frame '''
        rightFrame = Frame(self.app)
        
        self.canvas = Canvas(rightFrame, width=900, height=800, borderwidth=2, bg="light blue", relief=SUNKEN)
        self.canvas.pack()
    
        self.canvasDraw()
        
        rightFrame.pack(side=LEFT)
        
        
    def canvasDraw(self):    
            
        bdc = BasicBodice()
        segs = bdc.getBodiceOutput()
        for seg in segs:
            self.canvas.create_line(self.coordsys(seg), fill='red')
               
        self.canvas.scale("all", 0, 0, 10, 10) #("all", 0, 0, 4, 4)
        
        rlPDF(segs).drawPDF()
        
        
        
        
    def coordsys(self, pts):
        return [(x, 110-y) for x,y in pts]
            
        
    def saveInput(self):   
        
        resultsList = []
        for entry in self.entry:
            value = entry.results.get()
            value = entry.getresults(value)
            if value is not None:
                resultsList.append( float(value) )
                #print(value)
        
        return resultsList
        
        
    def run(self):
        self.app.mainloop()
        
        #self.app.mainloop()
        
         
    def getInput(self, fram): 
        
        for rec in self.data:
            key, val, des = rec
            
            ifram = Frame(fram)
            
            inp_label = Label(ifram, width=15, anchor=E, text=des)
            inp_label.pack(side=LEFT, padx=1, pady=3)
            
            cm_entry = FloatEntry(ifram, value=val, width=6, bd=2, textvariable=key )
            cm_entry.pack(side=LEFT,padx=5, pady=3)
            
            in_entry = FloatEntry(ifram, value=val, width=6, bd=2, textvariable=key)
            in_entry.pack(side=LEFT, padx=5, pady=3)
    
            ifram.pack(side=TOP) 
            
            self.entry.append(cm_entry)
            
            
            
class rlPDF():
    
    def __init__(self, data):
        self.data = data
    
    
    def drawPDF(self):
    
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A0, portrait                                      #letter, landscape
        
        c = canvas.Canvas('test5.pdf', pagesize=portrait(A0))

        c.drawString(100,100,"Hello World")
        
        data = self.data
        
        for pts in data:
            self.drwPath(c, pts)
        
        c.showPage()
        c.save()
    
    
    
    def drwPath(self, c, pts):
        from reportlab.lib.units import cm
        
        p = c.beginPath()
        
        x,y = pts[0]
        p.moveTo(x*cm, y*cm)
        
        for pt in pts:
            x,y = pt
            p.lineTo(x*cm, y*cm)
            
        p.close()
        
        c.drawPath(p) 
    
    
                
    
###############################################################################



if __name__ == "__main__":
  
   
    keys = ['NeckCirc',   'ArmScyeDepth', 'BustCirc',     'Nape2Waist', 'WaistCirc',  'Waist2Hip',  
            'HipCirc',    'DressLength',  'BottomCirc',   'Shoulder',   'ChestWidth', 'BackWidth', 
            'BreastDist', 'BustHeight',   'SleeveLength', 'SleeveCirc' ]
        
    values = [  37.5,   22.0,  105.0,  40.0,  90.0,  20.0, 
               117.5,  100.0,  125.0,  12.5,  32.5,  35.0, 
                22.5,    28.5,   15.0,  14.0  ]
        
    desc = ['Neck Circumference', 'ArmScye Depth', 'Bust Circumference',   'Nape to Waist', 'Waist Circumference', 'Waist to Hip',  
            'Hip Circumference',  'Dress Length',  'Bottom Circumference', 'Shoulder',      'Chest Width',         'Back Width',
            'Breast Distance',    'Bust Height',   'Sleeve Length',        'Sleeve Circumference'  ]
        
    data = [[keys[i], values[i], desc[i]] for i in range(len(keys))]
    
    
    app = Application(data)
    app.run()
    
    newvalues = app.saveInput()
    print (newvalues)
    
   