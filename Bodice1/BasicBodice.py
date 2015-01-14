'''
Created on Nov 30, 2014

@author: aditya reddy
'''
import math
from Point2D import Point
from Spline2D import Spline2D
from Offset2D import Offset2D

class BasicBodice(object):
    '''
    classdocs
    '''
    def __init__(self, dat=None):
        '''
        Constructor
        '''
        self.BodyCalc = {}
        
        self.defaultBodySizes(dat)
        self.defaultEaseValues()
        
        self.BustDartWidth()
        self.WaistDarts()
        self.ArmScyeCorners()
        
        miscal = self.MiscCalcs()
        
        self.BodiceFrm(miscal)
        
        self.BackBasicBodice(miscal)
        
        self.FrontBasicBodice(miscal)
        
        self.BasicSleeve()
        
        
    def getBodiceOutput(self):
        # Results will be sent back to client
        return [self.FrmRect,
                self.bakShoulderDart.getVrtxs(), 
                self.bakWaistDart.getVrtxs(), 
                self.bakBodice1Shape.getVrtxs(),
                self.bakBodice1Ofset,
                self.fntWaistDart.getVrtxs(),
                self.fntBodice1Shape.getVrtxs(),
                self.fntBodice1Ofset, 
                self.BodiceSleeve.getVrtxs(),
                self.Sleeve1Ofset ]    
        
        
    def __repr__(self):  
        # Basic Bodice Ver 1.0'
        s1 = '\nBody Sizes:\n'
        s2 = ', '.join('[{0:}: {1:.2f}]'.format(k, v) for k,v,d in self.BodySizes )
        s3 = '\nBody Ease Values:\n'
        s4 = ', '.join('[{0:}: {1:.2f}]'.format(k, self.BodyEase[k]) for k in self.BodyEase) 
        s5 = '\nBody Calc Values:\n'
        s6 = ', '.join('[{0:}: {1:.2f}]'.format(k, self.BodyCalc[k]) for k in self.BodyCalc) 
        
        return s1 + s2 + s3 + s4 + s5 + s6
        
      
    def defaultBodySizes(self, dat): 
        '''Body Sizes in CM'''
        
        keys = ['NeckCirc',   'ArmScyeDepth', 'BustCirc',     'Nape2Waist', 'WaistCirc',  'Waist2Hip',  
                'HipCirc',    'DressLength',  'BottomCirc',   'Shoulder',   'ChestWidth', 'BackWidth', 
                'BreastDist', 'BustHeight',   'SleeveLength', 'SleeveCirc' ]
        
        if dat==None:
            values = [  37.5,   22.0,  105.0,  40.0,  90.0,  20.0, 
                       117.5,  100.0,  125.0,  12.5,  32.5,  35.0, 
                        22.5,   28.5,   15.0,  14.0  ]
        else:
            values = dat
            
        desc = ['Neck Circumference', 'ArmScye Depth', 'Bust Circumference',   'Nape to Waist', 'Waist Circumference', 'Waist to Hip',  
                'Hip Circumference',  'Dress Length',  'Bottom Circumference', 'Shoulder',      'Chest Width',         'Back Width',
                 'Breast Distance',   'Bust Height',   'Sleeve Length',        'Sleeve Circumference'  ]
        
        
        self.BodySizes = list(zip(keys, values, desc))
        
        
        
    def defaultEaseValues(self): 
        '''Ease Values'''
        keys = [ 'FrontNeckDepEse', 'FrontNeckSideEse', 'BustEse', 'ChestWidthEse', 'BackWidthEse' ]
        values = [ -0.2, 0.7, 5.0, 0.5, 0.5 ] 
        self.BodyEase = dict(zip(keys, values))
        
        
        
    def BustDartWidth(self):
        '''Bust Dart Calculation'''     
        siz = { k:v for k,v,d in self.BodySizes }             
        self.BodyCalc['DartSize'] = 7.0 + (((siz['BustCirc'] - 88.0) / 4.0) * 0.6)
        

 
    def WaistDarts(self):
        '''Waist darts size distribution'''
        siz = { k:v for k,v,d in self.BodySizes }
        
        dif = ((siz['BustCirc'] + 3.0) - (siz['WaistCirc'] + 6.0)) / 2.0
       
        self.BodyCalc['FrontCenDart'] = (4.0 / 24.0) * dif
        self.BodyCalc['FrontSidDart'] = (5.0 / 24.0) * dif

        self.BodyCalc['SideFntDart'] = (5.0 / 24.0) * dif
        self.BodyCalc['SideBakDart'] = (3.0 / 24.0) * dif

        self.BodyCalc['BackDart'] = (3.0 / 24.0) * dif



    def ArmScyeCorners(self):   
        '''ArmScye corners calculation, Units: CM'''
        siz = { k:v for k,v,d in self.BodySizes }
        circ = siz['BustCirc']  
                       
        if circ > 107.0: 
            values = [3.50,3.00]
        elif circ > 94.0:
            values = [3.00,2.50]
        elif circ > 82.0: 
            values = [2.50, 2.00]
        else:   
            values = [2.25, 1.75]    
                            
        self.BodyCalc['BackCor'] = values[0]           
        self.BodyCalc['FrontCor'] = values[1]     
                     
