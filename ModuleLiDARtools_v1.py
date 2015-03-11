####################  ModuleLiDARtools_v1.py
class Paths:
    def __init__(self):
        #self.dtmworkspace = "M:\LiDAR_filesets\3_Salm\DEM_DTM" No closing \\ on dtm,las,scratch ws, but on scratchmerged.  FIX THIS!
        self.indexSHP = ""
        self.workspace = "A:\\"
        self.dtmworkspace = ""
        self.lasworkspace = ""
        self.chmworkspace = ""
        self.csvworkspace = ""
        self.metricsworkspace = ""
        self.lasExtent = ""
        self.lasnorm = ""
        self.dem = ""
        #self.lasworkspace = "D:\\LAS\\"
        self.scratch = "A:\\"
        self.scratchmerged = "J:\\Scratch\\merged\\"
        self.pathTrin = "X:\\01_Trinity\\"
        self.pathMill = "P:\\00_Parks\\2_Mill\\"
        #self.pathMill = "X:\\00_Parks\\2_Mill\\"
        self.pathBull = "X:\\00_Parks\\0_Bull\\"
        self.pathRwck = "X:\\00_Parks\\1_RWCk\\"
        self.pathSalm = "X:\\00_Parks\\3_Salm\\"
        self.pathTolo = "X:\\00_Parks\\4_Tolo\\"
        self.pathShastaRepair = "C:\\Scratch\\ShastaRepair_LAS\\pt2\\"
        self.OutputPath = "M:\\TreeHeightsProj\\"
        self.pathSctt = "X:\\05_Scott\\"
        self.templateRasters = "X:\\00_Parks\\_Data\\templates\\"
        self.tilename = ""
####################
def UniqueFileNamer(pathForFile = "A:\\",extension =".shp"):
    '''
    General Function to Create a Reasonably Unique File Name & Path
    takes two optional arguments:
    path for file <"A:\\">
    extension <".shp">
    '''
    import uuid
    uniqueFile = str(uuid.uuid4() )
    print "before: "+uniqueFile
    uniqueFile.replace("-","_")
    print "after: "+uniqueFile
    temp = uniqueFile[0:8]+uniqueFile[9:13]+uniqueFile[14:17]
    uniqueFile = temp
    uniquePathFile = pathForFile+"T"+str(uniqueFile)[0:12]+extension
    return uniquePathFile       


####################
def mscanArgs(args,strScan1,strScan2):
    '''matches strings based on position scanning '''
    stop = len(args) + 1
    k = 0
    myStr1 = str(strScan1)
    myStr2 = str(strScan2)
    for items in args:
        #print k, items
        if items == strScan1:
            if args[k+1] == strScan2:
                return k
        k = k+1
        if k == stop: return -1

####################
def list2commastring(listofstrings):
    joinedlistParameters = ""
    for items in listofstrings:
        if joinedlistParameters == "":
            joinedlistParameters = items
        else: joinedlistParameters = joinedlistParameters+","+items
    return joinedlistParameters
####################

####################
class GDALSampler:
    '''
    Creates a GDAL Sampler for querying rasters.  GDALSampler("C:\\Path\to\raster.ext")
    '''
    def __init__(self,fn = 'C:\\Scratch\\ShastaDEM\\shastaDEM.img'):

        # ----->  GDAL Init
        #from osgeo import gdal as gdal
        import arcpy
        import os
        environList = os.environ['PATH'].split(';')
        environList.insert(0, r'C:\Program Files\gdalwin32-1.6\bin')
        os.environ['PATH'] = ';'.join(environList)
        import osgeo.ogr as gdal       
        import osgeo.gdal as gdal

        ## -- HFA is the Imagine only driver  -->
        #driver = gdal.GetDriverByName('HFA')
        #driver.Register()
        ## <--  END HFA only
        gdal.AllRegister()
        
        #fn = 'C:\\Scratch\\ShastaDEM\\shastaDEM.img'
        self.ds = gdal.Open( str(fn) )
        #Get image Size
        
        self.cols = self.ds.RasterXSize
        self.rows = self.ds.RasterYSize
        self.bands = self.ds.RasterCount
        #Get reference info
        self.geotransform = self.ds.GetGeoTransform()
        self.originX = self.geotransform[0]
        self.originY = self.geotransform[3]
        self.pixelWidth = self.geotransform[1]
        self.pixelHeight = self.geotransform[5]
    
    def val(self,smplX,smplY):
        x = smplX
        y = smplY

        xOffset = int( (x - self.originX) / self.pixelWidth)
        yOffset = int( (y - self.originY) / self.pixelHeight)
         
        band = self.ds.GetRasterBand(1)
        #data = band.ReadAsArray(xOffset, yOffset, 1, 1)   <-----  GDAL 1.6
        data = band.ReadAsArray(xOffset, yOffset, 1, 1)
        value = data[0,0]
        return value
     
    
