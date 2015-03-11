class LASObj:
    """  the LAS File Object Class Defintion v 1.0
    Daryl Van Dyke - Klamath Strategic Habitat Conservation Analyst """
    ####################
    def __init__(self,fname,workPaths):
        import os, shlex, subprocess
        from os import path,system
        from ModuleLiDARtools_v1 import mscanArgs

        # Scalar Attributes
        self.workPaths = workPaths
        lasfilepath = self.workPaths.lasworkspace+fname
        self.strpath = self.workPaths.lasworkspace+fname
        extentPath =  self.workPaths.lasExtent+fname
        self.strExtentPath = extentPath
        #print self.strpath
        path_and_name = os.path.split(lasfilepath)
        path_and_name_extent = os.path.split(extentPath)

        self.las_dir = path_and_name[0]
        self.las_extent_dir = path_and_name_extent[0]

        self.las_name = path_and_name[1]
        self.las_extent_name = path_and_name_extent[1]

        self.dtm_dir = ""
        self.dtm_name = path_and_name[0:len(path_and_name)-4]
        self.tilename = self.dtm_name

        p3 = subprocess.Popen(['lasinfo',self.las_extent_name], cwd=self.las_extent_dir, 
                              stdout=subprocess.PIPE, stderr = subprocess.STDOUT)

        lasinfo = p3.communicate()[0]
        args = shlex.split(lasinfo)            
        addr = mscanArgs(args,'min','x')

        Xmin = args[addr+4]
        Ymin = args[addr+5]
        Zmin = args[addr+6]
        addr = addr + 7
        Xmax = args[addr+4]
        Ymax = args[addr+5]
        Zmax = args[addr+6]

        self.minX = float(Xmin)
        self.maxX = float(Xmax)
        self.minY = float(Ymin)
        self.maxY = float(Ymax)
        self.minZ = float(Zmin)
        self.maxZ = float(Zmax)
        
        self.minXTile = 0.
        self.maxXTile = 0.
        self.minYTile = 0.
        self.maxYTile = 0.
        
        self.edgeBuffer = 35.

    ####################
    def makeNormalizedLAS(self,workPaths,inputDEM=""):
        """  Make a ground normalized LAS file"""
        import os
        from ModuleLiDARtools_v1 import GDALSampler
        from os import path
        import liblas, struct
        from liblas import file,header,point

        import arcgisscripting

        gp = arcgisscripting.create(9.3)
        gp.AddToolbox("C:\Program Files (x86)\ArcGIS\ArcToolBox\Toolboxes\Conversion Tools.tbx")
        gp.overwriteoutput = 1        
        ws = workPaths.dem
        
        # 0 - Init Paths & Objects
        if inputDEM == "":
            gp.Workspace = ws
            fcs = gp.ListRasters("*")
            if len(fcs) != 1: 
                print "Problem with the DEM"
                exit
            myDEM = workPaths.dem+fcs[0]
        else: myDEM = inputDEM
        
        # 1 - Init GDAL Connection

        smpl = GDALSampler(myDEM)
        
        # 2 - Init LAS Connection
        
        idata = file.File(self.strpath,mode = 'r')
        
        # 3 - Make Child LAS for LAS_norm

        h = header.Header()

        oLAS = workPaths.lasnorm+self.las_name[0:len(self.las_name)-4]+"_norm.las"
        odata = file.File(oLAS, mode='w',header=h)
        
        # 4 - Copy
        
        badZs = 0
        for p in idata:
            pt = liblas.point.Point()
            pt = p
            zAdj = smpl.val(p.x,p.y)
            newZ = p.z - zAdj
            pt.z = newZ
            if zAdj < 0.: 
                #print zAdj
                badZs += 1
                #pass
            else: odata.write(pt)
            
        odata.close()
        idata.close()
        
        # 5 - Set Header info
        f = file.File(oLAS)
        oh = f.header
        f.close()
        
        oh.system_id = "KSHC - daryl_van_dyke@fws.gov"
        oh.software_id = "ground normalized LAS"
        #g = liblas.guid.GUID()
        #oh.guid = g
        
        f = file.File(oLAS, mode='w+', header=oh)
        f.close()
        
        os.system("lasinfo -i "+oLAS+" -repair")
        print "There were "+str(badZs)+" bad Z elevations."
        print "  for the LAS_norm produced at: "+oLAS
        print " "
        print " "
        
    ####################
    def makeCHM_UTMN83(self,workPaths,dblRes=1.0,peaks=0):
        """Make a CHM.  (objPaths,<dblResolution>=1.0,<peaks? 0/1>)=0"""
        print "Make a CHM.  (objPaths,<dblResolution>,<peaks? 0/1>)"
        import os
        from os import path
        option = ""
        option0 = "CanopyModel /ground:"
        option1 = "CanopyModel /peaks /ground:"
        if peaks == 0:
            text1 = option0
        else:
            text1 = option1
        text2 = " "+str(dblRes)+" m m 1 10 2 2 "
        #ORI: os.system(text1+workPaths.dtmworkspace+r"\r"+self.las_name[0:8]+".dtm "+workPaths.scratch+r'/'+self.las_name[0:8]+text2+self.strpath)
        os.system(text1+workPaths.dtmworkspace+"r"+self.las_name[0:8]+".dtm "+workPaths.scratch+"temp"+text2+self.strpath)
        os.system("ClipDTM "+workPaths.scratch+"temp "+workPaths.scratch+self.las_name[0:8]+"chm"+str(dblRes)+".dtm "+str(self.minX-25.)+" "+str(self.minY-25.)+" "+str(self.maxX+25.)+" "+str(self.maxY+25.))
        ############################################################################
    ####################
    def makeCHM_StatePlaneFt(self,workPaths,dblRes=1.0,peaks=0):
        """Make a CHM.  (objPaths,<dblResolution>=1.0,<peaks? 0/1>)=0"""
        print "Make a CHM.  (objPaths,<dblResolution>,<peaks? 0/1>)"
        import os
        from os import path
        option = ""
        option0 = "CanopyModel /ground:"
        option1 = "CanopyModel /peaks /ground:"
        if peaks == 0:
            text1 = option0
        else:
            text1 = option1
        text2 = " "+str(dblRes)+" F F 2 10 2 2 "
        #ORI: os.system(text1+workPaths.dtmworkspace+r"\r"+self.las_name[0:8]+".dtm "+workPaths.scratch+r'/'+self.las_name[0:8]+text2+self.strpath)
        os.system(text1+workPaths.dtmworkspace+"*.dtm "+workPaths.scratch+"temp"+text2+self.strpath)
        strLength  = len(self.las_name)
        s = "ClipDTM "+workPaths.scratch+"temp "+workPaths.chmworkspace + \
          self.las_name[0:(strLength-4)] + "chm"+str(dblRes) + \
          ".dtm "+str(self.minX-25.)+" "+str(self.minY-25.)+" "+str(self.maxX+25.)+ \
          " "+str(self.maxY+25.)
        os.system( s )
        #os.system("ClipDTM "+workPaths.scratch+"temp "+workPaths.chmworkspace +
                    #self.las_name[0:(len(self.las_name)-4))] + "chm"+str(dblRes) +
        #".dtm "+str(self.minX-25.)+" "+str(self.minY-25.)+" "+str(self.maxX+25.)+
        #" "+str(self.maxY+25.) )
        ############################################################################

    ####################
    def makeMetrics(self,workPaths,dblCoverCutoff=1.0,listParameters=["count","min","max","mean",
                                                                      "mode","stddev","variance","cv",
                                                                      "cover","skewness","kurtosis","p05",
                                                                      "p10","p20","p25","p30","p40","p50",
                                                                      "p60","p70","p80","p90","p95"],dblCellSize=25.):
        """  Make a set of metrics. ( objPaths ,{ dblCoverCutoff , listParameters , dblCellSize } )"""
        import os
        from os import path
        from ModuleLiDARtools_v1 import list2commastring

        halfwidth = dblCellSize/2.0
        strX1Y1X2Y2 = str(self.minX+halfwidth)+","+str(self.minY+halfwidth)+","+str(self.maxX+halfwidth)+","+str(self.maxY+halfwidth)
        rasterparameters = list2commastring(listParameters)    
        text1 = "GridMetrics /raster:"+rasterparameters
        #text2 = " /ascii /nocsv /outlier:0,200 /align:"+workPaths.dtmworkspace+r"\r"+self.las_name[0:8]+".dtm "+workPaths.dtmworkspace+r"\r"+self.las_name[0:8]+".dtm 3 1 "+workPaths.scratch+r'/'+self.las_name[0:8]+" "+self.strpath
        #text2 = " /ascii /nocsv /outlier:0,200 /align:"+workPaths.dtmworkspace+r"\r"+self.las_name[0:8]+".dtm "+workPaths.dtmworkspace+r"\r"+self.las_name[0:8]+".dtm "+str(dblCoverCutoff)+" 1 "+workPaths.scratch+self.las_name[0:8]+"_cov"+str(int(dblCoverCutoff))+".dtm "+self.strpath
        text2 = " /fuels /outlier:-10,200 /gridxy:"+strX1Y1X2Y2+" "+workPaths.dtmworkspace+r"\r"+self.las_name[0:8]+".dtm "+str(dblCoverCutoff)+" "+str(dblCellSize)+" "+workPaths.scratch+self.las_name[0:8]+"_cov"+str(int(dblCoverCutoff))+".dtm "+self.strpath
        print text1+text2
        os.system(text1+text2)

    ####################
    def makeCloudMetrics(self, workPaths, dblCoverCutoff=1.0,FirstOnly = False ):
        """  Gimme Some Strings, big D"""
        import os, shlex, subprocess, uuid, csv
        from os import path,system
        from ModuleLiDARtools_v1 import CloudMetrics
        
        #os.system("CloudMetrics /firstreturn /above:"+str(cutoffHeight)+" "+workPath+ldas+" "+workPath+ldas+"_15metr.csv")        
        cutoffHeight = "/above:"+str(dblCoverCutoff)
        
        #init call to CloudMetrics

        uniqueFile = uuid.uuid4()
        uniqueCSV = str(uniqueFile)+".csv"
        CSVlocation = workPaths.workspace+uniqueCSV
        #p3 = subprocess.Popen(['CloudMetrics','/firstreturn',cutoffHeight, 
                               #self.las_name, workPaths.workspace+uniqueCSV ], 
                              #cwd=self.las_extent_dir, 
                              #stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
        if FirstOnly:
            os.system("CloudMetrics /above:"+str(dblCoverCutoff)+ \
                      " "+self.strpath+" "+CSVlocation)
        else:
            os.system("CloudMetrics /firstreturn /above:"+str(dblCoverCutoff)+ \
                      " "+self.strpath+" "+CSVlocation)
        #print "CloudMetrics /firstreturn /above:"+str(dblCoverCutoff)+ \
        #          " "+self.strpath+" "+CSVlocation
        
        self.CloudMetrics = CloudMetrics(CSVlocation,dblCoverCutoff,FirstOnly)       
    ####################
          
    ####################
    def makeNormalizedLAS_GDAL_ORI(self,inputDEM_TIF):
        """  Make a ground normalized LAS file"""
        import os
        from ModuleLiDARtools_v1 import GDALSampler
        from os import path
        import liblas, struct

        dem = 'J:\\LiDAR_filesets\\2_Mill\\DEM\\mill_v6.tif'
        lasworkspace = "J:\\LiDAR_filesets\\2_Mill\\LAS_b"
        lasworkspaceo = "J:\\LiDAR_filesets\\2_Mill\\LAS_normGDAL"
        dataset = gdal.Open( dem )#, GA_ReadOnly)
        ws = lasworkspace
        #gp.workspace = ws
        dirList = os.listdir(ws)
        print dirList
        for files in dirList:
            if "las" in files:
                f = file.File(ws+"\\"+files,mode='r')
                header = f.header
                #h = header.Header()
                #header.dataformat_id = 3
                #header.minor_version = 1
                fout = file.File(lasworkspaceo+"\\"+files,mode='w',header=header)
                pt = liblas.point.Point()
                for p in f:
                    #if p.classification == 1:
                    elevation = CellValue( dataset, 1, p.x,p.y)
                        #print p.x, p.y,'elev =',elevation
                    temp_pz = p.z - elevation
                    #if p.z > elevation - 0.5:
                    #    if p.z < elevation + 2.5:
                    p.z = temp_pz
                    pt = p
                    fout.write(pt)
                fout.close()
    ####################
    def  makeGridMetrics(self, dblCellSize = 1, dblCoverCutoff = 1., logFirstOnly = False):
        import os, shlex, subprocess, uuid, csv
        from os import path,system
        from ModuleLiDARtools_v1 import CloudMetrics, UniqueFileNamer

        cutoffHeight = str(dblCoverCutoff)
        
        #init call to GridMetrics
        uniqueFile = uuid.uuid4()
        uniqueCSV = str(uniqueFile)+".csv"
        #CSVlocation = self.workPaths.workspace+uniqueCSV
        CSVlocation = self.workPaths.metricsworkspace+uniqueCSV
        CSVlocation_realName = self.workPaths.metricsworkspace+self.las_name[0:(len(self.las_name)-4)]+".csv"
        
        if logFirstOnly:
            text1 = "GridMetrics /first /ascii /raster:count /align:"+self.workPaths.Snap1+\
                    self.las_name[0:5]+"Snap"+self.las_name[5:(len(self.las_name)-4)]+".dtm "
                    #self.las_name[0:(len(self.las_name)-4)]+".dtm "
        else:
            text1 = "GridMetrics /ascii /raster:count /align:"+self.workPaths.Snap1+\
                    self.las_name[0:5]+"Snap"+self.las_name[5:(len(self.las_name)-4)]+".dtm "
            #text1 = "GridMetrics /ascii /nocsv /raster:count /align:X:\\05_Scott\\Snap\\ScottSnap_25m.dtm "
           
        strOptions = ""
        
        #os.system(" "+text1+self.workPaths.dtmworkspace+"*.dtm "+cutoffHeight \
                  #+" "+str(dblCellSize) +" "+ CSVlocation +" "+self.strpath)
        os.system(" "+text1+self.workPaths.dtmworkspace+"*.dtm "+cutoffHeight \
                  +" "+str(dblCellSize) +" "+ CSVlocation_realName +" "+self.strpath)
        #print "SQUID!!!"
        
    ####################
    def getExtentsFromTileSHP(self):
        import ogr, sys, os
        import arcgisscripting
        from ModuleLiDARtools_v1 import UniqueFileNamer
        
        gp = arcgisscripting.create(9.3)
        
        os.chdir(self.workPaths.indexSHP)
        fs = os.listdir("")
        for f in fs:
            if ".shp.xml" in f:
                fs.remove(f)
        for f in fs:
            if ".shp" in f:
                thisF = f
        
        #text = '"label" = '+"'Scott_"+textnum+"'"
        text =  '"label" = ' + "'" + self.las_name[0:len(self.las_name)-4] + "'"
        uniquePathFile = UniqueFileNamer()
        gp.Select_analysis(self.workPaths.indexSHP+thisF, uniquePathFile, text)
        desc = gp.describe(uniquePathFile)
        
        self.minXTile = int(desc.extent.Xmin)-int(self.edgeBuffer)
        self.maxXTile = int(desc.extent.Xmax)+int(self.edgeBuffer)
        self.minYTile = int(desc.extent.Ymin)-int(self.edgeBuffer)
        self.maxYTile = int(desc.extent.Ymax)+int(self.edgeBuffer)
        
        #driver = ogr.GetDriverByName('ESRI Shapefile')
        #dataSource = driver.Open(thisF, 0)
        
        #layer = dataSource.GetLayer(0)
        gp.delete_management(uniquePathFile)
        print "squid"
    
    ####################
    def makeNormalizedLAS_MP(self,objGP,workPaths,inputDEM=""):
        """  Make a ground normalized LAS file"""
        import os
        from ModuleLiDARtools_v1 import GDALSampler
        from os import path
        import liblas, struct
        from liblas import file,header,point

        gp = objGP
        
        gp.overwriteoutput = 1        
        ws = workPaths.dem
        
        # 0 - Init Paths & Objects
        if inputDEM == "":
            gp.Workspace = ws
            fcs = gp.ListRasters("*")
            if len(fcs) != 1: 
                print "Problem with the DEM"
                exit
            myDEM = workPaths.dem+fcs[0]
        else: myDEM = inputDEM
        
        # 1 - Init GDAL Connection

        smpl = GDALSampler(myDEM)
        
        # 2 - Init LAS Connection
        
        idata = file.File(self.strpath,mode = 'r')
        
        # 3 - Make Child LAS for LAS_norm

        h = header.Header()

        oLAS = workPaths.lasnorm+self.las_name[0:len(self.las_name)-4]+"_norm.las"
        odata = file.File(oLAS, mode='w',header=h)
        
        # 4 - Copy
        
        for p in idata:
            pt = liblas.point.Point()
            pt = p
            zAdj = smpl.val(p.x,p.y)
            newZ = p.z - zAdj
            pt.z = newZ
            if zAdj < 0.: 
                #print zAdj
                pass
            else: odata.write(pt)
            
        odata.close()
        idata.close()
        
        # 5 - Set Header info
        f = file.File(oLAS)
        oh = f.header
        f.close()
        
        oh.system_id = "KSHC - daryl_van_dyke@fws.gov"
        oh.software_id = "ground normalized LAS"
        #g = liblas.guid.GUID()
        #oh.guid = g
        
        f = file.File(oLAS, mode='w+', header=oh)
        f.close()
        
        os.system("lasinfo -i "+oLAS+" -repair")

        
    ####################
        
        
        
        
        