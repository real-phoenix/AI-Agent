import pygame
import sys
from constants import *
from shot import Shot
from player import Player
from asteroids import Asteroids
from asteroidfield import AsteroidField

def main(): 
    print("Starting Asteroids!")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Screen width: {SCREEN_WIDTH}") 
    print(f"Screen height: {SCREEN_HEIGHT}") 

    timeClock = pygame.time.Clock() 
    del_t = 0

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids_all = pygame.sprite.Group()
    all_shots = pygame.sprite.Group()

    Player.containers = (updateable, drawable)
    Asteroids.containers = (updateable, drawable, asteroids_all)
    AsteroidField.containers = (updateable)
    Shot.containers = (updateable, drawable, all_shots)

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updateable.update(del_t)

        for asteroid in asteroids_all: 
            for shot in all_shots: 
                if shot.collides_with(asteroid): 
                    asteroid.split()
                    shot.kill()

        for asteroid in asteroids_all: 
            if player.collides_with(asteroid): 
                print("Game Over!")
                pygame.quit()
                sys.exit()

        screen.fill((0,0,0))

        for obj in drawable: 
            obj.draw(screen)

        pygame.display.flip()
        del_t = timeClock.tick(60)/1000

if __name__ == "__main__": 
    main()