try:
    from osgeo import ogr, osr, gdal
    from osgeo.gdal import gdalconst
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')