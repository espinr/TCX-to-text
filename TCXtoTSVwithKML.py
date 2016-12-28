#-------------------------------------------------------------------------------
# Name:        TCXtoTSVwithKML.py
# Purpose:     Simple script to convert TCX files into a Tab Separated Values 
#              text file with a row as KML linestrings 
#
#               User will need to set the input file(s) directory (line 47),
#               and output path and filename (line 53)
#
# Author:      Martin Alvarez - @espinr
#
# Created:     December/2016
#       Code forked from https://github.com/bspauld/TCXtoShape
#
#       Code requires following python libraries:
#
#       Fiona - http://toblerity.org/fiona/manual.html
#       Shapely - http://toblerity.org/shapely/manual.html
#       pyproj - https://pypi.python.org/pypi/pyproj/
#-------------------------------------------------------------------------------

import os, sys, re
from xml.etree.ElementTree import fromstring
import fiona
from fiona.crs import from_epsg
from shapely.geometry import mapping, Point, LineString
import pyproj
import datetime as dt
from datetime import timedelta,datetime

#Set Parameters for Geographic Transformation
geod = pyproj.Geod(ellps='WGS84')

#function to return the data in the specific TCX tags - code from https://github.com/jhofman/fitnesshacks
def findtext(e, name, default=None):
    """
    findtext
    helper function to find sub-element of e with given name and
    return text value
    returns default=None if sub-element isn't found
    """
    try:
        return e.find(name).text
    except:
        return default

#input data path - where all the TCX renamed files live
path = './data'

#Set RunID
RunID = 1

#output folder and file
outputFilePath =  './output/runningStringlines.txt'

outputPointsTXT = open(outputFilePath, 'a' )
outputPointsTXT.write('RunID\tTime\tDistance\tgeometry\n')


listing = [f for f in os.listdir(path) if re.match(r'.*\.tcx', f)]

for infile in listing:

    try:
        #build empty list
        datalist = []

        #Input file TCX file
        inputFile = infile
        outputShapefileName = (infile.split("."))[0]

        print("Proccesing "+outputShapefileName + " Run")

        istream = open(path+'/'+inputFile,'r')

        #initialize an ID counter
        idval = 0

        # read xml contents
        xml = istream.read()

        # parse tcx file
        xml = re.sub('xmlns=".*?"','',xml)

        # parse xml
        tcx=fromstring(xml)

        #pull the activity type from the TCX file
        activity = tcx.find('.//Activity').attrib['Sport']

        print ("    TCX Extraction > Run ID: " + str(RunID) + "...")

        #build a list for all the points from the TCX file
        for lap in tcx.findall('.//Lap'):

            trackpoints = []

            DistanceMeters = float(findtext(lap, 'DistanceMeters'))
            timestamp = lap.attrib['StartTime']


            for point in lap.findall('.//Trackpoint'):

                AltitudeMeters = float(findtext(point, 'AltitudeMeters'))

                LatitudeDegrees = float(findtext(point, 'Position/LatitudeDegrees'))
                LongitudeDegrees = float(findtext(point, 'Position/LongitudeDegrees'))
                dateTime = str(findtext(point, 'Time'))

                trackpoints.append((dateTime,LongitudeDegrees,LatitudeDegrees,AltitudeMeters))

            datalist.append((timestamp,DistanceMeters,trackpoints))

        #set counters as global variables
        distanceCounter = 0.0
        timeCounter = datetime.strptime(str("0.0"), "%S.%f")
        timeCounterSecs = 0

        #move through the TCX file to calculate run values and append a Text file
        for i in range(len(datalist)):
            timestamp = str(datalist[i][0])
            distance = str(datalist[i][1])
            coordinatesList = datalist[i][2]

            kml = '<LineString><coordinates>'

            #latlonPoint = Point([LongitudeDegreesList,LatitudeDegreesList])
            for j in range(len(coordinatesList)):
                kml += str(coordinatesList[j][1])+","+str(coordinatesList[j][2])+","+str(coordinatesList[j][3])+" "

            kml += '</coordinates></LineString>'
      
            # Write to text file
            outputPointsTXT.write(str(RunID)+'\t'+str(timestamp)+'\t'+str(distance)+'\t'+str(kml)+'\n')

        #increment RunID
        RunID = RunID + 1

        outpath = ""


        print ("    Done!")
    except Exception as exception:
        print ("======== ERROR during extraction " + str(exception))
    
print('Script Complete')
outputPointsTXT.close()