#--------------------------------------------------------------                       
     
    def MiscCalcs(self):
        '''Misc Calculations'''
        siz = { k:v for k,v,d in self.BodySizes }
        
        ''' ArmScye level calculation '''
        bustWd = (siz['BustCirc'] / 2.0) + self.BodyEase['BustEse']
        chestWd = (siz['ChestWidth'] + self.BodyCalc['DartSize']) / 2.0;
        backWd = (siz['BackWidth'] / 2.0) + self.BodyEase['BackWidthEse']
        ArmScyeWd = bustWd - (chestWd + backWd);
  
        ''' Back Bodice heights '''
        bh0 = 1.5
        bhH = (siz['ArmScyeDepth'] / 5.0) - 0.7
        bh1 = siz['ArmScyeDepth'] + 0.5
        
        ''' Front Bodice heights '''
        fhS = (siz['NeckCirc'] / 5.0) + self.BodyEase['FrontNeckDepEse'] # D-S
        fh1 = bh0 + bh1 + ((siz['BustCirc'] - 92) / 8.0);
    
        ''' Common heights '''
        h2 = siz['Nape2Waist'] - (siz['ArmScyeDepth'] + 0.5)
        h3 = siz['Waist2Hip']
        h4 = siz['DressLength'] - (bh1 + h2 + h3)
      
        ''' Frame height and width '''
        frmht = fh1 + h2 + h3 + h4
        frmwd = (siz['BottomCirc'] / 2.0) + 2.4 + 2.4
        
        ''' Frame starting point '''
        usrpt = [5.0, 100.0]
       
        ''' Back Bodice starting point '''
        BakBdcPt = [ usrpt[0], usrpt[1] - (fh1 - bh0 - bh1) ]
      
        ''' Front Bodice starting point '''
        FntBdcPt = [ usrpt[0] + frmwd, usrpt[1] ]
         
        return [bustWd,chestWd,backWd,ArmScyeWd, bh0,bhH,bh1, fhS,fh1, h2,h3,h4, frmht,frmwd, usrpt,BakBdcPt,FntBdcPt]
    
#--------------------------------------------------------------    
    
    def BodiceFrm(self, miscal):
        ''' Rectangle Frame '''
        #bustWd,chestWd,backWd,ArmScyeWd, bh0,bhH,bh1, fhS,fh1, h2,h3,h4, frmht,frmwd, usrpt,BakBdcPt,FntBdcPt = miscal
        
        fh1, h2,h3,h4, frmht,frmwd, usrpt = miscal[8:15]
        x,y = usrpt
        
        border = [[None,None] for i in range(11)]
        
        for i in [0,4,5,8,9,1]:  # x value
            border[i][0] = x
            
        for i in [3,6,7,10,2]:   # x value
            border[i][0] = x + frmwd
            
        for i in [0,4,3]:   # Hor1: y values
            border[i][1] = y    
          
        for i in [5,6]:   # Hor1: y values
            border[i][1] = y - fh1    
            
        for i in [8,7]:   # Hor1: y values
            border[i][1] = y - fh1 - h2    
            
        for i in [9,10]:   # Hor1: y values
            border[i][1] = y - fh1 - h2 - h3      
              
        for i in [1,2]:   # Hor1: y values
            border[i][1] = y - frmht                               #y- fh1 - h2 - h3 - h4 
        
        self.FrmRect = border
        
