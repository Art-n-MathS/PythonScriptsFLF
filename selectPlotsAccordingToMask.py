#  @author Dr. Milto Miltiadou
#  @date March 2023
#  @version 1.0
#
## package selectPlotsAccordingToMask
#  @brief Script that calculates the average daily precipitation of a given country 
#  @param[in] icsv : name of plot csv file
#  @param[in] proj : the projection of the plots
#  @param[in] mask : a GEOTIFF image exported using the Masks class - see Masks_test.ipynb example on how to export the combined masks of your interests
#  @returns ocsv   : the exported plot csv file containing only the plots within the non-masked area
#
#
#  how to run: python selectPlotsAccordingToMask.py -icsv <plotsfilename> -proj <projection> -mask <maskfilename> -ocsv <outputPlotFilename> 
#  how to run: python selectPlotsAccordingToMask.py -icsv <plots.csv> -proj <projection> -mask <mask.tif> -ocsv <filteredPlots.csv> 
#
# example:  python "C:/Users/mm2705/Documents/Cambridge/Scripts/PythonScriptsFLF/selectPlotsAccordingToMask.py" -icsv "C:/Users/mm2705/Documents/Cambridge/Scripts/SampleData/mergedcsv.csv" -proj "EPSG:3042" -mask "C:/Users/mm2705/Documents/Cambridge/Scripts/SampleData/SpainMaskGSWLmaksDistAsc30.tif" -ocsv "C:/Users/mm2705/Documents/Cambridge/Scripts/SampleData/filteredPlots.csv"
#

import argparse
import pandas as pd
import numpy as np
import gdal
from gdalconst import *


# parsing command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("-icsv",
     required=True,
     help="Input csv file 1",
     metavar='<string>')
parser.add_argument("-proj",
     required=True,
     help="The label of the column that the merge will be based on",
     metavar='<string>')
parser.add_argument("-mask",
     required=True,
     help="Input csv file 2",
     metavar='<string>')
parser.add_argument("-ocsv",
     required=True,
     help="The name of the output filtered csv file",
     metavar='<string>')

params = vars(parser.parse_args())
icsv  = params["icsv"]
proj  = params["proj"]
mask  = params["mask"]
ocsv   = params["ocsv" ]

print ("icsv = ", icsv) 
print ("proj = ", proj)
print ("mask = ", mask)
print ("ocsv  = ", ocsv ) 


df1 = pd.read_csv(icsv)