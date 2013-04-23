import pygame
from math import hypot

def getstuff(imgs,snds):
    global sheet, sounds
    sheet = (imgs[0].subsurface(0,0,16,16), imgs[0].subsurface(16,0,16,16), imgs[0].subsurface(32,0,16,16), imgs[0].subsurface(48,0,16,16), imgs[0].subsurface(64,0,16,16),
             imgs[0].subsurface(80,0,16,16))
    sounds = [snds]

class Fish(pygame.sprite.Sprite):
    def __init__ (self, loc):
        pygame.sprite.Sprite.__init__(self)
        self.ai = 0
        self.image = sheet[0]
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.active = False

    def slap(self, mountains, aliens, birds, pools):
        if self.active:
            for m in mountains:
                if not m.away:
                    if self.rect.colliderect(m.rect):
                        sounds[0].play()
                        if m.slap():
                            self.active = False
                        return

            for a in aliens:
                if self.rect.colliderect(a.rect):
                    a.slap()
                    self.active = False
                    sounds[0].play()
                    return
                    
            for b in birds:
                if self.rect.colliderect(b.rect):
                    b.slap(mountains)
                    self.active = False
                    sounds[0].play()
                    return
                    
        else:
            # if you are not currently holding a fish
            for m in mountains:
                # only if you are holding the mountain
                if m.active and self.rect.colliderect(m.rect):
                    # drop the mountain
                    m.drop()
                    # and if you drop it in a pool, plug the pool
                    for p in pools:
                        if p.active:
                            if hypot(m.rect.centerx-p.center[0],m.rect.centery-p.center[1]) <= p.radius:
                                m.plugging = True
                                p.plug()
                                m.pluggedpool = p
                                return
                # if you are not holding a mountain
                else:
                    # if you click it
                    if self.rect.colliderect(m.rect):
                        # if it is plugging
                        if m.plugging:
                            # unplug the pool
                            m.pluggedpool.unplug()
                        # pick up the mountain because you clicked it for some reason
                        m.pickup()
                        return
            for p in pools:
                if p.active:
                    if hypot(self.rect.centerx-p.center[0],self.rect.centery-p.center[1]) <= p.radius:
                        self.active = True
                        return
            return

    def update(self, loc):
        self.rect.center = loc
        
        # animation time
        self.ai += 1
        self.image = sheet[self.ai%6]

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect.topleft)