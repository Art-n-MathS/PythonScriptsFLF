#  @author Dr. Milto Miltiadou
#  @date 22nd Nov 2022
#  @version 1.0
#
## package main
#  @brief This script takes as input a field plot and converts all commas (that are used to indicate decimal places) to dots
#
#  how to run: python FixCSVs.py -in <inputDir> -out <outputDir>
#
# example: python "C:/Users/mm2705/Documents/Cambridge/Scripts/PythonScriptsFLF/FixCSVs.py" -in "C:/Users/mm2705/Documents/Cambridge/Milto_SPSW/L0/" -out "C:/Users/mm2705/Documents/Cambridge/Milto_SPSW/L1/"
#

import argparse
import sys
import os
import FoldersManager




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
inpDir = params["in"     ]
outDir = params["out"    ]

print ("inImgDir     = ", inpDir) 
print ("outImgDir    = ", outDir)

dirs = FoldersManager.creatFolders(inpDir,outDir)
os.chdir(inpDir)
for d in dirs:
    os.chdir(inpDir)
    listOfCsvsIn  = FoldersManager.getFilesNames(d,".csv")
    for csvFile in listOfCsvsIn :
        print("processing", csvFile, "in", d, "--------------")
        finp = open(inpDir+"/"+d+"/"+csvFile,"r+")
        os.chdir(outDir+"/"+d)
        fout = open(csvFile,"w+")
        for line in finp:
            semicolons = line.count(';')
            if (semicolons<3):
                fout.write(line)
            else :
                line = line.replace(',','.')
                line = line.replace(';',',')
                fout.write(line)









