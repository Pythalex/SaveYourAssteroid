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
    img = pygame.image.load("resources" + sep + "asteroid.png")

    speed = 3.5
    rotating_speed = 1

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

if __name__ == '__main__':

    pygame.init()
    pygame.display.set_mode((400, 300))

    actor = Obstacle(None, 0, 32)
    old_x = actor.rect.x
    actor.move(0)
    actor.move(2)
    assert(actor.rect.x == old_x)
    assert(actor.is_out_of_bound(1, 200, 0, 200)[0])
    assert(actor.is_out_of_bound(0, 30, 0, 200)[0])
    assert(not actor.is_out_of_bound(0, 200, 0, 200)[0])