import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape): 
    def __init__(self, position, direction):
        super().__init__(position.x, position.y, SHOT_RADIUS)
        self.velocity = direction * PLAYER_SHOOT_SPEED

    def update(self, del_t):
        self.position += self.velocity * del_t

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, 2)