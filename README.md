# GT06ScannerClient

The GT06ScannerClient was written to be run on a mobile computer to update a system compatible with the GT06 protocol.  Specifically, this client targets the open source Traccar platform and was developed based on this codebase.

## Prerequisites

The GT06ScannerClient relies on the following prerequisites:

* Python version 3.4 or greater
* Git
* pip for installation of Python modules
* A mobile internet connection for communication with the server
* for the server, you will need to know the
  * hostname/ip address of the host server
  * port for GT06 communication
* A GPS receiver attached to the computer running the script
* for the GPS receiver, you will need to know the
  * port running the GPS receiver, this will differ between Windows and *NIX machines
  * baud speed that the GPS receiver is running

## Installation

* In the installation directory run

```bash
git clone https://github.com/lmandres/GT06ScannerClient.git
cd GT06ScannerClient
git pull
```

* You can create a virtual environment to run the application (This step is optional).

```bash
python3 -m venv venv
source venv/bin/activate
```

* Install the prerequisite Python modules

```bash
pip install -r requirements.txt
```

## Configuration

* Edit the config.xml file to point to the correct server and device information.
* In this installation, you can use your favorite editor.  However, for this example we will be using Windows Notepad.
* Open the file for editing.

```bash
notepad config.xml
```

* The following settings should be as follows:
  * /ScannerSettings/ScannerIDNumber - Scanner identifier number (This is usually the IMEI)
  * /ScannerSettings/GT06ClientSettings/Hostname - Hostname or IP address of the GPS tracking server
  * /ScannerSettings/GT06ClientSettings/Port - The port number for the service running the GT06 protocol on the host server
  * /ScannerSettings/GT06ClientSettings/UpdateDelay - The delay (in seconds) to wait between GPS scanner updates to the server
  * /ScannerSettings/GPSSettings/Port - The port to the device on the machine.  This will differ between *NIX and Windows computers.
    * On *NIX, this will usually be a path to the port in the /dev directory
    * On Windows, this will probably be a COM port
  * /ScannerSettings/GPSSettings/Baud - The port speed of the GPS device

## Running the application

* To run the application, you will have to do the following steps, based on your installation.
* Change into the directory containing the GT06ScannerClient script:

```bash
cd GT06ScannerClient
```

* If you installed the Python module dependencies in a virtual environment (after following the optional venv step), you will need to ensure that you source the virtual environment.

```bash
source venv/bin/activate
```

* Run the client application

```bash
python runClient.py
```
