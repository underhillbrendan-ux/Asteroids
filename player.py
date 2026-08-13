import sys
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
from sounds import sound_manager
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, "_MEIPASS"):
        return pathlib.Path(sys._MEIPASS) / relative_path
    return pathlib.Path(".") / relative_path

class Player(CircleShape):
    image = None
    rotated_cache = {}  # Cache for all 360 pre-rotated directions

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0

        # Load base image once
        if Player.image is None:
            ship_path = resource_path(pathlib.Path("assets") / "Ship.png")
            Player.image = pygame.image.load(ship_path).convert_alpha()

            # Scale and explicitly call convert_alpha() on the scaled surface
            diameter = int(self.radius * 3)
            scaled_base = pygame.transform.smoothscale(Player.image, (diameter, diameter)).convert_alpha()

            # Pre-render all 360 integer angles
            Player.rotated_cache = {
                angle: pygame.transform.rotate(scaled_base, angle).convert_alpha()
                for angle in range(360)
            }

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 2
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        angle = int(-self.rotation + 180) % 360
        rotated_image = Player.rotated_cache[angle]

        center_x = round(self.position.x)
        center_y = round(self.position.y)
        rotated_rect = rotated_image.get_rect(center=(center_x, center_y))

        screen.blit(rotated_image, rotated_rect)

    def shoot(self):
        if self.cooldown_timer > 0:
            return

        self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = velocity * PLAYER_SHOOT_SPEED
        
        # Zero-lag audio playback from sound_manager
        sound_manager.laser.play()

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

        if self.velocity.length_squared() < 0.01:
            self.velocity = pygame.Vector2(0, 0)

        self.position += self.velocity * dt
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT