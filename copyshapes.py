#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osgeo import ogr

def filter_file(filter_func, infile, outfile):
    """
    Saves all infile shapes which pass through filter_func to outfile.
    
    Example:
    filter_file(lambda x: x.GetField('ISO2') == 'CZ', 'TM_WORLD_BORDERS-0.3.shp', 'cz.shp')
    """
    driver = ogr.GetDriverByName('ESRI Shapefile')
    
    inDS = driver.Open(infile)
    inLayer = inDS.GetLayer()
    
    outDS = driver.CreateDataSource(outfile)
    outLayer = outDS.CreateLayer('filtered')
    
    feat = inLayer.GetFeature(0) # first feature
    for field in feat.keys():
        outLayer.CreateField(feat.GetFieldDefnRef(field))
    del feat
    
    featureDefn = outLayer.GetLayerDefn()
    for i in range(inLayer.GetFeatureCount()):
        feat = inLayer.GetFeature(i)
        if not filter_func(feat):
            continue
        
        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(feat.GetGeometryRef())
        for field in feat.keys():
            outFeature.SetField(field, feat.GetField(field))
        outLayer.CreateFeature(outFeature)
