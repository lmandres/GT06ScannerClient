import GT06ScannerClient


if __name__ == "__main__":

    scanner = GT06ScannerClient.GT06ScannerClient()
    try:
        scanner.connectDevices()
        scanner.runScannerClient()
    except KeyboardInterrupt:
        pass
    finally:
        scanner.disconnectDevices()