#--------------------------------------------------------------        
        
    def BackBasicBodice(self, miscal):
        ''' Rectangle Frame '''
        #bustWd,chestWd,backWd,ArmScyeWd, bh0,bhH,bh1, fhS,fh1, h2,h3,h4, frmht,frmwd, usrpt,BakBdcPt,FntBdcPt = miscal
        bustWd,chestWd,backWd,x, bh0,bhH,bh1, x,x, h2,h3,h4, x,x, x,BakBdcPt,x = miscal
         
        siz = { k:v for k,v,d in self.BodySizes }  
        cal = self.BodyCalc 
        
        Zrw1 = (siz['NeckCirc'] / 5.0) - 0.2   # O-G 
        G2I = siz['Shoulder'] + 1.0

        h1w2 = backWd;
        h1w1 = (bustWd + backWd - chestWd) / 2.0;
        h1w0 = backWd / 2.0;

        h2w1  = h1w1 - cal['SideBakDart']     #  Waist level
        h2w2  = h1w0 - cal['BackDart']
        h2w3  = h1w0 + cal['BackDart']
        
        h3w1 = backWd + ((siz['HipCirc'] / 2.0) - chestWd - backWd) / 2.0
        h4w1 = backWd + ((siz['BottomCirc'] / 2.0) - chestWd - backWd) / 2.0
        
        
        pO = Point(*BakBdcPt)
        pA = pO.pol_Dn(bh0)            
        pH = pA.pol_Dn(bhH)

        pB = pA.pol_Dn(bh1)            #float[] pB  = pol270(pA, bh1);
        pE = pB.pol_Dn(h2)            #float[] pE  = pol270(pB, h2);
        pE1 = pE.pol_Dn(h3)            #float[] pE1 = pol270(pE, h3);
        pE2 = pE1.pol_Dn(h4)           #float[] pE2 = pol270(pE1, h4);

        pZ = pB.pol_Rt(h1w1)           #float[] pZ  = pol000(pB, h1w1);
        pAA = pE.pol_Rt(h2w1)          #float[] pAA = pol000(pE, h2w1);
        pA1 = pE1.pol_Rt(h3w1)         #float[] pA1 = pol000(pE1, h3w1);
        pA2 = pE2.pol_Rt(h4w1)         #float[] pA2 = pol000(pE2, h4w1);
        
        pL = pB.pol_Rt(h1w2)                                   #float[] pL  = pol000(pB, h1w2);
        pL1 = pL.polar_pt(0.25*math.pi, cal['BackCor'])        #float[] pL1 = pol045(pL, BackCor);
        pN =  pL.pol_Up((bh1 - bhH) / 2.0)                     #float[] pN  = pol090(pL, (bh1 - bhH) / 2.0f);
        
        pG = pO.pol_Rt(Zrw1)                                   #float[]  pG = pol000( pO , Zrw1);
        opp = bh0 + bhH;  
        hor = math.sqrt(math.pow(G2I, 2.0) - math.pow(opp, 2.0))
        pI1 = pG.pol_Dn(opp).pol_Rt(hor)                       #float[] pI1 = pol000(pol270(pG, opp), hor);
        
        pP = pB.pol_Rt(h1w0)                                   #float[] pP  = pol000(pB, h1w0);
        pQ1 = pE.pol_Rt(h2w2)                                  #float[] pQ1 = pol000(pE, h2w2);
        pQ2 = pE.pol_Rt(h2w3)                                  #float[] pQ2 = pol000(pE, h2w3);
        pQ0 = pE1.pol_Rt(h1w0)                                 #float[] pQ0 = pol000(pE1, h1w0);
        
        pJ = pG.mid_pt(pI1)                                    #float[] pJ  = midPt(pG, pI1);
        pK = pJ.polar_pt(pJ.angle_to(pP), 15.)                 #float[] pK  = polarPt(pJ, (float) angleTo(pJ, pP), 15.0f);
        pJ1 = pJ.polar_pt(pJ.angle_to(pG), 0.5)                #float[] pJ1 = polarPt(pJ, (float) angleTo(pJ, pG), 0.5f);
        pJ2 = pJ.polar_pt(pJ.angle_to(pI1), 0.5)               #float[] pJ2 = polarPt(pJ, (float) angleTo(pJ, pI1), 0.5f);
        
        
        self.bakShoulderDart = Lines([pJ1, pK, pJ2])
        self.bakWaistDart = Lines([pQ0, pQ1, pP, pQ2, pQ0])
        
        rad = ((Zrw1*Zrw1) + (bh0*bh0)) / (2. * bh0)  #(a.a + b.b) / 2.b
        cpt = pA.pol_Up(rad)
        #         [0   1   2]   3   [4]  5  6    7   8   9   10   [11  12   13]  14
        cnpts = [ pZ, pL1, pN, pI1, pG, pA, pH, pB, pE, pE1, pE2, pA2, pA1, pAA, pZ ]     
             
        splines = Spline2D(cnpts[:4]).getSpline() + [3] + \
                  self.__getCircularPline(cpt, pG, pA) + [5,6,7,8,9,10] + \
                  Spline2D(cnpts[11:]).getSpline() + [14]   
                        
        shape = [cnpts[i]  if type(splines[i]) is int else [cnpts[i]]+splines[i]  for i in range(len(cnpts))]
        self.bakBodice1Shape = Lines(shape)
        
        bbofs = Offset2D( Lines(shape[10:]).getVrtxs(), -2.4)
        bbofs.appendNextPtsAry( Lines(shape[:6]).getVrtxs(), -0.8)
        self.bakBodice1Ofset = bbofs.getPts()
        
