from circleshape import CircleShape
from shot import Shot
from constants import *
from particle import Particle
import pygame
import random

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shooting_timer = 0
        self.score = 0

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        
    def thruster(self):
        particles = []
        backward = pygame.Vector2(0, -1).rotate(self.rotation + 180)
        particle_position = self.position - backward * self.radius
        # create a couple particles in random directions
        for _ in range(10):
            spread = 60
            angle = self.rotation + 180 + random.uniform(-spread, spread)
            speed = random.uniform(200, 300)
            velocity = pygame.Vector2(0, 1).rotate(angle) * speed
            particle = Particle(particle_position.x, particle_position.y, velocity, (random.randint(20, 255), 0, 0), random.uniform(0.25, 0.5))
            particles.append(particle)
        return particles

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.acceleration += forward * PLAYER_ACCELERATION * dt

    def shoot(self):
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    
    def add_score(self, asteroid_type):
        # 0 -> small
        # 1 -> medium
        # 2 -> large
        match asteroid_type:
            case 0:
                self.score += SMALL_ASTEROID_SCORE
            case 1:
                self.score += MEDIUM_ASTEROID_SCORE
            case 2:
                self.score += LARGE_ASTEROID_SCORE

    def update(self, dt):
        keys = pygame.key.get_pressed()

        self.rotation %= 360
        self.acceleration = pygame.Vector2(0, 0)

        # key checks
        if keys[pygame.K_a]:
            self.rotate(-dt)
        
        if keys[pygame.K_d]:
            self.rotate(dt)
            
        if keys[pygame.K_w]:
            self.move(dt)
            self.thruster()

        if keys[pygame.K_SPACE]:
            if self.shooting_timer <= 0:
                self.shoot()
                self.shooting_timer = PLAYER_SHOOT_COOLDOWN

        # physics updates
        self.velocity += self.acceleration
        self.position += self.velocity
        if self.velocity.length() > 0: self.velocity.clamp_magnitude_ip(MAX_PLAYER_VELOCITY)
        self.velocity *= PLAYER_DAMPING

        self.shooting_timer -= dt

        # wrap around
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
            
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    # TODO: implement this with triangular hitbox
    # def check_collision(self, other):
        # pass
        
        