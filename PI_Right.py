# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 12:19:37 2022

@author: tju
"""

import pandas as pd
import PI_Left as LF
import math
import os

def find_Lab(Target_L,Target_a,Target_b,c_length=0.01,delta_E=10):
    cC=1
    
    directory=os.getcwd()    
    AllData=LF.import_data(f"{directory}//AllData.xlsx")
    find_result=[]
    i=1
    alln=int((1/c_length)*(1/c_length))
    
    #Loop search
    while cC>=0:
        cM=0
        cY=1-cC-cM
        while cY>=0:
            comp_Slambda=LF.complex_Slambda(AllData,cC,cM,cY)
            print(f"processing progress:{i}/{alln}")
            a=LF.XYZ(AllData,comp_Slambda)
            result_c=LF.caculation(a[0],a[1],a[2])
            delta=math.sqrt((result_c[0]-Target_L)**2+(result_c[1]-Target_a)**2+(result_c[2]-Target_b)**2)
            if delta<delta_E:
                decision=True
                find_result.append((cC,cM,cY,delta,decision))
            
            #Recalculate cM, cY
            cM +=c_length
            cY=1-cC-cM
            i+=1
        cC -=c_length
    
    #Determine whether there is a solution
    if len(find_result)==0:
        return "No solution!"
    else:
        # Convert to DataFrame output
        find_pd=pd.DataFrame(find_result)
        find_pd.columns=["C_Ratio","M_Ratio","Y_Ratio","Delta","Solution"]
        return find_pd

if __name__=='__main__': 
   L=float(input('Please enter the target L value:'))
   a=float(input('Please enter the target a value:'))
   b=float(input('Please enter the target b value:'))
   length=float(input('Please enter the concentration gradient, recommended (0.001, 0.005, 0.01):'))
   delta=int(input('Please enter the target threshold value:'))
   
   solution=find_Lab(L, a, b,length, delta)
   solution.sort_values(by='Delta', ascending=True, inplace=True, ignore_index=True)
   print(solution)
   