####################

####################################################################################################
class CloudMetrics:
    """  A class to store a set of metrics from FUSION """
    def __init__(self, CSVLocation, dblCutoff, FirstOnly):
        import csv
        self.FirstOnly = FirstOnly
        self.dblCutoff = dblCutoff
        self.CloudM = {}
        #self.CloudM['FileTitle']=''
        #self.CloudM['Total_retu']=''
        #self.CloudM['Ret1_cnt']=''
        #self.CloudM['Ret2_cnt']=''
        #self.CloudM['Ret3_cnt']=''
        #self.CloudM['Ret4_cnt']=''
        #self.CloudM['Ret5_cnt']=''
        #self.CloudM['Ret6_cnt']=''
        #self.CloudM['Ret7_cnt']=''
        #self.CloudM['Ret8_cnt']=''
        #self.CloudM['Ret9_cnt']=''
        #self.CloudM['Othr_cnt']=''
        #self.CloudM['Elev_Min']=''
        #self.CloudM['Elev_Max']=''
        #self.CloudM['Elev_Mean']=''
        #self.CloudM['Elev_Mode']=''
        #self.CloudM['Elev_StdDev']=''
        #self.CloudM['Elev_Vari']=''
        #self.CloudM['Elev_CV']=''
        #self.CloudM['Elev_IQD']=''
        #self.CloudM['Elev_Skew']=''
        #self.CloudM['Elev_Kurt']=''
        #self.CloudM['Elev_AAD']=''
        #self.CloudM['Elev_L1']=''
        #self.CloudM['Elev_L2']=''
        #self.CloudM['Elev_L3']=''
        #self.CloudM['Elev_L4']=''
        #self.CloudM['Elev_L_CV']=''
        #self.CloudM['Elev_L_ske']=''
        #self.CloudM['Elev_L_kur']=''
        #self.CloudM['Elev_P01']=''
        #self.CloudM['Elev_P05']=''
        #self.CloudM['Elev_P10']=''
        #self.CloudM['Elev_P20']=''
        #self.CloudM['Elev_P25']=''
        #self.CloudM['Elev_P30']=''
        #self.CloudM['Elev_P40']=''
        #self.CloudM['Elev_P50']=''
        #self.CloudM['Elev_P60']=''
        #self.CloudM['Elev_P70']=''
        #self.CloudM['Elev_P75']=''
        #self.CloudM['Elev_P80']=''
        #self.CloudM['Elev_P90']=''
        #self.CloudM['Elev_P95']=''
        #self.CloudM['Elev_P99']=''
        #self.CloudM['Int_Minimu']=''
        #self.CloudM['Int_Maximu']=''
        #self.CloudM['Int_Mean']=''
        #self.CloudM['Int_Mode']=''
        #self.CloudM['Int_StdDev']=''
        #self.CloudM['Int_Varian']=''
        #self.CloudM['Int_CV']=''
        #self.CloudM['Int_Interq']=''
        #self.CloudM['Int_Skewne']=''
        #self.CloudM['Int_Kurtos']=''
        #self.CloudM['Int_AAD']=''
        #self.CloudM['Int_L1']=''
        #self.CloudM['Int_L2']=''
        #self.CloudM['Int_L3']=''
        #self.CloudM['Int_L4']=''
        #self.CloudM['Int_L_CV']=''
        #self.CloudM['Int_L_skew']=''
        #self.CloudM['Int_L_kurt']=''
        #self.CloudM['Int_P01']=''
        #self.CloudM['Int_P05']=''
        #self.CloudM['Int_P10']=''
        #self.CloudM['Int_P20']=''
        #self.CloudM['Int_P25']=''
        #self.CloudM['Int_P30']=''
        #self.CloudM['Int_P40']=''
        #self.CloudM['Int_P50']=''
        #self.CloudM['Int_P60']=''
        #self.CloudM['Int_P70']=''
        #self.CloudM['Int_P75']=''
        #self.CloudM['Int_P80']=''
        #self.CloudM['Int_P90']=''
        #self.CloudM['Int_P95']=''
        #self.CloudM['Int_P99']=''
        #self.CloudM['Perc1stAbove']=''
        #self.CloudM['PercAllAbove']=''
        #self.CloudM['PercAllFirst']=''
        #self.CloudM['FirstAbove']=''
        #self.CloudM['AllAbove']=''
        #self.CloudM['Per1AbvMean']=''
        #self.CloudM['Per1AbvMode']=''
        #self.CloudM['PerAAbvMean']=''
        #self.CloudM['PerAAbvMode']=''
        #self.CloudM['PerMeanFirst']=''
        #self.CloudM['PerModeFirst']=''
        #self.CloudM['FirstAbvMean']=''
        #self.CloudM['FirstAbvMode']=''
        #self.CloudM['AllAbvMean']=''
        #self.CloudM['AllAbvMode']=''
        #self.CloudM['Total_1st']=''
        #self.CloudM['Total_All']=''

        #try:
        f = open(CSVLocation)
        CSVreader = csv.reader( f )
        row1 = CSVreader.next()
        row2 = CSVreader.next()
        
        del row1
        
        #self.CloudM['DataFile']=(row2[0])
        #self.CloudM['FileTitle']=(row2[1])
        #self.CloudM['Total_retu']=int(row2[2])
        #self.CloudM['Ret1_cnt']=int(row2[3])
        #self.CloudM['Ret2_cnt']=int(row2[4])
        #self.CloudM['Ret3_cnt']=int(row2[5])
        #self.CloudM['Ret4_cnt']=int(row2[6])
        #self.CloudM['Ret5_cnt']=int(row2[7])
        #self.CloudM['Ret6_cnt']=int(row2[8])
        #self.CloudM['Ret7_cnt']=int(row2[9])
        #self.CloudM['Ret8_cnt']=int(row2[10])
        #self.CloudM['Ret9_cnt']=int(row2[11])
        #self.CloudM['Othr_cnt']=int(row2[12])
        #self.CloudM['Elev_Min']=float(row2[13])
        #self.CloudM['Elev_Max']=float(row2[14])
        #self.CloudM['Elev_Mean']=float(row2[15])
        #self.CloudM['Elev_Mode']=float(row2[16])
        #self.CloudM['Elev_StdDev']=float(row2[17])
        #self.CloudM['Elev_Vari']=float(row2[18])
        #self.CloudM['Elev_CV']=float(row2[19])
        #self.CloudM['Elev_IQD']=float(row2[20])
        #self.CloudM['Elev_Skew']=float(row2[21])
        #self.CloudM['Elev_Kurt']=float(row2[22])
        #self.CloudM['Elev_AAD']=float(row2[23])
        #self.CloudM['Elev_L1']=float(row2[24])
        #self.CloudM['Elev_L2']=float(row2[25])
        #self.CloudM['Elev_L3']=float(row2[26])
        #self.CloudM['Elev_L4']=float(row2[27])
        #self.CloudM['Elev_L_CV']=float(row2[28])
        #self.CloudM['Elev_L_ske']=float(row2[29])
        #self.CloudM['Elev_L_kur']=float(row2[30])
        #self.CloudM['Elev_P01']=float(row2[31])
        #self.CloudM['Elev_P05']=float(row2[32])
        #self.CloudM['Elev_P10']=float(row2[33])
        #self.CloudM['Elev_P20']=float(row2[34])
        #self.CloudM['Elev_P25']=float(row2[35])
        #self.CloudM['Elev_P30']=float(row2[36])
        #self.CloudM['Elev_P40']=float(row2[37])
        #self.CloudM['Elev_P50']=float(row2[38])
        #self.CloudM['Elev_P60']=float(row2[39])
        #self.CloudM['Elev_P70']=float(row2[40])
        #self.CloudM['Elev_P75']=float(row2[41])
        #self.CloudM['Elev_P80']=float(row2[42])
        #self.CloudM['Elev_P90']=float(row2[43])
        #self.CloudM['Elev_P95']=float(row2[44])
        #self.CloudM['Elev_P99']=float(row2[45])
        #self.CloudM['Int_Minimu']=float(row2[46])
        #self.CloudM['Int_Maximu']=float(row2[47])
        #self.CloudM['Int_Mean']=float(row2[48])
        #self.CloudM['Int_Mode']=float(row2[49])
        #self.CloudM['Int_StdDev']=float(row2[50])
        #self.CloudM['Int_Varian']=float(row2[51])
        #self.CloudM['Int_CV']=float(row2[52])
        #self.CloudM['Int_Interq']=float(row2[53])
        #self.CloudM['Int_Skewne']=float(row2[54])
        #self.CloudM['Int_Kurtos']=float(row2[55])
        #self.CloudM['Int_AAD']=float(row2[56])
        #self.CloudM['Int_L1']=float(row2[57])
        #self.CloudM['Int_L2']=float(row2[58])
        #self.CloudM['Int_L3']=float(row2[59])
        #self.CloudM['Int_L4']=float(row2[60])
        #self.CloudM['Int_L_CV']=float(row2[61])
        #self.CloudM['Int_L_skew']=float(row2[62])
        #self.CloudM['Int_L_kurt']=float(row2[63])
        #self.CloudM['Int_P01']=float(row2[64])
        #self.CloudM['Int_P05']=float(row2[65])
        #self.CloudM['Int_P10']=float(row2[66])
        #self.CloudM['Int_P20']=float(row2[67])
        #self.CloudM['Int_P25']=float(row2[68])
        #self.CloudM['Int_P30']=float(row2[69])
        #self.CloudM['Int_P40']=float(row2[70])
        #self.CloudM['Int_P50']=float(row2[71])
        #self.CloudM['Int_P60']=float(row2[72])
        #self.CloudM['Int_P70']=float(row2[73])
        #self.CloudM['Int_P75']=float(row2[74])
        #self.CloudM['Int_P80']=float(row2[75])
        #self.CloudM['Int_P90']=float(row2[76])
        #self.CloudM['Int_P95']=float(row2[77])
        #self.CloudM['Int_P99']=float(row2[78])
        #self.CloudM['Perc1stAbove']=float(row2[79])
        #self.CloudM['PercAllAbove']=float(row2[80])
        #self.CloudM['PercAllFirst']=float(row2[81])
        #self.CloudM['FirstAbove']=int(row2[82])
        #self.CloudM['AllAbove']=int(row2[83])
        #self.CloudM['Per1AbvMean']=float(row2[84])
        #self.CloudM['Per1AbvMode']=float(row2[85])
        #self.CloudM['PerAAbvMean']=float(row2[86])
        #self.CloudM['PerAAbvMode']=float(row2[87])
        #self.CloudM['PerMeanFirst']=float(row2[88])
        #self.CloudM['PerModeFirst']=float(row2[89])
        #self.CloudM['FirstAbvMean']=int(row2[90])
        #self.CloudM['FirstAbvMode']=int(row2[91])
        #self.CloudM['AllAbvMean']=int(row2[92])
        #self.CloudM['AllAbvMode']=int(row2[93])
        #self.CloudM['Total_1st']=int(row2[94])
        #self.CloudM['Total_All']=int(row2[95])
	self.CloudM['DataFile']=(row2[0])
	self.CloudM['FileTitle']=(row2[1])
	self.CloudM['Total_retu']=int(row2[2])
	self.CloudM['Ret1_cnt']=int(row2[3])
	self.CloudM['Ret2_cnt']=int(row2[4])
	self.CloudM['Ret3_cnt']=int(row2[5])
	self.CloudM['Ret4_cnt']=int(row2[6])
	self.CloudM['Ret5_cnt']=int(row2[7])
	self.CloudM['Ret6_cnt']=int(row2[8])
	self.CloudM['Ret7_cnt']=int(row2[9])
	self.CloudM['Ret8_cnt']=int(row2[10])
	self.CloudM['Ret9_cnt']=int(row2[11])
	self.CloudM['Othr_cnt']=int(row2[12])
	self.CloudM['Elev_Min']=float(row2[13])
	self.CloudM['Elev_Max']=float(row2[14])
	self.CloudM['Elev_Mean']=float(row2[15])
	self.CloudM['Elev_Mode']=float(row2[16])
	self.CloudM['Elev_StdDev']=float(row2[17])
	self.CloudM['Elev_Vari']=float(row2[18])
	self.CloudM['Elev_CV']=float(row2[19])
	self.CloudM['Elev_IQD']=float(row2[20])
	self.CloudM['Elev_Skew']=float(row2[21])
	self.CloudM['Elev_Kurt']=float(row2[22])
	self.CloudM['Elev_AAD']=float(row2[23])
	self.CloudM['Elev_MADmed']=float(row2[24])
	self.CloudM['Elev_MADmode']=float(row2[25])
	self.CloudM['Elev_L1']=float(row2[26])
	self.CloudM['Elev_L2']=float(row2[27])
	self.CloudM['Elev_L3']=float(row2[28])
	self.CloudM['Elev_L4']=float(row2[29])
	self.CloudM['Elev_L_CV']=float(row2[30])
	self.CloudM['Elev_L_ske']=float(row2[31])
	self.CloudM['Elev_L_kur']=float(row2[32])
	self.CloudM['Elev_P01']=float(row2[33])
	self.CloudM['Elev_P05']=float(row2[34])
	self.CloudM['Elev_P10']=float(row2[35])
	self.CloudM['Elev_P20']=float(row2[36])
	self.CloudM['Elev_P25']=float(row2[37])
	self.CloudM['Elev_P30']=float(row2[38])
	self.CloudM['Elev_P40']=float(row2[39])
	self.CloudM['Elev_P50']=float(row2[40])
	self.CloudM['Elev_P60']=float(row2[41])
	self.CloudM['Elev_P70']=float(row2[42])
	self.CloudM['Elev_P75']=float(row2[43])
	self.CloudM['Elev_P80']=float(row2[44])
	self.CloudM['Elev_P90']=float(row2[45])
	self.CloudM['Elev_P95']=float(row2[46])
	self.CloudM['Elev_P99']=float(row2[47])
	self.CloudM['CanRelRatio']=float(row2[48])
	self.CloudM['ElevSQRTmeanSQ']=float(row2[49])
	self.CloudM['ElevCURTmeanCUBE']=float(row2[50])
	self.CloudM['Int_Min']=float(row2[51])
	self.CloudM['Int_Max']=float(row2[52])
	self.CloudM['Int_Mean']=float(row2[53])
	self.CloudM['Int_Mode']=float(row2[54])
	self.CloudM['Int_StdDev']=float(row2[55])
	self.CloudM['Int_Var']=float(row2[56])
	self.CloudM['Int_CV']=float(row2[57])
	self.CloudM['Int_IQ']=float(row2[58])
	self.CloudM['Int_Skew']=float(row2[59])
	self.CloudM['Int_Kurt']=float(row2[60])
	self.CloudM['Int_AAD']=float(row2[61])
	self.CloudM['Int_L1']=float(row2[62])
	self.CloudM['Int_L2']=float(row2[63])
	self.CloudM['Int_L3']=float(row2[64])
	self.CloudM['Int_L4']=float(row2[65])
	self.CloudM['Int_L_CV']=float(row2[66])
	self.CloudM['Int_L_skew']=float(row2[67])
	self.CloudM['Int_L_kurt']=float(row2[68])
	self.CloudM['Int_P01']=float(row2[69])
	self.CloudM['Int_P05']=float(row2[70])
	self.CloudM['Int_P10']=float(row2[71])
	self.CloudM['Int_P20']=float(row2[72])
	self.CloudM['Int_P25']=float(row2[73])
	self.CloudM['Int_P30']=float(row2[74])
	self.CloudM['Int_P40']=float(row2[75])
	self.CloudM['Int_P50']=float(row2[76])
	self.CloudM['Int_P60']=float(row2[77])
	self.CloudM['Int_P70']=float(row2[78])
	self.CloudM['Int_P75']=float(row2[79])
	self.CloudM['Int_P80']=float(row2[80])
	self.CloudM['Int_P90']=float(row2[81])
	self.CloudM['Int_P95']=float(row2[82])
	self.CloudM['Int_P99']=float(row2[83])
	self.CloudM['Perc1stAbove']=float(row2[84])
	self.CloudM['PercAllAbove']=float(row2[85])
	self.CloudM['PercAllFirst']=float(row2[86])
	self.CloudM['FirstAbove']=float(row2[87])
	self.CloudM['AllAbove']=float(row2[88])
	self.CloudM['Per1AbvMean']=float(row2[89])
	self.CloudM['Per1AbvMode']=float(row2[90])
	self.CloudM['PerAAbvMean']=float(row2[91])
	self.CloudM['PerAAbvMode']=float(row2[92])
	self.CloudM['PerMeanFirst']=float(row2[93])
	self.CloudM['PerModeFirst']=float(row2[94])
	self.CloudM['FirstAbvMean']=float(row2[95])
	self.CloudM['FirstAbvMode']=float(row2[96])
	self.CloudM['AllAbvMean']=float(row2[97])
	self.CloudM['AllAbvMode']=float(row2[98])
	self.CloudM['Total_1st']=float(row2[99])
	self.CloudM['Total_All']=float(row2[100])


        del row2
