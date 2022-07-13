
import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import math
import pandas as pd
from scipy import interpolate
from scipy.interpolate import BSpline
from scipy.interpolate import CubicSpline
from decimal import Decimal
import datetime

class NASTRAN:

    def __init__(self, soltype,soltype2,caseName,codePATH,casePATH,inputPath,targetPath,matprop,elem,wing_param,flutter_param,airfoil_dat,Var):
        self._soltype        = soltype
        self._soltype2       = soltype2
        self._caseName       = caseName
        self._codePATH       = codePATH
        self._casePATH       = casePATH 
        self._inputPath      = inputPath
        self._targetPath     = targetPath
        self._matprop        = matprop
        self._elem           = elem
        self._wing_param     = wing_param
        self._flutter_param  = flutter_param
        self._airfoil_dat    = airfoil_dat
        self.Var             = Var
        self._nameBDF        = self._casePATH+"/"+self._caseName+".bdf"
        
        
        #Define design parameters        
        self._wing_param['sweep']   =Var[0]
        self._wing_param['taper']   =Var[1]
        self._wing_param['span']    =Var[2]
        self._matprop['E11']        =Var[3]
        self._matprop['G12']        =Var[4]
        self._matprop['density']    =Var[5]
        self._elem['mat_orien']     =Var[6]
        #self._flutter_param['mach'] =Var[7]
        
        
        
    def writeBDF(self):
        bdfFile = open(self._nameBDF, "w")
        bdfFile.close()
        
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")
            file.write("$ Nastran SOL103 BDF Creator Script - 2D shell \n")
            file.write("$ ITU GE CNN Project \n")
            file.write("$ developed by  : Dilan Kilic (kilicd15@itu.edu.tr) \n")
            file.write("$ created on    : "+str(datetime.datetime.now())[:-7]+"\n")
            file.write("$ Aerospace MDO Lab 2022 \n")
            file.write("$ ============================== \n")

        self.writeHEADER()
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")

        self.writeELEMENTS()
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")
            
        self.writeMAT()
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")
            
        self.writeNODES()
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")
            
        self.writeLBCS()
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")
                
        with open(self._nameBDF,"a") as file:
            file.write("$ Referenced Coordinate Frames \n")
            file.write("ENDDATA 37771225")
            file.write("\n")
       
    def writeBDFSOL145(self,caseName2):
        self._nameBDF = self._casePATH+"/"+caseName2+".bdf"
        bdfFile = open(self._nameBDF, "w")
        bdfFile.close()
        
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")
            file.write("$ Nastran SOL145 BDF Creator Script - 2D shell \n")
            file.write("$ ITU GE CNN Project \n")
            file.write("$ developed by  : Dilan Kilic (kilicd15@itu.edu.tr) \n")
            file.write("$ created on    : "+str(datetime.datetime.now())[:-7]+"\n")
            file.write("$ Aerospace MDO Lab 2022 \n")
            file.write("$ ============================== \n")

        self.writeHEADERSOL145()
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")

        self.writeELEMENTS()
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")
            
        self.writeMAT()
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")
            
        self.writeNODES()
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")
            
        self.writeLBCS()
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")
            
        self.writeFLUT()
        with open(self._nameBDF,"a") as file:
            file.write("$ ============================== \n")
                
        with open(self._nameBDF,"a") as file:
            file.write("$ Referenced Coordinate Frames \n")
            file.write("ENDDATA 37771225")
            file.write("\n")

        
    def writeHEADER(self):
        with open(self._nameBDF,"a") as file: 
            file.write("$ MSC.Nastran input file \n")
            file.write("$ Patran 2019 \n")
            file.write("$ Direct Text Input for Nastran System Cell Section \n")
            file.write("$ Normal Modes Analysis, Database")
            file.write("\n")
            file.write(str(self._soltype)+"\n")
            file.write("CEND \n")
            file.write("ECHO = NONE \n")
            file.write("$ Using Nastran default values for RESVEC \n")
            file.write("SUBCASE 1 \n")
            file.write("   METHOD = 1 \n")
            file.write("   SPC = 2 \n")
            file.write("   VECTOR(SORT1,REAL)=ALL \n")
            file.write("BEGIN BULK \n")
            file.write("PARAM    POST    0 \n")
            file.write("PARAM   PRTMAXIM YES \n")
            file.write("EIGRL    1              500.     4       0                       MASS \n")
        
    def writeHEADERSOL145(self):
        
        with open(self._nameBDF,"a") as file: 
            file.write("$ MSC.Nastran input file \n")
            file.write("$ Patran 2019 \n")
            file.write("$ Direct Text Input for Nastran System Cell Section \n")
            file.write("$ Normal Modes Analysis, Database")
            file.write("\n")
            file.write(str(self._soltype2)+"\n")
            file.write("TIME 600 \n")
            file.write("CEND \n")
            file.write("ECHO = NONE \n")
            file.write("MAXLINES = 999999 \n")
            file.write("AECONFIG = sup_grp \n")
            file.write("SUBCASE 1 \n")
            file.write("   METHOD = 1 \n")
            file.write("   SPC = 2 \n")
            file.write("   VECTOR(SORT1,REAL)=ALL \n")
            file.write("FMETHOD = 1 \n")
            file.write("AESYMXZ = Symmetric \n")
            file.write("AESYMXY = Asymmetric \n")
            file.write("$ Direct Text Input for this Subcase \n")
            file.write("BEGIN BULK \n")
            file.write("$ Direct Text Input for Bulk Data \n")
            file.write("PARAM    POST    0 \n")
            file.write("PARAM    WTMASS 1. \n")
            file.write("PARAM    SNORM  20. \n")
            file.write("PARAM   PRTMAXIM YES \n")
            file.write("$EIGRL    1                       10      0 \n")
            file.write("EIGRL    1              500.     4       0                       MASS \n")
        
        
    def writeELEMENTS(self):
        with open(self._nameBDF,"a") as file: 
            file.write("$ Elements and Element Properties for region : pshell.1 \n")
            file.write("PSHELL   1       1      .0067    1      1.              .833333")
            file.write("\n")
            file.write('$ Pset: "pshell.1" will be imported as: "pshell.1"')
            file.write("\n")
            
            grid_index=np.zeros((self._elem['y_axis']+1,self._elem['x_axis']+1))
            
            count=0
            
            for j in range(self._elem['y_axis']+1):
                for i in range(self._elem['x_axis']+1):
                    grid_index[j,i]=i+1+count
                count+=self._elem['x_axis']+1
            
            i=0
            z=0
            
            for j in range(self._elem['y_axis']):
                for k in range(self._elem['x_axis']):
                    file.write("CQUAD4   %-4d    1       %-4d    %-4d    %-4d    %-4d   %d." % (int(i+1),int(grid_index[j,k]),int(grid_index[j,k+1]),int(grid_index[j+1,k+1]),int(grid_index[j+1,k]),int(self._elem['mat_orien'])))
                    file.write("      0.")
                    file.write("\n")
                    file.write("                        .%-4.4s   .%-4.4s   .%-4.4s   .%-4.4s" % (str(self.grid_thicks[j,k]).split('.')[1],str(self.grid_thicks[j,k+1]).split('.')[1],str(self.grid_thicks[j+1,k+1]).split('.')[1],str(self.grid_thicks[j+1,k]).split('.')[1]))
                    file.write("\n")
                    i+=1
                    
                    
                
    def writeMAT(self):
        with open(self._nameBDF,"a") as file: 
            file.write("$ Referenced Material Records \n")
            file.write("$ Material Record : mat8.1 \n")
            file.write("$ Description of Material : \n")
            file.write("MAT8*    1              %-4.5E     %-4.5E     .%-4.2s"% (Decimal(self._matprop["E11"]),Decimal(self._matprop["E22"]),str(self._matprop["v12"]).split('.')[1]))
            file.write("\n")
            file.write("*       %-4.5E                                     %-4.6s" % (Decimal(self._matprop["G12"]),str(self._matprop["density"])))
            file.write("\n")
            
    def writeNODES(self):
        with open(self._nameBDF,"a") as file: 
            file.write("$ Nodes of the Entire Model \n")  
            
            count=0
            for i in range(self._elem['y_axis']+1):
                for j in range(self._elem['x_axis']+1):
                    file.write("GRID     %-4.4s            %-6.6s .%-4.4s    0." % (str(count+1),str(self.grid_points[i,j]),str(self.grid_points_y[i,j]).split('.')[1]))
                    file.write("\n")
                    count+=1
        
    def writeLBCS(self):
        with open(self._nameBDF,"a") as file: 
            
            file.write("$ Loads for Load Case : Untitled.SC1 \n")
            file.write("SPCADD   2       1       3")
            file.write("\n")
            file.write("$ Displacement Constraints of Load Set : spc1.3 \n")
            file.write("SPC1     3       126     "+str(self._elem['x_axis']+2)+"      THRU    "+str(((self._elem['x_axis']+1)*(self._elem['y_axis']+1))))
            file.write("\n")
            file.write("$ Displacement Constraints of Load Set : spc1.1\n")
            
            if self._wing_param["bcs"]=="cantilever":
                for i in range((self._elem["x_axis"]+1)*(self._elem["y_axis"]+1)):
                    if i==0 or i==self._elem["x_axis"]:
                        file.write("SPC1     1       126     "+"%s" % str(i+1)+"\n")
                    elif i>0 and i<self._elem["x_axis"]:
                        file.write("SPC1     1       123456  "+ str(i+1)+"\n")         
                    else:
                        file.write("SPC1     1       6       "+"%s" %str(i+1)+"\n")
            
       
    def writeFLUT(self):
        with open(self._nameBDF,"a") as file: 
            
            # Find min and max natural frequencies
            if self.NatFreq[0]<=10:
                minf=self.NatFreq[0]-2
                maxf=math.ceil(self.NatFreq[-1]/10)*10
            else:
                minf=round(self.NatFreq[0]/10)*10
                maxf=math.ceil(self.NatFreq[-1]/10)*10
              
            # Calculate reduced frequency (k)
            """
            if self._flutter_param['mach']<0.6 and self._flutter_param['mach']>0.5:
                vmin=100
                vmax=200
            elif self._flutter_param['mach']<0.7 and self._flutter_param['mach']>0.6:
                vmin=200
                vmax=300
            elif self._flutter_param['mach']>0.7:
                vmin=250
                vmax=350
            """
            vmin=350
            vmax=450
            
            kmin=(2*math.pi*minf*self._wing_param['chord'])/(vmax)
            
            kmax=(2*math.pi*maxf*self._wing_param['chord'])/(vmin)


            file.write("$ MKAERO2 card \n")
            file.write("$ \n")
            file.write("$  Mach-Frequency Pair  .MRG_MK_3 \n")
            file.write("MKAERO2 .9      "+"%-6.6s  .9      %-6.6s" % (str(kmin),str(kmax)))
            file.write("\n")
            file.write("$ \n")
            file.write("$ Aeroelastic Model Parameters \n")
            file.write("PARAM   AUNITS  1. \n")
            file.write("$ \n")
            file.write("$ Aeroelastic Model Parameters \n")
            file.write("$ \n")
            file.write("$ Global Data for Steady Aerodynamics \n")
            file.write("$ \n")
            file.write("$ A half-span model is defined \n")
            file.write("$ \n")
            
            # calculate wing reference area
            wingarea=((self._wing_param['taper']*self._wing_param['chord'])+self._wing_param['chord'])*self._wing_param['span']*0.5
            
            file.write("AERO    0       1.      "+str(self._wing_param['chord'])+"  1.226"+"\n")
            file.write("AEROS   0       0       "+str(self._wing_param['chord'])+"  ")
            file.write("%-6.6s  %-6.6s" %(str(self._wing_param['span']),str(wingarea)))
            file.write("\n")
            file.write("$ \n")
            file.write("$ Flat Aero Surface: plate_1001 \n")
            file.write("$ \n")
            file.write("PAERO1  100001 \n")
            file.write("CAERO1  100001  100001  0       45      15                      1 \n")
            file.write("        0.      0.      0.      %-6.6s  %-6.6s  %-6.6s  0.      %-6.6s" 
                       % (str(self._wing_param['chord']),str(self.grid_points[self._elem['y_axis']][0]),
                          str(self._wing_param['span']),str(self._wing_param['taper']*self._wing_param['chord'])))
            
            file.write("\n")
            file.write("$ Surface Spline: spl_100001 \n")
            file.write("$ \n")
            file.write("SPLINE4 1       100001  1               1               FPS     BOTH \n")
            file.write("AELIST	1	100001	THRU	100675 \n")
            file.write("$ \n")
            file.write("SET1	1	1	THRU	231 \n")
            file.write("$ \n")
            file.write("$ Density Ratios \n")
            file.write("FLFACT  1       .105 \n")
            file.write("$ \n")
            file.write("$ Mach number sets \n")
            file.write("FLFACT  2       .9 \n")
            file.write("$ \n")
            file.write("$ Velocity sets \n")

            #file.write("FLFACT  3       -150.   -160.   -170.   -180.   -190.   -200.   -210. \n")
            #file.write("        -220.   -230.   -240.   -250. \n")

            #file.write("FLFACT  3       -250.   -260.   -270.   -280.   -290.   -300.   -310. \n")
            #file.write("        -320.   -330.   -340.   -350. \n")
            
            
            file.write("FLFACT  3       -350.   -360.   -370.   -380.   -390.   -400.   -410. \n")
            file.write("        -420.   -430.   -440.   -450. \n")
            

            file.write("FLUTTER 1       PK      1       2       3                       .001 \n")
            
    
    def read_coords(self):
        
        # Pre-allocate variable and coordinate arrays
        coordinates = []

        # Read files
        for filecount in range(1):

            # Screen print
            print('Reading the coordinate data file: {}'.format(filecount+1))

            # Read coordinates as dataframe
            try:
                coord_df = pd.read_csv(self._codePATH+"/"+self._airfoil_dat+".csv", usecols=["$ upper_x","$ upper_z","$ lower_x","$ lower_z"])
            except:
                raise Exception('Coordinates cannot be read.')
            
            # Convert dataframes to arrays
            coords = coord_df.to_numpy()
            
            # Store in the class
            coordinates.append(coords)
            coords = np.array(coordinates)
            

            upper_coords=coords[0:, 0:np.shape(coords)[1], 0:2]
            lower_coords=coords[0:, 0:np.shape(coords)[1], 2:]
            
            
            self._upper_coords=upper_coords
            self._lower_coords=lower_coords
            self._coords=coords

        return self._upper_coords, self._lower_coords

    def interpolate_coords(self,x):
        
        upper_x=self._upper_coords[0,0:np.shape(self._coords)[1],0]
        upper_z=self._upper_coords[0,0:np.shape(self._coords)[1],1]
       
        lower_x=self._lower_coords[0,0:np.shape(self._coords)[1],0]
        lower_z=self._lower_coords[0,0:np.shape(self._coords)[1],1]
        
    

        upper_interp= interpolate.splrep(upper_x, upper_z,k=5,s=0)
        upper_interp=interpolate.splev(x, upper_interp)
        
        lower_interp = interpolate.splrep(lower_x, lower_z,k=5,s=0)
        lower_interp=interpolate.splev(x, lower_interp)
        
        node_interp=x
        
        eps=10e-4

        for i in range(len(upper_interp)):
            if abs(upper_interp[i])<eps:
                upper_interp[i]=0
                
        for i in range(len(lower_interp)):
            if abs(lower_interp[i])<eps:
                lower_interp[i]=0
        
        self.upper_interp=upper_interp
        self.lower_interp=lower_interp
        self.node_interp=node_interp        
        
        return self.upper_interp,self.lower_interp,self.node_interp


    def make_grids(self):
        
        num_grids=self._elem['x_axis']*self._elem['y_axis']
        num_nodes=(self._elem['x_axis']+1)*(self._elem['y_axis']+1)
        

        sweep_le=(self._wing_param['span']/math.tan(self._wing_param['sweep']*math.pi/180))-(self._wing_param['taper']*self._wing_param['chord']/4)    
        
        
        sweep_le=(self._wing_param['span'])/(sweep_le+(self._wing_param['chord']/4))
        
        sweep_in=math.degrees(math.atan(sweep_le))
        
        sweep_le=90-sweep_in

        
        
        tip_le=self._wing_param['span']/math.tan(sweep_in*math.pi/180)
        tip_chord=self._wing_param['taper']*self._wing_param['chord']
        
        root_chord=self._wing_param['chord']
        span=self._wing_param['span']
        y_int=span/self._elem['y_axis']
        x_int=root_chord/self._elem['x_axis']
        
        chord_lengths=[]
        k=span-y_int
        l=y_int
        for i in range(self._elem['y_axis']):
            
            chord_lengths.append((k*root_chord+l*tip_chord)/(k+l))
            k-=y_int
            l+=y_int
            

        chord_le=[]
        l=y_int
        for i in range(self._elem['y_axis']):
            chord_le.append(l/(math.tan(sweep_in*math.pi/180)))
            l+=y_int    

        grid_points=np.zeros((self._elem['y_axis']+1,self._elem['x_axis']+1))
        grid_points_y=np.zeros((self._elem['y_axis']+1,self._elem['x_axis']+1))
        grid_points[0]=self.node_interp
        

        for i in range(self._elem['y_axis']):
            grid_points_y[i+1]=y_int*(i+1)
            
            
        for i in range(self._elem['y_axis']):
            grid_points[i+1]=np.linspace(chord_le[i], chord_le[i]+chord_lengths[i], num=self._elem['x_axis']+1)

        self.grid_points=grid_points
        self.grid_points_y=grid_points_y
        self.num_grids=num_grids
        self.num_nodes=num_nodes
        self.sweep_le=sweep_le
        self.chord_lengths=chord_lengths
        
        return self.num_grids,self.num_nodes,self.sweep_le,self.grid_points,self.grid_points_y

    def make_thick(self,upper_interpR):
       
        grid_thicks=np.zeros((self._elem['y_axis']+1,self._elem['x_axis']+1))
        grid_thicks[0]=upper_interpR
        
        
        for i in range(self._elem['y_axis']):
            #upper_interp,lower_interp,node_interp=NASTRAN.interpolate_coords(self,np.linspace(0.0,self.chord_lengths[i],self._elem['x_axis']+1))
            upper_interp=upper_interpR*(self.chord_lengths[i]/self._wing_param['chord'])
            grid_thicks[i+1]=upper_interp
            
        self.grid_thicks=grid_thicks
        
        return self.grid_thicks

    def runBDF(self):
        os.chdir(self._casePATH)

        cmd1=' "C:/Program Files/MSC.Software/MSC_Nastran/2019fp1/bin/nast20191.exe" '
        
        os.system(cmd1+self._casePATH+"/"+self._caseName+".bdf")
        
        print("\n")
        print("==============================")
        print(" SOL 103 - MSC Nastran - Completed For Case: "+self._caseName)
        print("==============================") 
        print("\n")
    
    def runBDFSOL145(self,caseName2):
        os.chdir(self._casePATH)

        cmd1=' "C:/Program Files/MSC.Software/MSC_Nastran/2019fp1/bin/nast20191.exe" '
        
        os.system(cmd1+self._casePATH+"/"+caseName2+".bdf")
        
        print("\n")
        print("==============================")
        print(" SOL 145 - MSC Nastran - Completed For Case: "+caseName2)
        print("==============================") 
        print("\n")
    
    def READF06(self):
        
        configfile=self._casePATH+"/"+self._caseName+".f06"
        cfg = open(configfile,'r')

        items=np.zeros((10,7))
        for line in cfg:
            if '$' in line:
                pass

            # Find natural frequencies from .txt
            elif '1         1' in line:
                items[0] = line.split()
            elif '2         2' in line:
                items[1] = line.split()
            elif '3         3' in line:
                items[2] = line.split()
            elif '4         4' in line:
                items[3] = line.split()

        mode_num=4
        NatFreq=[]
        for i in range(mode_num):
            NatFreq.append(items[i,4])
            
        self.NatFreq=NatFreq  
        
        
        return self.NatFreq
    
    
    def READF06SOL145(self,caseName2):
        configfile=self._casePATH+"/"+caseName2+".f06"
        cfg = open(configfile,'r')
        
        
    
    def WRITEinputs(self):
        
        configfile=self._inputPath+"/"+self._caseName+".csv"
        
        
        df = pd.DataFrame(data={"sweep": [self.Var[0]], "taper": [self.Var[1]], "span":[self.Var[2]],
                                "E11":[self.Var[3]],"G12":[self.Var[4]],"mat_den":[self.Var[5]],
                                "mat_orien":[self.Var[6]]})
        
        df.to_csv(configfile, sep=',',index=False)
        
    def WRITEtargets(self,caseName2):
        
        configfile=self._targetPath+"/"+"target_"+self._caseName+".csv"
        
        list_2=[3,4,5]
        
        df = pd.DataFrame(data={"NatFreq": pd.Series(self.NatFreq)})
        
        df.to_csv(configfile, sep=',',index=False)
        
        # Create empty csv file to write flutter velocities
        
        configfile=self._targetPath+"/"+"target_"+caseName2+".csv"
        
        xx=3.0
        
        df = pd.DataFrame(data={"FlutterSpeed": pd.Series(xx)})
        
        df.to_csv(configfile, sep=',',index=False)
