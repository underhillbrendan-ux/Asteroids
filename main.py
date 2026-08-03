import sys
import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot

def main():
    print("Starting Asteroids")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize Pygame and set up the display
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    # Set up sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    # Assign static container groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,) 
    Shot.containers = (shots, updatable, drawable)

    # Instantiate game entities
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()  # Spawns asteroids periodically into 'asteroids' group

    # Set up clock
    clock = pygame.time.Clock()
    dt = 0.0

    # Game Loop
    while True:
        log_state()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update all objects in updatable group
        updatable.update(dt)


        for asteroid in asteroids:
            if player.collide_with(asteroid):
                log_event("player_hit")
                print("Game over")
                sys.exit()
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collide_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()       
        # Render step
        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        # Cap frame rate at 60 FPS and calculate delta time in seconds
        dt = clock.tick(60) / 1000.0


if __name__ == "__main__":
    main()