#  @author Dr. Milto Miltiadou
#  @date March 2023
#  @version 1.0
#
## package selectPlotsAccordingToMask
#  @brief Script that calculates the average daily precipitation of a given country 
#  @param[in] icsv : name of plot csv file
#  @param[in] proj : the projection of the plots
#  @param[in] xcol : the name of the column containing the x-coordinates
#  @param[in] ycol : the name of the column containing the y-coordinates
#  @param[in] mask : a GEOTIFF image exported using the Masks class - see Masks_test.ipynb example on how to export the combined masks of your interests
#  @param[in] r    : nn or q3  the way the mask will be reprojected. nn visually seems to be more precise but q3 produces clearer results, smoother blobs also serves as a noise removal algorithm
#  @returns ocsv   : the exported plot csv file containing only the plots within the non-masked area
#
#
#  how to run: python selectPlotsAccordingToMask.py -icsv <plotsfilename> -proj <projection> -xcol <colname> -ycol <colname> -mask <maskfilename> -r <nn or q3> -ocsv <outputPlotFilename> 
#  how to run: python selectPlotsAccordingToMask.py -icsv <plots.csv> -proj <projection> -mask <mask.tif> -ocsv <filteredPlots.csv> 
#
# example windows:  python "C:/Users/mm2705/Documents/Cambridge/Scripts/PythonScriptsFLF/selectPlotsAccordingToMask.py" -icsv "C:/Users/mm2705/Documents/Cambridge/Scripts/SampleData/mergedcsv.csv" -proj "EPSG:3042" -xcol "CX" -ycol "CY" -mask "C:/Users/mm2705/Documents/Cambridge/Scripts/SampleData/SpainMaskGSWLmaksDistAsc30.tif" -r "q3" -ocsv "C:/Users/mm2705/Documents/Cambridge/Scripts/SampleData/filteredPlots.csv"
# example linux:  python3 "/home/milto/Documents/FLFScripts/PythonScriptsFLF/selectPlotsAccordingToMask.py" -icsv "/home/milto/Documents/FLFScripts/sampleData/mergedcsv.csv" -proj "EPSG:3042" -xcol "CX" -ycol "CY" -mask "/home/milto/Documents/FLFScripts/sampleData/SpainMaskGSWLmaksDistAsc30.tif" -r "q3" -ocsv "/home/milto/Documents/FLFScripts/sampleData/filteredPlots.csv"
#

import argparse
import GeoImage
import pandas as pd
import numpy as np
import subprocess
import os
from osgeo import gdal, ogr, osr
#from gdalconst import *
#import ogr


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
parser.add_argument("-xcol",
     required=True,
     help="The name column containing the x-coordinates",
     metavar='<string>')
parser.add_argument("-ycol",
     required=True,
     help="The name column containing the y-coordinates",
     metavar='<string>')
parser.add_argument("-mask",
     required=True,
     help="Input mask in GeoTIFF format",
     metavar='<string>')
parser.add_argument("-r",
     required=False,
     help="How mask will be reprojected to match the plot data - nn for neighrest neigbour and q3 for third quartile resampling",
     metavar='<string>')
parser.add_argument("-ocsv",
     required=True,
     help="The name of the output filtered csv file",
     metavar='<string>')

r = "nn"
params = vars(parser.parse_args())
icsv  = params["icsv"]
proj  = params["proj"]
xcol  = params["xcol"]
ycol  = params["ycol"]
mask  = params["mask"]
r     = params["r" ]
ocsv  = params["ocsv"]

print ("icsv = ", icsv) 
print ("proj, xcol, ycol = ", proj, xcol, ycol)
print ("mask, r = ", mask, r)
print ("ocsv  = ", ocsv ) 

strprojlist = list([a for a in proj
            if a.isalpha() or a.isnumeric()])
strproj     = "".join(strprojlist)


maskGeoTif = GeoImage.GeoImage(mask)
reprojMask = mask + strproj + ".tif"
print ("Reprojecting mask to match the coordinate system of the plot data")
print ("Name of file to be exported: ", reprojMask)
if os.path.isfile(reprojMask):
    print("WARNING: reprojected mask already exist at",reprojMask,"and have not been re-generated")
else: #-r q3
     if (r=="nn" or r == "q3"):
        cmd = "gdalwarp -r " + r + " -co COMPRESS=LZW -t_srs " + proj + " " + mask + " " + reprojMask
     else:
         raise Exception("ERROR: unknown reprojection method. nn and q3 only supported")
         exit(1)
     subprocess.call(cmd, shell=True)

df1 = pd.read_csv(icsv)
df1["index"] = list(range(0,len(df1)))
Xdata   = df1[xcol   ]
Ydata   = df1[ycol   ]
indexes = df1["index"]

if(len(Xdata)!=len(Ydata) or len(indexes)!=len(Ydata)):
    raise Exception("ERROR: the number of x and y coordinates and indexes should be equal!")
#else:
    # the number of x and y coordinates are equal

maskGeoTifReproj = GeoImage.GeoImage(reprojMask)  

maskGeoTifReproj.loadBand(1)
for i in range(0, len(Xdata)):
    maskVal = maskGeoTifReproj.getPixelValuefromGeo(Xdata[i],Ydata[i])
    if (int(maskVal)==0):
        idx = indexes[i]
        df1=df1.drop(idx)

df1.to_csv(ocsv, index=False)

print ("   ***   EXIT   ***")