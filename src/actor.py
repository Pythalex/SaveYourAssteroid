"""
Actor module.
Abstract actor based on pygame Sprite.

Pythalex - April 2018
Ludum Dare 41

"""

import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface

class Actor(Sprite):
    """
    Represents an abstract actor
    """

    game_master = None

    # Actor movement speed
    speed = 10

    def __init__(self, master, img: Surface, x: int = 0, y: int = 0):
        Sprite.__init__(self)

        self.game_master = master
        self.image = img.convert_alpha()
        self.rect = img.get_rect(bottomleft=(x, y))

        # actor collision boxes
        self.orig_hitboxes = []
        self.hitboxes = []
        self.update_hitboxes()

    def move(self, direction: int) -> None:
        """
        Anticlockwise directions.
        """

        # east
        if direction == 0:
            self.rect.move_ip(self.speed, 0)
        # north
        elif direction == 1:
            self.rect.move_ip(0, -self.speed)
        # west
        elif direction == 2:
            self.rect.move_ip(-self.speed, 0)
        # south
        elif direction == 3:
            self.rect.move_ip(0, self.speed)

        self.update_hitboxes()

    def update_hitboxes(self) -> None:
        """
        Set the hitboxes x,y at the position of the player
        """
        for rect in range(len(self.hitboxes)):
            self.hitboxes[rect].x = self.orig_hitboxes[rect].x +\
                self.rect.x
            self.hitboxes[rect].y = self.orig_hitboxes[rect].y +\
                self.rect.y

    def detect_collision(self, actor) -> bool:
        """
        Detect collision with another actor
        """
        # For each sub hitbox of self, test if it collides
        # with the whole hitbox of the given actor
        for hitbox in self.hitboxes:
            # If a intersection is found
            if hitbox.collidelist(actor.hitboxes) != -1:
                    return True
        return False

    def is_out_of_bound(self, x_bound_inf: int, x_bound_sup: int,
                        y_bound_inf: int, y_bound_sup: int) -> (bool, bool):
        """
        Indicates whether the actor leaves the given bound.
        The bound are inclusives.
        """

        x_out = (self.rect.x < x_bound_inf) or\
            (self.rect.x + self.rect.width > x_bound_sup)
        y_out = (self.rect.y < y_bound_inf) or\
            (self.rect.y + self.rect.height > y_bound_sup)
        return (x_out, y_out)

    def draw(self, window):
        """
        Draw the player on the given surface window
        """
        window.blit(self.image, (self.rect.x, self.rect.y))

if __name__ == '__main__':

    pygame.init()
    pygame.display.set_mode((400, 300))

    surf = pygame.surface.Surface((100, 100))
    actor = Actor(None, surf)
    old_x = actor.rect.x
    actor.move(0)
    actor.move(2)
    assert(actor.rect.x == old_x)
    assert(actor.is_out_of_bound(1, 200, 0, 200)[0])
    assert(actor.is_out_of_bound(0, 50, 0, 200)[0])
    assert(not actor.is_out_of_bound(0, 200, 0, 200)[0])