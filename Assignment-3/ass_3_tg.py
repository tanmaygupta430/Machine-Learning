import sys
import random 
eta= 0.001
theta=0.000000001

datafile=sys.argv[1]
a=open(datafile)
data=[]
i=0
fl1=a.readline()
while(fl1!=""):
    x=fl1.split()
    fl2=[]
    for k in range(0,len(x),1):
        fl2.append(float(x[k]))
    data.append(fl2)
    fl1=a.readline()
rows=len(data)
a.close()

labels=sys.argv[2]
fl2=open(labels)
trainlabels={}
no=[]
no.append(0)
no.append(0)
line_2=fl2.readline()
while(line_2!=''):
   b=line_2.split()
   trainlabels[int(b[1])]=int(b[0])
   line_2=fl2.readline()
   no[int(b[0])] +=1
   
for q in range(rows):
     a=1
     data[q].append(float(a))

w=[]
cols=len(data[0])
for i in range(0,cols,1):
   w.append(random.uniform(-0.01,0.01))


w=[]
cols=len(data[0])
for i in range(0,cols,1):
    w.append(random.uniform(-0.01, 0.01))

'''for k,i in enumerate(trainlabels.keys()):
    if trainlabels[i]==0:
        trainlabels[i]=-1
'''

import math
object_1=0
dp=0
for k,i in enumerate(trainlabels.keys()): 
    for j in range(0,cols,1):
        dp= w[j]*data[i][j]
        x= math.log(1/(1+math.exp((-1)*(dp))))
        m= ((-1)*trainlabels[i])*x
        y= math.log((math.exp(-1*dp))/(1+math.exp(-1*dp)))
        n= y*(1-trainlabels[i])
    object_1= m-n
print(object_1)
        
        #dp_1+= data[i][j]*w[j]
    #dp_1= trainlabels[i]*dp_1
    #dp=1-dp_1
    #object_1+=max(0,dp)

dp_2=0
n=0
while True:
    n+=1
    func=[]
    object_2=0
    for i in range(0,len(data[0]),1):
        func.append(0)
    for k,i in enumerate(trainlabels.keys()):
        dp_2=0
        for j in range(0,cols,1):
            dp_2+= data[i][j]*w[j]
        dp_2=trainlabels[i]*dp_2
        if (dp_2<1):
            for j in range(0,cols,1):
                func[j]+=-trainlabels[i]*data[i][j]
    for j in range(0,len(data[0]),1):
         w[j]-=func[j]*eta
    for k,i in enumerate(trainlabels.keys()):
        dp_3=0
        dp_4=0
        for j in range(0,cols,1):
            dp_3+=w[j]*data[i][j]
        dp_3= trainlabels[i]*dp_3    
        dp_4= 1-dp_3
        object_2+= max(0,dp_4)
    n=object_1-object_2
    object_1=object_2
    if abs(n)<theta:
        break
print(w)

for i in range(0,rows,1):
    if i not in trainlabels.keys():
        result=0
        for j in range(0,cols,1):
            result+=w[j]*data[i][j]
        if result<0:
           print(0,i)
        if result>0:
           print(1,i)
           
w1=0
for t in range(0,cols-1,1):
    w1+=w[t]**2
w1=w1**0.5
w0=cols-1
w2=w[w0]
dist=w2/w1
print(abs(dist))        