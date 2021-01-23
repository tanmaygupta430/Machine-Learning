import sys
import array
import copy
import random

from sklearn import svm
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors.nearest_centroid import NearestCentroid
from tqdm import tqdm

def extract_Column(arg_matrix, i):
    return [[row[i]] for row in arg_matrix]

def merge_Column(a, b):
    return [x + y for x, y in zip(a, b)]

def CreateDataSet(fea, dat):
    newData = extract_Column(dat, fea[0])
    fea.remove(fea[0])
    length = len(fea)
    for i in range(0, length, 1):
        temp = extract_Column(dat, fea[0])
        newData = merge_Column(newData, temp)
        fea.remove(fea[0])
    return newData

def Pearson_Correlation(x, y, fi):
    sumX = 0
    sumX2 = 0
    ro = len(x)
    co = len(x[0])
    switch = 0
    pc = array.array("f")
    for i in tqdm(range(0, co, 1)):
        switch += 1
        sumY = 0
        sumY2 = 0
        sumXY = 0
        for j in range(0, ro, 1):
            if (switch == 1):
                sumX += y[j]
                sumX2 += y[j] ** 2
            sumY += x[j][i]
            sumY2 += x[j][i] ** 2
            sumXY += y[j] * x[j][i]
        r = (ro * sumXY - sumX * sumY) / ((ro * sumX2 - (sumX ** 2)) * (ro * sumY2 - (sumY ** 2))) ** (0.5)
        pc.append(abs(r))

    savedforPrinting = array.array("f")
    my_Features = array.array("i")
    for i in tqdm(range(0, fi, 1)):
        selectedFeatures = max(pc)
        savedforPrinting.append(selectedFeatures)
        feature_Index = pc.index(selectedFeatures)
        pc[feature_Index] = -1
        my_Features.append(feature_Index)
    return my_Features

print("Reading data file")
# Read data file
datafile = sys.argv[1]
data = []
with open(datafile, "r") as infile:
    for line in infile:
        temp = line.split()
        l = array.array("i")
        for i in temp:
            l.append(int(i))
        data.append(l)

# Read labels from file

label_file = sys.argv[2]
train_labels = array.array("i")
with open(label_file, "r") as infile:
    for line in infile:
        temp = line.split()
        train_labels.append(int(temp[0]))

print("Reading data complete")

feat = 10
rows = len(data)
cols = len(data[0])
rowsl = len(train_labels)

# Dimensionality Reduction
print("Feature Selection started")
neededFea = Pearson_Correlation(data, train_labels, 2000)
print("Done with feature selection", end="")

savedFea = copy.deepcopy(neededFea)
data1 = CreateDataSet(neededFea, data)

clf_svm = svm.SVC(gamma=0.001)
clf_log = linear_model.LogisticRegression()
clf_gnb = GaussianNB()
clf_nc = NearestCentroid()

all_Accuracies = array.array("f")
all_Features = []

accuracy_svm = 0
accuracy_score = 0
accuracy_log = 0
accuracy_gnb = 0
accuracy_nc = 0

my_accuracy = 0

iterations = 5
for i in range(iterations):

    print(i)
    
    rowIDs = []
    for i in range(0, len(data), 1):
            rowIDs.append(i)
    
    random.shuffle(rowIDs)

    trainX, trainY = [], []
    validX, validY = [], []
    
    for i in range(0, int(.9*len(rowIDs)), 1):
            idx = rowIDs[i]
            trainX.append(data1[idx])
            trainY.append(train_labels[idx])
    for i in range(int(.9*len(rowIDs)), len(rowIDs), 1):
            idx = rowIDs[i]
            validX.append(data1[idx])
            validY.append(train_labels[idx])
    
