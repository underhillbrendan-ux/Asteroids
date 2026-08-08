import pathlib
import pygame
from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    FRICTION,
    PLAYER_ACCELERATION
)
from shot import Shot


class Player(CircleShape):
    # Class-level variable to store the unscaled base image
    image = None

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0  # Shot cooldown timer initialized to 0

        # Load the ship PNG once if it hasn't been loaded yet
        if Player.image is None:
            ship_path = pathlib.Path("assets") / "Ship.png"
            Player.image = pygame.image.load(ship_path).convert_alpha()

        # Scale the image to match the player's diameter (2 * radius)
        diameter = int(self.radius * 3.5)
        self.scaled_image = pygame.transform.scale(Player.image, (diameter, diameter))

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        # 1. Rotate the pre-scaled image.
        # Pygame rotates counter-clockwise (+deg), but Pygame screen vectors (+Y down)
        # rotate clockwise, so we negate self.rotation.
        angle = -self.rotation

        angle = -self.rotation + 180

        rotated_image = pygame.transform.rotate(self.scaled_image, angle)

        # 2. Get the new bounding box rect centered on self.position
        # (When surfaces rotate in Pygame, their width/height change slightly, so re-centering is required)
        rotated_rect = rotated_image.get_rect(center=(self.position.x, self.position.y))

        # 3. Render onto screen
        screen.blit(rotated_image, rotated_rect)

    def shoot(self):
        if self.cooldown_timer > 0:
            return

        self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = velocity * PLAYER_SHOOT_SPEED

    def accelerate(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt

    def rotate(self, dt):
        self.rotation += dt * PLAYER_TURN_SPEED

    def update(self, dt: float) -> None:
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt)
        if keys[pygame.K_d]:
            self.rotate(-dt)
        if keys[pygame.K_w]:
            self.accelerate(dt) 
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        self.velocity *= max(0, 1 - (FRICTION * dt))
        self.position += self.velocity * dt
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT