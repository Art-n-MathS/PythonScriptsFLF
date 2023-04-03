## @package GeoImage
#  This class contains an image and can apply various functions to it 
#  (for example canny edge).
#  @author Dr. Milto Miltiadou
#  @date Oct 2017 - V2 Aug 2019 - V3 Jan 2023
#  @version 3.0
#
#  This code was originally created as part of the SEODWARF project. New features added as part of the ASTARTE and UKRI Future Leaders project 
#

from ast import Delete
import numpy as np
import sys
#import gdal
#from gdalconst import *
try:
    from osgeo import ogr, osr, gdal
    from osgeo.gdal import gdalconst
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

## 
class GeoImage:


    ## The constructor
    #  @param i_inputTif the input image in tif format
    def __init__(self, i_inputTif):
        self.name = i_inputTif
        self.inp_raster = gdal.Open(i_inputTif)
        self.noOfBands = self.inp_raster.RasterCount
        self.bandLoaded = False
        self.imArr = []
        self.cols = self.inp_raster.RasterXSize
        self.rows = self.inp_raster.RasterYSize
        self.proj = self.inp_raster.GetProjection()
        srs=osr.SpatialReference(wkt=self.proj)
        if srs.IsProjected:
            print (srs.GetAttrValue('projcs'))
            print (srs.GetAttrValue('geogcs'))

        ## the geo transformation of the image
        self.geoTransform = self.inp_raster.GetGeoTransform()
        self.xOrigin     = self.geoTransform[0] 
        self.yOrigin     = self.geoTransform[3] 
        self.pixelWidth  = self.geoTransform[1] 
        self.pixelHeight = -self.geoTransform[5] 
        print ("-----------------------------------")
        print ("xmin, xmax:", self.xOrigin, self.xOrigin+self.rows*self.pixelWidth)
        print ("ymin, ymax:", self.yOrigin-self.cols*self.pixelHeight, self.yOrigin)
        print ("pixelwidth x pixelheight:", self.pixelWidth, self.pixelHeight)
        print ("cols x rows:", self.cols, self.rows)
        #print ("Projection: ", self.proj)

        print ("-----------------------------------")

    def getNoOfBands(self):
        return self.noOfBands

    def loadBand(self,band):
        print("Loading Band ", band, " of ", self.name)
        if (band>self.noOfBands):
            sys.exit("ERROR: requested to load a non-existing band!")
        if (self.imArr!=[]) :
            del self.imArr
        self.imArrband = self.inp_raster.GetRasterBand(band)
        self.imArr     = np.array(self.imArrband.ReadAsArray())
        self.datatype = self.imArrband.DataType
        ## the value that represents null within the image
        self.noValue = self.imArrband.GetNoDataValue()
        
        



        self.bandLoaded = True

        ## the projection of the image
        self.projection = self.inp_raster.GetProjection()

    ## method that takes as input a geolocation and returns the pixels value that it lies inside
    def getPixelValuefromGeo(self, i_geoX, i_geoY): 
       if not self.bandLoaded :
           sys.exit("ERROR: Please load a band first")
       if(self.yOrigin>i_geoY or self.xOrigin<i_geoX or self.yOrigin-i_geoY>self.rows*self.pixelHeight or i_geoX-self.xOrigin>self.cols*self.pixelWidth):
          return self.noValue
       xOffset = int((i_geoX-self.xOrigin) / self.pixelWidth)
       yOffset = int((self.yOrigin-i_geoY) / self.pixelHeight)
       #print ("self.yOrigin, i_geoY",self.yOrigin,i_geoY, yOffset)
       #print ("self.xOrigin, i_geoX",self.xOrigin,i_geoX, xOffset)

       if (xOffset>=0 and xOffset<self.cols and yOffset>=0 and yOffset<self.rows):
          return self.imArr[yOffset][xOffset]
       else:
          return self.noValue
    
    ## method that returns the value of a pixel
    #  @param[in] i_r row of the pixel
    #  @param[in] i_c column of the pixel
    def getPixelValue(self, i_r, i_c): 
       if not self.bandLoaded :
           sys.exit("ERROR: Please load a band first")
       return self.imArr[i_r][i_c]

           
    ## method that returns geolocation of a given pixel in the form [x y]
    # @param[in] i_x the x coordinate of the pixel
    # @param[in] i_y the y coordinate of the pixel
    # @returns [x, y] the geolocations of the given pixel\
    def getGeolocation(self, i_x, i_y):        
        if (not self.bandLoaded) :
           sys.exit("ERROR: Please load a band first")
        # print ("getting geolocations")
        if (i_x>=self.cols or i_y>=self.rows or i_x<0 or i_y<0):
           return [0,0] # returns a pixel that is always outside study area and will be ignored at next next
        #print ("------------------------------------------------------------------")
        #print ("i_x,i_y",i_x,i_y)
        #print ("self.xOrigin,self.yOrigin",self.xOrigin,self.yOrigin)
        #print ("self.pixelWidth,self.pixelHeight",self.pixelWidth,self.pixelHeight)
        #print ("self.xOrigin+i_x*self.pixelWidth,self.yOrigin-i_y*self.pixelHeight",self.xOrigin+i_x*self.pixelWidth,self.yOrigin+i_y*self.pixelHeight)
        #print ("------------------------------------------------------------------")
        return [self.xOrigin+i_x*self.pixelWidth,self.yOrigin+i_y*self.pixelHeight]
        
    ## Method that returns the number of rows
    # the numbers of rows within the image
    def getNoOfRows(self):
       return self.rows
    
    ## Checks if the given value is equal to the no value or zero
    #  @param[in] i_value value to be tested
    #  @returns true if it is NoValue/Zero and false otherwise
    def isNoValueOrLessthanZero(self, i_value):
       if not self.bandLoaded :
           sys.exit("ERROR: Please load a band first")
       if (i_value == self.noValue):
          return 1
       if (i_value < -0.000001):
          return 1
       return 0
    
    
    
    ## Method the returns the number of cols
    # @returns the number of columns within the image
    def getNoOfCols(self):
       return self.cols
    
    ## Method that returns pixel width in the x axis 
    # @returns pixels wdith in the x-axis
    def getPixelWidth(self):
       return self.pixelWidth
       
    ## Method that returns pixel height in the y-axis 
    # @returns pixels height in the y-axis
    def getPixelHeight(self):
       return self.pixelHeight