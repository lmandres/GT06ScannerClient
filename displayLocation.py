from io import BytesIO

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
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.font = pygame.font.Font(None, 36)

        self.displayWidth = screen.get_width()
        self.displayHeight = screen.get_height()

    def getMapImg(self, latitude, longitude):

        url = (
            self.mapsURL +
            "/" +
            str(longitude) + "," + str(latitude) + ",15/" +
            str(self.displayWidth) + "x" + str(self.displayHeight) +
	    ".png"
        )
        resp = requests.get(url) 
        mapImg = pygame.image.load(BytesIO(resp.content))

        return mapImg	

    def displayMapsCoord(self, latitude, longitude):

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
            screen.blit(mapImg, (0, 0))
        except Exception as ex:
            screen.fill((0, 0, 0))
            text = font.render(str(ex), False, (255, 255, 255))
            screen.blit(text, [0, 0])

        doExit = False
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                doExit = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                doExit = True
        if doExit:
            pygame.quit()
            raise KeyboardInterrupt

    def closeDisplay(self):
        pygame.quit()
