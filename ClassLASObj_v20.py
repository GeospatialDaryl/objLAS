class LASObj:
    """  the LAS File Object Class Defintion v 2.0
    Daryl Van Dyke - Klamath Strategic Habitat Conservation Analyst """
    ####################
    def __init__(self,lasfilepath,extentPath):
        import os, shlex, subprocess
        from os import path,system
        from ModuleLiDARtools_v1 import mscanArgs
        import arcpy

        # Scalar Attributes
        self.strpath = lasfilepath
        self.strExtentPath = extentPath
	self.scratch = "C:\\Scratch\\"
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
        self.ap = arcpy

        p3 = subprocess.Popen(['lasinfo',self.las_extent_name], cwd=self.las_extent_dir, 
                              stdout=subprocess.PIPE, stderr = subprocess.STDOUT)

        lasinfo = p3.communicate()[0]
        args = shlex.split(lasinfo)
        if mscanArgs(args,'Min','X'):
            addr = mscanArgs(args,'Min','X')
        else:
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
    def makeCloudMetrics(self, dblCoverCutoff=3.0,FirstOnly = False ):
	    """  Gimme Some Strings, big D"""
	    import os, shlex, subprocess, uuid, csv
	    from os import path,system
	    from ModuleLiDARtools_v1 import CloudMetrics
    
	    #os.system("CloudMetrics /firstreturn /above:"+str(cutoffHeight)+" "+workPath+ldas+" "+workPath+ldas+"_15metr.csv")        
	    cutoffHeight = "/above:"+str(dblCoverCutoff)
    
	    #init call to CloudMetrics
    
	    uniqueFile = uuid.uuid4()
	    uniqueCSV = str(uniqueFile)+".csv"
	    CSVlocation = self.scratch+uniqueCSV
	    print CSVlocation
    
	    #p3 = subprocess.Popen(['CloudMetrics','/firstreturn',cutoffHeight, 
		                   #self.las_name, CSVlocation ], 
		                  #cwd=self.las_dir, 
		                  #stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
	    
	    try:
		p3 = subprocess.check_call(['CloudMetrics','/firstreturn',cutoffHeight, 
		                   self.las_name, CSVlocation ], 
		                  cwd=self.las_dir, 
		                  stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
	    except subprocess.CalledProcessError as err:
		    print "Error:", err
				  
    
    
	    self.CloudMetrics = CloudMetrics(CSVlocation,dblCoverCutoff,FirstOnly) 
	    os.remove(CSVlocation)

    ####################
          
  