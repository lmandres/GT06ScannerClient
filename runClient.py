import argparse

import GT06ScannerClient


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="CLI command to run GT06ScannerClient."
    )
    parser.add_argument(
        "-c",
        "--config",
        help="Specify alternate configuration file.",
        default="config.xml"
    )
    parser.add_argument(
        "-i",
        "--id",
        help="Scanner ID number for GPS tracker (Usually IMEI number)."
    )
    parser.add_argument(
        "-s",
        "--server_address",
        help="Hostname or IP address of GPS tracker server."
    )
    parser.add_argument(
        "-p",
        "--server_port",
        type=int,
        help="Port number for GT06 protocol of GPS tracker server."
    )
    parser.add_argument(
        "-d",
        "--update_delay",
        type=int,
        help="Delay (in seconds) between GPS tracker server updates."
    )
    parser.add_argument(
        "-g",
        "--gps_port",
        help="Communication port or path for GPS tracker module."
    )
    parser.add_argument(
        "-b",
        "--gps_baud",
        type=int,
        help="Baud speed for communication with GPS tracker module."
    )
    parser.add_argument(
        "-m",
        "--maps_url",
        help="URL for map tile server images."
    )
    parser.add_argument(
        "-x",
        "--magnification",
        help="Magnification for tile server images."
    )
    parser.add_argument(
        "-z",
        "--zoom",
        help="Zoom for tile server images."
    )
    args = parser.parse_args()
    print(args)
    
    scanner = GT06ScannerClient.GT06ScannerClient(
        configFile=args.config,
        scannerIDIn=args.id,
        serverAddressIn=args.server_address,
        serverPortIn=args.server_port,
        updateDelayIn=args.update_delay,
        gpsPortIn=args.gps_port,
        gpsBaudIn=args.gps_baud,
        mapsURLIn=args.maps_url,
        mapsZoomIn=args.zoom,
        mapsMagnificationIn=args.magnification
    )
    try:
        scanner.connectDevices()
        scanner.runScannerClient()
    except KeyboardInterrupt:
        pass
    finally:
        scanner.disconnectDevices()
