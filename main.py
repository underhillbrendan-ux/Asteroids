import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from player import Player
def main():
    print("Starting Asteroids")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize Pygame and set up the display
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    player = Player(
    SCREEN_WIDTH / 2,
    SCREEN_HEIGHT / 2,
    )
    # Set up clock and delta time tracking
    clock = pygame.time.Clock()
    dt = 0.0

    # Game Loop
    while True:
        log_state()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        player.update(dt)
        # Render step
        screen.fill("black")
        player.draw(screen)
        pygame.display.flip()
        
        
        

        # Cap frame rate at 60 FPS and calculate delta time in seconds
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()