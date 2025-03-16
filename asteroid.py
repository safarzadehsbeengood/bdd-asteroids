import pygame
from constants import *
from circleshape import CircleShape
from particle import Particle
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt 

    def explode(self):
        particles = []
        # create 20 particles
        for _ in range(20):
            angle = random.uniform(0, 360)
            speed = random.uniform(50, 150)
            velocity = pygame.Vector2(1, 0).rotate(angle) * speed
            particle = Particle(self.position.x, self.position.y, velocity, random.uniform(0.5, 1.0))
            particles.append(particle)
        return particles

    def split(self):
        particles = self.explode()
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        new_angle = random.uniform(20, 50)
        v1, v2 = self.velocity.rotate(new_angle), self.velocity.rotate(-new_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        a1, a2 = Asteroid(self.position.x, self.position.y, new_radius), Asteroid(self.position.x, self.position.y, new_radius)
        a1.velocity = v1 * 1.2
        a2.velocity = v2 * 1.2

