import random
import pygame
import pathlib
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
from logger import log_event


class Asteroid(CircleShape):
    # Class-level variable to store the original image so it's loaded only once
    image = None

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

        # Load the image once if it hasn't been loaded yet

        if Asteroid.image is None:
            asteroid_path = pathlib.Path("assets/asteroid.png")
            Asteroid.image = pygame.image.load(asteroid_path).convert_alpha()

        # Scale the sprite to match the asteroid's diameter (2 * radius)
        diameter = int(self.radius * 2)
        self.scaled_image = pygame.transform.scale(Asteroid.image, (diameter, diameter))

    def draw(self, screen: pygame.Surface) -> None:
        # Create a rect centered at self.position so the image draws over the collision circle
        image_rect = self.scaled_image.get_rect(center=(self.position.x, self.position.y))
        screen.blit(self.scaled_image, image_rect)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        # Destroy the current asteroid
        self.kill()

        # If it's the smallest size, don't spawn new ones
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Log the split event
        log_event("asteroid_split")

        # Generate a random angle for splitting
        random_angle = random.uniform(20, 50)

        # Create two new rotated velocity vectors
        velocity1 = self.velocity.rotate(random_angle)
        velocity2 = self.velocity.rotate(-random_angle)

        # Calculate new radius for smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Spawn the two smaller asteroids at the current position
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Assign increased velocities (1.2x faster)
        asteroid1.velocity = velocity1 * 1.2
        asteroid2.velocity = velocity2 * 1.2