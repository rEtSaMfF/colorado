import pygame
from math import hypot

def getstuff(imgs,snds):
    global sheet, sounds
    sheet = (imgs[0].subsurface(0,0,16,16), imgs[0].subsurface(16,0,16,16), imgs[0].subsurface(32,0,16,16), imgs[0].subsurface(48,0,16,16), imgs[0].subsurface(64,0,16,16),
             imgs[0].subsurface(80,0,16,16))
    sounds = [snds]

class Bullet(pygame.sprite.Sprite):
    def __init__ (self, loc, dir):
        pygame.sprite.Sprite.__init__(self)
        self.ai = 0
        self.image = sheet[0]
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.dir = [dir[0]-loc[0],dir[1]-loc[1]]
        blah = hypot(self.dir[0],self.dir[1])
        self.dir[0] = self.dir[0]/blah
        self.dir[1] = self.dir[1]/blah
        self.speed = 5

    def update(self, aliens):
        self.rect.centerx += self.dir[0] * self.speed
        self.rect.centery += self.dir[1] * self.speed
        
        # kill if we go off screen
        if self.rect.right > 640:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.top < 0:
            self.kill()
        if self.rect.bottom > 480:
            self.kill()
        
        # collision time
        for a in aliens:
            if self.rect.colliderect(a.rect):
                sounds[0].play()
                a.kill()
                self.kill()
                return

        # animation time
        self.ai += 1
        self.image = sheet[self.ai%6]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)