#    X_train, X_test, y_train, y_test = train_test_split(
#        data1, train_labels, test_size=0.3)

    newRows = len(trainX)
    newCols = len(trainX[0])
    newRowst = len(validX)
    newColst = len(validX[0])
    newRowsL = len(trainY)

    Pear_Features = Pearson_Correlation(trainX, trainY, feat)

    all_Features.append(Pear_Features)
    argument = copy.deepcopy(Pear_Features)

    data_fea = CreateDataSet(argument, trainX)

    clf_svm.fit(data_fea, trainY)
    clf_log.fit(data_fea, trainY)
    clf_gnb.fit(data_fea, trainY)
    clf_nc.fit(data_fea, trainY)

    TestFeatures = Pearson_Correlation(validX, validY, feat)

    test_fea = CreateDataSet(TestFeatures, validX)

    len_test_fea = len(test_fea)
    counter_svm = 0
    counter_log = 0
    counter_gnb = 0
    counter_nc = 0
    my_counter = 0
    
    for j in range(0, len_test_fea, 1):
        predLab_svm = int(clf_svm.predict([test_fea[j]]))
        predLab_log = int(clf_log.predict([test_fea[j]]))
        predLab_gnb = int(clf_gnb.predict([test_fea[j]]))
        predLab_nc = int(clf_nc.predict([test_fea[j]]))
        h = predLab_svm + predLab_log + predLab_gnb + predLab_nc
        if (h >= 3):
            my_predLab = 1
        elif (h <= 1):
            my_predLab = 0
        else:
            my_predLab = predLab_svm
        if (my_predLab == validY[j]):
            my_counter += 1
        if (predLab_svm == validY[j]):
            counter_svm += 1
        if (predLab_log == validY[j]):
            counter_log += 1
        if (predLab_gnb == validY[j]):
            counter_gnb += 1
        if (predLab_nc == validY[j]):
            counter_nc += 1


    accuracy_svm += counter_svm / len_test_fea
    accuracy_log += counter_log / len_test_fea

    accuracy_gnb += counter_gnb / len_test_fea
    accuracy_nc += counter_nc / len_test_fea

    my_accuracy += my_counter / len_test_fea
    all_Accuracies.append(my_counter / len_test_fea)


bestAc = max(all_Accuracies)
bestInd = all_Accuracies.index(bestAc)
best_Features = all_Features[bestInd]

print("\nFeatures: ", feat)

originalFea = array.array("i")
for i in range(0, feat, 1):
    realIndex = savedFea[best_Features[i]]
    originalFea.append(realIndex)

print("The features are: ", originalFea)
feature_file = open("features", "w+")
for i in range(0, len(originalFea), 1):
    feature_file.write(str(originalFea[i]) + "\n")

# Calculate Accuracy
argument1 = copy.deepcopy(originalFea)
Acc_Data = CreateDataSet(argument1, data)

clf_svm.fit(Acc_Data, train_labels)
clf_log.fit(Acc_Data, train_labels)
clf_gnb.fit(Acc_Data, train_labels)
clf_nc.fit(Acc_Data, train_labels)

svm_counter = 0
LeCounter = 0
k = len(Acc_Data)
for i in range(0, k, 1):
    predLab_svm = int(clf_svm.predict([Acc_Data[i]]))
    predLab_log = int(clf_log.predict([Acc_Data[i]]))
    predLab_gnb = int(clf_gnb.predict([Acc_Data[i]]))
    predLab_nc = int(clf_nc.predict([Acc_Data[i]]))
    h = predLab_svm + predLab_log + predLab_gnb + predLab_nc
    if (h >= 3):
        my_predLab = 1
    elif (h <= 1):
        my_predLab = 0
    else:
        my_predLab = predLab_svm
    if (my_predLab == train_labels[i]):
        LeCounter += 1
    if (predLab_svm == train_labels[i]):
        svm_counter += 1

FinalAcc = LeCounter / k
SVMAc = svm_counter / k
print("Accuracy: ", FinalAcc * 100)

# Read Test data
test_file = sys.argv[3]
test_data = []
with open(test_file, "r") as infile:
    for line in infile:
        temp = line.split()
        l = array.array("i")
        for i in temp:
            l.append(int(i))
        test_data.append(l)

argument2 = copy.deepcopy(originalFea)
test_data1 = CreateDataSet(argument2, test_data)

# create a file
f1 = open("testLabels.txt", "w+")

for i in range(0, len(test_data1), 1):
    lab1 = int(clf_svm.predict([test_data1[i]]))
    lab2 = int(clf_log.predict([test_data1[i]]))
    lab3 = int(clf_gnb.predict([test_data1[i]]))
    lab4 = int(clf_nc.predict([test_data1[i]]))
    h = lab1 + lab2 + lab3 + lab4
    if (h >= 3):
        f1.write(str(1) + " " + str(i) + "\n")
    elif (h <= 1):
        f1.write(str(0) + " " + str(i) + "\n")
    else:
        f1.write(str(lab1) + " " + str(i) + "\n")

print("\nPredicted labels of the test data are saved in testLabels file")
print("Done everything")