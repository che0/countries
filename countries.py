#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osgeo import ogr

class Point(object):
    """ Wrapper for ogr point """
    def __init__(self, lat, lng):
        """ Coordinates are in degrees """
        self.point = ogr.Geometry(ogr.wkbPoint)
        self.point.AddPoint(lng, lat)
    
    def getOgr(self):
        return self.point
    ogr = property(getOgr)

class Country(object):
    """ Wrapper for ogr country shape. Not meant to be instantiated directly. """
    def __init__(self, shape):
        self.shape = shape
    
    def getIso(self):
        return self.shape.GetField('ISO2')
    iso = property(getIso)
    
    def __str__(self):
        return self.shape.GetField('NAME')
    
    def contains(self, point):
        return self.shape.geometry().Contains(point.ogr)

class CountryChecker(object):
    """ Loads a country shape file, checks coordinates for country location. """
    
    def __init__(self, country_file):
        driver = ogr.GetDriverByName('ESRI Shapefile')
        self.countryFile = driver.Open(country_file)
        self.layer = self.countryFile.GetLayer()
        
        self.allCountries = ogr.Geometry(ogr.wkbMultiPolygon)
        self.allCountries.Empty()
        for i in xrange(self.layer.GetFeatureCount()):
            country = self.layer.GetFeature(i)
            print 'adding %s' % country.GetField('NAME')
            self.allCountries = self.allCountries.Union(country.geometry())
    
    def getCountry(self, point):
        """
        Checks given gps-incoming coordinates for country.
        Output is either country shape index or None
        """
        
        for i in xrange(self.layer.GetFeatureCount()):
            country = self.layer.GetFeature(i)
            if country.geometry().Contains(point.ogr):
                return Country(country)
        
        # nothing found
        return None
    
    def inSomeCountry(self, point):
        """ Checks whether given point is in any country. """
        return self.allCountries.Contains(point.ogr)

class CountryMapper(object):
    """ Uses a CountryChecker to create a country map of given area. """
    
    def __init__(self, checker, step=0.01):
        """ Initializes mapper with a given checkers and step (in degrees). """
        self.checker = checker
        self.step = step
    
    @staticmethod
    def fracRange(start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step
    
    def findLastEmptyLng(self, lat, minLng, maxLng):
        """ Finds last longitude without country. """
        lng = minLng
        while lng < maxLng:
            oldLng = lng
            lng += 0.5
            if self.checker.inSomeCountry(Point(lat, lng)):
                return oldLng
        return lng
    
    def mapLine(self, lat, minLng, maxLng):
        """ Creates map line for given latitude. """
        output = []
        lng = minLng
        curCountry = None
        curCountryStart = None
        triedFastForward = False
        while lng < maxLng:
            oldLng = lng
            if curCountry == None and not triedFastForward:
                lng = self.findLastEmptyLng(lat, curCountryStart or minLng, maxLng)
                triedFastForward = True
            else:
                lng += self.step
            point = Point(lat, lng)
            if curCountry == None:
                changed = self.checker.inSomeCountry(point)
            else:
                point = Point(lat, lng)
                changed = not curCountry.contains(point)
            if not changed:
                continue
            newCountry = self.checker.getCountry(point)
            print lat, lng, newCountry
            triedFastForward = False
            if curCountry != None:
                output.append((curCountryStart, oldLng, curCountry.iso))
            curCountry = newCountry
            curCountryStart = lng
        
        if curCountry != None:
            output.append((curCountryStart, lng, curCountry.iso))
        
        return output
    
    def createMap(self, minLat, maxLat, minLng, maxLng):
        """
        Creates a "map", consisting of dictionary of latitudes, which each has
        a list of tuples (minLng, maxLng, country).
        """
        out = {}
        for lat in self.fracRange(minLat, maxLat, self.step):
            out[lat] = self.mapLine(lat, minLng, maxLng)
        return out
