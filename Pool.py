import pygame
from math import hypot

class Pool(pygame.sprite.Sprite):
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        self.center = loc
        self.radius = 10.0
        self.active = True
    
    def plug(self):
        self.active = False
    
    def unplug(self):
        self.active = True
    
    def update(self,mountains):
        if self.active:
            self.radius += 1.0/45
        for m in mountains:
            if hypot(m.rect.centerx-self.center[0],m.rect.centery-self.center[1]) >= self.radius:
                if self == m.pluggedpool:
                    self.unplug()
    
    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, (0,0,255), self.center, int(self.radius), 0)
