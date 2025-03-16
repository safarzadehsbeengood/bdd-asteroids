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
    Particle.containers = (particles, updatable, drawable)

    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    Shot.containers = (shots, updatable, drawable)

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # create the screen

    while True:
        # get events and quit if needed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black") # fill with black

        updatable.update(dt)

        # check collisions
        for asteroid in asteroids:
            if player.check_collision(asteroid):
                print("Game Over!")
                sys.exit(0)
            for shot in shots:
                if asteroid.check_collision(shot):
                    shot.kill()
                    asteroid.split()

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip() # refresh the screen

        dt = clock.tick(FPS) / 1000 # get amount of time since last tick


if __name__ == "__main__":
    main()


