import sys
import random

#for reading data file 
datafile=sys.argv[1]
file=open(datafile)
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
file.close()
#print(data)

#for reading training labels
labelfile=sys.argv[2]
f2=open(labelfile)
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
    if trainlabels.get==0:
        trainlabels[i]=-1
#print(trainlabels)

    
for q in range(0,rows,1):
    a=1
    data[q].append(float(a))

traindata = []
testdata = []   
for i,line in enumerate(data):
   if i in trainlabels.keys():
       traindata.append(line)
   else:
       testdata.append(line)  
    #if i, line in enumerate(data):
    #    print(line)

#print(data)
#type(data)
#print(w0)
w=[]
cols=len(data[0])
for i in range(0,cols,1):
    w.append(random.uniform(-0.01, 0.01))
#print(w)
'''
b=0
for i in range(0,rows,1):
    temp = 0
    for j in range(0,cols,1):
        temp += (w[j] * data[i][j])
    b += temp**2
'''
obj =0

for i in range(len(trainlabels)):
    if trainlabels[i] == 0:
        trainlabels[i] = -1

#if trainlabels.get()==0:
#    trainlabels[i]=-1

for i in range(len(traindata)):
    dot =0
    for j in range(cols):
        #dot[j]=dot[j]+(w[j]*traindata[i][j])
       dot += w[j] * traindata[i][j]
    dot = trainlabels[i] - dot
    obj += dot**2  #obj = obj + temp**2 (temp**2 = temp^2)

#print(obj)
#print(rows,cols)
#print(dot)


  
eta=.001
theta=.001
labels= []
for key in trainlabels.values():
    labels.append(key)
n = 0
while True:
    n += 1
    f=[]
    obj_upd=0
    dot_2=0 
    for i in range(cols):
        f.append(0)
    
    for i in range(len(traindata)):
        temp = 0
        
        #calc wT.x
        for k in range(0,cols,1):
            temp+= w[k]*traindata[i][k]
        
        #calc y-wT.x
        temp = labels[i]-temp
        
        if(trainlabels.get(i)!=None):
           for j in range(0,cols,1):
              f[j]+= temp*(traindata[i][j])
#              print(i, j, '\t', traindata[i][j], '\t', temp)
        
    for j in range(0,cols,1):
        w[j]=w[j] + eta * (f[j])
    
    for i in range(0,len(traindata), 1):
        dot_2 = 0
        for j in range(0,cols,1):
            dot_2 += w[j] * traindata[i][j]
        dot_2 = labels[i] - dot_2
        obj_upd += dot_2**2 
    b= obj - obj_upd
    obj = obj_upd
    if (b < theta):
         break
#print(n)
print('FINAL W:', w[:-1])

#x=[]

for i in range(8,len(data),1): 
    
    temp = 0
    
    for j in range(0,cols,1):
        temp+=  w[j]*data[i][j]
    if temp<0:
#        x.append(0)
        print(0,i)
    if temp>0:
#        x.append(1)
        print(1,i)    
 
w1=0        
for t in range(0,cols-1,1):
    w1+= w[t]**2
w1= w1**0.5 
w0= cols-1 
w2= w[w0]
dist= w2/w1
print(abs(dist))


#wo_den= (w[0]**2 + w[1]**2)
#wo_den1= wo_den ** 0.5 
#dist= w[2]/wo_den1
#print(abs(dist))
    
         
         
         
        



  #W.append(w1[i])W.extend(w0[i])
  #W.append(w2[i])
#print(W[i])

#z=[]
#for i in range(0,rows,1):
    
 #   z= (data[i] * (W[i])) 
#int(z[i])
