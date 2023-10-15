import pygame as p

class patty(p.sprite.Sprite):

    def __init__(self):
        super.__init__()


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
        print(img.get_width(), img.get_height())
        self.grillimg = p.transform.scale(img, (img.get_width() * (self.width / img.get_width()), img.get_height() * (self.height / img.get_height())))


    def drawMe(self, screen):

        p.draw.rect(screen, (0,0,0), self.rect, self.width)
        p.draw.rect(screen, (255,255,255), self.rect, 2)
        screen.blit(self.grillimg, (self.x, self.y))

        return