#!/Library/Frameworks/EPD64.framework/Versions/Current/bin/python

import sys
from numpy import *
import math
import os
import json
import csv

# get the demographic centers of NYC

def readDemographics():
	counter=0
	data = {}
	with open('Demographic_Statistics_By_Zip_Code.csv', 'rb') as csvfile:
		demo_reader = csv.reader(csvfile)
		for row in demo_reader:
			if counter==0:
				header=row
				for term in header:
					data[term]=[]
				counter+=1
				continue

			for i,val in enumerate(row):
				if header[i]!="JURISDICTION NAME":
					data[header[i]].append(float(val))
				else:
					data[header[i]].append(val)
			counter+=1

	for key in data.keys():
		data[key] = array(data[key])
	data["ZIP"] = data["JURISDICTION NAME"]
	return data

def addPopulation(the_data):
	the_data["population"]=zeros(len(data["ZIP"]))

	fin = open("ZipCodeElecPop.tsv")
	summed_pop=0
	for line in fin:
		if '#' in line:
			continue
		vals=line.split()
		zip = vals[0]
		pop = int(vals[3])

		# there are some zipcodes that don't appear in the demographic info.
		# We add their population to their largest neighbor:
		if zip == "10069":
			zip = "10023"
		if zip == "10075":
			zip = "10028"
		if zip == "10282":
			zip = "10007"
		if zip == "10308":
			zip = "10306"
		if zip == "10470":
			zip = "10466"
		if zip == "11004":
			zip = "11426"
		if zip == "11040":
			zip = "11426"
		if zip == "11109":
			zip = "11101"
		if zip == "11363":
			zip = "11362"
		
		summed_pop+=pop
		inds = where(the_data["ZIP"]==zip)[0]
		if len(inds) == 0 and pop>0:
			print zip
		ind = inds[0]
		the_data["population"][ind]=pop
	return the_data

def getZipCodeLatLongs():
	zipToLatLong = json.load(open("zipToLatLong.json"))
	return zipToLatLong

def getCenters(data):
	zipToLatLong = getZipCodeLatLongs()
	centers = {}
	for key in data.keys():
		if "PERCENT" in key:
			root = key.split("PERCENT")[1].strip().lower()
		elif key == "population":	
			root = key
		else:
			continue
		
		print root
		if "total" in root:
			continue
		lat = 0
		lon = 0
		for i in range(len(data["ZIP"])):
			zip = data["ZIP"][i]
			frac = data["population"][i] * data[key][i]

			if frac == 0:
				continue
			norm = dot(data["population"],data[key])
			weight = frac/norm
			lat += weight*zipToLatLong[zip][0]		
			lon += weight*zipToLatLong[zip][1]
		centers[root] = [lat,lon]
	
	print centers
	json.dump(centers,open("demographicCenters.json",'w'))

if __name__ == "__main__":
	data = readDemographics()
	data = addPopulation(data)
	getCenters(data)