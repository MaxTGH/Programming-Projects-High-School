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
    hardnessCollectionSeries.append(dataCollection[i].loc[:,"Hardness (ppm)"]) #extracting the hardness data and putting it into a list 
    hardnessCollectionSeries[i].to_sql(name = "Hardness of Tank " + str(i+1), con = connection, if_exists = "replace", index = False,     #creating sql file for hardness data from each tank
                 dtype = {'Hardness':'real'})

    
hardnessCollectionList.append(hardnessCollectionSeries[i]["Hardness (ppm)"].tolist()) #changing the series to a list 
hardnessCollectionList.pop[0]
percents = []
#analyze the data
for i in range(4):
    start = hardnessCollectionList[i][0]
    end = hardnessCollectionList[i][-1]
    difference = m.abs(start-end)
    percentChange = difference / start
    percents.append(percentChange)
    std = np.std(hardnessCollectionList)
    n = len(hardnessCollectionList)
    print("Tank " + str(i+1) + "\n" + "Difference: " + str(difference) + "\n" + "Percent Change: " + 
          str(percentChange) + "\n" + "Standard deviation: " + std + "\n" + "Number of Values: ")
#printing values from analyzing data
string = ""
for i in range(4):
    if (int(percentChange[i]) > 0.5):
        string += str(i + 1) + " "
print("Tanks " + string + " had their hardness levels decrease by half.")  