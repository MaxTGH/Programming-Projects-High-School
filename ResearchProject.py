import numpy as np 
import pandas as pd
import sqlite3
import math as m

#reading excel files for each tank
tankA = pd.read_excel(
    '/Users/maxni/research/data.xlsx', 
    sheet_name='Tank A',                              
    header=0)                                          
print(tankA)

tankB = pd.read_excel(
    '/Users/maxni/research/data.xlsx', 
    sheet_name='Tank B',
    header=0)

tankC = pd.read_excel(
    '/Users/maxni/research/data.xlsx', 
    sheet_name='Tank C',
    header=0)

tankD = pd.read_excel(
    '/Users/maxni/research/data.xlsx', 
    sheet_name='Tank D',
    header=0)


connection = sqlite3.connect('/Users/maxni/sqlite/Atest.db')
hardnessCollectionSeries = []
hardnessCollectionList = []
dataCollection = [tankA, tankB, tankC, tankD] #grouping them into a list


for i in range(4):
    dataCollection[i].to_sql(name = "Tank " + str(i+1), con = connection, if_exists = "replace", index = False, 
                 dtype = {'Temperature (°C)':'real', 'Salinity (ppt)': 'real','DO (mg/L)':'real', 'pH':'real',      #creating sql file for the data from each tank
                          'SPC (μS/cm)':'real', 'Iron (ppm)':'real','Copper (ppm)':'real','Nitrate (ppm)':'real',
                          'Nitrite (ppm)':'real','Hardness (ppm)':'real'}) 
    hardnessCollectionSeries.append[dataCollection[i].loc[:,"Hardness (ppm)"]] #extracting the hardness data and putting it into a list 
    hardnessCollectionSeries[i].to_sql(name = "Hardness of Tank " + str(i+1), con = connection, if_exists = "replace", index = False,     #creating sql file for hardness data from each tank
                 dtype = {'Hardness':'real'})

    
hardnessCollectionList.append[hardnessCollectionSeries[i]["Hardness (ppm)"].tolist()] #changing the series to a list 
hardnessCollectionList.pop[0]
testValues = []
#complete a paired t-test for each set of data
for i in range(4):
    start = hardnessCollectionList[i][0]
    end = hardnessCollectionList[i][-1]
    std = np.std(hardnessCollectionList)
    n = len(hardnessCollectionList)
    t = (start - end) / (std * m.sqrt(n))
    testValues.append(t)                 #Append t-test values to the list

print(testValues)

#compare value from test to critical value and see if it is significantly different
for i in range(4):
    string = "Tank " + str(i+1)
    if testValues[i] < 1.7207:               #critical Value
        string += " True"
    else:
        string += " False"
    print(string + "\n")
        





