from xml.etree import ElementTree
import logging, codecs, sys


class ConfigReader():


    configXML = None


    def __init__(self, fileName="config.xml"):
        self.configXML = ElementTree.parse(fileName)

    def getTextByXPath(self, xpath):
        returnValue = None
        try:
            returnValue = self.configXML.find(xpath).text
        except:
            pass
        return returnValue

    def getScannerID(self):
        scannerID = self.getTextByXPath(".//ScannerIDNumber")
        try:
            bytes.fromhex(scannerID)
        except ValueError:
           logging.exception("ScannerID is expected to be HEX value")
           sys.exit(255)
        return scannerID

    def getGT06ServerHostname(self):
        return self.getTextByXPath(".//GT06ClientSettings/Hostname")

    def getGT06ServerPort(self):
        returnValue = None
        try:
            returnValue = int(
                self.getTextByXPath(".//GT06ClientSettings/Port")
            )
        except:
            pass
        return returnValue

    def getGT06ServerUpdateDelay(self):
        returnValue = None
        try:
            returnValue = int(
                self.getTextByXPath(".//GT06ClientSettings/UpdateDelay")
            )
        except:
            pass
        return returnValue

    def getGPSDevicePort(self):
        return self.getTextByXPath(".//GPSSettings/Port")

    def getGPSDeviceBaud(self):
        returnValue = None
        try:
            returnValue = int(
                self.getTextByXPath(".//GPSSettings/Baud")
            )
        except:
            pass
        return returnValue

    def getMapsURL(self):
        return self.getTextByXPath(".//DisplaySettings/MapsURL")

    def getMapsZoom(self):
        returnValue = None
        try:
            returnValue = int(
                self.getTextByXPath(".//DisplaySettings/Zoom")
            )
        except:
            pass
        return returnValue

    def getMapsMagnification(self):
        returnValue = 1
        try:
            returnValue = int(
                self.getTextByXPath(".//DisplaySettings/Magnification")
            )
        except:
            pass
        return returnValue
