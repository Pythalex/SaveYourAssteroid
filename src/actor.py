"""
Actor module.
Abstract actor based on pygame Sprite.

Pythalex - April 2018
Ludum Dare 41

"""

import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect

class Actor(Sprite):
    """
    Represents an abstract actor
    """

    # the master instance
    game_master = None

    # The original hitbox
    orig_hitboxes = []
    # Theses hitboxes get their (x, y) updated to follow the sprite
    hitboxes = []

    # Actor movement speed
    speed = 6

    # The actor's sprite current rotation
    rotation = 0

    # Activate the collisions
    can_collide = True

    def __init__(self, master : "Game", img: Surface, x: int = 0, y: int = 0):
        Sprite.__init__(self)

        self.game_master = master
        self.set_image(img, x, y)

        # actor collision boxes
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

        if actor.can_collide and self.can_collide:
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
        window.blit(self.image, self.rect.topleft)

    def rotate(self, angle):
        """
        rotate an image while keeping its center and size
        """
        self.rotation += angle
        orig_rect = self.rect.copy()
        rot_image = self.orig_image.copy()
        rot_image = pygame.transform.rotate(rot_image, self.rotation)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        rot_rect.bottomleft = orig_rect.bottomleft
        self.image = rot_image
        self.rect = rot_rect

    def set_image(self, image: Surface, x_pos: int = 0, y_pos: int = 0):
        """
        Set the given image as actor sprite. A position (x, y) can
        be given to change the image rect origin.
        """
        self.orig_image = image.convert_alpha()
        self.image = self.orig_image.copy()
        self.rect = image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def copy(self):
        """
        Make a copy of the actor
        """
        copy = Actor(self.game_master, self.image, self.rect.x, self.rect.y)
        return copy


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
    actor.rotate(90)
    actor.rotate(-90)