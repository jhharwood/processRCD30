# ****************************************************************************
#
# NAME: J. Heath Harwood
# DATE: 24  March 2017
#
#
# DESCRIPTION:  This script modifys the FlightData.xml file, and create the batch scripts
#               to download and develop the RCD30 imagery
#
#
# DEPENDENCIES: Python Standard Library, lxml
#
# SOURCE(S):
#   
##############################################################################

###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.IMPORT STATEMENTs.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>###

import os, glob, sys, re
from lxml import etree
from xml.parsers.expat import ExpatError
import argparse
import easygui
import fnmatch

###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.CONSTANTS.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>###

framePro = r'C:\Program Files\Leica Geosystems\FramePro\FramePro.exe'

###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.CLASSES.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>###

class ImageSession(object):
    """This class defines a image collection session. Sessions have the following properties:

    Attributes:
        Session ID: Flight date/timestamped for the corresponding session; sessions id's are unique.
        Flight Database File: This file is the *.fpd2 file SQL database file; all valid sessions have this file.  No
                            was collected if this file does not exist.
        FlightData Project: This file is the FlightData.pro.  All sessions have this regardless if data was collected
                            or not.
        Flight Data XML: This file (FlightData.xml) contains all the event markers in xml format.
        Longitude: This information is in the FlightData.xml; Only valid collection sessions have a longitude.
        Latitude: This information is in the FlightData.xml; Only valid collection sessions have a latitude.
        Mission: Mission plan folder; The name of these folder/directories change with every project.
    """


    def __init__(self, sessionID, rawDir, dwnDir, devDir, mission):
        self.sessionID = sessionID
        self.rawDir = rawDir
        self.dwnDir = dwnDir
        self.devDir = devDir
        self.mission = mission

    def runDownload(framePro, inDir, outDir):

        """
        Creates a download command for downloading image with FramePro on a Session
        :param framePro: Location of FramePro exe
        :param inDir: Raw Session location
        :param outDir: Download Location
        :return: cmd

        """
        cmd = ('"' + framePro + '"' + ' ' + inDir + ' ' + outDir)
        print cmd
        return os.system(cmd)

    def runDevelop(framePro, inDir, outDir, fplan):

        """

        Creates a develop command for developing images with FramePro on a Session
        :param framePro: Location of FramePro exe
        :param inDir: Download Session location
        :param outDir: Developed image dataset Location
        :param ortho: Processing workflow desired; can either be ortho or atmospheric
        :param fplan: Flight plan for the desired session
        :return: cmd

        """

        cmd = ('"' + framePro + '"' + ' ' + inDir + ' ' + outDir + ' "Ortho" ' + fplan)
        print cmd
        return os.system(cmd)

###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.FUNCTIONS.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>###
def editFlightXML(xml):

    """

    :param xml:
    :return:
    """

    #-------- Parse the XML file: --------#
    try:
        #Parse the given XML file:
        doc = etree.parse(xml)                                                      # use etree from lxml package
    except ExpatError as e:                                                         # use this to proof read xml
        print "[XML] Error (line %d): %d" % (e.lineno, e.code)
        print "[XML] Offset: %d" % (e.offset)
        raise e
    except IOError as e:                                                            # prints the associate error
        print "[XML] I/O Error %d: %s" % (e.errno, e.strerror)
        raise e
    else:
        # Change the GpsToUtcOffset tag value from -15 to 0
        find_gps_ts = doc.find('GpsToUtcOffset')                                    # this ask to find the element tag
        find_gps_ts.set('offsetSec','-17')                                            # once found we set the new value

        # now go find the longitutde value using xpath; ahh so nice!!!
        find_long = doc.xpath('//sessions//session//project//flight_plan//line//frame//longitude')
        i = 0;                                                                      # set up an iterator to use a
                                                                                    # loop variable to move down the xml
        for node1 in find_long:
            print "This is the original Longitude: " + find_long[i].text
            reLong = float(find_long[i].text)                                       # changing value from string to float
            #print format(reLong,'.12f')

            # the longitude is from 0 up to 279; we need a neg value ie. from 180 to -180 or Easting/Westing number
            newLong = reLong - 360
            print "This is the calculated new longitude: " + format(newLong, '.12f')
            addNewLong = format(newLong, '.12f')
            find_long[i].text = addNewLong
            print "This is the updated new longitude in the xml: " + find_long[i].text
            find_long[i].set('updated', 'yes')                                      # sets the new value in the xml
            i += 1
            print "Longitude Iteration number: " + str(i)

        print "Wrote new longitude positions to file " + xml + "\n"
        doc.write(xml)

def getMPNames(xml):

    """

    :param xml:
    :return:
    """

    #-------- Parse the XML file: --------#
    try:
        #Parse the given XML file:
        doc = etree.parse(xml)                                                      # use etree from lxml package
    except ExpatError as e:                                                         # use this to proof read xml
        print "[XML] Error (line %d): %d" % (e.lineno, e.code)
        print "[XML] Offset: %d" % (e.offset)
        raise e
    except IOError as e:                                                            # prints the associate error
        print "[XML] I/O Error %d: %s" % (e.errno, e.strerror)
        raise e
    else:
        # Get list of Flight Plans
        fpList = []
        i = 0;
        findFPName = doc.xpath('//sessions//session//project//flight_plan')
        for node in findFPName:
            if findFPName[i].get('id') is "":
                #print 'This is not a valid flight plan'
                pass
            else:
                print "This is the Flight Plan Name " + findFPName[i].get('id')
                fpList.append(findFPName[i].get('id'))
                #print fpList
            i += 1
        return fpList

