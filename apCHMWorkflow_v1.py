import arcpy
import os
from arcpy.sa import *

arcpy.CheckOutExtension("Spatial")
listSHPs = []

scratchSpot = "R:\\Scratch.gdb\\"
dirSourceSHP = "R:\\Shasta_VegPoly_f.gdb\\"
dirOutput = "Z:\\Shasta_CanopyObjects\\Shasta_CanopyObjects.gdb\\"

arcpy.env.overwriteOutput = 1

arcpy.env.workspace = dirSourceSHP
listSHPs = arcpy.ListFeatureClasses()
    
for items in listSHPs:
    try:
        errorString = ""
        print "Starting "+items
        
        inSHP = dirSourceSHP+items
        outSHP = dirOutput+items[:-4]+"_canopy"
        inRAS = "Z:\\Shasta_CanopyHt_FLT\\Shasta3ftCHM.gdb\\"+items[:-4]+"_elevchm"
        outStat = dirOutput+items[:-4]+"_ZStat"
        
        arcpy.MultipartToSinglepart_management(inSHP,outSHP)
        errorString = "ERROR: AddField"
        arcpy.AddField_management(outSHP,"ZstatID","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
        errorString = "ERROR: CalculateField"
        arcpy.CalculateField_management(outSHP,"ZstatID","[OBJECTID]","VB","#")
        errorString = "ERROR: ZonalStatistics"
        arcpy.sa.ZonalStatisticsAsTable(outSHP,"ZstatID",inRAS,outStat,"DATA","MIN_MAX_MEAN")
        errorString = "ERROR: JoinField"
        arcpy.JoinField_management(outSHP,"ZstatID",outStat,"ZSTATID","COUNT;AREA;MIN;MAX;MEAN")
        errorString = "ERROR: Delete"
        arcpy.Delete_management(outStat,"Table")
        errorString = ""
    except:
        print "--> problem:  :"+items+":"+errorString
        #STOP
    
##arcpy.MultipartToSinglepart_management("R:/Shasta_VegPoly_f.gdb/B0503_veg",
##                                           "Z:/Shasta_CanopyObjects/Shasta_CanopyObjects.gdb/B0503_canopy")
##
##arcpy.AddField_management("Z:/Shasta_CanopyObjects/Shasta_CanopyObjects.gdb/B0503_canopy",
##                          "ZstatID","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
##
##arcpy.CalculateField_management("Z:/Shasta_CanopyObjects/Shasta_CanopyObjects.gdb/B0503_canopy",
##                                "ZstatID","[OBJECTID]","VB","#")
##
##arcpy.sa.ZonalStatisticsAsTable("Z:/Shasta_CanopyObjects/Shasta_CanopyObjects.gdb/B0503_canopy",
##                                "ZstatID","Z:/Shasta_CanopyHt_FLT/Shasta3ftCHM.gdb/B0503_elevchm",
##                                "Z:/Shasta_CanopyObjects/Shasta_CanopyObjects.gdb/B0503_ZStat","DATA","MIN_MAX_MEAN")
##
##arcpy.JoinField_management("Z:/Shasta_CanopyObjects/Shasta_CanopyObjects.gdb/B0503_canopy",
##                           "ZstatID","Z:/Shasta_CanopyObjects/Shasta_CanopyObjects.gdb/B0503_ZStat","ZSTATID","COUNT;AREA;MIN;MAX;MEAN")
##
##arcpy.Delete_management("Z:/Shasta_CanopyObjects/Shasta_CanopyObjects.gdb/B0503_ZStat","Table")


