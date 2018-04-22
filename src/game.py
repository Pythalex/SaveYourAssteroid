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
    MAXIMUM_OBSTACLE = 10
    # min time laps between two spawn
    obstacles_spawn_laps = 0.1
    # time of last spawn
    obstacles_last_spawn = -1
    obstacles_spawn_rate = 2
    obstacles_max_spawn_rate = 5
    obstacles = []

    # Items
    item_spawn_rate = 0.1
    # Minimum timelaps between two item spawns
    item_spawn_laps = 3
    # time of last item spawn
    item_last_spawn = -1
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
                -Obstacle.img.get_rect().height))
            if avoided > 10: 
                avoided = 10
            self.obstacles[-1].speed += (avoided * Obstacle.speed / 20.0)
            # start timelaps
            self.obstacles_last_spawn = time.time()

    def random_spawn_item(self) -> None:
        """
        Randomly spawns a item on the screen with more
        chance to spawn at the top than at the bottom, in order
        to encourage players to take chances.
        """
        # screen is cut into 4 parts
        # part 0 is the top part, it has 50% of spawn
        # part 1 is below, has 25% of spawn
        # part 2 has 20% of spawn
        # else it's spawn in part 3 (5%)

        rand = random.randint(0, 100)
        x_pos = random.randrange(0, self.window_width - Obstacle.img.get_rect().width)
        y_pos = random.randint(0, 5) / 4.0

        part0 = 50
        part1 = 25
        part2 = 5
        part_height = self.window_height / 4.0

        if rand >= part0:
            y_pos = (y_pos * part_height)
        elif rand >= part1:
            y_pos = (y_pos * part_height) + part_height
        elif rand >= part2:
            y_pos = (y_pos * part_height) + 2 * part_height
        else:
            y_pos = (y_pos * part_height) + 3 * part_height

        # start timelaps
        self.item_last_spawn = time.time()

        #TODO: make the item type vary when there will be more of them
        self.items.append(Slower(self, x_pos, y_pos))

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

            if player.is_alive():
                player.make_action()
            else:
                player.move(3)

    def process_activated_items(self) -> None:
        """
        Applies the activated items' effects on the players.
        """
        i = 0
        while i < len(self.activated_items):
            item = self.activated_items[i]
            self.players = item.apply(self.players)
            if item.times_up():
                del self.activated_items[i]
                i -= 1
            i += 1

    def process_obstacles_movements(self) -> None:
        """
        Makes the obstacles move downward.
        """
        for obstacle in self.obstacles:
            obstacle.rotate(obstacle.rotating_speed)
            obstacle.move()

    def player_leave_border(self, player) -> (bool, bool):
        """
        Indicates whether the player leaves the borders.
        The first boolean means the player leaves the right/left
        border, the second one means the player leaves the up/down
        border.
        """
        return player.is_out_of_bound(- player.rect.width / 2, 
            self.window_width + player.rect.width / 2, 
            0, self.window_height - 1)

    def detect_collisions_with_players(self, player) -> bool:
        """
        Indicates whether the player collides with another player.
        """
        for player2 in self.players:
            if player != player2:
                if player.detect_collision(player2):
                    return True
        return False

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

        # If one of the player collided with an obstacle or a border
        for p_idx in range(self.nb_of_players):
            player = self.players[p_idx]

            # check if the player leave the borders
            player_leave = self.player_leave_border(player)
            # left / right borders
            if player_leave[0]: 
                player.kill()
            elif player_leave[1]:
                if player.is_alive():
                    player.rect.clamp_ip(self.window.get_rect())

            # If the player collides with another one, cancel last action
            # NOTE : this feature is broken because we don't check the responsible
            # of the collision, hence, one player will "vibrate" when other players
            # collide with him, because the order of detection is always the same.
            if self.detect_collisions_with_players(player):
                player.cancel_action()
            
            # If a player collides with an item, activate it
            i = 0
            while i < len(self.items):
                item = self.items[i]
                if player.detect_collision(item):
                    self.activated_items.append(item)
                    item.activate(player)
                    del self.items[i]
                    i -= 1
                i += 1

            # If the player collides with an asteroid, he loses a life and the asteroid
            # is broken into pieces
            for obstacle in self.obstacles:
                if player.detect_collision(obstacle):
                    obstacle.destroy()
                    player.kill()

        # Cancel item effects
        self.restore_players_backup()

        # If only one player remains, he wins
        # pid, only_one = self.only_one_alive()
        # if only_one:
            # print("Bravo player {} !".format(pid))
            # end = True

        # If no player still remains, nobody wins
        #if not any(self.still_alive()):
            #print("Tout le monde est mort.")
            #end = True

        # Spawns with increasing frequence over time
        if time.time() - self.obstacles_last_spawn >= self.obstacles_spawn_laps:
            if random.randrange(0, int(self.FPS / self.obstacles_spawn_rate)) == 0:
                self.create_obstacle(avoided)
        # increase obstacle spawn rate
        self.obstacles_spawn_rate += (avoided / 20.0 * self.obstacles_spawn_rate)
        if self.obstacles_spawn_rate > self.obstacles_max_spawn_rate:
            self.obstacles_spawn_rate = self.obstacles_max_spawn_rate

        # Spawn an item
        if time.time() - self.item_last_spawn >= self.item_spawn_laps:
            if random.randrange(0, (self.FPS / self.item_spawn_rate)) == 0:
                self.random_spawn_item()

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
        self.draw_items()
        self.draw_obstacles()

        pygame.display.update()

    def game_loop(self) -> None:
        """
        The game loop.
        """

        end = False
        avoided = 0
        self.background = Actor(self, self.background_img, 0, self.window_height - 1)

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