import codecs
import socket
import logging, sys

import crc_itu


class GT06Client():

    serverAddress = None
    serverPort = None
    timeOut = None

    infoSerial = 0
    socket = None

    def __init__(self, serverAddress=None, serverPort=None, timeOut=60):
        if serverAddress:
            self.serverAddress = serverAddress
        if serverPort:
            self.serverPort = serverPort
        self.timeOut = timeOut

    def getServerPort(self):
        return self.serverPort

    def setServerPort(self, serverPort):
        self.serverPort = serverPort

    def getServerAddress(self):
        return self.serverAddress

    def setServerAddress(self, serverAddress):
        self.serverAddress = serverAddress

    def getTimeOut(self):
        return self.timeOut

    def setTimeOut(self, timeOut):
        self.timeOut = timeOut

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.serverAddress, self.serverPort))
        except OSError as e:
            logging.exception(f"Cannot connect to {self.serverAddress}:{self.serverPort}")
            sys.exit(255)
        self.socket.settimeout(self.timeOut)

    def disconnect(self):
        self.socket.close()

    def makeBasicMessage(self, protocolIn, messageIn): 

        self.infoSerial += 1
        self.infoSerial %= 0x10000

        returnBytes = None

        packetLen = 0
        try:
            packetLen = int(len(bytes.fromhex(messageIn))+5)
        except ValueError:
            pass

        crcCheckFormat = "{:02x}{:02x}{}{:04x}"
        crcCheckString = crcCheckFormat.format(
            packetLen,
            int(protocolIn),
            messageIn,
            int(self.infoSerial)
        )

        messageFormat = "7878{}{:04x}0d0a"

        errorCheck = 0
        try:
            errorCheck = crc_itu.crc16(bytes.fromhex(crcCheckString))
        except ValueError:
            pass

        messageOut = messageFormat.format(
            crcCheckString,
            errorCheck
        )

        returnBytes = bytes.fromhex(messageOut)

        return returnBytes

    def makeBasicMessageResponse(self, protocolIn):

        returnBytes = None

        crcCheckFormat = "{:02x}{:02x}{:04x}"
        crcCheckString = crcCheckFormat.format(
            5,
            int(protocolIn),
            int(self.infoSerial)
        )
            
        messageFormat = "7878{}{:04x}0d0a"

        errorCheck = 0
        try:
            errorCheck = crc_itu.crc16(bytes.fromhex(crcCheckString))
        except ValueError:
            pass

        messageOut = messageFormat.format(
            crcCheckString,
            errorCheck
        )

        returnBytes = bytes.fromhex(messageOut)

        return returnBytes

    def sendLoginMessage(self, imeiIn):

        serverResp = None

        try:
            int(imeiIn)
        except ValueError:
            raise ValueError("IMEI string contains non-numeric digits.")

        self.socket.sendall(self.makeBasicMessage(1, imeiIn))
        try:
            serverResp = self.socket.recv(1024)
        except socket.timeout:
            pass

        if self.makeBasicMessageResponse(1) != serverResp:
            return False
        else:
            return True

    def sendGPSMessage(self, gpsHash):

        serverResp = None

        try:
            bytes.fromhex(gpsHash)
        except ValueError:
            raise ValueError("GPS hash string contains non-hexadecimal digits.")

        self.socket.sendall(self.makeBasicMessage(16, gpsHash))
        try:
            serverResp = self.socket.recv(1024)
        except socket.timeout:
            pass

        if self.makeBasicMessageResponse(16) != serverResp:
            return False
        else:
            return True
