import sys
import pygame
import pathlib
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from particles import Particle
from player import Player
from score import Scoreboard
from shot import Shot
from spawner import create_particle_explosion
from sounds import generate_explosion_sound

def main():
    # Initialize Pygame and set up the display with RESIZABLE flag
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Asteroids")
    # sounds init
    explosion = generate_explosion_sound()
    # Keep the raw image in memory and create a scaled copy
    bg_path = pathlib.Path("assets") / "Background.png"
    bg_raw = pygame.image.load(bg_path).convert()
    bg_image = pygame.transform.scale(bg_raw, screen.get_size())

    # Set up sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()

    # Assign static container groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (particles, updatable, drawable)

    # Fonts for game-over screen
    game_over_font = pygame.font.Font(None, 96)
    score_font = pygame.font.Font(None, 48)
    restart_font = pygame.font.Font(None, 32)

    def reset_game():
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()
        particles.empty()

        new_player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        new_field = AsteroidField()
        new_scoreboard = Scoreboard(x=20, y=20)
        return new_player, new_field, new_scoreboard

    player, asteroid_field, scoreboard = reset_game()

    clock = pygame.time.Clock()
    dt = 0.0
    game_over = False

    # Game Loop
    while True:

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #  Re-scale background whenever window is resized or maximized
            elif event.type == pygame.VIDEORESIZE:
                bg_image = pygame.transform.scale(bg_raw, screen.get_size())

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if game_over and event.key == pygame.K_r:
                    player, asteroid_field, scoreboard = reset_game()
                    game_over = False

        if not game_over:
            updatable.update(dt)
        else:
            particles.update(dt)

        if not game_over:
            for asteroid in asteroids:
                if player.collide_with(asteroid):
                    create_particle_explosion(
                        player.position.x, player.position.y
                    )
                    log_event("player_died")
                    game_over = True
                    explosion.play()
                    player.kill()
                    break

        if not game_over:
            for asteroid in list(asteroids):
                for shot in list(shots):
                    if asteroid.collide_with(shot):
                        create_particle_explosion(
                        asteroid.position.x, asteroid.position.y
                        )
                        explosion.play()
                        scoreboard.add_score(100)
                        asteroid.split()
                        shot.kill()
                        break

        # Draw the re-scaled background
        screen.blit(bg_image, (0, 0))

        for obj in drawable:
            obj.draw(screen)

        scoreboard.draw(screen)

        if game_over:
            # Use current screen width/height so text stays centered on maximize
            current_w, current_h = screen.get_size()

            game_over_text = game_over_font.render(
                "GAME OVER", True, (0, 0, 0)
            )
            final_score_text = score_font.render(
                f"Final Score: {scoreboard.score}", True, (50, 205, 50)
            )
            restart_text = restart_font.render(
                "Press R to restart or ESC to quit", True, (0, 0, 0)
            )

            screen.blit(
                game_over_text,
                game_over_text.get_rect(
                    center=(current_w / 2, current_h / 2 - 80)
                ),
            )
            screen.blit(
                final_score_text,
                final_score_text.get_rect(
                    center=(current_w / 2, current_h / 2)
                ),
            )
            screen.blit(
                restart_text,
                restart_text.get_rect(
                    center=(current_w / 2, current_h / 2 + 60)
                ),
            )

        pygame.display.flip()

        # Cap frame rate at 60 FPS and calculate delta time
        dt = clock.tick(60) / 1000.0


if __name__ == "__main__":
    main()