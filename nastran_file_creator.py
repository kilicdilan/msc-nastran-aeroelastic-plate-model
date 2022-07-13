# Nastran Input File Creator (SOL103)

import os
import csv
from numpy import true_divide
import mainfile_nastran as ns
import numpy as np
import matplotlib.pyplot as plt
import math
import time

codePath = os.path.dirname(os.path.realpath(__file__)); os.chdir(codePath)


#-------------------------------------
#Define Variable Limits
#-------------------------------------
VarLim = np.zeros((8,2))
"""
VarLim[0,:] = [35,55]       #Sweep at c/4
VarLim[1,:] = [0.4,0.75]    #Taper ratio
VarLim[2,:] = [0.6,0.9]     #Span
VarLim[3,:] = [2E9,4E9]     #E11
VarLim[4,:] = [2E8,6E8]     #G12
VarLim[5,:] = [360,390]     #Density
VarLim[6,:] = [45,90]      #Material oritentation
#VarLim[7,:] = [0.5,0.9]     #Mach number
"""


#Base - 503
VarLim[0,:] = [45,45]       #Sweep at c/4
VarLim[1,:] = [0.66,0.66]    #Taper ratio
VarLim[2,:] = [0.762,0.762]     #Span
VarLim[3,:] = [3.15106E9,3.15106E9]     #E11
VarLim[4,:] = [4.39218E8,4.39218E8]     #G12
VarLim[5,:] = [381.98,381.98]     #Density
VarLim[6,:] = [45,45]      #Material oritentation

"""

#361.9861024847676 m/s - 501
VarLim[0,:] = [53.58289672866801,53.58289672866801]       #Sweep at c/4
VarLim[1,:] = [0.5051902091397895,0.5051902091397895]    #Taper ratio
VarLim[2,:] = [0.697218164592212,0.697218164592212]     #Span
VarLim[3,:] = [3492716644.25987,3492716644.25987]     #E11
VarLim[4,:] = [498266750.69463426,498266750.69463426]     #G12
VarLim[5,:] = [383.5505390637289,383.5505390637289]     #Density
VarLim[6,:] = [47.1935853079916,47.1935853079916]      #Material oritentation
"""
	
	
"""
# SLSQP - 502
#362.11464978 m/s
VarLim[0,:] = [53.677543673728515,53.677543673728515]       #Sweep at c/4
VarLim[1,:] = [0.5046929087361638,0.5046929087361638]    #Taper ratio
VarLim[2,:] = [0.6927402359926341,0.6927402359926341]     #Span
VarLim[3,:] = [3373377037.1820135,3373377037.1820135]     #E11
VarLim[4,:] = [491582815.4964578,491582815.4964578]     #G12
VarLim[5,:] = [383.88692657804944,383.88692657804944]     #Density
VarLim[6,:] = [47.2517464227584,47.2517464227584]      #Material oritentation
"""

	
"""
# BFGS - 504
#362.0246124870075 m/s
VarLim[0,:] = [53.682638417352734,53.682638417352734]       #Sweep at c/4
VarLim[1,:] = [0.5048313924995831,0.5048313924995831]    #Taper ratio
VarLim[2,:] = [0.6911320102521049,0.6911320102521049]     #Span
VarLim[3,:] = [3325654074.117793,3325654074.117793]     #E11
VarLim[4,:] = [489819125.42341727,489819125.42341727]     #G12
VarLim[5,:] = [383.9946248684892,383.9946248684892]     #Density
VarLim[6,:] = [47.242708615500106,47.242708615500106]      #Material oritentation
"""



# Genetic - 600
#362.0246124870075 m/s
VarLim[0,:] = [3.93773795e+01,3.93773795e+01]       #Sweep at c/4
VarLim[1,:] = [7.09624247e-01,7.09624247e-01]    #Taper ratio
VarLim[2,:] = [6.33829117e-01,6.33829117e-01]     #Span
VarLim[3,:] = [3.99585806e+09,3.99585806e+09 ]     #E11
VarLim[4,:] = [2.00026174e+08,2.00026174e+08]     #G12
VarLim[5,:] = [ 3.75597347e+02, 3.75597347e+02]     #Density
VarLim[6,:] = [8.50157298e+01,8.50157298e+01]      #Material oritentation


#-------------------------------------
# Read and Scale Sampling
#-------------------------------------
#Sampling file name
i_ini =  600 #int(sys.argv[1]) #input("Initial: ")
i_fin =  601 #int(sys.argv[2]) #input("Final: ")
smplName = "halton_structural.csv" #str(sys.argv[3])
caseFolder = "01_Case_Data" #str(sys.argv[4])

#Find number of samples
with open(codePath+"/00_Base_Files/"+smplName, newline='') as csvfile:
    data= list(csv.reader(csvfile))
    a1 = data[0]
    Nvar = len(a1)
    NSamples = len(data)

VarN = np.zeros((Nvar,NSamples))  #Normalized variable array
Var  = np.zeros((Nvar,NSamples))  #Variable array
with open(codePath+"/00_Base_Files/"+smplName, newline='') as csvfile:
    data= list(csv.reader(csvfile))
    for i in range(NSamples):
        a = data[i]
        for j in range(Nvar):            
            VarN[j,i] = a[j]
