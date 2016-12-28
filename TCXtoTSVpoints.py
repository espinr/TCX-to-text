#-------------------------------------------------------------------------------
# Name:        TCXtoTSVpoints.py
# Purpose:     Simple script to convert TCX files into a Tab Separated Values 
#              text file with two rows for coordinates (lat-long points).
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
outputFilePath =  './output/runningPoints.txt'

outputPointsTXT = open(outputFilePath, 'a' )
outputPointsTXT.write('RunID,DateVal,Lat,Lon\n')


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

        #output crs
        crs = fiona.crs.from_epsg(4326)

        print ("    Start TCX Extraction Run ID: " + str(RunID) + "...")

        #build a list for all the points from the TCX file
        for lap in tcx.findall('.//Lap/'):

            for point in lap.findall('.//Trackpoint'):

                idval = idval + 1
                timestamp = findtext(point, 'Time')
                AltitudeMeters = float(findtext(point, 'AltitudeMeters'))
                DistanceMeters = float(findtext(point, 'DistanceMeters'))

                LatitudeDegrees = float(findtext(point, 'Position/LatitudeDegrees'))
                LongitudeDegrees = float(findtext(point, 'Position/LongitudeDegrees'))

                datalist.append((idval,timestamp,AltitudeMeters,DistanceMeters,LatitudeDegrees,LongitudeDegrees))

        #move through the TCX file to calculate run values and append a Text file
        for i in range(len(datalist)):
                if i < (len(datalist))-1:
                    idvalList = datalist[i][0]
                    timestampList = datalist[i][1]
                    #not needed for output
                    #AltitudeMetersList = datalist[i][2]
                    #DistanceMetersList  = datalist[i][3]

                    #set coordinates for first point
                    LatitudeDegreesList = datalist[i][4]
                    LongitudeDegreesList = datalist[i][5]

                    dateHolder = (timestampList.split("T")[0]).replace("T","")

                    # Write to text file
                    outputPointsTXT.write(str(RunID)+','+str(dateHolder)+','+str(LatitudeDegreesList)+','+str(LongitudeDegreesList)+'\n')

        #increment RunID
        RunID = RunID + 1

        outpath = ""


        print ("    Extraction Complete")
        print()
    except Exception as exception:
        print ("======== ERROR during extraction ")
    
print('Script Complete')
outputPointsTXT.close()