#--------------------------------------------------------------        
     
    def FrontBasicBodice(self, miscal):
        ''' Front Basic Bodice '''
        bustWd,chestWd,backWd,ArmScyeWd, bh0,bhH,bh1, fhS,fh1, h2,h3,h4, frmht,frmwd, usrpt,BakBdcPt,FntBdcPt = miscal
        
        siz = { k:v for k,v,d in self.BodySizes }  
        cal = self.BodyCalc     
        ese = self.BodyEase
       
        h0w2 = (siz['NeckCirc'] / 5.) + ese['FrontNeckSideEse']   # R-D
        h0w1 = h0w2 + cal['DartSize']

        h1w1 = (bustWd - backWd + chestWd) / 2.
        h1w2 = chestWd
        h1w3 = siz['BreastDist'] / 2.
        
        h2w1 = h1w1 - cal['SideFntDart']  # Waist level
        h2w2 = h1w3 + cal['FrontCenDart']
        h2w3 = h1w3 - cal['FrontSidDart']
        
        # Hip and Bottom levels
        h3w1 = chestWd + ((siz['HipCirc'] / 2.) - chestWd - backWd) / 2.
        h4w1 = chestWd + ((siz['BottomCirc'] / 2.) - chestWd - backWd) / 2.
        
        pD = Point(*FntBdcPt)
        pS  = pD.pol_Dn(fhS)   
        pC  = pD.pol_Dn(fh1)    
        pF  = pC.pol_Dn(h2)
        pF1 = pF.pol_Dn(h3)
        pF2 = pF1.pol_Dn(h4)

        pZ  = pC.pol_Lt(h1w1)
        pAA = pF.pol_Lt(h2w1)
        pA1 = pF1.pol_Lt(h3w1)
        pA2 = pF2.pol_Lt(h4w1)
        
        pR  = pD.pol_Lt(h0w2)
        pBP = Point(h1w3, 2.5)    
        pBP = pC - pBP          #check
        # pW  = pD.pol_Lt(h0w1)   #  old method
        
        pT  = pC.pol_Lt(h1w2)
        pT1 = pT.polar_pt(0.75*math.pi, cal['FrontCor'])
        pY  = pT.pol_Up(siz['ArmScyeDepth'] / 3.)
        
        ''' Dart Radious correction '''
        
        rad = pBP.distance_to(pR) 
        dartAng = math.asin(cal['DartSize'] / (2. * rad)) * 2.    # asin calculation
        pW  = pBP.polar_pt(pBP.angle_to(pR)+dartAng, rad)
        
        opp = ((fh1 - bh0 - bh1) + 1.5 + bhH + 1.5) - (pD.gety() - pW.gety())
        adj = math.sqrt(siz['Shoulder']*siz['Shoulder'] - opp*opp)     
        pX  = pW - Point(adj, opp)       
                
        # pMid = pBP   # to kill pMid
    
        mpt  = pX.mid_pt(pW)
        pMid = pBP.polar_pt(pBP.angle_to(mpt)-dartAng, pBP.distance_to(mpt))
        pW   = mpt  #check
    
        ''' Inside dart '''
        
        pV1 = pF.pol_Lt(h2w2)
        pV2 = pF.pol_Lt(h2w3)
        pV0 = pF1.pol_Lt(h1w3)
        self.fntWaistDart = Lines([pV0, pV1, pBP, pV2, pV0])
        
        # front neck circular points
        rad = ((h0w2*h0w2) + (fhS*fhS)) / (2. * min(h0w2, fhS))  
        cpt = pR.pol_Rt(rad)  if fhS > h0w2 else  pS.pol_Up(rad)
        #        [0   1   2]  3   4    5    6    [7]  8   9  10  11   12   [13  14   15]  16
        cnpts = [pZ, pT1, pY, pX, pW, pBP, pMid, pR, pS, pC, pF, pF1, pF2, pA2, pA1, pAA, pZ]
             
        splines = Spline2D(cnpts[:4]).getSpline() + [3,4,5,6] + \
                  self.__getCircularPline(cpt, pR, pS) + [8,9,10,11,12] + \
                  Spline2D(cnpts[13:]).getSpline() + [16]                   
     
        shape = [cnpts[i]  if type(splines[i]) is int else [cnpts[i]]+splines[i]  for i in range(len(cnpts))]
        self.fntBodice1Shape = Lines(shape)
        
        fbofs = Offset2D( Lines(shape[12:]).getVrtxs(), 2.4)
        fbofs.appendNextPtsAry( Lines(shape[:9]).getVrtxs(), 0.8)
        self.fntBodice1Ofset = fbofs.getPts()
        
        
       
    def __getCircularPline(self, cpt, pt1, pt2, inc=0.1, d=0.05 ):
        ''' Circular polyline points '''
        an1 = cpt.angle_to(pt1)                          
        an2 = cpt.angle_to(pt2)
        rad = cpt.distance_to(pt1)
        
        splin = []
        for i in range(10):   
            ani = an1 + (an2 - an1) * (d + (i * inc))         
            splin += [ cpt.polar_pt(ani, rad) ]
            
        return [ splin ]   
        
