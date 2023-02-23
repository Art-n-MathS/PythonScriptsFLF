#  @author Dr. Milto Miltiadou
#  @date Jan 2023
#  @version 1.0
#
## package GetPrecipitationOfCountry
#  @brief Script that calculates the average daily precipitation of a given country 
#  @param[in] precipitationFile : a tif file containing precipitation data downloaded from ftp:/palantir.boku.ac.at/Public/ClimateData/v3/AllDataRasters/prec
#  @param[in] countriesShapefile: the cleaned NTUTS shapefile containing the boundaries of the European countries
#  @param[in] countryAcronym   : a 2 character Acronym indicating the country of interest
#  @returns[out] csvFile        : a csv file with two columns, the first column contains the numbers 1-365 indicating the Julian calendar and the other column the average daily precipitation of the selected country
#
#  how to run: python GetPrecipitationOfCountry.py -tif <precipitationFile> -shp <countriesShapefile> -country <countryAcronym> -out <csvFile> 
#
#
# example:  python "C:/Users/mm2705/Documents/Cambridge/Scripts/PythonScriptsFLF/GetPrecipitationOfCountry.py" -tif "C:/Users/mm2705/Prcp/DownscaledPrcp2014.tif" -shp "C:/Users/mm2705/Documents/Cambridge/Milto_SPSW/Shapefiles/CountriesPolygonNuts/CountriesPolygonNuts.shp" -country "ES" -out "C:/Users/mm2705/Documents/Cambridge/Milto_SPSW/csvPrcp/Prcp2016ES.csv"
#


import argparse
import sys
import os
try:
    from osgeo import ogr, osr, gdal
    from osgeo.gdal import gdalconst
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')


import geopandas as gpd

shapefile = gpd.read_file("shapefile.shp")
print(shapefile)


def create_filtered_shapefile(value, filter_field, in_shapefile, out_shapefile):
    input_layer = ogr.Open(in_shapefile).GetLayer()

    # Filter by our query
    query_str = '"{}" = "{}"'.format(filter_field, value)
    print(query_str)
    input_layer.SetAttributeFilter(query_str)

    # Copy Filtered Layer and Output File
    driver = ogr.GetDriverByName('ESRI Shapefile')
    out_ds = driver.CreateDataSource(out_shapefile)
    out_layer = out_ds.CopyLayer(input_layer, str(value))
    del input_layer, out_layer, out_ds
    return out_shapefile



# Enable GDAL/OGR exceptions
gdal.UseExceptions()

# parsing command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("-tif",
     required=True,
     help="Name of precipitation .tif file",
     metavar='<string>')
parser.add_argument("-shp",
     required=True,
     help="Name of shapefile defining the boundaries of the European countries",
     metavar='<string>')
parser.add_argument("-country",
     required=True,
     help="Acronym of country of interest",
     metavar='<string>')
parser.add_argument("-out",
     required=True,
     help="Name of .csv file to be exported with average daily precipitation values",
     metavar='<string>')


params = vars(parser.parse_args())
tifFil = params["tif"    ]
shpfile= params["shp"    ]
country= params["country"]
outCsv = params["out"    ]

print ("tifFil  = ", tifFil ) 
print ("shpfile = ", shpfile)
print ("country = ", country) 
print ("outCsv  = ", outCsv )

driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(shpfile, 0)
layer = dataSource.GetLayer()

layerDef = layer.GetLayerDefn()
fields = [layerDef.GetFieldDefn(i).GetName() for i in range(layerDef.GetFieldCount())]
field = "NUTS_ID"
if(field not in fields):
    sys.exit('ERROR: cannot field ', fields, 'in provided shapefile')
#else :
    # field exist in shapefile

query_str = '"{}" = "{}"'.format(field, country)
print(query_str)
layer.SetAttributeFilter(query_str)
tmpShp = shpfile[0:len(shpfile)-4]+country+".shp"


