#  @author Dr. Milto Miltiadou
#  @date Jan 2023
#  @version 1.0
#
## package GetAveDailyPrpcPerCountry
#  @brief Script that calculates the average daily precipitation of a given country 
#  @param[in] precipitationFile : a tif file containing precipitation data downloaded from ftp:/palantir.boku.ac.at/Public/ClimateData/v3/AllDataRasters/prec
#  @param[in] countriesShapefile: the cleaned NTUTS shapefile containing the boundaries of the European countries
#  @param[in] countryAcronym   : a 2 character Acronym indicating the country of interest
#  @returns[out] csvFile        : a csv file with two columns, the first column contains the numbers 1-365 indicating the Julian calendar and the other column the average daily precipitation of the selected country
#
#  how to run: python GetAveDailyPrpcPerCountry.py -prcp <precipitationFile.tif> -countries <countries.tif> -out <aveDaily.csv> 
#
#
# example:  python "C:/Users/mm2705/Documents/Cambridge/Scripts/PythonScriptsFLF/GetAveDailyPrpcPerCountry.py" -prcp "C:/Users/mm2705/Prcp/DownscaledPrcp2014.tif" -countries "C:/Users/mm2705/Documents/Cambridge/Milto_SPSW/CountriesRasterPrcp2.tif" -out "C:/Users/mm2705/Documents/Cambridge/Milto_SPSW/csvPrcp/Prcp2014.csv"
#


import argparse
import sys
import os
try:
    from osgeo import ogr, osr, gdal
    from osgeo.gdal import gdalconst
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')
import GeoImage

# Enable GDAL/OGR exceptions
gdal.UseExceptions()

# parsing command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("-prcp",
     required=True,
     help="Name of precipitation .tif file",
     metavar='<string>')
parser.add_argument("-countries",
     required=True,
     help="Name of raster defining the boundaries of the European countries",
     metavar='<string>')
parser.add_argument("-out",
     required=True,
     help="Name of .csv file to be exported with average daily precipitation values",
     metavar='<string>')


params = vars(parser.parse_args())
prcp     = params["prcp"    ]
countries= params["countries"]
outCsv   = params["out"    ]

print ("prcp      = ", prcp ) 
print ("countries = ", countries)
print ("outCsv    = ", outCsv) 


countriesMask = GeoImage.GeoImage(countries)

# load important parameters
nrowsMask = countriesMask.getNoOfRows()
ncolsMask = countriesMask.getNoOfCols()
print(nrowsMask,ncolsMask, " = nrowsMask,nrowsMask")

prcpGeoImg    = GeoImage.GeoImage(prcp)
nrowsPrcp = prcpGeoImg.getNoOfRows()
ncolsPrcp = prcpGeoImg.getNoOfCols()
noOfBands = prcpGeoImg.getNoOfBands()
print(nrowsPrcp,ncolsPrcp, " = nrowsPrcp,ncolsPrcp")
if(nrowsMask!=nrowsPrcp or ncolsMask!=ncolsPrcp):
    sys.exit("ERROR: Mask and Precipitation files should have the same dimensions i.e., be aligned")
#else
#  // the mask and the precipitation tif files are aligned 

# load band of mask, done here to avoid loading (and saving time) it if they are not aligned
countriesMask.loadBand(1)
uniqueValues = []
cols         = []
rows         = []


for  c in range(0,ncolsMask):
    for r in range(0,nrowsMask):
        value = countriesMask.getPixelValue(r,c)
        if value < 0 : 
            continue
        try: 
            index = uniqueValues.index(value)
        except:
            uniqueValues.append(value)
            index = len(uniqueValues)-1
            cols = cols + [[]]
            rows = rows + [[]]
        cols[index].append(c)
        rows[index].append(r)

print(uniqueValues)
print(len(cols))
print(len(rows))
#store locations of pixels for each country

f = open(outCsv,"w")


# TO DO: find average precipitation of each country and export in Csv
f.write(",")
for v in range(0,len(uniqueValues)):
    f.write(str(uniqueValues[v]))
    f.write(",")
f.write("\n")
for i in range (1,noOfBands+1):
    f.write(str(i))
    f.write(",")
    prcpGeoImg.loadBand(i)
    sum = 0.0
    for v in range(0,len(uniqueValues)):
        if (len(rows[v])!=len(cols[v])):
            print(len(rows[v]),len(cols[v]))
            sys.exit("ERROR: No of cols and rows indexes should have been the same")
        average = 0.0
        n=0.0
        for r in range (0,len(rows[v])):
            value = float(prcpGeoImg.getPixelValue(rows[v][r],cols[v][r]))/100.0
            if value > 0 :
                average = average * (n/(n+1.0)) + (value/(n+1.0))
                n=n+1.0
        f.write(str(average))
        if(v!=len(uniqueValues)-1):
            f.write(",")
       
#   print(i)
    f.write("\n")
   
f.close()



