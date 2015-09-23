def MoransI(data,field,arcpy):
    '''   Calculate Morans-I stats for a *field* given a *data*
    returns 3-tuple of floats:  ( Morans-I val, Z-score, P-value ) '''
    res = arcpy.SpatialAutocorrelation_stats(data,field,"NO_REPORT","INVERSE_DISTANCE","EUCLIDEAN_DISTANCE","NONE")
    return ( float(res.getOutput(0)), float(res.getOutput(1)), float(res.getOutput(2)) )
    
def MoransIv2(data,field,arcpy):
    '''   Calculate Morans-I stats for a *field* given a *data*
    returns 3-tuple of floats:  ( Morans-I val, Z-score, P-value ) 
    This version handles bad values without crashing - returning a (0,0,0) tuple.
    '''
    try:
        res = arcpy.SpatialAutocorrelation_stats(data,field,"NO_REPORT","INVERSE_DISTANCE","EUCLIDEAN_DISTANCE","NONE")
        outTuple = ( float(res.getOutput(0)), float(res.getOutput(1)), float(res.getOutput(2)) )
    except:
        outTuple = ( 0., 0., 0.)
    return outTuple
