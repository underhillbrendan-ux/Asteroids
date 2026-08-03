import pygame
from shot import Shot
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS, 
    LINE_WIDTH, 
    PLAYER_TURN_SPEED, 
    PLAYER_SPEED, 
    PLAYER_SHOOT_SPEED, 
    PLAYER_SHOOT_COOLDOWN_SECONDS
)


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0  # Shot cooldown timer initialized to 0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(
            screen,
            "white",
            self.triangle(),
            LINE_WIDTH
        )

    def shoot(self):
        # Prevent shooting if cooldown timer is active
        if self.cooldown_timer > 0:
            return

        # Reset the cooldown timer
        self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        # Create a new Shot at the player's current position
        shot = Shot(self.position.x, self.position.y)
        
        # Define the base direction vector (pointing down initially)
        velocity = pygame.Vector2(0, 1)
        
        # Rotate the vector to match the player's facing direction/rotation
        velocity = velocity.rotate(self.rotation)
        
        # Scale up the velocity vector by the shooting speed multiplier
        shot.velocity = velocity * PLAYER_SHOOT_SPEED

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * dt * PLAYER_SPEED

    def rotate(self, dt):
        self.rotation += dt * PLAYER_TURN_SPEED

    def update(self, dt: float) -> None:
        # Decrease cooldown timer each frame
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt)
        if keys[pygame.K_d]:
            self.rotate(-dt)
        if keys[pygame.K_w]:
            self.move(dt)    
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()