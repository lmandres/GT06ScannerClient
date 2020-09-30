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
