"""
Obstacle module.
Represents an obstacle on the road.

Pythalex - April 2018
Ludum Dare 41

"""

import os
import random
import pygame
from actor import Actor
from pygame.rect import Rect

class Obstacle(Actor):

    sep = os.path.sep
    sprite_intact = pygame.image.load("resources" + sep + "asteroid.png")
    sprite_destroyed = pygame.image.load("resources" + sep + "asteroid_destroyed.png")
    img = sprite_intact

    speed = 3.5
    rotating_speed = 1

    destroyed = False

    def __init__(self, master, x: int, y: int):

        Actor.__init__(self, master, self.img, x, y)

        self.rotating_speed = (1 if random.randint(0, 2) == 0 else -1 ) *\
           (random.randrange(0, 3) + 0.5)

        self.move_x = random.randrange(-1, 2) * (random.randint(0, 50) / 10.0)

        self.orig_hitboxes = [
            Rect(5, 5, 29, 30)
        ]
        self.hitboxes = [
            Rect(5, 5, 29, 30)
        ]

    def move(self):
        """
        Moves the asteroid.
        """
        self.rect.move_ip(self.move_x, self.speed)
        self.update_hitboxes()

    def destroy(self):
        """
        Destroys the asteroid.
        It can no longer hit anybody.
        """
        self.destroyed = True
        self.can_collide = False
        self.set_image(self.sprite_destroyed, self.rect.x, self.rect.y)

if __name__ == '__main__':

    pygame.init()
    pygame.display.set_mode((400, 300))

    actor = Obstacle(None, 0, 32)
    old_x = actor.rect.x
    actor.move()
    actor.move()
    actor.destroy()
    assert actor.destroyed == True