# score.py
import pygame


class Scoreboard:
    def __init__(self, x=20, y=20):
        self.score = 0
        self.x = x
        self.y = y
        # Uses default Pygame font, size 36
        self.font = pygame.font.Font(None, 36)

    def add_score(self, points):
        self.score += points

    def draw(self, screen):
        # Render the score text surface
        score_surface = self.font.render(f"Score: {self.score}", True, "white")
        screen.blit(score_surface, (self.x, self.y))