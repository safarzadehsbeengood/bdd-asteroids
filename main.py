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

    bg = pygame.image.load("./img/space.jpg")
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg.set_alpha(128)
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

    def render_text(text, x, y):
        text_render = font.render(text, True, WHITE)
        text_rect = text_render.get_rect()
        text_rect.center = (x, y)
        return text_render, text_rect 

    score, score_rect = render_text(f"score: {player.score}", 60, 20)
    lives, lives_rect = render_text(f"lives: {player.lives}", 60, 50)

    running = True

    while True:
        # get events and quit if needed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        screen.blit(bg, (0, 0))

        updatable.update(dt)

        # check collisions
        for asteroid in asteroids:
            if player.dying_cooldown <= 0 and player.check_collision(asteroid):
                player.die()
                lives, lives_rect = render_text(f"lives: {player.lives}", 60, 50)
                if player.lives <= 0:
                    print("Game Over!")
                    running = False
            for shot in shots:
                if asteroid.check_collision(shot):
                    shot.kill()
                    player.add_score(asteroid.kind)
                    score, score_rect = render_text(f"score: {player.score}", 60, 20)
                    asteroid.split()

        if not running: break

        if player.dying_cooldown > 0:
            player.dying_cooldown -= 1

        for obj in drawable:
            obj.draw(screen)

        for particle in particles:
            if particle.alpha <= 0:
                particle.kill()

        screen.blit(score, score_rect)
        screen.blit(lives, lives_rect)
        mode, mode_rect = render_text(f"weapon: {"triple shot" if player.shot_mode else "single shot"}", SCREEN_WIDTH // 2, 20)
        screen.blit(mode, mode_rect)

        pygame.display.flip() # refresh the screen

        dt = clock.tick(FPS) / 1000 # get amount of time since last tick
    
    game_over_timer = FPS * 3 # 3 seconds of game over screen

    game_over, game_over_rect = render_text("Game Over!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    while game_over_timer > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        screen.blit(game_over, game_over_rect)
        pygame.display.flip()
        game_over_timer -= 1
        dt = clock.tick(FPS) / 1000

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


