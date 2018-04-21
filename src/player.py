"""
Player module.
Represents a player, real or bot.

Pythalex - April 2018
Ludum Dare 41

"""

import os
import pygame
from pygame.surface import Surface
from pygame.rect import Rect

from actor import Actor
from playercontroller import Player_Controller

PLAYER_COUNT = 0
MAX_COLORS = 4

class Player(Actor):
    """
    Represents a player.
    """

    # collision boxes
    hitboxes = [
        Rect(17, 30, 6, 4), # check front collision first
        Rect(15, 23, 9, 7),
        Rect(11, 15, 18, 8),
        Rect(7, 7, 26, 8),
        Rect(3, 0, 34, 7)
    ]

    # Player is alive
    alive = True

    # The controller
    controller = None
    configured_controller = False

    # path related
    sep = os.path.sep

    def __init__(self, master, x: int = 0, y: int = 0):

        # Used for color affectation
        global PLAYER_COUNT

        # Create actor
        Actor.__init__(self, master, Surface((0, 0)), x, y)

        # Choose sprite
        self.img = pygame.image.load("resources" + self.sep + "player_{}.png".format(
            PLAYER_COUNT % MAX_COLORS + 1))
        self.rect = self.img.get_rect()

        # Next time, another color is used
        PLAYER_COUNT += 1

        # player controller
        self.controller = Player_Controller(self)

    def configure_controller(self, key_up: int, key_left: int, 
                             key_down: int, key_right: int) -> None:
        """
        Configure the controller by giving the movements keys' ID
        """
        self.controller.key_up = key_up
        self.controller.key_left = key_left
        self.controller.key_down = key_down
        self.controller.key_right = key_right
        self.configured_controller = True

    def make_action(self):
        """
        Let the player make an action.
        """
        if not self.configured_controller:
            print("Controller not configured for player.")
        else:
            self.controller.make_action()

    def is_alive(self):
        """
        Indicates whether the player is alive
        """
        return self.alive

    def kill(self):
        """
        Kills the player
        """
        self.alive = False

    def draw(self, window):
        """
        Draw the player on the given surface window
        """
        window.blit(self.img, (self.rect.x, self.rect.y))
