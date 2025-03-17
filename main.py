import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle
import sys

def main():

    pygame.init()
    clock = pygame.time.Clock()

    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # instantiate player

    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (particles, updatable, drawable)

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    font = pygame.font.SysFont(None, 32)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # create the screen

    def render_text(text, value, offset):
        score = font.render(f"{str(text)}: " + str(value), False, WHITE)
        score_rect = score.get_rect()
        score_rect.center = (SCREEN_WIDTH // 2 + offset, 20)
        return score, score_rect

    score, score_rect = render_text("score", player.score, -100)
    lives, lives_rect = render_text("lives", player.lives, 100)
    
    dying_cooldown = 0

    while True:
        # get events and quit if needed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black") # fill with black

        updatable.update(dt)

        # check collisions
        for asteroid in asteroids:
            if dying_cooldown <= 0 and player.check_collision(asteroid):
                player.die()
                lives, lives_rect = render_text("lives", player.lives, 100)
                if player.lives <= 0:
                    print("Game Over!")
                    sys.exit(0)
                dying_cooldown = FPS * DYING_COOLDOWN # DYING_COOLDOWN seconds before checking player collisions
            for shot in shots:
                if asteroid.check_collision(shot):
                    shot.kill()
                    player.add_score(asteroid.kind)
                    score, score_rect = render_text("score", player.score, -100)
                    asteroid.split()

        if dying_cooldown > 0:
            dying_cooldown -= 1

        for obj in drawable:
            obj.draw(screen)

        for particle in particles:
            if particle.alpha <= 0:
                particle.kill()

        screen.blit(score, score_rect)
        screen.blit(lives, lives_rect)

        pygame.display.flip() # refresh the screen

        dt = clock.tick(FPS) / 1000 # get amount of time since last tick


if __name__ == "__main__":
    main()


