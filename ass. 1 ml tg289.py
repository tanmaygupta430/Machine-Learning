# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 08:07:02 2019

@author: ACER
"""
import sys

#for reading data file 
datafile=sys.argv[0]
file=open("testBayes.data")
data=[]
i=0
l1=file.readline()
while(l1!=''):
    b=l1.split()
    l2=[]
    for j in range(0,len(b),1):
        l2.append(float(b[j]))
    data.append(l2)
    l1=file.readline()
rows=len(data)
cols=len(data[0])
file.close()

#for reading training labels
labelfile=sys.argv[0]
f2=open("testBayes.trainlabels.0")
trainlabels={}
no=[]
no.append(0)
no.append(0)
line=f2.readline()
while(line!=''):
    a=line.split()
    trainlabels[int(a[1])]=int(a[0])
    line=f2.readline()
    no[int(a[0])] +=1
    
#for calculating mean ave_0 and ave_1 
ave_0=[]
for t in range(0,cols,1):
    ave_0.append(1)
ave_1=[]
for t in range(0,cols,1):
    ave_1.append(1)    

for u in range (0, rows, 1):
    if(trainlabels.get(u) != None and trainlabels[u] == 0):
        for t in range(0, cols, 1):
            ave_0[t] = ave_0[t] + data[u][t]
    if(trainlabels.get(u) != None and trainlabels[u] == 1):
        for t in range(0, cols, 1):
            ave_1[t] = ave_1[t] + data[u][t]      
  
for t in range(0, cols, 1):
        ave_0[t] = ave_0[t]/no[0]
        ave_1[t] = ave_1[t]/no[1] 

#for standard deviation dev_0 and dev_1
dev_0=[]
for t in range(0,cols,1):
    dev_0.append(0)
dev_1=[]
for t in range(0,cols,1):
    dev_1.append(0)
    
for u in range(0,rows,1):
    if(trainlabels.get(u)!=None and trainlabels[u]==0):
        for t in range(0,cols,1):
            dev_0[t]=dev_0[t]+(data[u][t]-ave_0[t])**2
            
    if(trainlabels.get(u)!=None and trainlabels[u]==1):
        for t in range(0,cols,1):
            dev_1[t]=dev_1[t]+(data[u][t]-ave_1[t])**2


for t in range(0,cols,1):
    dev_0[t]=dev_0[t]/no[0]**0.5
    dev_1[t]=dev_1[t]/no[1]**0.5

#for naive bayes classifier nv0 and nv1 
for u in range(0,rows,1):
    if(trainlabels.get(u)== None):
        nv0=0
        nv1=0
        for t in range(0,cols,1):
            nv0=nv0+((data[u][t]-ave_0[t])/dev_0[t])**2
            nv1=nv1+((data[u][t]-ave_1[t])/dev_1[t])**2
        if (nv0<nv1):
            print("0",u)
        else:
            print("1",u)

