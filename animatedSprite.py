import pygame as p

framerate = 60

class animatedSprite(p.sprite.Sprite):

    def __init__(self, x, y, images):
        super().__init__()

        self.images = images
        self.rect = p.Rect(x, y, images[0].get_width(), images[0].get_height())

        self.animSpeed = 0
        self.frames = len(images)
        self.currFrame = 0


    def play(self, screen):

        currFrame = int(self.currFrame // 1)

        screen.blit(self.images[currFrame], (self.rect.x, self.rect.y))

        if self.currFrame < self.frames - self.animSpeed:
            self.currFrame += self.animSpeed
        else:
            self.currFrame = 0


    # speed is frames
    def set_speed(self, speed):
        self.animSpeed = speed