import pygame
from circleshape import CircleShape


class Particle(CircleShape):  # Changed Particles -> Particle
    def __init__(
        self,
        x: float,
        y: float,
        radius: float,
        velocity: pygame.Vector2,
        lifetime: float,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        super().__init__(x, y, radius)
        self.velocity = velocity
        self.lifetime = lifetime
        self.initial_lifetime = lifetime
        self.initial_radius = radius
        self.color = color

    def update(self, dt: float) -> None:
        # Move the particle
        self.position += self.velocity * dt

        # Countdown lifetime
        self.lifetime -= dt

        # Gradually shrink radius over time
        if self.initial_lifetime > 0:
            self.radius = max(0.0, self.initial_radius * (self.lifetime / self.initial_lifetime))

        # Remove the sprite when it expires
        if self.lifetime <= 0 or self.radius <= 0:
            self.kill()

    def draw(self, screen: pygame.Surface) -> None:
        if self.radius > 0:
            pygame.draw.circle(screen, self.color, self.position, self.radius)


    