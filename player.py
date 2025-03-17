from circleshape import CircleShape
from shot import Shot
from constants import *
import pygame

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

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

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

        if keys[pygame.K_a]:
            self.rotate(-dt)
        
        if keys[pygame.K_d]:
            self.rotate(dt)
            
        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(dt)
        
        if keys[pygame.K_SPACE]:
            if self.shooting_timer <= 0:
                self.shoot()
                self.shooting_timer = PLAYER_SHOOT_COOLDOWN

        self.shooting_timer -= dt

    # TODO: implement this with triangular hitbox
    # def check_collision(self, other):
        # pass
        
        