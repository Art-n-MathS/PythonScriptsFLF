#  @author Dr. Milto Miltiadou
#  @date Dec 2022
#  @version 1.0
#
## package main
#  @brief This script takes as input the Spain plot file extract the field data collected during and after a given year
# it exports a .csv file for each year of data available
#
#  how to run: python FixCSVs.py -in <inputFile> -out <outputFileDir> 
#
# example: python "C:/Users/mm2705/Documents/Cambridge/Scripts/PythonScriptsFLF/unwrap.py" -in "C:/Users/mm2705/Documents/Cambridge/Milto_SPSW/L1/Spain/plot234_column.csv" -out "C:/Users/mm2705/Documents/Cambridge/Milto_SPSW/L2/Spain"
#

import argparse
import sys
import os
import FoldersManager
import os
from array import *
import pandas as pd
import glob

# parsing command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("-in",
     required=True,
     help="Name of input CSV file",
     metavar='<string>')
parser.add_argument("-out",
     required=True,
     help="Name of CSV file to be exported",
     metavar='<string>')

cdir=os.getcwd()
params = vars(parser.parse_args())
inpFil = params["in"     ]
outDir = params["out"    ]

print ("inImgDir     = ", inpFil) 
print ("outImgDir    = ", outDir)

# removes the path and the extension of the input file 
filename = os.path.splitext(os.path.basename(inpFil))[0]

# Find the columns that include years and 
count = 0
yearsCols  = []  # index of columns containing years
yearsNo    = []  # number of reapeated measuremen
yearsColsCleaned = []
yearsNoCleaned   = []
finp = open(inpFil,"r+")
for line in finp:
    if (count == 0) :
        countCol = 0
        labels = line.split(',')
        for label in labels :
            if label[0:4] == "year" :
               yearsCols  = yearsCols  + [countCol]
               yearsNo = yearsNo + [int(label[4:5])]
            countCol = countCol + 1
            
    if (count == 1) :
        words = line.split(',')
        tmp = yearsCols
        yearsColsCleaned = []
        for yC in yearsCols :
            if int(words[yC])>1900 : # then this is not a year 
                yearsColsCleaned = yearsColsCleaned + [yC] 
                yearsNoCleaned   = yearsNoCleaned   + [yearsNo[yearsCols.index(yC)]]
        break
    count = count + 1


print("yearsColsCleaned", yearsColsCleaned)
print("yearsNoCleaned  ",  yearsNoCleaned )

finp.seek(0)
count = 0

#Initialise a 2D array to store the indexes of the columns that will be used for each file to be created 
array2DIndexes = [[]]
for i in range(len(yearsColsCleaned)-1) :
    array2DIndexes = array2DIndexes + [[]]

print (yearsColsCleaned, "yearsColsCleaned")
print (array2DIndexes, "array2DIndexes")

for line in finp:
    if (count == 0) :
        countCol = 0
        labels = line.split(',')
        for label in labels :
            if(countCol<6) : #constant labels
                for i in range(len(array2DIndexes)) :
                   array2DIndexes[i] = array2DIndexes[i] + [countCol]
            else :
                for y in yearsNoCleaned :              
                    if str(y) in label :
                        array2DIndexes[yearsNoCleaned.index(y)] = array2DIndexes[yearsNoCleaned.index(y)] + [countCol]
            countCol = countCol + 1
        count  = count + 1

print (array2DIndexes)


# TO DO: FIRST EXPORT A SINGLE FILE WITH THE YEARS IN ONE LINE
# in a temporary created directory named tmp
if (os.path.exists(outDir+"/tmp")):
    print("WARNING: Directory ", outDir+"/tmp", " already exist and will be deleted!")
else:
    os.mkdir(outDir+"/tmp")
for i in range(len(yearsNoCleaned)):
    file = outDir+"/tmp/"+filename + "_"+ str(yearsNoCleaned[i]) + ".csv"
    fout = open(file,"w+")
    finp.seek(0)
    count = 0
    for line in finp:
        if (count == 0) :
            print (i, count, "--------------")
            count = count + 1
            labels = line.split(',')
            for c in range(len(array2DIndexes[i])-1):
                #print(labels[array2DIndexes[i][c]],labels[array2DIndexes[i][c]].replace(str(yearsNoCleaned[i]),""),str(i))
                label = labels[array2DIndexes[i][c]].replace(str(yearsNoCleaned[i]),"")
                label = label.replace(str(yearsNoCleaned[i]+1),"n")
                label = label.replace(str(yearsNoCleaned[i]-1),"p")
                fout.write(label+",")
            if("\n" in labels[array2DIndexes[i][len(array2DIndexes[i])-1]]):
                fout.write(labels[array2DIndexes[i][len(array2DIndexes[i])-1]][0:len(labels[array2DIndexes[i][len(array2DIndexes[i])-1]])-1].replace(str(yearsNoCleaned[i]),"")+",RepeatYear" +"\n")
            else : 
                fout.write(labels[array2DIndexes[i][len(array2DIndexes[i])-1]].replace(str(yearsNoCleaned[i]),"")+",RepeatYear" +"\n")
            continue

        words = line.split(',')
        for c in range(len(array2DIndexes[i])-1):

            fout.write(words[array2DIndexes[i][c]]+",")
        if("\n" in words[array2DIndexes[i][len(array2DIndexes[i])-1]]):
            fout.write(words[array2DIndexes[i][len(array2DIndexes[i])-1]][0:len(words[array2DIndexes[i][len(array2DIndexes[i])-1]])-1]+","+ str(yearsNoCleaned[i]) +"\n")
        else : 
            fout.write(words[array2DIndexes[i][len(array2DIndexes[i])-1]]+","+ str(yearsNoCleaned[i]) +"\n")

        #print("-----------------")
    fout.close()

finp.close()


# find all files in outDir+"/tmp/" and replace year(n+1) to year_ny, cut(n+1) to cut_ny, cut(n-1) to cut_py and year(n-1) to cut(np)
#files = glob.glob(outDir+"/tmp/", filename + "_"+"*.csv")


# merging the files
joined_files = os.path.join(outDir+"/tmp/", filename + "_"+"*.csv")
# A list of all joined files is returned
joined_list = glob.glob(joined_files)
# Finally, the files are joined
df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)
print("Exporting unwrapped data into: ", outDir+filename+".csv")
df.to_csv(outDir+ "/"+filename+".csv")



exit() # remove finip.close() to use any of the following code
finp.seek(0)

count = 0
uniqueYears = []
# create a list with all the unique years and sort it 
for line in finp:
    if (count == 0) :
        count  = count + 1
        continue 
    else :
        words = line.split(',')
        for yC in yearsColsCleaned :
            if (words[yC]) not in uniqueYears :
                uniqueYears = uniqueYears + [(words[yC])]

#uniqueYears.sort()

print(uniqueYears, "uniqueYears")

# create a file for each year with the associated field data
count = 0
for uY in range(len(uniqueYears)):
    finp.seek(0)
    file = outDir+"/"+filename + str(uniqueYears[uY]) + ".csv"
    print("Generating File: ", file)
    fout = open(file,"w+")
    # 
    currentYear = 0
    yearsNo     = 0
    while (line in finp):
        words = line.split(',') 
        years = []
        for yC in yearsColsCleaned:
            if uniqueYears[uY] == words[y] :
                currentYear = uniqueYears[uY]
                yearsNo     = yearsNoCleaned[yearsColsCleaned.index(yC)]
                break
        if(currentYear!=0):
            break
        #find it's first appearance and get yearsNo to know which cols to include        
            
    fout.close()
    


finp.close()
