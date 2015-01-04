'''
Created on Dec 2, 2014

@author: aditya reddy
'''
import tkinter as tk
from tkinter import *

class tkCanvas2D(Tk):
    '''
    classdocs
    '''
    def __init__(self, parent):
        '''
        Constructor
        '''
        Tk.__init__(self, parent)
        self.parent = parent
        self.frame = Frame(parent) #.pack(fill="both", expand=True)
        #self.initialize()
   
        #def initialize(self):
        #self.grid()
    
        self.canvas = Canvas(self.frame, width=300, height=500, borderwidth=2, bg='white', relief=SUNKEN)
        self.canvas.grid(row=0, column=2, sticky=E, rowspan=16)

if __name__ == "__main__":
    app = tkCanvas2D(None)
    app.title('Basic Bodice')
    app.mainloop()
