import pygame
from math import hypot
from random import randint

def getstuff(imgs):
    global sheet
    sheet = (imgs[0].subsurface(0,0,32,32), imgs[0].subsurface(0,0,32,32), imgs[0].subsurface(0,0,32,32), imgs[0].subsurface(0,0,32,32),
             imgs[0].subsurface(32,0,32,32), imgs[0].subsurface(32,0,32,32), imgs[0].subsurface(32,0,32,32), imgs[0].subsurface(32,0,32,32))

class Alien(pygame.sprite.Sprite):
    def __init__(self, loc, mountain, randloc=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = sheet[0]
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.mountain = mountain
        self.ai = 0
        if randloc:
            s = randint(0,3)
            if s == 0:
                self.rect.centery = 0
                self.rect.centerx = randint(0,640)
            elif s == 1:
                self.rect.centery = 480
                self.rect.centerx = randint(0,640)
            elif s == 2:
                self.rect.centery = randint(0,480)
                self.rect.centerx = 0
            elif s == 3:
                self.rect.centery = randint(0,480)
                self.rect.centerx = 640
    
    def slap(self):
        self.kill()
    
    def update(self):
        if self.rect.colliderect(self.mountain.rect):
            self.movetowards(self.mountain.start)
            self.mountain.movetowards(self.mountain.start)
            self.mountain.beingpulled = True
            if self.mountain.plugging:
                self.mountain.pluggedpool.unplug()
                self.mountain.plugging = False
        else:
            self.movetowards(self.mountain.rect.center)
            self.mountain.beingpulled = False
            self.mountain.count = 0
        if hypot(self.mountain.rect.centerx-self.mountain.start[0],self.mountain.rect.centery-self.mountain.start[1]) <= 1:
            self.mountain.away = False
            self.mountain.hits = 10
            self.kill()
            
        self.ai += 1
        self.image = sheet[self.ai%8]
            
        # animations lol
            
    def movetowards(self, loc):
        if self.rect.centerx < loc[0]:
            self.rect.centerx += randint(0,1)
        else:
            self.rect.centerx -= randint(0,1)
        if self.rect.centery < loc[1]:
            self.rect.centery += randint(0,1)
        else:
            self.rect.centery -= randint(0,1)
        # if self.rect.centerx < loc[0]:
            # self.rect.centerx += 1
        # else:
            # self.rect.centerx -= 1
        # if self.rect.centery < loc[1]:
            # self.rect.centery += 1
        # else:
            # self.rect.centery -= 1
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)