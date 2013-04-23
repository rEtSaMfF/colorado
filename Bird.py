import pygame
import Mountain
from random import randint

def getstuff(imgs):
    global sheet
    sheet = (imgs[0].subsurface(0,0,32,32), imgs[0].subsurface(32,0,32,32), imgs[0].subsurface(64,0,32,32), imgs[0].subsurface(96,0,32,32))

class Bird(pygame.sprite.Sprite):
    def __init__(self, birds):
        pygame.sprite.Sprite.__init__(self)
        self.ai = 0
        self.image = sheet[0]
        self.rect = self.image.get_rect()
        self.rect.top = randint(0,480-self.rect.height)
        self.rect.left = 0.0
        self.checkspawn(birds)
        self.speed = randint(1,3)

    def checkspawn(self, birds):
        for b in birds:
            if self.rect.colliderect(b.rect):
                self.rect.top = randint(0,480-self.rect.height)
                self.checkspawn(birds)
    
    def slap(self, mountains):
        mountains.add(Mountain.Mountain(self.rect.center))
        self.kill()
    
    def update(self):
        self.rect.left += self.speed
        if self.rect.left >= 640:
            self.kill()
            
        # animation time
        self.ai += 1
        self.image = sheet[self.ai%4]
            
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)