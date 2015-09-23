class Vec2D:
    import math 
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return self.x*other.x + self.y*other.y
    def Vmul(self, other):
        return self.x*other.x + self.y*other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '(%g, %g)' % (self.x, self.y)

    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5

    def __ne__(self, other):
        return not self.__eq__(other)  # reuse __eq__

class XSpt():   
    def __init__(self,objXS,x,y,z,i):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.i = float(i)
        self.m = float(objXS.Slope_m)
        self.objXS = objXS
        self.offset_X = objXS.Begin_X
        self.offset_Y = objXS.Begin_Y
        self.off_X = self.x - self.offset_X
        self.off_Y = self.y - self.offset_Y
        self.ptV = Vec2D(self.off_X,self.off_Y)

        #project point onto line
        #self.XSdist = ( ( self.ptV * objXS.U ) / ( objXS.U * objXS.U) ) * objXS.U
        #self.XSdist = Vmul( Vmul( self.ptV , objXS.U ) / Vmul( objXS.U , objXS.U) ) , objXS.U)
        num =  self.ptV * objXS.U 
        denom =  objXS.U * objXS.U
        projX = (num/denom) * objXS.U_x
        projY = (num/denom) * objXS.U_y
        Vhat = Vec2D( projX,projY)        
        self.XSdist =  abs(Vhat)

