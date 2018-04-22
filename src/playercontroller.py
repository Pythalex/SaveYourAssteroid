"""
Actor module.
Abstract actor based on pygame Sprite.

Pythalex - April 2018
Ludum Dare 41

"""

import pygame

class Player_Controller(object):
    """
    Allows a human player to control the character
    in the game.
    """

    # The player master
    master = None

    key_up = -1
    key_left = -1
    key_down = -1
    key_right = -1

    # back up for item effects
    old_key_up = -1
    old_key_down = -1
    old_key_right = -1
    old_key_left = -1

    def __init__(self, player_master):
        self.master = player_master

    def make_action(self):
        """
        Checks for player inputs and returns them
        """
        keys = pygame.key.get_pressed()

        if keys[self.key_up]:
            self.master.move(1)
        if keys[self.key_left]:
            self.master.move(2)
        if keys[self.key_down]:
            self.master.move(3)
        if keys[self.key_right]:
            self.master.move(0)

if __name__ == '__main__':

    pygame.init()
    pygame.display.set_mode((400, 300))

    from player import Player
    player = Player(None, 50, 50)
    player.configure_controller(pygame.K_UP, pygame.K_LEFT, 
        pygame.K_DOWN, pygame.K_RIGHT)
    
    player.make_action()
