import pygame, math, random
import Bullet

def getstuff(imgs):
    global images
    images = imgs

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.spd = 2
        self.image = images[0].subsurface(0,0,32,32)
        self.rect = self.image.get_rect()
        self.rect.center = (320,240)
        self.loc = [self.rect.left, self.rect.top]
        self.xspeed = 0
        self.yspeed = 0

    def move(self, x, y):
        self.moving = True
        if x != 0:
            self.xspeed = x
        else:
            self.yspeed = y

    def stopmove(self, x, y):
        if x != 0:
            self.xspeed = 0
        else:
            self.yspeed = 0

        if self.xspeed == 0 and self.yspeed == 0:
            self.moving = False

    def shoot(self, m1, bullets):
        bullets.add(Bullet.Bullet(self.rect.center, m1))

    def update(self):
        oldloc = self.rect.center

        coll = False
        if self.xspeed != 0 and self.yspeed != 0:
            self.loc[0] += self.spd * self.xspeed * .7
        else:
            self.loc[0] += self.spd * self.xspeed
        self.rect.topleft = self.loc
        if self.rect.left < 0:
            coll = True
            self.rect.left = 0
        elif self.rect.right > 640:
            coll = True
            self.rect.right = 640
        if coll:
            self.loc = [self.rect.left, self.rect.top]

        coll = False
        if self.xspeed != 0 and self.yspeed != 0:
            self.loc[1] += self.spd * self.yspeed * .7
        else:
            self.loc[1] += self.spd * self.yspeed
        self.rect.topleft = self.loc
        self.rect.topleft = (self.rect.left+12, self.rect.top+12)
        if self.rect.top < 0:
            coll = True
            self.rect.top = 0
        elif self.rect.bottom > 480:
            coll = True
            self.rect.bottom = 480

        if coll:
            self.loc = [self.rect.left, self.rect.top]

    def draw(self, screen):
        screen.blit(self.image, self.loc)
