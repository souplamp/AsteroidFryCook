import pygame as p
from timer import Timer

class patty(p.sprite.Sprite):

    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.state = 0  # state of the patty, like not-yet-placed, cooking, cooked, burned
        
        # drawn images
        self.imgSet = []
        self.imgSet.append(p.image.load("./sprites/grill/pattiesempty.png").convert_alpha())
        self.imgSet.append(p.image.load("./sprites/grill/patties.png").convert_alpha())
        self.imgSet.append(p.image.load("./sprites/grill/pattiesflip.png").convert_alpha())

    def drawMe(self, screen):
        if self.state == 0:
            img = self.imgSet[0]
        elif self.state == 1:
            img = self.imgSet[1]
        else:
            img = self.imgSet[2]

        screen.blit(img, (self.rect.x, self.rect.y))
    
    def checkClick(self, mX, mY):

        if self.rect.collidepoint(mX, mY):
            print("click on patty! state = ", self.state)
            if self.state < 4:
                self.state += 1
            else:
                self.state = 0

            print("updated state to: ", self.state)


class grill():

    def __init__(self, width, height, screenWidth, screenHeight):
        self.width = width
        self.height = height
        self.gameWidth = screenWidth
        self.gameHeight = screenHeight
        self.x = screenWidth - width
        self.y = screenHeight - height
        self.rect = p.Rect(self.x, self.y, width, height)

        # grill image stuff
        img = p.image.load("./sprites/grill/grill.png").convert_alpha()
        self.grillimg = p.transform.scale(img, (img.get_width() * (self.width / img.get_width()), img.get_height() * (self.height / img.get_height())))

        # grill spots. Some rects where clickable patties will be
        self.spot0 = p.Rect(self.x + 80, self.y + 135, 70, 40)
        self.spot1 = p.Rect(self.x + 160, self.y + 100, 70, 40)
        self.spot2 = p.Rect(self.x + 240, self.y + 135, 70, 40)
        self.spot3 = p.Rect(self.x + 320, self.y + 100, 70, 40)

        # Patties
        self.patties = [patty(self.spot0), patty(self.spot1), patty(self.spot2), patty(self.spot3)]



    def drawMe(self, screen):

        p.draw.rect(screen, (0,0,0), self.rect, self.width)
        p.draw.rect(screen, (255,255,255), self.rect, 2)
        screen.blit(self.grillimg, (self.x, self.y))

        for pat in self.patties:
            pat.drawMe(screen)

        return
    

    def clickCheck(self, mX, mY):
        pass