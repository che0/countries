These are two miniature tools intended to help with the task of finding what country are given GPS coordinates in.

The tools are:

 -- copyshapes.py
 Filter country shapes to create a smaller shape file. Use like this:
 1) get world borders from http://thematicmapping.org/downloads/world_borders.php
 2) run python
      import copyshapes
      copyshapes.filter_file(
            lambda x: x.GetField('REGION') == 150,
            'TM_WORLD_BORDERS-0.3.shp', 'EUROPE.shp'
      )

 -- countries.py
 Find what countries given GPS coordinates are.
 Example:
     import countries
     cc = countries.CountryChecker('TM_WORLD_BORDERS-0.3.shp')
     print cc.getCountry(countries.Point(49.7821, 3.5708)).iso


LICENSE:

This code is in public domain.
