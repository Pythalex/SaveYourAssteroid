"""
Item module.
Abstract item based on an actor.

Pythalex - April 2018
Ludum Dare 41

"""

import os
import time
import pygame
from pygame.surface import Surface
from pygame.rect import Rect
from actor import Actor
from player import Player

class Item(Actor):
    """
    Represents an abstract item
    """

    # The player who activated the item
    activator = None
    # duration in s of the item benefits/malus
    duration = 5 

    # time during which the item is alive
    time_alive = 8
    time_alive_start = 0

    # timer start
    start = 0

    enabled = False

    # If bonus = False, the item is a malus. Used for random spawn
    bonus = True

    def __init__(self, master: "Game", x: int = 0, y: int = 0):

        # hitboxes
        self.orig_hitboxes = [
            Rect(1, 1, 19, 19)
        ]

        self.hitboxes = [
            Rect(1, 1, 19, 19)
        ]

        Actor.__init__(self, master, Surface((100, 100)), x, y)

        self.time_alive_start = time.time()

    def activate(self, activator: Player):
        """
        Activates the item effect.
        """
        self.activator = activator
        self.enabled = True
        self.start = time.time()

    def apply(self, players : "list of Player") -> "list of Player":
        """
        Applies the script if and only if the item is enabled and
        an good activator has been given.
        """
        if self.enabled and not self.times_up():
            return self.script(players)
        else:
            return players

    def script(self, players : "list of Player") -> "list of Player":
        """
        Applies the item's script to the players.
        Must be overriden if you create a real item.
        """
        return players

    def times_up(self) -> bool:
        """
        Indicates if the item's effect duration has been reached.
        """
        return self.enabled and time.time() - self.start >= self.duration

    def move(self, direction: int = 0) -> None:
        """
        The items doesn't move by default.
        """
        return None


class Slower(Item):
    """
    Slows every players except the activator.
    """

    duration = 5

    def __init__(self, master: "Game", x: int, y: int):
        Item.__init__(self, master, x, y)
        self.image = pygame.image.load("resources" + os.path.sep + "items" +\
                              os.path.sep + "slower.png")
        self.set_image(self.image, x, y)

    def script(self, players: "list of Player") -> "list of Player":
        """
        Applies the script.
        """
        for player in players:
            if player != self.activator:
                player.speed = player.speed / 2.0
        return players

class OneLife(Item):
    """
    Give the player one life
    """

    duration = 1
    used = False

    def __init__(self, master: "Game", x: int, y: int):
        Item.__init__(self, master, x, y)
        self.image = pygame.image.load("resources" + os.path.sep + "items" +\
                              os.path.sep + "life.png")
        self.set_image(self.image, x, y)

    def script(self, players: "list of Player") -> "list of Player":
        """
        Applies the script.
        """
        if not self.used:
            for player in players:
                if player == self.activator:
                    player.lifes += 1
                    print(player.lifes)
        self.used = True
        return players

class InvertControl(Item):
    """
    Invert the player's controls
    """

    duration = 5
    bonus = False

    def __init__(self, master: "Game", x: int, y: int):
        Item.__init__(self, master, x, y)
        self.image = pygame.image.load("resources" + os.path.sep + "items" +\
                              os.path.sep + "invert_control.png")
        self.set_image(self.image, x, y)

    def script(self, players: "list of Player") -> "list of Player":
        """
        Applies the script.
        """
        for player in players:
            if player == self.activator:
                old_up = player.controller.key_up
                player.controller.key_up = player.controller.key_down
                player.controller.key_down = old_up
                old_left = player.controller.key_left
                player.controller.key_left = player.controller.key_right
                player.controller.key_right = old_left
        return players

if __name__ == '__main__':

    ### Item class tests ###

    pygame.init()
    pygame.display.set_mode((400, 300))

    actor = Item(None)
    assert not actor.times_up()
    actor.activate(None)
    old_x = actor.rect.x
    actor.move(0)
    actor.move(2)
    assert actor.rect.x == old_x
    assert actor.is_out_of_bound(1, 200, 0, 200)[0]
    assert not actor.is_out_of_bound(0, 200, 0, 200)[0]
    actor.rotate(90)
    actor.rotate(-90)
    assert actor.script([]) == []
    print("sleep for {}".format(actor.duration))
    time.sleep(actor.duration)
    assert actor.times_up()
