"""
Main game module.
Controls game's flow and the mechanics.

Pythalex - April 2018
Ludum Dare 41

"""

import os
import random
import copy
import pygame

import time
from actor import Actor
from player import Player
from bot import Bot
from obstacle import Obstacle
from items import *

class Game(object):
    """
    Represents the game master and is the first class
    to be called.
    """

    # The main window
    window = None
    window_width = 400
    window_height = 400

    # A list of current players
    players = []
    nb_of_players = 0

    # A stack of current obstacles
    MAXIMUM_OBSTACLE = 6
    obstacles = []

    # Items
    items = []
    activated_items = []

    # default font size
    FONTSIZE = 50

    # clock for FPS fix
    CLOCK = pygame.time.Clock()
    FPS = 60

    # background related
    sep = os.path.sep
    background_img = pygame.image.load("resources" + sep + "background.png")
    background = None
    background_scroll = 1 # speed

    def __init__(self, nb_of_players: int = 2):
        """
        Create game. 2 players are default but
        you can choose a bigger number. The number
        of player must be >= 2.
        """
        # Argument check
        if nb_of_players not in range(2, 5):
            print("ERROR: The given number of player must be in [2;4], current" +
                  "is {}".format(nb_of_players))
        else:
            self.nb_of_players = nb_of_players

        self.init_pygame_modules()
        self.create_window(self.window_width, self.window_height)
        self.create_players(nb_of_players)

    def init_pygame_modules(self):
        """
        Initiates pygame modules and check for errors.
        """
        pygame.init()
        # TODO: Check for sound module errors

    def create_window(self, width: int, height: int) -> None:
        """
        Create the main surface of given size.
        """
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ludum Dare 41 - Pythalex")

    def create_players(self, nb_of_players: int) -> None:
        """
        Creates a given number of players.
        """

        # y position never changes
        y_pos = self.window_height / 2
        x_pos = 0

        for i in range(nb_of_players):
            x_pos = (float(i + 1) / float(nb_of_players + 1)) * self.window_width
            if True:
                self.players.append(Player(self, x_pos, y_pos))
            else:
                self.players.append(Bot(self, x_pos, y_pos))

        # commands configuration
        if nb_of_players == 2:
            self.players[0].configure_controller(
                pygame.K_w,
                pygame.K_a,
                pygame.K_s,
                pygame.K_d
            )
            self.players[1].configure_controller(
                pygame.K_UP,
                pygame.K_LEFT,
                pygame.K_DOWN,
                pygame.K_RIGHT
            )
        elif nb_of_players == 3:
            self.players[0].configure_controller(
                pygame.K_w,
                pygame.K_a,
                pygame.K_s,
                pygame.K_d
            )
            self.players[1].configure_controller(
                pygame.K_i,
                pygame.K_j,
                pygame.K_k,
                pygame.K_l
            )
            self.players[2].configure_controller(
                pygame.K_UP,
                pygame.K_LEFT,
                pygame.K_DOWN,
                pygame.K_RIGHT
            )
        else:
            self.players[0].configure_controller(
                pygame.K_w,
                pygame.K_a,
                pygame.K_s,
                pygame.K_d
            )
            self.players[1].configure_controller(
                pygame.K_i,
                pygame.K_j,
                pygame.K_k,
                pygame.K_l
            )
            self.players[2].configure_controller(
                pygame.K_UP,
                pygame.K_LEFT,
                pygame.K_DOWN,
                pygame.K_RIGHT
            )
            self.players[3].configure_controller(
                pygame.K_8,
                pygame.K_4,
                pygame.K_5,
                pygame.K_6
            )

    def maximum_obstacle_spawned(self) -> bool:
        """
        Indicate whether the maximum number of spawned
        obstacles has been reached.
        """
        return len(self.obstacles) == self.MAXIMUM_OBSTACLE

    def create_obstacle(self, avoided: int = 0):
        """
        Makes an obstacle spot randomly.
        """
        if not self.maximum_obstacle_spawned():
            self.obstacles.append(Obstacle(self, random.randrange(0, self.window_width),
                0))
            if avoided > 10: 
                avoided = 10
            self.obstacles[-1].speed += (avoided * Obstacle.speed / 20.0)

    def delete_obstacles_far_away(self) -> int:
        """
        Delete the obstacles which have left the screen. 
        Returns the number of deleted obstacles
        """
        i = 0
        deleted = 0
        for obstacle in self.obstacles:
            if obstacle.rect.y - obstacle.rect.height > self.window_height or\
                obstacle.rect.x + obstacle.rect.width < 0 or\
                obstacle.rect.x > self.window_width:
                del self.obstacles[i]
                deleted += 1
            i += 1
        return deleted

    def process_players_inputs(self) -> None:
        """
        Checks players' inputs and call associated methods.
        """
        for i in range(self.nb_of_players):
            # Make the players move
            player = self.players[i]
            player.make_action()

    def process_activated_items(self) -> None:
        """
        Applies the activated items' effects on the players.
        """
        for i in range(len(self.activated_items)):
            item = self.activated_items[i]
            self.players = item.apply(self.players)
            if item.times_up():
                del self.activated_items[i]

    def process_obstacles_movements(self) -> None:
        """
        Makes the obstacles move downward.
        """
        for obstacle in self.obstacles:
            obstacle.rotate(obstacle.rotating_speed)
            obstacle.move()

    def detect_collisions(self) -> ((bool, bool), ...):
        """
        For each player detects collisions and
        return a boolean list associating for each
        player whether he collided with left right border
        and up down borders.
        """

        collisions = []
        for player in self.players:
            out = player.is_out_of_bound(0, self.window_width - 1, 0,
                                         self.window_height - 1)
            if not out[0]:
                for obstacle in self.obstacles:
                    if obstacle.detect_collision(player):
                        out = (True, True)
            collisions.append(out)
        return collisions

    def still_alive(self) -> (bool, ...):
        """
        Returns a list associating for each player his
        live state. i.e. (True, False) means player 1 is alive
        and player 2 is dead.
        """
        lives = []
        for player in self.players:
            lives.append(player.is_alive())
        return lives

    def number_still_alive(self) -> int:
        """
        Returns the number of players who are still alive.
        """
        alives = 0
        for player in self.players:
            if player.is_alive():
                alives += 1
        return alives

    def only_one_alive(self) -> (int, bool):
        """
        Indicates whether there is only one player alive.
        """
        alives_id = []
        alives = 0
        for player in self.players:
            if alives > 1:
                return (-1, False)
            if player.is_alive():
                alives_id.append(player)
                alives += 1
        return (alives_id[0], True if alives == 1 else False)

    def draw_background(self) -> None:
        """
        Displays the background
        """
        self.background.draw(self.window)

    def draw_players(self) -> None:
        """
        Draws the players.
        """
        for player in self.players:
            player.draw(self.window)

    def draw_obstacles(self) -> None:
        """
        Draws the obstacles.
        """
        for obstacle in self.obstacles:
            obstacle.draw(self.window)

    def draw_items(self) -> None:
        """
        Draws the unactivated items.
        """
        for item in self.items:
            item.draw(self.window)

    def make_players_backup(self) -> None:
        """
        Saves the players variables that are
        affected by items for restore.
        """
        for player in self.players:
            player.old_speed = player.speed

    def restore_players_backup(self) -> None:
        """
        Restores the players variables that are affected
        by items.
        """
        for player in self.players:
            player.speed = player.old_speed

    def update(self, avoided: int) -> (bool, int):
        """
        Process inputs, detect collisions and move obstacles.
        """

        end = False
        
        self.make_players_backup()

        # Process window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

        # Process activated items effects
        self.process_activated_items()

        # Process players input (moves)
        self.process_players_inputs()

        # Process obstacles movements (falling)
        self.process_obstacles_movements()

        # Process collisions (car crashes)
        collided = self.detect_collisions()

        # If one of the player collided with an obstacle or a border
        for p_idx in range(self.nb_of_players):
            player = self.players[p_idx]

            # obstacle or left/right border -> kill
            if collided[p_idx][0]:
                player.kill()

            # Up down border, just keep the player in the screen
            elif collided[p_idx][1]:
                player.rect.clamp_ip(self.window.get_rect())

            # For each other players, test collisions
            for p_idx2 in range(self.nb_of_players):
                if p_idx != p_idx2:
                    # collide with player 2
                    player2 = self.players[p_idx2]
                    if player.detect_collision(player2):
                        player.cancel_action()
            
            # items collisions
            for i in range(len(self.items)):
                item = self.items[i]
                # Activate the item
                if player.detect_collision(item):
                    self.activated_items.append(item)
                    item.activate(player)
                    del self.items[i]

        # Cancel item effects
        self.restore_players_backup()

        # If only one player remains, he wins
        pid, only_one = self.only_one_alive()
        if only_one:
            print("Bravo player {} !".format(pid))
            end = True

        # If no player still remains, nobody wins
        elif not any(self.still_alive()):
            print("Tout le monde est mort.")
            end = True

        # Spawns with increasing frequence over time
        if random.randrange(0, (30 - avoided) if (avoided < 20) else 10) == 0:
            self.create_obstacle(avoided)

        # delete the obstacles which have left the screen
        avoided += self.delete_obstacles_far_away()

        # Scroll background
        self.background.rect.y += self.background_scroll
        if self.background.rect.y >= 0:
            self.background.rect.bottomleft = (0, self.window_height - 1)

        return (end, avoided)

    def draw(self) -> None:
        """
        Draw everything.
        """
        self.draw_background()
        self.draw_players()
        self.draw_obstacles()
        self.draw_items()
        pygame.display.update()

    def game_loop(self) -> None:
        """
        The game loop.
        """

        end = False
        avoided = 0
        self.background = Actor(self, self.background_img, 0, self.window_height - 1)
        self.items.append(Slower(self, x=self.window_width / 2,
                                 y=self.window_height / 2))

        while not end:

            # Process inputs, detect collisions and spawn things
            end, avoided = self.update(avoided)

            # Draw everything
            self.draw()

            # Tick
            self.CLOCK.tick(self.FPS) # 60 FPS
   
        # Display end board (if any)

    def run_game(self) -> None:
        """
        Runs the game ...
        """
        self.game_loop()
        pygame.quit()

# Runs the game
if __name__ == '__main__':

    game = Game(2)
    game.run_game()