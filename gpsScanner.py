import _thread
import math
import re
import time

import serial


class GPSScanner():

    serialPort = None
    serialBaud = None
    gpsSerial = None

    locationHash = None
    runLocationThread = None

    def __init__(self, serialPortIn=None, serialBaudIn=None):
        if serialPortIn:
            self.serialPort = serialPortIn
        if serialBaudIn:
            self.serialBaud = serialBaudIn

    def resetConnection(self):
        try:
            self.gpsSerial.close()
            self.gpsSerial = serial.Serial(
                self.serialPort,
                self.serialBaud
            )
        except:
            pass

    def getSerialBaud(self):
        return self.serialBaud

    def setSerialBaud(self, serialBaudIn):
        self.serialBaud = serialBaudIn

    def getSerialPort(self):
        return self.serialPort

    def setSerialPort(self, serialPortIn):
        self.serialPort = serialPortIn

    def getLocationHash(self):
        return self.locationHash

    def runLocate(self):

        def doThreadLoop():
            self.locationHash = self.doDecodeGPS()
            while self.runLocationThread:
                self.locationHash.update(self.doDecodeGPS())

        self.locationHash = {}
        self.runLocationThread = True

        self.gpsSerial = serial.Serial(self.serialPort, self.serialBaud)
        _thread.start_new_thread(doThreadLoop, ())

    def stopLocate(self):
        self.runLocationThread = False
        if self.gpsSerial is not None:
            self.gpsSerial.close()

    def doDecodeGPS(self):

        def doGPSCheckSum(stringIn):
            checkSum = 0
            for charIndex in stringIn:
                checkSum ^= ord(charIndex)
            return str(hex(checkSum)).upper()[2:]

        returnHash = {}

        match = None
        while True:

            serialLine = b""
            try:
                serialLine = self.gpsSerial.readline()
            except:
                self.resetConnection()

            match = re.match(
                b'^\$(GPGGA|GPRMC|GPGLL|GPGSV),(.*)\*(.*)',
                serialLine
            )
            if match:
                 checkStr = "{},{}".format(
                     match.group(1).decode("utf-8"),
                     match.group(2).decode("utf-8")
                 )
                 funcSum = doGPSCheckSum(checkStr)
                 gpsSum = str(match.group(3).decode("utf-8"))[:2]
                 if funcSum == gpsSum:
                     break
        if match.group(1) == b'GPRMC':
            returnHash = self.decodeGPRMC(match.group(2).decode('utf-8'))
        elif match.group(1) == b'GPGGA':
            returnHash = self.decodeGPGGA(match.group(2).decode('utf-8'))
        elif match.group(1) == b'GPGLL':
            returnHash = self.decodeGPGLL(match.group(2).decode('utf-8'))
        elif match.group(1) == b'GPGSV':
            returnHash = self.decodeGPGSV(match.group(2).decode('utf-8'))

        return returnHash

    def decodeGPGLL(self, stringIn):

        returnHash = {}
        gpsArray = stringIn.split(',')

        try:

            returnHash['latitude'] = ((float(gpsArray[0]) - math.floor(float(gpsArray[0]) / 100) * 100) / 60) + math.floor(float(gpsArray[0]) / 100)
            returnHash['latitudeDir'] = gpsArray[1]

            returnHash['longitude'] = ((float(gpsArray[2]) - math.floor(float(gpsArray[2]) / 100) * 100) / 60) + math.floor(float(gpsArray[2]) / 100)
            returnHash['longitudeDir'] = gpsArray[3] 

            returnHash['time'] = str(gpsArray[4][0:2]) + ':' + str(gpsArray[4][2:4]) + ':' + str(gpsArray[4][4:6])
            returnHash['timestamp'] = gpsArray[4]

        except IndexError:
            pass
        except ValueError:
            pass

        return returnHash

    def decodeGPGGA(self, stringIn):

        returnHash = {}
        gpsArray = stringIn.split(',')

        try:

            returnHash['latitude'] = ((float(gpsArray[1]) - math.floor(float(gpsArray[1]) / 100) * 100) / 60) + math.floor(float(gpsArray[1]) / 100)
            returnHash['latitudeDir'] = gpsArray[2]

            returnHash['longitude'] = ((float(gpsArray[3]) - math.floor(float(gpsArray[3]) / 100) * 100) / 60) + math.floor(float(gpsArray[3]) / 100)
            returnHash['longitudeDir'] = gpsArray[4]

            returnHash['altitude'] = float(gpsArray[8])
            returnHash['altitudeUnits'] = gpsArray[9]

            returnHash['time'] = str(gpsArray[0][0:2]) + ':' + str(gpsArray[0][2:4]) + ':' + str(gpsArray[0][4:6])
            returnHash['timestamp'] = gpsArray[0]

        except IndexError:
            pass
        except ValueError:
            pass

        return returnHash

    def decodeGPRMC(self, stringIn):

        returnHash = {}
        gpsArray = stringIn.split(',')

        try:

            returnHash['latitude'] = ((float(gpsArray[2]) - math.floor(float(gpsArray[2]) / 100) * 100) / 60) + math.floor(float(gpsArray[2]) / 100)
            returnHash['latitudeDir'] = gpsArray[3]

            returnHash['longitude'] = ((float(gpsArray[4]) - math.floor(float(gpsArray[4]) / 100) * 100) / 60) + math.floor(float(gpsArray[4]) / 100)
            returnHash['longitudeDir'] = gpsArray[5]

            returnHash['groundSpeedKnots'] = float(gpsArray[6])
            returnHash['course'] = float(gpsArray[7])

            returnHash['date'] = str(int(gpsArray[8][4:6])) + '-' + str(gpsArray[8][2:4]) + '-' + str(gpsArray[8][0:2])
            returnHash['time'] = str(gpsArray[0][0:2]) + ':' + str(gpsArray[0][2:4]) + ':' + str(gpsArray[0][4:6])
            returnHash['timestamp'] = gpsArray[0]

        except IndexError:
            pass
        except ValueError:
            pass

        return returnHash

    def decodeGPGSV(self, stringIn):

        returnHash = {}
        gpsArray = stringIn.split(',')

        try:
            returnHash["satellitesInView"] = gpsArray[2]
        except IndexError:
            pass

        return returnHash
