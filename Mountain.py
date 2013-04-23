import pygame
import Alien
from random import randint

def getstuff(imgs):
    global sheet
    sheet = (imgs[0].subsurface(0,0,64,64), imgs[0].subsurface(64,0,64,64))

class Mountain(pygame.sprite.Sprite):
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        self.image = sheet[0]
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.start = loc
        self.hits = 10
        self.active = False
        self.away = False
        self.plugging = False
        self.beingpulled = False
        self.count = 0
        self.pluggedpool = None
    
    def slap(self):
        self.hits -= 1
        if self.hits <= 0:
            self.pickup()
            return True
        return False
    
    def pickup(self):
        if self.hits <= 0:
            self.active = True
            self.away = True
            self.plugging = False
    
    def drop(self):
        self.active = False
    
    def update(self, loc, aliens):
        if self.active:
            self.rect.center = loc
        if self.away:
            self.count += 1
            if self.count >= 300:
                self.count = 0
                aliens.add(Alien.Alien(self.start,self))
                
    def movetowards(self, loc):
        if self.rect.centerx < loc[0]:
            self.rect.centerx += randint(0,1)
        else:
            self.rect.centerx -= randint(0,1)
        if self.rect.centery < loc[1]:
            self.rect.centery += randint(0,1)
        else:
            self.rect.centery -= randint(0,1)
    
    def draw(self, screen):
        if self.away:
            pygame.draw.circle(screen, (0,0,0), self.start, 5, 0)
            screen.blit(sheet[1], self.rect.topleft)
        else:
            screen.blit(sheet[0], self.rect.topleft)