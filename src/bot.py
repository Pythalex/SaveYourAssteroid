"""
Bot module.
Represents a player, real or bot.

Pythalex - April 2018
Ludum Dare 41

"""

import os
import pygame
from pygame.surface import Surface
from pygame.rect import Rect

import player
from player import Player
from playercontroller import Player_Controller

class Bot(Player):
    """
    Represents a bot.
    """

    def __init__(self, master, x: int = 0, y: int = 0):

        # Create actor
        Player.__init__(self, master, x, y)

    def make_action(self):
        """
        Let the player make an action.
        """
        print("Bot says : I promise I'm trying to do something !!!")

if __name__ == '__main__':

    pygame.init()
    pygame.display.set_mode((400, 300))

    actor = Bot(None)
    old_x = actor.rect.x
    actor.move(0)
    actor.move(2)
    assert(actor.rect.x == old_x)
    assert(actor.is_out_of_bound(1, 200, 0, 200)[0])
    assert(actor.is_out_of_bound(0, actor.rect.width - 1, 0, 200)[0])
    assert(not actor.is_out_of_bound(0, 200, 0, 200)[0])
    assert(actor.is_alive())
    actor.kill()
    assert(not actor.is_alive())
    actor.make_action()