#--------------------------------------------------------------        
             
    def BasicSleeve(self):
        ''' Basic Bodice Sleeve '''
        siz = { k:v for k,v,d in self.BodySizes }
        
        fntAsCurve = self.fntBodice1Shape.getSlice(0, 2) # Front ArmSche Curve
        bakAsCurve = self.bakBodice1Shape.getSlice(0, 2) # Back ArmSche Curve
        
        y0 = fntAsCurve.getVrtxs()[0][1]
        y1 = y0 + siz['ArmScyeDepth'] * (0.5 / 3.)
        y2 = y0 + siz['ArmScyeDepth'] * (1.0 / 3.)     
        y3 = y0 + siz['ArmScyeDepth'] * (2.0 / 3.)
        
        
        pAF, Len1, Len2 = fntAsCurve.HorLineInters(y1)
        
        hyp = Len2 + 1.25 # fun to be created
        opp = y3 - y1;
        adj = math.sqrt(hyp*hyp - opp*opp);
        pAG = Point(pAF.getx()-adj, y3)
        
        hyp = Len1 - 0.38
        opp = y1 - y0
        adj = math.sqrt(hyp*hyp - opp*opp);
        pAI = Point(pAF.getx()+adj, y0)
        
        
        pAD, Len1, Len2 = bakAsCurve.HorLineInters(y2)
        
        hyp = Len2 + 1.25
        opp = y3 - y2
        adj = math.sqrt(hyp*hyp - opp*opp)
        pAH = Point(pAG.getx()-adj, y2)
        
        hyp = Len1 - 0.38
        opp = y2 - y0
        adj = math.sqrt(hyp*hyp - opp*opp)
        pAJ = Point(pAH.getx()-adj, y0)
        
        
        pt1 = pAF.mid_pt(pAI).polar_pt(pAF.angle_to(pAI)-math.pi*0.5, 1.)
        pt2 = pAF.mid_pt(pAG).polar_pt(pAF.angle_to(pAG)-math.pi*0.5, 2.)
        pt3 = pAH.mid_pt(pAG).polar_pt(pAH.angle_to(pAG)-math.pi*0.5, 1.)
        pt4 = pAH.mid_pt(pAJ).polar_pt(pAH.angle_to(pAJ)-math.pi*0.5, 0.75)
          
        pAL = pAJ - Point(-2., siz['SleeveLength'])
        pAM = pAI - Point( 2., siz['SleeveLength'])
        
        #        [0    1    2    3    4    5    6    7]   8    9    10   11  
        cnpts = [pAI, pt1, pAF, pt2, pAG, pt3, pAH, pt4, pAJ, pAL, pAM, pAI];
        
        splines = Spline2D(cnpts[:9]).getSpline() + [8,9,10,11]
        
        shape = [cnpts[i]  if type(splines[i]) is int else [cnpts[i]]+splines[i]  for i in range(len(cnpts))]
        self.BodiceSleeve = Lines(shape)
        
        self.Sleeve1Ofset = Offset2D( Lines(shape).getVrtxs(), 0.8).getPts()
         
        
          
