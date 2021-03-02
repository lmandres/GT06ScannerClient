import io
import math

import pygame
import requests


class DisplayLocation():

    
    mapsURL = None
    mapZoom = None
    magnification = None
    currMaps = {}

    screen = None
    font = None
    displayWidth = None
    displayHeight = None


    def __init__(self, mapsURLIn, mapsZoomIn=15, mapsMagnificationIn=1):

        if mapsURLIn:
            self.mapsURL = mapsURLIn

        pygame.init()
        self.screen = pygame.display.set_mode(
            (0,0),
            pygame.FULLSCREEN
        )
        self.font = pygame.font.Font(None, 36)

        self.displayWidth = self.screen.get_width()
        self.displayHeight = self.screen.get_height()

        self.mapZoom = mapsZoomIn
        self.magnification = mapsMagnificationIn

    def degToTileNumber(self, latitude, longitude, zoom):
        
        lat_rad = math.radians(latitude)
        n = 2.0 ** zoom
        xtile = (longitude + 180.0) / 360.0 * n
        ytile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n

        return (xtile, ytile)

    def getMapImg(self, xtile, ytile, zoom):

        magstr = ""
        if self.magnification > 1:
            magstr = "@{}".format(self.magnification)

        url = self.mapsURL + "/{}/{}/{}{}.png".format(
            zoom,
            xtile,
            ytile,
            magstr
        )
        print(url)
        resp = requests.get(url)
        mapImg = pygame.image.load(
            io.BytesIO(resp.content)
        )

        return mapImg	

    def displayMapCoords(self, latitude, longitude):

        try:

            fltxtile, fltytile = self.degToTileNumber(latitude, longitude, self.mapZoom)
            offsetx = self.magnification*256*(fltxtile-int(fltxtile))
            offsety = self.magnification*256*(fltytile-int(fltytile))

            prevMaps = self.currMaps
            self.currMaps = {}

            for x in range(
                -round(self.displayWidth*self.magnification/256/2)-2,
                round(self.displayWidth*self.magnification/256/2)+2,
                1
            ):
                for y in range(
                    -round(self.displayWidth*self.magnification/256/2)-2,
                    round(self.displayHeight*self.magnification/256/2)+2,
                    1
                ):
                    if (int(fltxtile)+x) not in self.currMaps.keys():
                        self.currMaps[int(fltxtile)+x] = {}
                        if (int(fltytile)+y) not in self.currMaps[int(fltxtile)+x].keys():
                            self.currMaps[int(fltxtile)+x][int(fltytile)+y] = None
                    if (
                        (int(fltxtile)+x) in prevMaps.keys() and
                        (int(fltytile)+y) in prevMaps[int(fltxtile)+x].keys()
                    ):
                        self.currMaps[int(fltxtile)+x][int(fltytile)+y] = prevMaps[int(fltxtile)+x][int(fltytile)+y]
                    else:
                        self.currMaps[int(fltxtile)+x][int(fltytile)+y] = self.getMapImg(
                            int(fltxtile) + x,
                            int(fltytile) + y,
                            self.mapZoom
                        )
                    
                    self.screen.blit(
                        self.currMaps[int(fltxtile)+x][int(fltytile)+y],
                        (
                            round(self.displayWidth/2) + self.magnification*x*256 - offsetx,
                            round(self.displayHeight/2) + self.magnification*y*256 - offsety
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                raise KeyboardInterrupt

    def closeDisplay(self):
        pygame.quit()
