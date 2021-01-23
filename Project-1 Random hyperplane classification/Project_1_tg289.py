import random
from RandomHyperplane import RandomHyperplane

#Read Data File
DataList = open('Assignment5/climate/climate.data').readlines()
DataList = [line.split() for line in DataList]
DataList = [list(map(float, line)) for line in DataList]
#Read Label File
trainlabels={}
with open('Assignment5/climate/climate.trainlabels.0') as f:
   x = f.readline()
   while x != '':
       a = x.split()
       trainlabels[int(a[1])] = int(a[0])
       x = f.readline()

Labels={}
with open('Assignment5/climate/climate.labels') as f:
   x = f.readline()
   while x != '':
       a = x.split()
       Labels[int(a[1])] = int(a[0])
       x = f.readline()

object=RandomHyperplane(DataList,trainlabels,10000)
p1=object.prediction_orignal()
p2=object.predict_random_hyperplane_data()


value=[]
for i in range(len(DataList)):
    if trainlabels.get(i) is  None:
        value.append(Labels[i])

error_orignal=0
error_hyper=0
for i in range(len(p1)):
    if p1[i]!=value[i]:
        error_orignal+=1
    if p2[i]!=value[i]:
        error_hyper+=1

print(p1)
print(p2)
print(value)
print('Orignal test error:',(error_orignal/len(p1)))
print('hyperplane data test error:',(error_hyper/len(p2)))
