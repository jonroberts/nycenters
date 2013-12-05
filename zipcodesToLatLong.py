#!/Library/Frameworks/EPD64.framework/Versions/Current/bin/python

import sys
from numpy import *
import math
import os
import json

# reads in the zipcodes and creates a central lat, long of the zipcodes from the bounding box.
zipcodes = json.load(open("nyc-zip-code-tabulation-areas-4326.json"))

# create a dictionary pof zipcodes to central lat/longs
zipToLatLong={}

for f in zipcodes["features"]:
	zip = f["properties"]["ZIP"]
	geometry = array(f["geometry"]["coordinates"])
	
	if zip == "11373" or zip == "10007":
		# lots of disconnected little pieces of this outline. We just need the first
		geometry = array(geometry[0][0]).transpose()
	else:
		geometry = array(geometry[0]).transpose()

	minLon=min(geometry[0])
	maxLon=max(geometry[0])
	
	minLat = min(geometry[1])
	maxLat = max(geometry[1])
	centerLon = (maxLon + minLon)/2.
	centerLat = (maxLat + minLat)/2.
	zipToLatLong[zip]=[centerLat,centerLon]

json.dump(zipToLatLong,open("zipToLatLong.json",'w'))
