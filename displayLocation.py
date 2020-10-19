import io

import pygame
import requests


class DisplayLocation():

    
    mapsURL = None

    screen = None
    font = None
    displayWidth = None
    displayHeight = None


    def __init__(self, mapsURLIn):

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

    def getMapImg(self, latitude, longitude):

        url = self.mapsURL + "/{:f},{:f},{}/{}x{}.png".format(
            longitude,
            latitude,
            15,
            self.displayWidth,
            self.displayHeight
        )
        print(url)
        resp = requests.get(url)
        mapImg = pygame.image.load(
            io.BytesIO(resp.content)
        )

        return mapImg	

    def displayMapCoords(self, latitude, longitude):

        try:
            mapImg = self.getMapImg(
                latitude,
                longitude
            )
            pygame.draw.circle(
                mapImg,
                (0, 0, 255),
                (
                    round(self.displayWidth/2),
                    round(self.displayHeight/2)
                ),
                10,
                2
            ) 
            self.screen.blit(mapImg, (0, 0))
        except Exception as ex:
            self.screen.fill((0, 0, 0))
            text = self.font.render(str(ex), False, (255, 255, 255))
            self.screen.blit(text, [0, 0])
        finally:
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                raise KeyboardInterrupt

    def closeDisplay(self):
        pygame.quit()