def checkFlightXML(xml):

    """

    :param xml:
    :return: True = 1; False = 0; Will return true if the FlightData.xml has a longitude to indicate that it's a valid flight file
            otherwise it's false as it only has Dark Frames
    """
    # -------- Parse the XML file: --------#
    try:
        # Parse the given XML file:
        doc = etree.parse(xml)  # use etree from lxml package
    except ExpatError as e:  # use this to proof read xml
        print "[XML] Error (line %d): %d" % (e.lineno, e.code)
        print "[XML] Offset: %d" % (e.offset)
        raise e
    except IOError as e:  # prints the associate error
        print "[XML] I/O Error %d: %s" % (e.errno, e.strerror)
        raise e

    else:
        # Check if there is a longitutde value using xpath; ahh so nice!!!
        find_lat = doc.xpath('//sessions//session//project//flight_plan//line//frame//latitude')
        find_long = doc.xpath('//sessions//session//project//flight_plan//line//frame//longitude')
        if find_long and find_lat is True:
            print "The FlightData.xml has valid positional information; Will continue to process the imagery"
            return True
        else:
            print "The FlightData.xml does not have valid positional information; Will move to another dataset"
            return False

def openSession(fdDir,sessID):
    """

    :param session id: Uses the session id to open the right folder and begin processing the project
    :return: changes dir for processing
    """
    for dirName, subdirList, fileList in os.walk(fdDir, topdown=True):
        for dirName in fnmatch.filter(subdirList, sessID):
            print dirName

def valid_file(filepathname):

    """

    :param path/to/file:
    :return:

    """
    if not os.path.exists(filepathname):
        raise argparse.ArgumentTypeError\
            ("Cannot find directory {}".format(filepathname))

    return filepathname

def valid_fileDir(filepathname):

    """

    :param path/to/dir:
    :return:

    """
    dirname = os.path.dirname(filepathname)
    print dirname
    if not os.path.exists(dirname):
        raise argparse.ArgumentTypeError\
            ("Cannot find directory {}".format(dirname))

    return dirname

def getFields():
    # Get input and output folders for sessions
    msg = "Enter the FramePro Exe, Session Name, Download Location, Dataset Folder, Flight Plan"
    title = "Modify Field Names"
    fieldNames = ["FramePro","Session Name","Download Location", "Dataset", "Flight Plan"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = easygui.multenterbox(msg,title, fieldNames)

    # make sure that none of the fields was left blank
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        if errmsg == "": break # no problems found
        fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
    #print "Reply was:", fieldValues
    return fieldValues

def defineLocs():
    # Get input and output folders for sessions
    msg = "Enter the Download Location"
    title = "Modify Field Names"
    fieldNames = ["Download Location"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = easygui.multenterbox(msg,title, fieldNames)

    # make sure that none of the fields was left blank
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        if errmsg == "": break # no problems found
        fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
    #print "Reply was:", fieldValues
    return fieldValues

def getFlightDateDir():
    msg = "Choose the Flight Data Directory (i.e., YYYYMMDD_#"
    title = "Flight Data Directory"
    default = None
    dir = easygui.diropenbox(msg, title, default)
    print dir
    return dir

def getFpd2List(fdDir):
    fpd2List = []
    filePaths = []
    for dirName, subdirList, fileList in os.walk(fdDir, topdown=True):
        for fname in fileList:
            if fname.endswith('.fpd2'):
                filePath = os.path.join(dirName, fname)
                filePaths.append(filePath)
                fpd2 = fname
                fpd2List.append(fpd2)

    return filePaths, fpd2List

def getSessionIDs(fdDir):
    sessIDs = []
    for dirName, subdirList, fileList in os.walk(fdDir, topdown=True):
        for fname in fileList:
            if fname.endswith('.fpd2'):
                fpd2 = fname
                # get session id form fpd2 file name
                sessID = fpd2.split('_')[0]
                sessIDs.append(sessID)
                #print sessIDs

    return sessIDs

def displaySessionCount(self):
    print "The total number of Image Sessions is: " % ImageSession.numSessions

def displayMissionCount(self):
    numMissions = len(self.missions)
    print "The total number of Missions in this Session are: " % numMissions

def displayImageSessions(self):
    args = {self.sessionID, self.fpd2, self.proFD, self.xmlFD, self.longFD, self.latFD, self.missions}
    """
    The Session ID is: {0}
    The Flight Database file is: {1}
    The Mission names are: {2}
    """.format(**args)

# create windose sessions bat file function
def session_bat_writer(fdDir, sessionBat, rawFLDate):
    with open(fdDir + '\\%s.bat', 'a')%(rawFLDate) as sess_bat_file:
        sess_bat_file.write(sessionBat + '\n')

def readSess(rawDir):

        # Open raw data directory
        flightDateDir = rawDir
        #print flightDateDir
        # Get the paths to the fpd2 Files
        fpd2Paths = getFpd2List(flightDateDir)[0]
        # Get list of fpd2 files
        fpd2List = getFpd2List(flightDateDir)[1]

        sessionList = []
        # Loop through all the fpd2 files and sessions to run sessions
        for paths in fpd2Paths:
            sessPath = os.path.dirname(paths)
            print sessPath
            session = sessPath.split('\\')[-1]
            print session
            return session
            # Change directory to current session directory
            os.chdir(sessPath)
            # Get FlightData.xml file
            flDataXML = os.path.join(sessPath, "FlightData.xml")
            mpList = rcd30.getMPNames(flDataXML)
            for mission in mpList:
                print 'The current processing is ' + mission
                #rcd30.ImageSession.runDownload(framePro,sessPath,)


    

