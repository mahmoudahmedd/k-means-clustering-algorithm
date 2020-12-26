import pandas as pd
import numpy as np

import random
from math import sqrt


def parseExcelFile(_fileName):
    # The name of your excel file
    fileName = _fileName
    
    # Read an Excel table into a pandas DataFrame
    df = pd.io.excel.read_excel(fileName, engine='openpyxl')

    # DataFrame to list
    df = df.values.tolist()
    
    # Shows headers with top 5 rows
    # print(df[:5])
    
    return df

def generateK(_df, _k):
    centers = []
    samples = random.sample(range(0, len(_df) - 1), _k)
    
    for i in range(0, len(samples)):
        centers.append(_df[samples[i]][1:])
    
    assignments = []
    for i in range(0, _k):
        assignments.append([])
    
    return centers, assignments

def distance(_center, _point):
    # dimensions + 1 for Student ID
    dimensions = len(_center) - 1
    
    summation = 0
    for i in range(0, dimensions):
        summation += (_center[i] - _point[i + 1]) ** 2
    return sqrt(summation)

def assignPoints(_df, _centers, _assignments):
    assignments = []
    for i in range(0, len(_centers)):
        assignments.append([])
    
    for i in range(0, len(_df)):
        minimumDistance = 999999999
        
        index = 0
        for j in range(0, len(_centers)):
            d = distance(_centers[j], _df[i])
            
            if(d < minimumDistance):
                index = j
                minimumDistance = d
            
        assignments[index].append(_df[i])
        
    return assignments

# Calculate center for each assigned group
def updateCenters(_assignments):
    k = len(_assignments)
    assignments = []
    for i in range(0, k):
        assignments.append([])

    
    for i in range(0, k):
        avg = []
        for k in range(0, 21):
            avg.append(0)
        
        for j in range(0, len(_assignments[i])):
            avg = np.sum([avg, _assignments[i][j]], axis=0)

        if(len(_assignments[i]) != 0):
            avg = np.divide(avg, len(_assignments[i]))
            avg = avg.tolist()
        
        assignments[i] = avg[1:]
    return assignments

# Input
k = 2

df = parseExcelFile('Course Evaluation .xlsx')
centers, assignments = generateK(df, k)

new = assignPoints(df, centers, assignments)
old = None
newCenters = []
while new != old:
    newCenters = updateCenters(new)
    old = new
    new = assignPoints(df, newCenters, old)


for i in range(0, len(new)): 
    print(len(new[i]))
    
    
res = []
for i in range(0, len(new)):
    res.append([])
    for j in range(0, len(new[i])):
        res[i].append([distance(newCenters[i], new[i][j]), new[i][j] ])
    

# Sort by distance
for i in range(0, len(res)):
    res[i] = sorted(res[i],key=lambda x: (x[0]) , reverse=True)


# Detect outlier data
for i in range(0, k):
    out = 2
    for j in range(0, len(res[i])):
        res[i][j].pop(0)
        res[i][j].pop(0)
        
        out = out - 1
        
        if out <= 0:
            break
    

print(res)
    