####################################################################################################
class StandMetrics(CloudMetrics):
    """ A subclass of CloudMetrics for Forest Stand Analysis
    """
    def __init__(self,path):
	    import os
	    os.system("cloudmetrics /new /above:3 "+path+" c:\\Scratch\\out.csv")
	    CloudMetrics.__init__(self, "c:\\Scratch\\out.csv", 3.0, False)





####################

####################
def WriteOutputTable(listOfGPSPointObjs, myPaths, strNameOfOutputTable="output.csv"):
    import csv
    pathForOutput = myPaths.OutputPath
    outputWriter = csv.writer(open(pathForOutput+strNameOfOutputTable,'w'))
    #write header
    headerRow = ['DataFile' ,   #0
                 'Points' ,   #1
                 'Elev Minimum' ,   #2
                 'Elev Maximum' ,   #3
                 'Elev Mean' ,   #4
                 'Elev Median' ,   #5
                 'Elev Mode' ,   #6
                 'Elev StdDev' ,   #7
                 'Elev Variance' ,   #8
                 'Elev InterquartileDistance' ,   #9
                 'Elev Skewness' ,   #10
                 'Elev Kurtosis' ,   #11
                 'Elev AAD' ,   #12
                 'Elev P25' ,   #13
                 'Elev P50' ,   #14
                 'Elev P75' ,   #15
                 'Elev P05' ,   #16
                 'Elev P10' ,   #17
                 'Elev P20' ,   #18
                 'Elev P30' ,   #19
                 'Elev P40' ,   #20
                 'Elev P50' ,   #21
                 'Elev P60' ,   #22
                 'Elev P70' ,   #23
                 'Elev P80' ,   #24
                 'Elev P90' ,   #25
                 'Elev P95' ,   #26
                 'Int Minimum' ,   #27
                 'Int Maximum' ,   #28
                 'Int Mean' ,   #29
                 'Int Median' ,   #30
                 'Int Mode' ,   #31
                 'Int StdDev' ,   #32
                 'Int Variance' ,   #33
                 'Int InterquartileDistance' ,   #34
                 'Int Skewness' ,   #35
                 'Int Kurtosis' ,   #36
                 'Int AAD' ,   #37
                 'Int P25' ,   #38
                 'Int P50' ,   #39
                 'Int P75' ,   #40
                 'Int P05' ,   #41
                 'Int P10' ,   #42
                 'Int P20' ,   #43
                 'Int P30' ,   #44
                 'Int P40' ,   #45
                 'Int P50' ,   #46
                 'Int P60' ,   #47
                 'Int P70' ,   #48
                 'Int P80' ,   #49
                 'Int P90' ,   #50
                 'Int P95' ,   #51
                 'Cover3' ,   #52
                 'Cover6' ,   #53
                 'Cover9' ,   #54
                 'Cover12' ,   #55
                 'Cover15' ,   #56
                 'Trans_3_6' ,   #57
                 'Trans_3_9' ,   #58
                 'Trans_6_9' ,   #59
                 'Trans_3_12' ,   #60
                 'Trans_6_12' ,   #61
                 'Trans_9_12' ,   #62
                 'Trans_3_15' ,   #63
                 'Trans_6_15' ,   #64
                 'Trans_9_15' ,   #65
                 'Trans_12_15' ,    #66
                 'PlotID' ,       #67
                 'oDOB'   , #68
                 'oTPA'  ,  #69
                 'oBAAcre' ,   #70
                 'oBA07'  ,  #71
                 'oQMD07' ,   #72
                 'oSDI07'    #73
                 ]
    outputWriter.writerow(headerRow)
    for GPSPointObj in listOfGPSPointObjs:
        outputWriter.writerow(  [  
            GPSPointObj.metrics3.DataFile , #0
            GPSPointObj.metrics3.Points , #1
            GPSPointObj.metrics3.Elev_Minimum , #2
            GPSPointObj.metrics3.Elev_Maximum , #3
            GPSPointObj.metrics3.Elev_Mean , #4
            GPSPointObj.metrics3.Elev_Median , #5
            GPSPointObj.metrics3.Elev_Mode , #6
            GPSPointObj.metrics3.Elev_StdDev , #7
            GPSPointObj.metrics3.Elev_Variance , #8
            GPSPointObj.metrics3.Elev_InterquartileDistance , #9
            GPSPointObj.metrics3.Elev_Skewness , #10
            GPSPointObj.metrics3.Elev_Kurtosis , #11
            GPSPointObj.metrics3.Elev_AAD , #12
            GPSPointObj.metrics3.Elev_P25 , #13
            GPSPointObj.metrics3.Elev_P50 , #14
            GPSPointObj.metrics3.Elev_P75 , #15
            GPSPointObj.metrics3.Elev_P05 , #16
            GPSPointObj.metrics3.Elev_P10 , #17
            GPSPointObj.metrics3.Elev_P20 , #18
            GPSPointObj.metrics3.Elev_P30 , #19
            GPSPointObj.metrics3.Elev_P40 , #20
            GPSPointObj.metrics3.Elev_P50 , #21
            GPSPointObj.metrics3.Elev_P60 , #22
            GPSPointObj.metrics3.Elev_P70 , #23
            GPSPointObj.metrics3.Elev_P80 , #24
            GPSPointObj.metrics3.Elev_P90 , #25
            GPSPointObj.metrics3.Elev_P95 , #26
            GPSPointObj.metrics3.Int_Minimum , #27
            GPSPointObj.metrics3.Int_Maximum , #28
            GPSPointObj.metrics3.Int_Mean , #29
            GPSPointObj.metrics3.Int_Median , #30
            GPSPointObj.metrics3.Int_Mode , #31
            GPSPointObj.metrics3.Int_StdDev , #32
            GPSPointObj.metrics3.Int_Variance , #33
            GPSPointObj.metrics3.Int_InterquartileDistance , #34
            GPSPointObj.metrics3.Int_Skewness , #35
            GPSPointObj.metrics3.Int_Kurtosis , #36
            GPSPointObj.metrics3.Int_AAD , #37
            GPSPointObj.metrics3.Int_P25 , #38
            GPSPointObj.metrics3.Int_P50 , #39
            GPSPointObj.metrics3.Int_P75 , #40
            GPSPointObj.metrics3.Int_P05 , #41
            GPSPointObj.metrics3.Int_P10 , #42
            GPSPointObj.metrics3.Int_P20 , #43
            GPSPointObj.metrics3.Int_P30 , #44
            GPSPointObj.metrics3.Int_P40 , #45
            GPSPointObj.metrics3.Int_P50 , #46
            GPSPointObj.metrics3.Int_P60 , #47
            GPSPointObj.metrics3.Int_P70 , #48
            GPSPointObj.metrics3.Int_P80 , #49
            GPSPointObj.metrics3.Int_P90 , #50
            GPSPointObj.metrics3.Int_P95 , #51
            GPSPointObj.metrics3.Cover,  #52
            GPSPointObj.metrics6.Cover,  #53
            GPSPointObj.metrics9.Cover,  #54
            GPSPointObj.metrics12.Cover,  #55
            GPSPointObj.metrics15.Cover,  #56
            GPSPointObj.Trans_3_6 , #57
            GPSPointObj.Trans_3_9 , #58
            GPSPointObj.Trans_6_9 , #59
            GPSPointObj.Trans_3_12 , #60
            GPSPointObj.Trans_6_12 , #61
            GPSPointObj.Trans_9_12 , #62
            GPSPointObj.Trans_3_15 , #63
            GPSPointObj.Trans_6_15 , #64
            GPSPointObj.Trans_9_15 , #65
            GPSPointObj.Trans_12_15,  #66
            GPSPointObj.PlotName   ,   #67
            GPSPointObj.oDOB ,   #68
            GPSPointObj.oTPA ,   #69
            GPSPointObj.oBAAcre ,   #70
            GPSPointObj.oBA07 ,   #71
            GPSPointObj.oQMD07 ,   #72
            GPSPointObj.oSDI07   #73
        ] ) 