drv = ogr.GetDriverByName( 'ESRI Shapefile' )
if os.path.exists(tmpShp):    
    print("WARNING: ", tmpShp, " already existed and it was deleted\n")
    driver.DeleteDataSource(tmpShp)
print(tmpShp)
outds = drv.CreateDataSource( tmpShp )
print(outds)
outlyr = outds.CopyLayer(layer,country)
outds = None
del layer,dataSource,outlyr,outds


tmpTifFil = tifFil+country+".tif"

clip = gdal.Warp(destNameOrDestDS = tmpTifFil, 
                 srcDSOrSrcDSTab  = shpfile, 
                 cutlineDSName    = layer, # or geojson
                 cropToCutline    = True,
                 copyMetadata     = True,
                 dstNodata        = 0)      # Select the nodata value

# for feature in layer:
#     print (feature.GetField("NTUSID"))

# gdalwarp -dstnodata -cutline "C:/Users/mm2705/Documents/Cambridge/Milto_SPSW/Shapefiles/CountriesPolygonNuts/CountriesPolygonNuts.shp" "C:/Users/mm2705/Prcp/DownscaledPrcp2014.tif" "C:/Users/mm2705/Prcp/DownscaledPrcp2014EU.tif"


# gdalwarp -overwrite -of GTiff -tr 0.008333333333333333 -0.008333333333333333 -tap -cutline C:/Users/mm2705/Downloads/NUTS_2013_01M_SH/NUTS_2013_01M_SH/data/NUTS_RG_01M_2013.shp -cl NUTS_RG_01M_2013 -crop_to_cutline C:/Users/mm2705/Prcp/DownscaledPrcp2014.tif "C:/Users/mm2705/Prcp/DownscaledPrcp2014EU.tif"
# GDAL command output: 

# this command works!!!! it crops Spain
# gdalwarp -overwrite -of GTiff -tr 0.008333333333333333 -0.008333333333333333 -tap -cutline C:\Users\mm2705\Documents\Cambridge\Milto_SPSW\Shapefiles\CountriesPolygonNuts\CountriesPolygonNutsES.shp -cl CountriesPolygonNutsES -crop_to_cutline C:/Users/mm2705/Prcp/DownscaledPrcp2014.tif C:/Users/mm2705/AppData/Local/Temp/processing_BFfzDl/2e105f577a0d48faa49dc34ca9e17181/OUTPUT.tif


# run this to rasterise countries according to their id
# gdal_rasterize -l CountriesPolygonNutsIDs -a CountryID -ts 13920.0 6030.0 -init -1.0 -a_nodata -1.0 -te -63.153455 -21.3873095 55.8366285 71.185318001 -ot Int16 -of GTiff -co COMPRESS=DEFLATE -co PREDICTOR=2 -co ZLEVEL=9 -a_srs EPSG:4326 C:\Users\mm2705\Documents\Cambridge\Milto_SPSW\Shapefiles\CountriesPolygonNuts\CountriesPolygonNutsIDs.shp C:/Users/mm2705/Documents/Cambridge/Milto_SPSW/Shapefiles/CountriesPolygonNuts/CountriesRasterPrcp1.tif
# gdal_rasterize -l CountriesPolygonNutsIDs -a CountryID -ts 13920.0 6030.0 -tr 0.008333333333333333 0.008333333333333333 -init -1.0 -a_nodata -1 -te -40.5 25.25 75.5 75.5 -ot Int16 -of GTiff -co COMPRESS=DEFLATE -co PREDICTOR=2 -co ZLEVEL=9 C:\Users\mm2705\Documents\Cambridge\Milto_SPSW\Shapefiles\CountriesPolygonNuts\CountriesPolygonNutsIDs.shp C:/Users/mm2705/Documents/Cambridge/Milto_SPSW/Shapefiles/CountriesPolygonNuts/CountriesRasterPrcp2.tif