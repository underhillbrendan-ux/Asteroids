import random
import pygame
from particles import Particle



def create_particle_explosion(x: float, y: float, count: int = 20) -> None:
    for _ in range(count):
        # Generate a random speed and 360-degree direction
        speed = random.uniform(50, 250)
        angle = random.uniform(0, 360)
        velocity = pygame.Vector2(1, 0).rotate(angle) * speed

        # Particle properties
        radius = random.uniform(2, 6)
        lifetime = random.uniform(0.2, 0.6)  # duration in seconds
        
        # Explosion colors (orange/yellow/white)
        color = random.choice([
            (255, 80, 0),
            (255, 200, 0),
            (255, 255, 255)
        ])

        # Instantiating Particle automatically adds it to Particle.containers
        Particle(x, y, radius, velocity, lifetime, color)