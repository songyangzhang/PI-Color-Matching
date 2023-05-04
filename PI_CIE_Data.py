# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 09:36:01 2022

@author: tju
"""

import pandas as pd
import os

directory=os.getcwd()
Slambda=pd.read_excel(f"{directory}//DigiData.xlsx")
a=Slambda.groupby('Wavelength')['Energy'].mean()



ma=list(range(801))[301:801]
Wave_eng=[]

for WL in ma:
    x1_index=(list(WL<a.index)).count(False)   
    k=(a.iloc[x1_index]-a.iloc[x1_index+1])/(a.index[x1_index]-a.index[x1_index+1])
       
    y=k*(WL-a.index[x1_index])+a.iloc[x1_index]  
   
    Wave_eng.append([WL,y])
    
CIE_Data=pd.DataFrame(Wave_eng,columns=['Wavelength','Energy'],dtype=float)
print(CIE_Data)

#CIE_Data.to_excel("CIEData.xlsx",encoding='utf-8')