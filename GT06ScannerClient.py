import datetime
import time

import crc_itu

import configReader
import displayLocation
import gpsScanner
import gt06Client


class GT06ScannerClient():


    configReader = None
    displayLocation = None
    gt06Client = None
    gpsScanner = None

    scannerID = None
    updateDelay = None

    def __init__(
        self,
        configFile="config.xml",
        scannerIDIn=None,
        serverAddressIn=None,
        serverPortIn=None,
        updateDelayIn=None,
        gpsPortIn=None,
        gpsBaudIn=None,
        mapsURLIn=None,
        mapsZoomIn=None,
        mapsMagnificationIn=None
    ):
        self.configReader = configReader.ConfigReader(configFile)
        serverAddress = self.configReader.getGT06ServerHostname()
        gpsPort = self.configReader.getGPSDevicePort()
        gpsBaud = int(self.configReader.getGPSDeviceBaud())
        mapsURL = self.configReader.getMapsURL()
        self.scannerID = self.configReader.getScannerID()

        try:
            serverPort = int(self.configReader.getGT06ServerPort())
        except TypeError:
            pass

        try:
            mapsZoom = int(self.configReader.getMapsZoom())
        except TypeError:
            mapsZoom = 16

        try:
            mapsMagnification = int(self.configReader.getMapsMagnification())
        except TypeError:
            mapsMagnification = 1

        try:
            self.updateDelay = int(self.configReader.getGT06ServerUpdateDelay())
        except TypeError:
            self.updateDelay = 1

        if serverAddressIn:
            serverAddress = serverAddressIn
        if serverPortIn:
            serverPort = int(serverPortIn)

        if gpsPortIn:
            gpsPort = gpsPortIn
        if gpsBaudIn:
            gpsBaud = int(gpsBaudIn)

        if scannerIDIn:
            self.scannerID = scannerIDIn

        if updateDelayIn:
            self.updateDelay = int(updateDelayIn)

        if mapsURL and mapsZoom != None and mapsMagnification != None:
            self.displayLocation = displayLocation.DisplayLocation(
                mapsURL,
                mapsZoom,
                mapsMagnification
            )
        elif mapsURL and mapsZoom != None:
            self.displayLocation = displayLocation.DisplayLocation(
                mapsURL,
                mapsZoom
            )
        elif mapsURL:
            self.displayLocation = displayLocation.DisplayLocation(
                mapsURL
            )

        if serverAddress and serverPort:
            self.gt06Client = gt06Client.GT06Client(
                serverAddress,
                serverPort
            )

        self.gpsScanner = gpsScanner.GPSScanner(
            gpsPort,
            gpsBaud
        )

    def connectDevices(self):
        self.gpsScanner.runLocate()
        if self.gt06Client:
            self.gt06Client.connect()
            self.gt06Client.sendLoginMessage(
                self.scannerID
            )

    def runScannerClient(self):

        def makeGPSMessageFromHash(hashIn):

            returnMessage = None

            try:

                messageOut = ""

                courseString = ""
                courseOut = 0
                courseOut1 = 0
                courseOut2 = 0

                dateList = hashIn["date"].split("-")
                timeList = hashIn["time"].split(":")
                numSats = hashIn["satellitesInView"]
                latitude = hashIn["latitude"]
                latitudeDir = hashIn["latitudeDir"]
                longitude = hashIn["longitude"]
                longitudeDir = hashIn["longitudeDir"]
                speed = hashIn["groundSpeedKnots"]
                course = hashIn["course"]

                messageOut += "{:02x}{:02x}{:02x}".format(
                    int(dateList[0]),
                    int(dateList[1]),
                    int(dateList[2])
                )

                messageOut += "{:02x}{:02x}{:02x}".format(
                    int(timeList[0]),
                    int(timeList[1]),
                    int(timeList[2])
                )


                messageOut += "{:01x}{:01x}".format(
                    12,
                    int(numSats)
                )

                latInHex = round(latitude*60.0*30000.0)
                longInHex = round(longitude*60.0*30000.0)
                messageOut += "{:08x}{:08x}".format(
                    latInHex,
                    longInHex
                )

                speed *= 1.852
                if speed > 255:
                    speed = 255
                messageOut += "{:02x}".format(
                    round(speed)
                )

                courseString += "11"
                courseString += "11"

                if longitudeDir == "E":
                    courseString += "0"
                elif longitudeDir == "W":
                    courseString += "1"
                else:
                    raise ValueError("Longitude direction is invalid.")

                if latitudeDir == "S":
                    courseString += "0"
                elif latitudeDir == "N":
                    courseString += "1"
                else:
                    raise ValueError("Latitude direction is invalid.")

                courseOut1 = int(courseString, 2)
                courseOut1 = courseOut1 << 10
                courseOut2 = int(course) % 360
                courseOut = courseOut1 | courseOut2

                messageOut += "{:04x}".format(courseOut)

                returnMessage = messageOut

            except:
                pass

            return returnMessage

        def makeLatLongFromHash(hashIn):

            latitude = None
            longitude = None

            try:

                latitude = hashIn["latitude"]
                latitudeDir = hashIn["latitudeDir"]
                longitude = hashIn["longitude"]
                longitudeDir = hashIn["longitudeDir"]

                if longitudeDir == "E":
                    longitude *= 1
                elif longitudeDir == "W":
                    longitude *= -1
                else:
                    raise ValueError("Longitude direction is invalid.")

                if latitudeDir == "S":
                    latitude *= -1
                elif latitudeDir == "N":
                    latitude *= 1
                else:
                    raise ValueError("Latitude direction is invalid.")

            except:
                pass

            return (latitude, longitude)

        prevTime = None
        while True:

            currTime = datetime.datetime.now()
            locationHash = self.gpsScanner.getLocationHash()

            gpsMessage = makeGPSMessageFromHash(
                locationHash
            )
            latitude, longitude = makeLatLongFromHash(
                locationHash
            )

            if self.displayLocation:
                self.displayLocation.displayMapCoords(latitude, longitude)
            else:
                print(locationHash)

            if not prevTime or (currTime - prevTime).seconds >= self.updateDelay:

                if self.gt06Client and gpsMessage:
                    self.gt06Client.sendGPSMessage(gpsMessage)

                prevTime = currTime

    def disconnectDevices(self):
        if self.displayLocation:
            self.displayLocation.closeDisplay()
        if self.gt06Client:
            self.gt06Client.disconnect()
        self.gpsScanner.stopLocate()