class ShastaXS():
    import os
    from osgeo import gdal 
    from osgeo import ogr 
    from osgeo import osr 
    from osgeo import gdal_array 
    from osgeo import gdalconst 
    from osgeo.gdalconst import *

    def __init__(self, listXSRow):
        self.OBJECTID = int( listXSRow[0] )
        #self.Join_Count = int( listXSRow[1] )
        self.Name = "XS"+str(listXSRow[2])
        self.CentroidX = float( listXSRow[7] )
        self.CentroidY = float( listXSRow[8] )
        #self.Group = int( listXSRow[5] )
        #self.Route = int( listXSRow[6] )
        self.routeM = int( listXSRow[2] )
        #self.Name_1 = listXSRow[8]
        self.Name_1 = self.Name
        self.Shape_Leng = float( listXSRow[12] )
        self.Begin_X = float( listXSRow[3] )
        self.Begin_Y = float( listXSRow[4] )
        self.End_X = float( listXSRow[5] )
        self.End_Y = float( listXSRow[6] )
        self.Length_ft = float( listXSRow[12] )
        self.Slope_m = float( listXSRow[9] )
        self.Compass_az = 10
        self.LASExists = int(0)
        self.nPts = int(0)
        self.U_x = (self.End_X)-(self.Begin_X)
        self.U_y = (self.End_Y)-(self.Begin_Y)
        self.dictXSpts = {}
        self.nXSpts = int(0)
        self.U = Vec2D(self.U_x,self.U_y)
        #self.u = self.U/(self.Length_ft)
        self.u_x = self.U_x/self.Length_ft
        self.u_y = self.U_y/self.Length_ft
        self.minZ = 0.
        self.WSurfZ = 0.
        self.ChannelCenterX = 0.
        self.ChannelCenterY = 0.
        self.rastLowestX = 0.
        self.rastLowestY = 0.
        self.rastLowestZ = 0.

    def MakeXS_v1(self,pathToDir="X:\\02_Shasta\\03_XS_LAS\\"):
        # http://stackoverflow.com/questions/1996518/retrieving-the-output-of-subprocess-call
        myName = str(self.Name_1)
        strCall = "C:\\FUSION\\las2txt.exe" + " -i " + pathToDir+myName+".las -o C:\\Scratch\\tempXS_las.xyz -parse xyzi"
        p = subprocess.Popen(strCall, stdout=subprocess.PIPE)
        result = p.communicate()[0]
        #list1 = os.popen(strCall).read()
        string = "hello2"
        print >>sys.stderr, "hello", len(result), string
        try:
            #retcode = call("las2txt" + " -i "+pathToDir+self.Name_1+".las -o ", shell=True)
            retcode = call(strCall, shell=True)
            if retcode < 0:
                print >>sys.stderr, "Child was terminated by signal", -retcode
            else:
                print >>sys.stderr, "Child returned", retcode
        except OSError, e:
            print >>sys.stderr, "Execution failed:", e
        BREAK

    def MakeXS(self,pathToDir="C:\\Users\\dkvandyke\\03_XS_LAS_v2\\"):
        import os,csv
        '''
        Make Me a Cross section <PathToDir> for exported XS File
        '''
        myName = str(self.Name_1[2:])
        strCall = "C:\\FUSION\\las2txt.exe" + " -i " + pathToDir+myName+".las -o A:\\tempXS_las.xyz -parse xyzi"
        try:
            os.system(strCall)
        except OSError, e:
            print >>sys.stderr, "Execution failed:", e

        f = open("A:\\tempXS_las.xyz", 'r')
        XYZreader = csv.reader(f, delimiter=" ")
        k = 0
        for rows in XYZreader:
            pt = XSpt(self,rows[0],rows[1],rows[2],rows[3])
            self.dictXSpts[k] = pt
            k = k + 1
        self.nXSpts = k

    def OutputXS(self,XSNum):
        fname = "R:\\Shasta_XS\\tabular\\"+self.Name_1+".csv"
        #File prep
        if os.path.isfile(fname):
            os.remove(fname)
        fout = open(fname,"w")
        header = "X,Y,Z,dist\n"
        fout.write(header)

        k = 0
        while k < self.nXSpts:    
            #value = (self.dictXSpts[XSNum].off_X,",", self.dictXSpts[XSNum].off_Y,",", self.dictXSpts[XSNum].z,",", self.dictXSpts[XSNum].XSdist,"\n")
            s = str(self.dictXSpts[k].off_X)+","+str(self.dictXSpts[k].off_Y)+","+str(self.dictXSpts[k].z)+","+str(self.dictXSpts[k].XSdist)+"\n"
            #s = str(value)
            k = k+1
            fout.write(s)

    def Scanner(self,XSNum):
        k = 0
        self.minZ = +100000.
        while k < self.nXSpts:
            if self.dictXSpts[k].z < self.minZ : self.minZ = self.dictXSpts[k].z
            k = k+1

    def CalcMinZ(self,XSNum):
        k = 0
        self.minZ = +100000.
        while k < self.nXSpts:
            if self.dictXSpts[k].z < self.minZ : self.minZ = self.dictXSpts[k].z
            k = k+1

    def MinZ(self):
        '''
        ndepth=int(50),     -    depth of XS in feet from lowest point 
        dblSliceWidth=.25,  -    Width of Sample
        dblSampleDeltaZ=0.1,-    Slicing Resolution (in Z)
        test=False          -    debug reporting
        '''
        tempList = []
        j = 0
        nlpts = self.nXSpts
        while j < nlpts:
            tempList.append(self.dictXSpts[j].z)
            j = j+1

        #Scan for minZ
        kount = 0
        self.minZ = +100000.
        while kount < self.nXSpts:
            if self.dictXSpts[kount].z < self.minZ :
                self.minZ = self.dictXSpts[kount].z
                self.ChannelCenterX = self.dictXSpts[kount].x
                self.ChannelCenterY = self.dictXSpts[kount].y
            kount = kount + 1

    def WSElev(self,ndepth=int(50),dblSliceWidth=.25,dblSampleDeltaZ=0.1,test=False,histo=False):
        '''
        ndepth=int(50),     -    depth of XS in feet from lowest point 
        dblSliceWidth=.25,  -    Width of Sample
        dblSampleDeltaZ=0.1,-    Slicing Resolution (in Z)
        test=False          -    debug reporting
        '''
        tempList = []
        j = 0
        nlpts = self.nXSpts
        while j < nlpts:
            tempList.append(self.dictXSpts[j].z)
            j = j+1

        #Scan for minZ
        kount = 0
        self.minZ = +100000.
        while kount < self.nXSpts:
            if self.dictXSpts[kount].z < self.minZ : self.minZ = self.dictXSpts[kount].z
            kount = kount + 1

        #build  bins & populate
        bins = []
        slices = int( ndepth * (1/dblSampleDeltaZ) )
        for ints in range(0,slices):
            number = self.minZ + 0.1*ints
            bins.append( [number,int(0) ] )

        for vals in bins:   #Scan and increment bins
            for zs in tempList:
                if zs <= vals[0] +dblSliceWidth and zs >= vals[0] - dblSliceWidth:
                    vals[1] = vals[1] + 1    

        if test:
            for pairs in bins:
                print pairs

        def SearchHisto(listBins,ratioTest=0.5):
            ''' Search histo gets a list of bins.
            Bin Lists are two element lists, [ [bin_UL_value , bin_count] ]
            '''
            localMax = int(-1)
            localMaxKey = int(0)
            j = 0
            while j < len(listBins):
                if listBins[j][1] >= localMax: 
                    localMax = listBins[j][1]
                    localMaxKey = j
                if listBins[j][1] < ratioTest * localMax:
                    if listBins[localMaxKey-1][1] == listBins[localMaxKey][1]:
                        return (listBins[localMaxKey-1][0] + listBins[localMaxKey][0] )/2.
                    elif listBins[localMaxKey-2][1] == listBins[localMaxKey][1]:
                        return (listBins[localMaxKey-2][0] + listBins[localMaxKey-1][0]+ listBins[localMaxKey][0] )/3.
                    else:
                        return listBins[localMaxKey][0]
                if test: print str(j)+" "+str(localMaxKey)+" "+str(localMax)
                j = j+1

        if test: print "Test"  
        if histo:
            from scitools.std import compute_histogram,plot
            x,y = compute_histogram(tempList,nbins=50)
            plot(x,y)
        #Here's the Call
        self.WSurfZ = SearchHisto(bins,0.8)

        # Now, calculate the centroid of the channel bottom (from WSurfZ)
        #def CalcCentroid(self,tolerance=0.7):
        tolerance = 1.7
        tempList = []      
        j = 0
        minX = 10000000.
        maxX = 0.
        minY = 100000000.
        maxY = 0.
        nlpts = self.nXSpts
        nptsSlice = 0.
        slicePts = []
        while j < nlpts:
            #if abs( self.dictXSpts[j].z - self.WSurfZ <= tolerance):
            if self.dictXSpts[j].z < self.WSurfZ + tolerance:
                slicePts.append(self.dictXSpts[j])
                nptsSlice = nptsSlice + 1		

                #if self.dictXSpts[j].x <= minX: 
                    #minX = self.dictXSpts[j].x 
                    #if test: print "minX",minX

                #if self.dictXSpts[j].x >= maxX: 
                    #maxX = self.dictXSpts[j].x 
                    #if test: print maxX

                #if self.dictXSpts[j].y <= minY: 
                    #minY = self.dictXSpts[j].y 
                    #if test: print "minY",minY

                #if self.dictXSpts[j].y >= maxY: 
                    #maxY = self.dictXSpts[j].y 
                    #if test:print "maxY",maxY

            j = j+1
        if test: print "Num Pts in Slice",nptsSlice

        #Report Location
        sumX = 0.
        sumY = 0.
        for pts in slicePts:
            sumX = sumX + pts.x
            sumY = sumY + pts.y
        #self.ChannelCenterX = (maxX-minX)/2. + minX
        #self.ChannelCenterY = (maxY-minY)/2. + minY
        self.ChannelCenterX = sumX/len(slicePts)
        self.ChannelCenterY = sumY/len(slicePts)

    def ChannelGeometry(self):
        
        #with my cross-section, k
        dictSamplePoints = {}
        i = 0        
        # ##########################
        # ###   Refactor Me
        # ##########################
        class GDALSampler:
            '''
            Creates a GDAL Sampler for querying rasters
            '''
            def __init__(self,fn = 'C:\\Scratch\\ShastaDEM\\shastaDEM.img'):

                # ----->  GDAL Init
                from osgeo import gdal
                driver = gdal.GetDriverByName('HFA')
                driver.Register()
                #fn = 'C:\\Scratch\\ShastaDEM\\shastaDEM.img'
                self.ds = gdal.Open(fn)
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
                data = band.ReadAsArray(xOffset, yOffset, 1, 1)
                value = data[0,0]
                return value
        rasterSample = GDALSampler()
        self.rastLowestZ = 1000000000000.
        while i < 151:
            smplX = self.Begin_X + i*self.u_x
            smplY = self.Begin_Y + i*self.u_y
            smplTuple = (smplX,smplY)
            #print smplTuple

            dictSamplePoints[str(i)] = rasterSample.val(smplX,smplY)
            if dictSamplePoints[str(i)] < self.rastLowestZ:
                self.rastLowestX = smplX
                self.rastLowestY = smplY
                self.rastLowestZ = dictSamplePoints[str(i)]
                #print self.rastLowestX,self.rastLowestY,self.rastLowestZ
            i = i + 1