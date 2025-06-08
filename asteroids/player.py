import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape): 
    def __init__(self, x, y): 
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation =0
        self.shoot_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)
    
    def rotate(self, del_t): 
        self.rotation+=PLAYER_TURN_SPEED*del_t

    def update(self, del_t):
        keys = pygame.key.get_pressed()

        if self.shoot_timer>0: 
            self.shoot_timer -= del_t

        if keys[pygame.K_a]:
            self.rotate(-del_t)
        if keys[pygame.K_d]:
            self.rotate(del_t)
        if keys[pygame.K_w]:
            self.move(del_t)
        if keys[pygame.K_s]:
            self.move(-del_t)

        if keys[pygame.K_SPACE] and self.shoot_timer<=0 : 
            self.shoot()
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN

    def move(self, del_t):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * del_t

    def shoot(self): 
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        Shot(self.position, direction)