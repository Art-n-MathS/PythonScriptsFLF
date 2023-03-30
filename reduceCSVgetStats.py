#  @author Dr. Milto Miltiadou
#  @date March 2023
#  @version 1.0
#
## package reduceCSVgetStats
#  @brief Takes as input a list of feature vectors exported by google earth engine using 
#  the fieldPlot class. The field Plot class takes as input field plot data. It gives an 
#  identifier to each plot and for each pixel within the plot it exports a feature vector. Here, 
#  the identifier is used to group the feature vectors into plots. For each group - plot - the 
#  mean and standard deviation of each feature is taken and this way data are reduced.
#  @param[in] icsv       : the feature vectors exported using the fieldPlot class
#  @param[in] indexCoName: a string defining the name of the column containing the unique 
#  identifiers of the plots
#  @returns[out] ocsv    : the reduced data where each plot identifier only appears once and 
#  only statistic (mean and std) about the extracted features are provided within the file.

#  how to run: python reduceCSVgetStats.py -icsv <icsv.csv> -indexCoName <indexCoName> -ocsv <ocsv.csv> 
#
#
# example:  python "C:/Users/mm2705/Documents/Cambridge/Scripts/PythonScriptsFLF/reduceCSVgetStats.py" -icsv "C:/Users/mm2705/Documents/Cambridge/Scripts/SampleData/TestIndClassSentinel2b.csv.csv" -indexCoName "class" -ocsv "C:/Users/mm2705/Documents/Cambridge/Scripts/SampleData/TestIndClassSentinel2b_reduced.csv"
#


import argparse
import pandas as pd
import numpy as np

# parsing command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("-icsv",
     required=True,
     help="Name of input csv file containing the feature vectors",
     metavar='<string>')
parser.add_argument("-indexCoName",
     required=True,
     help="Name of column containing the numbers identifiers of the plots created by fieldPlot class",
     metavar='<string>')
parser.add_argument("-ocsv",
     required=True,
     help="Name of csv file to be exported containing the reduced data",
     metavar='<string>')

params      = vars(parser.parse_args())
icsv        = params["icsv"       ]
indexCoName = params["indexCoName"]
ocsv        = params["ocsv"       ]

print ("icsv        = ", icsv       ) 
print ("indexCoName = ", indexCoName)
print ("ocsv        = ", ocsv       ) 


dfIn = pd.read_csv(icsv)
# remove columns that are GEE related
dfIn = dfIn.drop(columns=["system:index",".geo"])
# get a list with all the names of the feature vectors
originalLabels = list(dfIn.columns)
# get a list containing the ids of the plots, once each id only
plotIds = dfIn[indexCoName].unique()

# open the csv file to write the reduced data
f = open(ocsv, "w")
if len(originalLabels)<=0:
   raise Exception ("ERROR: the input csv file contains no feature vectors")
   exit(1)

# write the new labels into the output csv file
p =originalLabels
p.remove(indexCoName)
for id in p :
    f.write(id+"_mean,"+id+"_std,")
f.write(indexCoName+"\n")
print(originalLabels)


# Loop through the plots and find the mean std of each feature vector and 
# export it into the csv file
for id in plotIds :
     # select all rows that belong to the plot with id
     tmpDF = dfIn[dfIn[indexCoName]==id]
     tmpDF = tmpDF.drop(columns=[indexCoName])
     # Loop through each feature, calculate mean, std and save into csv file
     for featureLabel in tmpDF:
          print(featureLabel)
          featureList = tmpDF[featureLabel]
          mean = np.mean(featureList)
          std = np.std(featureList)
          f.write(str(mean)+","+str(std)+",")
          #print(featureList)
     f.write(str(id)+"\n")  
     print(id)
     print("------------------------------------")

print(plotIds)

f.close()