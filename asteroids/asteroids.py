import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroids(CircleShape): 
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, 2)
    
    def update(self, del_t):
        self.position += self.velocity*del_t

    def split(self): 
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS: 
            return 
    
        random_angle = random.uniform(20,50)

        velocity1 = self.velocity.rotate(random_angle)*1.2
        velocity2 = self.velocity.rotate(-random_angle)*1.2

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroids(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = velocity1

        asteroid2 = Asteroids(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = velocity2

        # if hasattr(self, 'groups'):
        #     for group in self.groups():
        #         group.add(asteroid1)
        #         group.add(asteroid2)
