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

    # original collision boxes
    # They are used for hitbox update when moving
    #orig_hitboxes = None
    #hitboxes = None

    pid = 0
    speed = 5
    # When lifes reaches 0, player dies
    lifes = 2

    # Player is alive
    alive = True

    # The controller
    controller = None
    configured_controller = False

    # path related
    sep = os.path.sep

    # old move action
    old_action = -1

    # backups
    old_speed = speed

    score = 0

    def __init__(self, master, x: int = 0, y: int = 0):

        # Create actor
        
        self.pid = len(master.players) % MAX_COLORS + 1
        self.sprite_idle = pygame.image.load("resources" + os.path.sep +\
         "player_{}_idle.png".format(self.pid))
        self.sprite_left = pygame.image.load("resources" + os.path.sep +\
         "player_{}_left.png".format(self.pid))
        self.sprite_right = pygame.image.load("resources" + os.path.sep +\
         "player_{}_right.png".format(self.pid))

        Actor.__init__(self, master, self.sprite_idle, x, y)

        # Choose sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # original collision boxes
        # They are used for hitbox update when moving
        self.orig_hitboxes = [
            Rect(17, 30, 6, 4), # check front collision first
            Rect(15, 23, 9, 7),
            Rect(11, 15, 18, 8),
            Rect(7, 7, 26, 8),
            Rect(3, 0, 34, 7)
        ]

        self.hitboxes = [
            Rect(17, 30, 6, 4),
            Rect(15, 23, 9, 7),
            Rect(11, 15, 18, 8),
            Rect(7, 7, 26, 8),
            Rect(3, 0, 34, 7)
        ]

        self.update_hitboxes()

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
        self.controller.old_key_up = self.controller.key_up
        self.controller.old_key_down = self.controller.key_down
        self.controller.old_key_left = self.controller.key_left
        self.controller.old_key_right = self.controller.key_right
        self.configured_controller = True

    def draw(self, window):
        """
        Draws the player
        """
        Actor.draw(self, window)
        self.image = self.sprite_idle

    def move(self, direction: int) -> None:
        """
        Anticlockwise directions.
        """

        if direction == 0:
            self.image = self.sprite_right
        elif direction == 2:
            self.image = self.sprite_left
            
        Actor.move(self, direction)
        self.old_action = direction

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

    def hurt(self):
        """
        Hurts the player (not the real one).
        """
        self.lifes -= 1
        if self.lifes <= 0:
            self.kill()

    def kill(self):
        """
        Kills the player.
        Give the player a score.
        """
        self.alive = False
        self.can_collide = False
        self.speed = 1
        self.score = int(self.game_master.avoided)

    def cancel_action(self):
        if self.old_action == 0:
            self.move(2)
        elif self.old_action == 1:
            self.move(3)
        elif self.old_action == 2:
            self.move(0)
        elif self.old_action == 3:
            self.move(1)

    def copy(self):
        """
        Make a copy of the player
        """
        copy = Player(self.game_master, self.rect.x, self.rect.y)
        copy.alive = self.alive
        copy.controller = self.controller
        copy.configured_controller = self.configured_controller
        copy.old_action = self.old_action
        return copy

if __name__ == '__main__':

    pygame.init()
    pygame.display.set_mode((400, 300))

    class Game():
        players = [1]

    actor = Player(Game())
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