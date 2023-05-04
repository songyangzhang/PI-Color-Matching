# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 12:19:37 2022

@author: tju
"""

import pandas as pd
import os

#import all data
def import_data(path):
    Taolambda=pd.read_excel(path,sheet_name="Tau")
    Taolambda['Wavelength']=Taolambda['Wavelength'].astype("float")
    b=[]
    for i in range(0,len(Taolambda)):
        b.append(i)
    Taolambda=Taolambda.iloc[b]
    print(Taolambda)
    
    Tenlambda=pd.read_excel(path,sheet_name="TenLambda")
    Tenlambda['Wavelength']=Tenlambda['Wavelength'].astype("float")
    print(Tenlambda)
    CMY=pd.read_excel(path,sheet_name="CMY")
    CMY['Wavelength']=CMY['Wavelength'].astype("float")   

    #Data initial processing
    FirstData=pd.merge(left=Taolambda,right=Tenlambda,how='left',on='Wavelength')   
    AllData=pd.merge(left=FirstData,right=CMY,how='left',on='Wavelength')[12:-10]
    print(AllData)
    return AllData


#Define absorbance to transmittance
def AtoT(A):
    return pow(10,-A)  


# Calculate the absorbance and transmittance of the ternary mixed film
def complex_Slambda(AllData,C1,C2,C3):
    comp_Slambda=pd.DataFrame()
    comp_Slambda["Wavelength"]=AllData["Wavelength"]
    comp_Slambda["complex_Abs"]=19*(C1*AllData['CA/um']+C2*AllData['MA/um']+C3*AllData['YA/um'])
    comp_Slambda["T"]=comp_Slambda["complex_Abs"].map(AtoT)
    return comp_Slambda


def absorbance(path,abs1=1):
    absorbance_lambda=pd.read_excel(path,sheet_name="Absorbance")
    absorbance_lambda['Wavelength']=absorbance_lambda['Wavelength'].astype("float")
    absorbance_lambda["T"]=absorbance_lambda.iloc[:,abs1].map(AtoT)
    return absorbance_lambda
    
  
#Calculate XYZ
def XYZ(AllData,comp_Slambda):    
    K=100/((AllData['y10']*AllData['Energy']).sum())
    X=K*(((AllData['x10']*AllData['Energy'])*comp_Slambda["T"]).sum())
    Y=K*(((AllData['y10']*AllData['Energy'])*comp_Slambda["T"]).sum())
    Z=K*(((AllData['z10']*AllData['Energy'])*comp_Slambda["T"]).sum())
    return X,Y,Z


#Define f function
def f(XYZ):
    if XYZ>pow(6/29,3):
        return pow(XYZ,1/3)
    else:
        return XYZ*841/108+(4/29)


#Define L, a, b values    
def caculation(X,Y,Z):
    # Several fixed constant values
    X0=94.811
    Y0=100
    Z0=107.304
    Lstar=116*f(Y/Y0)-16
    astar=500*(f(X/X0)-f(Y/Y0))
    bstar=200*(f(Y/Y0)-f(Z/Z0))
    return(round(Lstar,4),round(astar,4),round(bstar,4))


if __name__=='__main__': 
    directory=os.getcwd()
    path=f"{directory}//AllData.xlsx"
    AllData=import_data(path)
      
    comp_Slambda=absorbance(path,1)
    comp_Slambda2=pd.merge(left=AllData,right=comp_Slambda,how='left',on='Wavelength')[:441]
    a=XYZ(AllData,comp_Slambda2)
    print(caculation(a[0],a[1],a[2]))

