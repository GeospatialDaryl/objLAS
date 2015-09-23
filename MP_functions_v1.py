def WriteScottDEMDriverBAT(strPathNameforBat,listPYNames):
    ''' Function to Create Python Programs for the MP Batch Method.
    Takes (strPathNameForPy - a string Path Name for the .bat),
          (numProc -)
    '''
    f = open(strPathNameforBat, 'w')
    for items in listPYNames:
        s1 = 'start "Processor '+str(items)+'" c:\\Python25\\python.exe A:\\BATandPY\\'
        s2 = ".py"
        string = s1+str(items)+s2+" > A:\BATandPY\Proc"+str(items)+"_log.txt 2>&1 \n"
        f.write(string)
        f.write("TIMEOUT 7\n")

def WriteScottDEMConvertPY(strPathNameForPy,listTiles,ProcNum):
    ''' Function to Create Python Programs for the MP Batch Method.
    Takes (strPathNameForPy - a string Path Name for the .py),
          (lisTiles - a python List object of the tile numbers (integers) to be processed)
    '''
    f = open(strPathNameForPy, 'w')
    s1 = "from MP_functions_v1 import ScottDEMConvert\n"
    s2 = "listProcess = ["
    #listTemp = [1,2,3,4]    

    f.write(s1)
    f.write(s2)
    
    counter = 0
    for items in listTiles:
        f.write(str(items))
        if counter < (len(listTiles)-1): f.write(",")
        counter += 1
    f.write("]\n")
    f.write("\n")
    f.write("thisProc = "+str(ProcNum)+"\n")
    f.write("for items in listProcess:\n")
    f.write("    ScottDEMConvert(items,thisProc)\n")
    f.close()
        


def ScottDEMConvert(numbers,ProcNum):

    # Import system modules
    import sys, string, os, arcgisscripting, uuid
    from ModuleLiDARtools_v1 import UniqueFileNamer

    # Create the Geoprocessor object
    gp = arcgisscripting.create(9.3)

    # Load required toolboxes...
    gp.AddToolbox("C:/Program Files (x86)/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx")
    gp.AddToolbox("C:/Program Files (x86)/ArcGIS/ArcToolbox/Toolboxes/Analysis Tools.tbx")
    gp.overwriteoutput = 1

    # Local variables...
    thisRaster = "X:\\05_Scott\\Snap\\ScottSnap_1m.img"
    dem_be_1m_img = "C:\\Scratch\\scott_dem\\"
    FID0 = "R:\\ScottSnaps\\"
    temp2Path = "A:\\PolyExtractRaster\\"

    Scott_Valley_Processing_Tile__2_ = "Scott_Valley_Processing_Tile"

    

    #print "Here's the numbers "+str(numbers)
    if numbers < 10: textnum = "000"+str(numbers)
    elif numbers < 100: textnum = "00"+str(numbers)
    elif numbers < 1000: textnum = "0"+str(numbers)
    else: textnum = str(numbers)

    print "tile Scott_"+textnum

    text = '"label" = '+"'Scott_"+textnum+"'"
    PathSeed = "A:\\"+str(ProcNum)+"\\"
    uniquePathFile = UniqueFileNamer( pathForFile = PathSeed )
    print uniquePathFile
    Tester = True
    while Tester:
        try:
            gp.Select_analysis("X:\\05_Scott\\shp\\Scott_Valley_Processing_Tile_buf.shp", uniquePathFile, text)
            Tester = False
        except:
            pass
                       
    #Select_analysis("Scott_Valley_Processing_Tile","X:/05_Scott/shp/Scott_Valley_Processing_Tile1.shp",""label" = 'Scott_0001' ")
    ## Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "Scott_Valley_Processing_Tile"
#Select_analysis("Scott_Valley_Processing_Tile","X:/05_Scott/shp/Scott_Valley_Processing_Tile1.shp",""label" = 'Scott_0001' ")
    # Process: Copy Raster...

    gp.snapRaster = "X:\\05_Scott\\Snap\\ScottSnap_1m.img"

    gp.extent = uniquePathFile
    gp.delete_management(uniquePathFile)

    print FID0+"Scott_"+textnum, len(FID0+"S_"+textnum)
    #open squid
    fileForCopy = UniqueFileNamer(pathForFile = PathSeed ,extension="")
    print fileForCopy
    Tester = True
    while Tester:
        try:
            gp.CopyRaster_management(thisRaster, fileForCopy, "", "", "", "NONE", "NONE", "")
            Tester = False
        except:
            pass
    
    gp.snapRaster = fileForCopy
    gp.extent = fileForCopy
    fileForAscii = UniqueFileNamer(pathForFile = PathSeed ,extension=".asc")
    Tester = True
    while Tester:
        try:
            gp.RasterToASCII_conversion (fileForCopy, fileForAscii )
            Tester = False
        except:
            pass

    os.system("ASCII2DTM "+FID0+"ScottSnap_"+textnum+".dtm M M 1 10 2 2 " +fileForAscii)

    Tester = True
    while Tester:
        try:
            gp.delete_management(fileForAscii)
            Tester = False
        except:
            pass
    
    Tester = True
    while Tester:
        try:
            gp.delete_management(fileForCopy)
            Tester = False
        except:
            pass

    print "made DTM tile Scott_"+textnum
##################
def WriteScottDEMDriverBAT_2lvl(strPathNameforBat,listPYNames):
    ''' Function to Create Python Programs for the MP Batch Method.
    Takes (strPathNameForPy - a string Path Name for the .bat),
          (numProc -)
    '''
    f = open(strPathNameforBat, 'w')
    for items in listPYNames:
        s1 = 'start "Processor '+str(items)+'" A:\\BATandPY\\'
        s2 = ".bat \n"
        #string = s1+str(items)+s2+" > A:\BATandPY\Proc"+str(items)+"_log.txt 2>&1 \n"
        string = s1+str(items)+s2
        f.write(string)
        f.write("TIMEOUT 7\n")
    f.close

def WriteScottDEMConvertBAT_2lvl(strPathNameforBat,counter):
    ''' Function to Create sub Batch for PY for the MP Batch Method.
    Takes (strPathNameForPy - a string Path Name for the .bat),
          (numProc -)
    '''
    f = open(strPathNameforBat, 'w')

    #s1 = 'start "Processor '+str(counter)+'" c:\\Python25\\python.exe A:\\BATandPY\\'
    s1 = 'c:\\Python25\\python.exe A:\\BATandPY\\'
    s2 = ".py"
    string = s1+str(counter)+s2+" > A:\BATandPY\Proc"+str(counter)+"_log.txt 2>&1 \n"
    f.write(string)
    f.close()

def WriteScottDEMConvertPY_2lvl(strPathNameForPy,listTiles):
    ''' Function to Create Python Programs for the MP Batch Method.
    Takes (strPathNameForPy - a string Path Name for the .py),
          (lisTiles - a python List object of the tile numbers (integers) to be processed)
    '''
    f = open(strPathNameForPy, 'w')
    s1 = "from MP_functions import ScottDEMConvert\n"
    s2 = "listProcess = ["
    #listTemp = [1,2,3,4]    

    f.write(s1)
    f.write(s2)
    
    counter = 0
    for items in listTiles:
        f.write(str(items))
        if counter < (len(listTiles)-1): f.write(",")
        counter += 1
    f.write("]\n")
    f.write("\n")
    f.write("for items in listProcess:\n")
    f.write("    ScottDEMConvert(items)\n")
    f.close()
        
