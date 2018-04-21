"""
Obstacle module.
Represents an obstacle on the road.

Pythalex - April 2018
Ludum Dare 41

"""

import os
import pygame
from actor import Actor
from pygame.rect import Rect

class Obstacle(Actor):

    sep = os.path.sep
    img = pygame.image.load("resources" + sep + "obstacle.png")

    speed = 5

    def __init__(self, master, x: int, y: int):

        Actor.__init__(self, master, self.img, x, y)

        self.orig_hitboxes = [
            Rect(4, 4, 32, 32)
        ]
        self.hitboxes = [
            Rect(4, 4, 32, 32)
        ]

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