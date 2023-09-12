import copy
import io
import math
import threading

import pygame
import requests


class DisplayLocation():

    
    mapsURL = None
    mapZoom = None
    magnification = None
    currMaps = {}
    mapsCondition = threading.Condition()
    runMapThread = False
    mapThread = None
    fltxtile = None
    ftlytile = None

    screen = None
    font = None
    displayWidth = None
    displayHeight = None


    def __init__(self, mapsURLIn, mapsZoomIn=15, mapsMagnificationIn=1):

        if mapsURLIn:
            self.mapsURL = mapsURLIn

        pygame.init()
        pygame.display.init()

        self.screen = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN
        )
        self.font = pygame.font.Font(None, 36)

        self.displayWidth = self.screen.get_width()
        self.displayHeight = self.screen.get_height()

        self.mapZoom = mapsZoomIn
        self.magnification = mapsMagnificationIn

        self.runMapThread = True
        self.mapThread = threading.Thread(
            target=self.runLoadMapsThread
        )
        self.mapThread.start()

    def degToTileNumber(self, latitude, longitude, zoom):
        
        lat_rad = math.radians(latitude)
        n = 2.0 ** zoom
        xtile = (longitude + 180.0) / 360.0 * n
        ytile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n

        return (xtile, ytile)

    def getMapImg(self, xtile, ytile, zoom, magnification):

        magstr = ""
        if magnification > 1:
            magstr = "@{}x".format(magnification)

        url = self.mapsURL + "/{}/{}/{}{}.png".format(
            zoom,
            xtile,
            ytile,
            magstr
        )

        resp = requests.get(url)
        mapImg = pygame.image.load(
            io.BytesIO(resp.content)
        )

        return mapImg

    def getMapsCopy(self):

        self.mapsCondition.acquire()
        self.mapsCondition.wait()

        mapsCopy = self.currMaps.copy()
        for xkey in mapsCopy.keys():
            try:
                mapsCopy[xkey] = self.currMaps[xkey].copy()
            except:
                pass

        self.mapsCondition.release()

        return mapsCopy 

    def displayMapCoords(self, latitude, longitude):

        try:

            currMaps = {}
            if self.currMaps:
                currMaps = self.getMapsCopy()

            self.fltxtile, self.fltytile = self.degToTileNumber(latitude, longitude, self.mapZoom)
            offsetx = int(self.magnification*256.0*(self.fltxtile-math.floor(self.fltxtile)))
            offsety = int(self.magnification*256.0*(self.fltytile-math.floor(self.fltytile)))

            for x in range(
                -math.floor(self.displayWidth/(self.magnification*256)/2)-2,
                math.ceil(self.displayWidth/(self.magnification*256)/2)+3,
                1
            ):
                for y in range(
                    -math.floor(self.displayWidth/(self.magnification*256)/2)-2,
                    math.ceil(self.displayHeight/(self.magnification*256)/2)+3,
                    1
                ):

                    if (int(self.fltxtile)+x) not in currMaps.keys():
                        currMaps[int(self.fltxtile)+x] = {}
                    if (int(self.fltytile)+y) not in currMaps[int(self.fltxtile)+x].keys():
                        currMaps[int(self.fltxtile)+x][int(self.fltytile)+y] = None

                    try:
                        self.screen.blit(
                            currMaps[int(self.fltxtile)+x][int(self.fltytile)+y],
                            (
                                round(self.displayWidth/2) + self.magnification*x*256 - offsetx,
                                round(self.displayHeight/2) + self.magnification*y*256 - offsety
                            )
                        )
                    except:
                        pygame.draw.rect(
                            self.screen,
                            (0, 0, 0),
                            (
                                round(self.displayWidth/2) + self.magnification*x*256 - offsetx,
                                round(self.displayHeight/2) + self.magnification*y*256 - offsety,
                                self.magnification*256,
                                self.magnification*256
                            )
                        )
                    
            pygame.draw.circle(
                self.screen,
                (0, 0, 255),
                (
                    round(self.displayWidth/2),
                    round(self.displayHeight/2)
                ),
                10,
                2
            )
        except TypeError as te:
            self.screen.fill((0, 0, 0))
            text = self.font.render("Loading map . . .", False, (255, 255, 255))
            self.screen.blit(text, (0, 0))
        except Exception as ex:
            self.screen.fill((0, 0, 0))
            text = self.font.render(str(ex), False, (255, 0, 0))
            self.screen.blit(text, (0, 0))
        finally:
            pygame.display.flip()

            self.mapsCondition.acquire()
            self.currMaps.update(currMaps)
            self.mapsCondition.notify()
            self.mapsCondition.release()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                raise KeyboardInterrupt

    def runLoadMapsThread(self):

        def deleteMapKeys():

            delkeys = []

            for xkey in self.currMaps.keys():
                for ykey in self.currMaps[xkey].keys():
                    if (
                        ykey < math.floor(self.fltytile)-math.floor(self.displayHeight/(self.magnification*256)/2)-3 or
                        math.ceil(self.fltytile)+math.ceil(self.displayHeight/(self.magnification*256)/2)+4 < ykey
                    ):
                        delkeys.append((xkey, ykey,))
                    if (
                        xkey < math.floor(self.fltxtile)-math.floor(self.displayWidth/(self.magnification*256)/2)-3 or
                        math.ceil(self.fltxtile)+math.ceil(self.displayWidth/(self.magnification*256)/2)+4 < xkey
                    ):
                        delkeys.append((xkey, None,))

            for delkey in delkeys:
                if delkey[0] and delkey[1]:
                    try:
                        del self.currMaps[delkey[0]][delkey[1]]
                    except:
                        pass
                elif delkey[0] and not delkey[1]:
                    try:
                        del self.currMaps[delkey[0]]
                    except:
                        pass

        while self.runMapThread:

            self.mapsCondition.acquire()

            for xkey in self.currMaps.keys(): 
                for ykey in self.currMaps[xkey].keys():
                    if not self.currMaps[xkey][ykey]:
                        self.currMaps[xkey][ykey] = self.getMapImg(
                            xkey,
                            ykey,
                            self.mapZoom,
                            self.magnification
                        )

            deleteMapKeys()

            self.mapsCondition.notify()
            self.mapsCondition.release()


    def closeDisplay(self):
        self.runMapThread = False
        while self.mapThread.is_alive():
            pass
        pygame.quit()
