import ClassLASObj_v12
from ClassLASObj_v12 import *
#Class LTKPaths contains Machine Specific Paths
import ModuleLiDARtools_v1
from ModuleLiDARtools_v1 import * #Paths

import Queue, thread, time, os
from threading import Thread
import arcgisscripting

gp = arcgisscripting.create(9.3)
gp.AddToolbox("C:\Program Files (x86)\ArcGIS\ArcToolBox\Toolboxes\Conversion Tools.tbx")
gp.overwriteoutput = 1

utmn83 = "PROJCS['NAD_1983_UTM_Zone_10N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-123.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"


#instantiate Paths object
workPaths = Paths()
#create empty directory list of las files
listLASObj = []

# ##############ADJUST THE Target HERE ##########################
thisOperationPath = workPaths.pathSctt
multiProcessor_Count = 10
# ###############################################################

workPaths.lasworkspace = thisOperationPath+"LAS_b\\"
workPaths.dtmworkspace = thisOperationPath+"DTM\\"
workPaths.chmworkspace = thisOperationPath+"CHM\\"
workPaths.lasExtent    = thisOperationPath+"LAS\\"
workPaths.csvworkspace = thisOperationPath+"CSV\\"
workPaths.lasnorm      = thisOperationPath+"LAS_norm\\"
workPaths.dem          = thisOperationPath+"dem\\"

# ###############################################################


# Make a list of LAS in the directory of interest
dirList=os.listdir(workPaths.lasExtent)   # USE the LAS not LAS_b to make this list
# ## Instantiate the list of LASObjs
for fname in dirList:
    if "las" in fname:
        nameLASObj = LASObj(workPaths.lasworkspace+fname,workPaths.lasExtent+fname)
        print nameLASObj.las_name
        listLASObj.append(nameLASObj)
        del nameLASObj

countLASObj = 0
for LASObjs in listLASObj:
    countLASObj = countLASObj + 1
print str(countLASObj)+" Total Tiles"
#Declare test LASObj object
test = listLASObj[0]
counter = 0

def fMachine(x):
    x.makeNormalizedLAS_MP(gp,workPaths,"C:\\Scratch\\dem_be_1m.img")

def worker():
    while True:
        item = q.get()
        item = fMachine(item)
        print item
        q.task_done()

q = Queue.Queue()

for i in range(multiProcessor_Count):
    t = Thread(target=worker)
    t.setDaemon(True)
    t.start()
    print "Init of "+str(multiProcessor_Count)+" thread complete."

for item in listLASObj:
    q.put(item)
    print "loaded item "+item.las_name

q.join()       # block until all tasks are done



#for LASObjs in listLASObj:
    #counter = counter + 1
    #print "Tile "+LASObjs.las_name+", "+str(counter)+" of "+str(countLASObj)
    ##LASObjs.makeCHM_StatePlaneFt(workPaths)
    #print "hold"
    ##LASObjs.makeCloudMetrics(workPaths)
    #LASObjs.makeNormalizedLAS(workPaths)
    ##makeNormalizedLAS_MP(workPaths,8,"C:\\Scratch\\dem_be_1m.img")
    ##makeNormalizedLAS(workPaths,"C:\\Scratch\\dem_be_1m.img")
    ##LASObjs.makeMetrics(workPaths)
    ##LASObjs.makeMetrics(workPaths,6.,["cover"])
    ##LASObjs.makeMetrics(workPaths,9.,["cover"])

