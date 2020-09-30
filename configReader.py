from xml.etree import ElementTree


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
        return self.getTextByXPath(".//ScannerIDNumber")

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