for i in range(Nvar):
    Var[i,:] = np.interp(VarN[i,:], (VarN[i,:].min(), VarN[i,:].max()), (VarLim[i,0], VarLim[i,1]))


    
inputPath = codePath+"/"+"02_Case_Inputs"
try:
    os.mkdir(inputPath)
except:
    print("Input directory already exists")
    
targetPath = codePath+"/"+"03_Case_Targets"
try:
    os.mkdir(targetPath)
except:
    print("Target directory already exists")

csvErr = codePath+"/"+"Error_Case_"+str(i_ini)+"_"+str(i_fin)+".csv"
# -------------------------------------
# Main Iteration
#-------------------------------------
start=time.process_time()
for i in range(int(i_ini),int(i_fin)):
    caseName="AGARDSOL103_"+str(i)    
    casePath = codePath+"/"+caseFolder+"/"+caseName
    caseName2="AGARDSOL145_"+str(i)    
    casePath2 = codePath+"/"+caseFolder+"/"+caseName2
    try:
        os.mkdir(casePath)
    except:
        print("Case directory already exists")

    soltype="SOL 103"
    soltype2="SOL 145"
    airfoil_dat="agard_coord"
    
    #-------------------------------------
    # Define Case Properties
    #-------------------------------------
    
    matprop={'E11':3.15106E9,'E22':4.16218E8,'v12':.31,
             'G12':4.39218E8,'G23':"",'G13':"",'density':381.98}
    
    elem={'x_axis':10,'y_axis':20,'mat_orien':45}
    
    wing_param={'sweep':45,'taper':0.66,'chord':0.5578,'span':0.762,'bcs':"cantilever"}
    
    flutter_param={'mach':0.9,'min_vel':250,'max_vel':300}
    
    #-------------------------------------
    # NASTRAN Functions
    #-------------------------------------
    mainfile = ns.NASTRAN(soltype,soltype2,caseName,codePath,casePath,inputPath,targetPath,
                          matprop,elem,wing_param,flutter_param,airfoil_dat,Var[:,i])
    
    
    upper_coords, lower_coords=mainfile.read_coords()
    
    #Interpolate root values
    upper_interpR,lower_interpR,node_interpR=mainfile.interpolate_coords(np.linspace(0.0, 
                                              wing_param['chord'], elem['x_axis']+1))
    
    num_grids,num_nodes,sweep_le,grid_points,grid_points_y=mainfile.make_grids()
    
    
    grid_thicks=mainfile.make_thick(upper_interpR)
    
    
    #-------------------------------------
    # RUN SOL103
    #-------------------------------------
    print("==============================")
    print(" Started For Case: "+caseName)
    print("==============================") 
    # Write BDF for SOL103
    mainfile.writeBDF()
    
    # Run BDF for SOL103
    mainfile.runBDF()
    
    # Read F06 for SOL103
    NatFreq=mainfile.READF06()

    #-------------------------------------
    # RUN SOL145
    #-------------------------------------
    print("==============================")
    print(" Started For Case: "+caseName2)
    print("==============================") 
    # Write BDF for SOL145
    mainfile.writeBDFSOL145(caseName2)

    # Run BDF for SOL145
    mainfile.runBDFSOL145(caseName2)
    
    """
    # Read F06 for SOL145
    try:
        FlutterResults=mainfile.READF06SOL145(caseName2)
    except:
        with open(csvErr, "a") as file:
            file.write(str(i)); file.write(",")
            file.write("\n")
    """
    
    
    
        
    #-------------------------------------
    # Extract CNN Input & Target Files
    #-------------------------------------
    mainfile.WRITEinputs()
    mainfile.WRITEtargets(caseName2)
    
    #-------------------------------------
    # Plotting
    #-------------------------------------
    x= np.array(grid_points)
    y = np.array(grid_points_y)
    z = np.array(grid_thicks)
    
    
    fig = plt.figure(figsize=(6,5))
    left, bottom, width, height = 0.0, 0.0, 0.8, 0.8
    ax = fig.add_axes([left, bottom, width, height]) 
    
    cp = ax.pcolor(x, y, z, cmap=plt.cm.coolwarm,edgecolors='k')
    fig.colorbar(cp)
    ax.set_xlabel('x - chord length [m]')
    ax.set_ylabel('y - span length [m]')
    ax.set_title('AGARD 445.6 Wing Thickness Distribution')
    
    textstr = ('$\Lambda$= %.6s$^{\circ}$ \nSpan= %.6s m\n%s x %s Grid Size'
    % (str(wing_param['sweep']),str(wing_param['span']),str(elem['x_axis']),str(elem['y_axis'])))
    
    
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.4)
    
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)
    
    figName="AGARD_thick_dist_"+str(i)
    plt.savefig(casePath+'/'+figName+'.png', dpi=300,bbox_inches='tight')
    
   
    
end=time.process_time()
    
print(f"Total Evaluation Time for Case Number: {i_fin-i_ini} ==> {end-start}min")