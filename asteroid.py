import pygame
from constants import *
from circleshape import CircleShape
from particle import Particle
import random
import math

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.rotation_speed = random.uniform(-0.1, 0.1)
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(-1, 1)
        
        self.vertices = []
        num_vertices = random.randint(7, 12)  # Between 7-12 points makes good asteroids
        
        for i in range(num_vertices):
            # Calculate angle for this vertex
            angle = math.radians(i * 360 / num_vertices)
            
            # Random distance from center (with variation)
            distance = radius * random.uniform(0.7, 1.0)
            
            # Calculate vertex coordinates
            vertex_x = distance * math.cos(angle)
            vertex_y = distance * math.sin(angle)
            
            self.vertices.append((vertex_x, vertex_y))
            
        # Create a smaller, darker shape for crater details
        self.craters = []
        num_craters = random.randint(2, 5)
        
        for _ in range(num_craters):
            # Random position within the asteroid
            crater_angle = random.uniform(0, math.pi * 2)
            crater_distance = radius * random.uniform(0.2, 0.6)
            crater_x = crater_distance * math.cos(crater_angle)
            crater_y = crater_distance * math.sin(crater_angle)
            crater_size = radius * random.uniform(0.1, 0.3)
            self.craters.append((crater_x, crater_y, crater_size))
        
    def update(self, dt):
        # Update position
        self.position += self.velocity * dt 
        
        # Update rotation
        self.rotation += self.rotation_speed
        
    def draw(self, surface):
        rotated_vertices = []
        for x, y in self.vertices:
            # Apply rotation
            rot_x = x * math.cos(self.rotation) - y * math.sin(self.rotation)
            rot_y = x * math.sin(self.rotation) + y * math.cos(self.rotation)
            
            # Apply position
            rotated_vertices.append((self.position.x + rot_x, self.position.y + rot_y))
        
        # Draw the asteroid (main body)
        pygame.draw.polygon(surface, GRAY, rotated_vertices)
        pygame.draw.polygon(surface, WHITE, rotated_vertices, 1)  # Outline
        
        # Draw craters
        for cx, cy, csize in self.craters:
            # Rotate crater position
            rot_cx = cx * math.cos(self.rotation) - cy * math.sin(self.rotation)
            rot_cy = cx * math.sin(self.rotation) + cy * math.cos(self.rotation)
            
            # Draw crater
            pygame.draw.circle(surface, DARK_GRAY, (int(self.position.x + rot_cx), int(self.position.y + rot_cy)), int(csize))

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