######################################################################     
     
class Lines():
    '''
    classdocs
    '''
    def __init__(self, pts=[]):
        '''
        Constructor
        '''      
        self.pts = pts
        
        
    def __repr__(self): 
        
        s0 ='\n'
        for pts in self.pts:
            if pts.__class__.__name__=='Point':
                s0 += 'P{!s}'.format(pts)
                s0 += '\n'
            else:
                s0 += '  '.join('P{}{!s}'.format(i, pts[i]) for i in range(len(pts)) ) 
                s0 += '\n'
                
        return s0
       
        
    def getSlice(self, fm, to):   
        return Lines(self.pts[fm:to+1])
           
           
    def getVrtxs(self):
        return [pt.getxy() for pt in self.getflatlst()] 
        
        
    def getflatlst(self):
        fpts=[]
        self.doflat(self.pts, fpts) 
        return fpts
          
          
    def doflat(self, pts, fpts):
        ''' Flattening list ''' 
        if pts.__class__.__name__=='Point':
            fpts += [ pts ]   
        else:
            for pt in pts:
                self.doflat(pt, fpts) 
                
                    
                     
    def HorLineInters(self, y0):
        '''  Intersection of curve with Horizontal line '''
        pts = self.getflatlst()
        for i in range(1, len(pts)):
            if y0 >= pts[i-1].gety() and y0 <= pts[i].gety():
                break
        
        xy = self.LineXLine(*list(pts[i-1].getxy()+pts[i].getxy())+[1.,y0,2.,y0])
        pt = Point(*xy)
        
        len1 = self.getCurveLength(pts[:i]) + pts[i-1].distance_to(pt)                 
        len2 = self.getCurveLength(pts[i:]) + pts[i].distance_to(pt)
    
        return pt, len1, len2
        
        
        
    def getCurveLength(self, pts):
        ''' Poly line length '''
        return sum( [pts[i-1].distance_to(pts[i])  for i in range(1, len(pts))] )
        
        
        
    def LineXLine(self, x1, y1, x2, y2, x3, y3, x4, y4):
        ''' Intersection of two line '''
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
            return [ (B2*C1 - B1*C2)/det, (A1*C2 - A2*C1)/det ]
    
      
###############################################################################

def data2Server(sizes=None):

    if sizes==None:
        sizes = [  37.5,   22.0,  105.0,  40.0,  90.0,  20.0, 
                  117.5,  100.0,  125.0,  12.5,  32.5,  35.0, 
                   22.5,   28.5,   15.0,  14.0  ]    
        
    bdc = BasicBodice(sizes)
    bdcData = bdc.getBodiceOutput()
    
    return bdcData

###############################################################################

if __name__ == "__main__":
    
    values = [  37.5,   22.0,  105.0,  40.0,  90.0,  20.0, 
               117.5,  100.0,  125.0,  12.5,  32.5,  35.0, 
                22.5,   28.5,   15.0,  14.0  ]    
        
    bdc = BasicBodice(values)
    print(bdc)
    '''
    print('getbakBodice')
    bdcdat = bdc.getbakBodice()
    for pts in bdcdat:
        print ( '  '.join('P{}{!s}'.format(i, pts[i]) for i in range(len(pts))) ) 
    '''    
    
###############################################################################  

    '''
    self.NeckCirc     =  37.5
    
    self.ArmScyeDepth =  22.0
    self.BustCirc     = 105.0
    
    self.Nape2Waist   =  40.0
    self.WaistCirc    =  90.0
    
    self.Waist2Hip    =  20.0
    self.HipCirc      = 117.5
    
    self.DressLength  = 100.0
    self.BottomCirc   = 125.0
    
    self.Shoulder     =  12.5
    self.ChestWidth   =  32.5
    self.BackWidth    =  35.0

    self.BreastDist   =  22.5    # to be used
    self.BustHeight   =  28.5    # to be used
    
    self.SleeveLength =  15.0
    self.SleeveCirc   =  14.0
    '''        