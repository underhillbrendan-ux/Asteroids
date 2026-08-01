import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state

def main():
    print("Starting Asteroids")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize Pygame and set up the display
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    # Game Loop
    while True:
        log_state()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Render step
        screen.fill("black")
        pygame.display.flip()

if __name__ == "__main__":
    main()