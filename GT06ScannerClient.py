import time

import crc_itu

import gpsScanner
import gt06Client
import configReader


class GT06ScannerClient():


    gt06Client = None
    gpsScanner = None
    configReader = None


    imei = None

    def __init__(self):
        self.configReader = configReader.ConfigReader("config.xml")
        self.gt06Client = gt06Client.GT06Client(
            self.configReader.getGT06ServerHostname(),
            self.configReader.getGT06ServerPort()
        )
        self.gpsScanner = gpsScanner.GPSScanner(
            self.configReader.getGPSDevicePort(),
            self.configReader.getGPSDeviceBaud()
        )

    def connectDevices(self):
        self.gt06Client.connect()
        self.gpsScanner.runLocate()
        self.gt06Client.sendLoginMessage(
            self.configReader.getScannerID()
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
            
        while True:
            locationHash = self.gpsScanner.getLocationHash()
            gpsMessage = makeGPSMessageFromHash(
                locationHash
            )
            print("Scanning . . .")
            if gpsMessage:
                self.gt06Client.sendGPSMessage(gpsMessage)
                print(locationHash)
            time.sleep(
                self.configReader.getGT06ServerUpdateDelay()
            )

    def disconnectDevices(self):
        self.gpsScanner.stopLocate()
        self.gt06Client.disconnect()
