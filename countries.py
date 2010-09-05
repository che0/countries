#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osgeo import ogr

class CountryChecker(object):
    """ Loads a country shape file, checks coordinates for country location. """
    
    def __init__(self, country_file):
        driver = ogr.GetDriverByName('ESRI Shapefile')
        self.countryFile = driver.Open(country_file)
        self.layer = self.countryFile.GetLayer()
    
    def getCountry(self, lat, lng):
        """
        Checks given gps-incoming coordinates for country.
        Coordinates are in format (deg)(min).(min_frac)
        Output is either ISO code or None
        """
        
        def degs(val):
            return int(val / 100) + float(val%100)/60
        
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(degs(lat), degs(lng))
        
        for i in range(self.layer.GetFeatureCount()):
            country = self.layer.GetFeature(i)
            if country.geometry().Contains(point):
                return country.GetField('ISO2')
        
        # nothing found
        return None
