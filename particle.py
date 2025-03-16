import pygame

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, lifetime=1.0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.lifetime = lifetime
        self.alpha = 255
        self.fade_rate = 255 / lifetime

    def update(self, dt):
        self.position += self.velocity * dt
        self.alpha = max(0, self.alpha - self.fade_rate * dt)
        return self.alpha > 0

    def draw(self, screen):
        if self.alpha > 0:
            color = (255, 255, 255, int(self.alpha))
            surf = pygame.Surface((3, 3), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (1, 1), 1)
            screen.blit(surf, self.position)