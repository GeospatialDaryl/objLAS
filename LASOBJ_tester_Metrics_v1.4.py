import ClassLASObj_v10
from ClassLASObj_v10 import *
#Class LTKPaths contains Machine Specific Paths
import ModuleLiDARtools
from ModuleLiDARtools import Paths

import os
import arcgisscripting

gp = arcgisscripting.create(9.3)
gp.AddToolbox("C:\Program Files (x86)\ArcGIS\ArcToolBox\Toolboxes\Conversion Tools.tbx")
gp.overwriteoutput = 1

utmn83 = "PROJCS['NAD_1983_UTM_Zone_10N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-123.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"


#instantiate Paths object
workPaths = Paths()
#create empty directory list of las files
listLASObj = []

# Make a list of LAS in the directory of interest
dirList=os.listdir(workPaths.lasworkspace)
### Instantiate the list of LASObjs
for fname in dirList:
    if "las" in fname:
        nameLASObj = LASObj(workPaths.lasworkspace+fname)
        listLASObj.append(nameLASObj)
countLASObj = 0
for LASObjs in listLASObj:
    countLASObj = countLASObj + 1
print str(countLASObj)+" Total Tiles"
#Declare test LASObj object
test = listLASObj[0]
counter = 0

for LASObjs in listLASObj:
    counter = counter + 1
    print "Tile "+LASObjs.las_name+", "+str(counter)+" of "+str(countLASObj)
    #LASObjs.makeMetrics(workPaths)
    #LASObjs.makeMetrics(workPaths,6.,["cover"])
    #LASObjs.makeMetrics(workPaths,9.,["cover"])

listRasters = ["count","min","max","mean","mode","stddev","variance","cv","cover","skewness","kurtosis","p05","p10","p20","p25","p30","p40","p50","p60","p70","p80","p90","p95"]
for rasters in listRasters:
    os.system("mkdir "+workPaths.scratch+rasters)
    #os.system("move "+workPaths.scratch+"*"+rasters+"* "+workPaths.scratch+rasters)
    os.system("copy "+workPaths.scratch+"*"+rasters+"* "+workPaths.scratch+rasters)
    ws = workPaths.scratch+rasters+"\\"
    listDTMs = []
    listDTMs = os.listdir(ws)
    counter = 0
    for files in listDTMs:
        if "dtm" in files:
            counter = counter + 1
            print "Tile "+str(counter)+" of "+str(countLASObj)
            os.system("DTM2Ascii "+ws+files+" "+ws+files[0:10]+".asc")
            
    gp.Workspace = ws
    fcs = gp.ListRasters("*")
    counter = 0


    for fc in fcs:
        counter = counter + 1
        if counter == 1:
            gp.CopyRaster_management(workPaths.templateRasters+"rtempl_25",ws+rasters[0:8]+"_mos")
            print "Copied template to "+rasters+" directory"
        gp.DefineProjection_management(ws+"\\"+fc,utmn83)
        gp.ASCIIToRaster_conversion(ws+fc[0:10]+".asc",ws+"m"+fc[0:10],"FLOAT")
        if "asc" in fc:
            print "Mosaicking "+ws+"m"+fc[0:10]+" into  "+ws+rasters[0:8]+"_mos"
            gp.mosaic_management(ws+"m"+fc[0:10],ws+rasters[0:8]+"_mos","FIRST")
            print "Tile "+str(counter)+" of "+str(countLASObj)+" for parameter '"+rasters+"' complete."
