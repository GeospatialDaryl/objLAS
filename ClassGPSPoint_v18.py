class GPSPoint:
    """  the LiDAR Project GPSPoint class v1.7"""
    import ClassMetricsHolder
    from ClassMetricsHolder import SetOfCloudMetrics
    def __init__(self,PlotName,Xpos,Ypos,radius_m,objPaths,DOBirth,TreesPerAcre,BAPerAcre,BA2007,QMD2007,SDI2007):
        ################################################
        #
        def LASPathFromXY(coordX,coordY):
            """  Function to Determine the Root FilePath from XY Coords -> str_pathFileSet"""
            if coordY < 4477631:
                pathFileSet = objPaths.pathBull
            elif coordY < 4527737:
                pathFileSet = objPaths.pathSalm
            elif coordY < 4598613:
                pathFileSet = objPaths.pathRwck
            elif coordX > 403122:
                pathFileSet = objPaths.pathMill
            else:
                pathFileSet = objPaths.pathTolo
            return pathFileSet
        #
        ################################################
        self.X = Xpos
        self.Y = Ypos
        
        self.radius_m = radius_m
        
        self.PlotName = PlotName
        self.objPaths = objPaths
        
        #set tile for the point
        self.strX = str(self.X)
        self.tileX = float(self.strX[0:3])*1000.
        self.strY = str(self.Y)
        self.tileY = float(self.strY[0:4])*1000.
        
        self.strTileNum = self.strX[0:3]+"0"+self.strY[0:4]
        
        self.pathFileSet = LASPathFromXY(self.Y,self.Y)
        self.pathDTMtile = self.pathFileSet+"DEM_DTM\\r"+self.strTileNum+".dtm"
        self.pathLAStile = self.pathFileSet+"LAS_b\\"+self.strTileNum+"_b.las"
        
        self.metrics3 = self.SetOfCloudMetrics(3.)
        self.metrics6 = self.SetOfCloudMetrics(6.)
        self.metrics9 = self.SetOfCloudMetrics(9.)
        self.metrics12 = self.SetOfCloudMetrics(12.)
        self.metrics15 = self.SetOfCloudMetrics(15.)
        
        self.Trans_3_6 = 0.
        self.Trans_3_9 = 0.
        self.Trans_6_9 = 0.
        self.Trans_3_12 = 0.
        self.Trans_6_12 = 0.
        self.Trans_9_12 = 0.
        self.Trans_3_15 = 0.
        self.Trans_6_15 = 0.
        self.Trans_9_15 = 0.

        self.oDOB = DOBirth
        self.oBAAcre = BAPerAcre
        self.oTPA = TreesPerAcre
        self.oBA07 = BA2007
        self.oQMD07 = QMD2007
        self.oSDI07 = SDI2007
        
##########################################################################
###
###     Perturb XY Positions
###         
###
#########################################################################
    def XYperturb(self,SD):
        import random
        """Destructive Perturb GPS positions by a known SD  Use a BUP point! """
        self.X = random.gauss(self.X,SD)
        self.Y = random.gauss(self.Y,SD)
        
##########################################################################
###
###     Extract Cylinder
###
###
#########################################################################
    def ExtractCylinder(self,rad_m):
        import os
        from os import system
        import os.path
        
        workspacepath = self.objPaths.scratch+"_Cylinders\\"
        #dtmpath = objPaths.dtmworkspace
        #ldapath = objPaths.lasworkspace
        #hardwired variables: change above
        lX = self.X - rad_m
        lY = self.Y - rad_m
        uX = self.X + rad_m
        uY = self.Y + rad_m
        dtmtilepath = self.pathDTMtile
        lastilepath = self.pathLAStile 
        #test = "ClipData /shape:1 /height /dtm:"+dtmtilepath+" "+ldatilepath+" "+workspacepath+"\\tempCylinder.lda "+str(lX)+" "+str(lY)+" "+str(uX)+" "+str(uY)
        #print test
        #print "ClipData /shape:1 /height /dtm:"+dtmtilepath+" "+lastilepath+" "+workspacepath+self.PlotName+".lda "+str(lX)+" "+str(lY)+" "+str(uX)+" "+str(uY)
        #print "CloudMetrics /firstreturn /above:3 "+workspacepath+self.PlotName+".lda "+workspacepath+self.PlotName+"_metr.csv"
        testval = os.path.isfile(workspacepath+self.PlotName+".lda ")
        if testval:
            print "    Plot LDA file "+workspacepath+self.PlotName+".lda "+"already exists."
        else:
            print "    Generating plot LDA file "+workspacepath+self.PlotName+".lda "
            print "   ClipData /shape:1 /dtm:"+dtmtilepath+" "+lastilepath+" /zmin:-10. /zmax:150. /height "+workspacepath+self.PlotName+".lda "+str(lX)+" "+str(lY)+" "+str(uX)+" "+str(uY)
            os.system("ClipData /shape:1 /dtm:"+self.pathFileSet+"DEM_DTM\\r*.dtm"+" /zmin:-10. /zmax:150. /height "+lastilepath+" "+workspacepath+self.PlotName+".lda "+str(lX)+" "+str(lY)+" "+str(uX)+" "+str(uY))
        ##  metricsReader
        cutoffHeight = 3.
        os.system("CloudMetrics /firstreturn /above:"+str(cutoffHeight)+" "+workspacepath+self.PlotName+".lda "+workspacepath+self.PlotName+"_3metr.csv")
        self.metrics3.harvestMetrics(workspacepath,self.PlotName+"_3metr.csv")
        cutoffHeight = 6.
        os.system("CloudMetrics /firstreturn /above:"+str(cutoffHeight)+" "+workspacepath+self.PlotName+".lda "+workspacepath+self.PlotName+"_6metr.csv")
        self.metrics6.harvestMetrics(workspacepath,self.PlotName+"_6metr.csv")
        cutoffHeight = 9.
        os.system("CloudMetrics /firstreturn /above:"+str(cutoffHeight)+" "+workspacepath+self.PlotName+".lda "+workspacepath+self.PlotName+"_9metr.csv")
        self.metrics9.harvestMetrics(workspacepath,self.PlotName+"_9metr.csv")
        cutoffHeight = 12.
        os.system("CloudMetrics /firstreturn /above:"+str(cutoffHeight)+" "+workspacepath+self.PlotName+".lda "+workspacepath+self.PlotName+"_12metr.csv")
        self.metrics12.harvestMetrics(workspacepath,self.PlotName+"_12metr.csv")
        cutoffHeight = 15.
        os.system("CloudMetrics /firstreturn /above:"+str(cutoffHeight)+" "+workspacepath+self.PlotName+".lda "+workspacepath+self.PlotName+"_15metr.csv")
        self.metrics15.harvestMetrics(workspacepath,self.PlotName+"_15metr.csv")


        
        