####################

def RasterSampler(inRaster,X,Y):
    from ModuleLiDARtools_v1 import mscanArgs
    import subprocess
    import shlex
    
    #p3 = subprocess.Popen( ['C:\OSGeo4W\apps\gdal-dev\bin\gdallocationinfo.exe -geoloc',inRaster,X,Y] , 
    #                      stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
                          #cwd=self.las_extent_dir, 
    p3 = subprocess.Popen( ['C:\\OSGeo4W\\apps\\gdal-dev\\bin\\gdallocationinfo.exe', '-geoloc',inRaster,str(X),str(Y)] ,
                           stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
    locinfo = p3.communicate()[0]
    args = shlex.split(locinfo)            
    #addr = mscanArgs(args,'Min','X')  
    return float(args[-1])
    #return rasterVal,extant

####################
def DTMDescriber(objLAS):
    PASS
####################

#def LASPathFromXY_Global(X,Y,objPaths):
    #"""  Function to Determine the Root FilePath from XY Coords"""
    #if self.Y < 4477631:
        #self.pathFileSet = objPaths.pathBull
    #elif self.Y < 4527737:
        #self.pathFileSet = objPaths.pathSalm
    #elif self.Y < 4598613:
        #self.pathFileSet = objPaths.pathRwck
    #elif self.X > 403122:
        #self.pathFileSet = objPaths.pathMill
    #else:
        #self.pathFileSet = objPaths.pathTolo
    #return self.pathFileSet
