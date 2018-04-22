"""
Main game module.
Controls game's flow and the mechanics.

Pythalex - April 2018
Ludum Dare 41

"""

import sys
import os
import random
import time

import pygame
import pygame.gfxdraw

from actor import Actor
from player import Player
from bot import Bot
from obstacle import Obstacle
from items import Slower, OneLife, InvertControl
from pygame.font import Font, SysFont
from pygame.rect import Rect

class Game(object):
    """
    Represents the game master and is the first class
    to be called.
    """

    """ ATTRIBUTES """

    # The main window
    window = None
    window_width = 400
    window_height = 400

    # A list of current players
    players = []
    nb_of_players = 2

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

    # clock for FPS fix
    CLOCK = pygame.time.Clock()
    FPS = 60

    # background related
    sep = os.path.sep
    background_img = pygame.image.load("resources" + sep + "background.png")
    background = None
    background_scroll = 1 # speed

    # Font HUD
    hud_font = "System Bold"
    # default font size
    FONTSIZE = 30
    WHITE = (255, 255, 255)

    # score
    avoided = 0

    # time before displaying end board
    endlaps = 3
    end_time = 0

    """ CREATION / INIT METHODS """

    def __init__(self):
        """
        Create game. 2 players are default but
        you can choose a bigger number. The number
        of player must be >= 2.
        """

        self.init_pygame_modules()
        self.create_window(self.window_width, self.window_height)
        self.create_players(2)

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

        # destroy previous players
        self.players = []

        # y position never changes
        y_pos = self.window_height / 2
        x_pos = 0

        for i in range(nb_of_players):
            x_pos = (float(i + 1) / float(nb_of_players + 1)) * self.window_width
            self.players.append(Player(self, x_pos, y_pos))

        # commands configuration
        if nb_of_players == 1:
            self.players[0].configure_controller(
                pygame.K_UP,
                pygame.K_LEFT,
                pygame.K_DOWN,
                pygame.K_RIGHT
            )
        elif nb_of_players == 2:
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
                pygame.K_KP8,
                pygame.K_KP4,
                pygame.K_KP5,
                pygame.K_KP6
            )

    """ SPAWN AND DESTROY METHODS """

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
        y_pos = random.randint(0, 4) / 4.0

        # choose item to be spawn
        item_classes = [Slower, OneLife, InvertControl]
        if self.nb_of_players > 1:
            rand_class = random.randint(0, 2)
        else:
            rand_class = random.randint(1, 2)
        
        part0 = 50
        part1 = 25
        part2 = 5
        part_height = self.window_height / 4.0

        # If the item is a malus, parts chances are reversed
        if not item_classes[rand_class].bonus:
            part0 = 95
            part1 = 75
            part2 = 50

        if rand >= part0:
            y_pos = (y_pos * part_height)
        elif rand >= part1:
            y_pos = (y_pos * part_height) + part_height
        elif rand >= part2:
            y_pos = (y_pos * part_height) + 2 * part_height
        else:
            y_pos = (y_pos * part_height) + 3 * part_height

        print(part0)

        # start timelaps
        self.item_last_spawn = time.time()
        
        self.items.append(item_classes[rand_class](self, x_pos, y_pos))
        
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

    """ MOVEMENTS UPDATE METHODS """

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

    def process_item_timeouts(self) -> None:
        """
        Destroy items if their live duration is reached.
        """
        destroyed = True
        while destroyed:
            destroyed = False
            for i in range(len(self.items)):
                item = self.items[i]
                if time.time() - item.time_alive_start >= item.time_alive:
                    del self.items[i]
                    destroyed = True
                    break

    """ COLLISION DETECTIONS """

    def player_leave_border(self, player) -> (bool, bool):
        """
        Indicates whether the player leaves the borders.
        The first boolean means the player leaves the right/left
        border, the second one means the player leaves the up/down
        border.
        """
        if player.is_alive():
            return player.is_out_of_bound(- player.rect.width / 2, 
            self.window_width + player.rect.width / 2, 
            0, self.window_height - 1)
        else:
            return (False, False)

    def detect_collisions_with_players(self, player) -> bool:
        """
        Indicates whether the player collides with another player.
        """
        for player2 in self.players:
            if player != player2:
                if player.detect_collision(player2):
                    return True
        return False

    """ PLAYERS INFO """

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

    def sort_players(self) -> None:
        """
        Sorts the players by score comparison.
        """
        final = []
        while len(final) < self.nb_of_players:
            max = -1
            id = -1
            i = 0
            for player in self.players:
                if player.score > max:
                    max = player.score
                    id = i
                i += 1
            final.append(self.players[id])
            del self.players[id]
        self.players = final

    """ DRAW METHODS """

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

    """ ITEM EFFECTS BACK UPS """

    def restore_players_backup(self) -> None:
        """
        Restores the players variables that are affected
        by items.
        """
        for player in self.players:
            player.speed = player.old_speed
            player.controller.key_up = player.controller.old_key_up
            player.controller.key_down = player.controller.old_key_down
            player.controller.key_left = player.controller.old_key_left
            player.controller.key_right = player.controller.old_key_right

    """ GAME LOOP """

    def update(self) -> bool:
        """
        Process inputs, detect collisions and move obstacles.
        Returns whether the game is ended
        """

        end = False

        # Process window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

        # Process activated items effects
        self.process_activated_items()

        # destroy items if timeout
        self.process_item_timeouts()

        # Process players input (moves)
        self.process_players_inputs()

        # Process obstacles movements (falling)
        self.process_obstacles_movements()

        # If one of the player collided with an obstacle or a border
        for p_idx in range(self.nb_of_players):
            player = self.players[p_idx]

            # check if the player leave the borders
            player_leave = self.player_leave_border(player)
            # left / right borders -> kill
            if player_leave[0]: 
                player.kill()
            # up / down borders -> just bring them back
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
                    player.hurt()

        # Cancel item effects
        self.restore_players_backup()

        # If no player still remains, end
        if not any(self.still_alive()):
            end = True

        # Spawns with increasing frequence over time
        if time.time() - self.obstacles_last_spawn >= self.obstacles_spawn_laps:
            if random.randrange(0, int(self.FPS / self.obstacles_spawn_rate)) == 0:
                self.create_obstacle(self.avoided)
        # increase obstacle spawn rate
        self.obstacles_spawn_rate += (self.avoided / 20.0 * self.obstacles_spawn_rate)
        if self.obstacles_spawn_rate > self.obstacles_max_spawn_rate:
            self.obstacles_spawn_rate = self.obstacles_max_spawn_rate

        # Spawn an item
        if time.time() - self.item_last_spawn >= self.item_spawn_laps:
            if random.randrange(0, (self.FPS / self.item_spawn_rate)) == 0:
                self.random_spawn_item()

        # delete the obstacles which have left the screen
        self.avoided += self.delete_obstacles_far_away()

        # Scroll background
        self.background.rect.y += self.background_scroll
        if self.background.rect.y >= 0:
            self.background.rect.bottomleft = (0, self.window_height - 1)

        return end

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
        self.background = Actor(self, self.background_img, 0, self.window_height - 1)

        while not end:

            # Process inputs, detect collisions and spawn things
            game_end = self.update()

            if game_end and self.end_time == 0:
                self.end_time = time.time()

            if game_end and time.time() - self.end_time >= self.endlaps:
                end = True

            # Draw everything
            self.draw()

            # Tick
            self.CLOCK.tick(self.FPS) # 60 FPS

    """ HUD """

    def message(self, message: str, x_pos: int, y_pos: int, fontsize: int = None,
            color=WHITE) -> None:
        """
        Display a message for the next frame
        """
        font = pygame.font.SysFont(self.hud_font, 
            self.FONTSIZE if fontsize is None else fontsize)

        text = font.render(message, True, color)

        self.window.blit(text, (x_pos, y_pos))

    def title_screen(self) -> None:
        """
        Display the title screen and wait for input.
        """
        end = False

        while not end:

            self.window.fill((0, 0, 0))
            self.message("Game title", 120, 150, 50)
            self.message("Press a key", 150, 200)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    end = True

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

    def ask_number_of_player(self) -> int:
        """
        Ask the player the number of players to
        play with. Returns this number
        """
        number = 1
        n_min = 1
        n_max = 4
        grey = (70, 70, 70)

        end = False
        while not end:
            self.window.fill((0, 0, 0))
            self.message("Choose the number of players", 50, 100, 30)

            x_center = self.window_width / 2 - 20
            y_center = self.window_height / 2 - 20

            x_delta = 15
            y_delta = 5

            tri_width = 50
            tri_height = 30
            y_padding = 30

            up_triangle = ((x_center - x_delta, y_center - y_delta), 
                (x_center - x_delta + tri_width, y_center - y_delta), 
                (x_center - x_delta + tri_width / 2, y_center - y_delta - tri_height))

            down_triangle = ((x_center - x_delta, y_center + y_delta + y_padding), 
                (x_center - x_delta + tri_width, y_center + y_delta + y_padding), 
                (x_center - x_delta + tri_width / 2, 
                    y_center + y_delta + tri_height + y_padding))

            up_color = self.WHITE if number < n_max else grey
            down_color = self.WHITE if number > n_min else grey

            pygame.draw.polygon(self.window, up_color, up_triangle)
            pygame.gfxdraw.aapolygon(self.window, up_triangle, up_color)

            self.message("{}".format(number), x_center, y_center, 50)

            pygame.draw.polygon(self.window, down_color, down_triangle)
            pygame.gfxdraw.aapolygon(self.window, down_triangle, down_color)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if number < n_max:
                            number += 1
                    elif event.key == pygame.K_DOWN:
                        if number > n_min:
                            number -= 1
                    if event.key == pygame.K_RETURN:
                        end = True
            
            pygame.display.update()
            self.CLOCK.tick(self.FPS)

        return number
                
    def explain_commands(self) -> None:
        """
        Display commands for each player
        """

        end = False
        while not end:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        end = True

            self.window.fill((0, 0, 0))

            x_base = 3.0/5.0 * self.window_width
            y_base = lambda i : i * 80 + 50 
            key_width = 50
            key_height = 25
            padding = 5
            id_padding = 5
            id_size = 25
            
            for i in range(self.nb_of_players):

                y = y_base(i)

                player = self.players[i]
                self.message("Player {}".format(i + 1), 50, y + 15, 25)
                self.window.blit(player.image, (120, y))

                y += 10

                # key up
                pygame.draw.rect(self.window, self.WHITE,
                                 Rect(x_base, y - key_height - padding, key_width, key_height),
                                 1)

                self.message(pygame.key.name(player.controller.key_up), x_base + id_padding,
                             y - key_height + id_padding - padding, id_size)

                # key down
                pygame.draw.rect(self.window, self.WHITE,
                                 Rect(x_base, y, key_width, key_height), 1)

                self.message(pygame.key.name(player.controller.key_down), x_base + id_padding,
                             y + id_padding, id_size)

                # key left
                pygame.draw.rect(self.window, self.WHITE,
                                 Rect(x_base - key_width - padding, y, key_width, key_height),
                                 1)

                self.message(pygame.key.name(player.controller.key_left), x_base - key_width +\
                             id_padding, y + id_padding, id_size)

                # key right
                pygame.draw.rect(self.window, self.WHITE,
                                 Rect(x_base + key_width + padding, y, key_width, key_height),
                                 1)

                self.message(pygame.key.name(player.controller.key_right), x_base + key_width +\
                             id_padding + padding, y + id_padding, id_size)

            pygame.display.update()
            self.CLOCK.tick(self.FPS)
    
    def end_board(self) -> None:
        """
        Displays the scores
        """
        end = False
        while not end:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        end = True

            self.window.fill((0, 0, 0))

            x_base = 3.0/5.0 * self.window_width
            y_base = lambda i : i * 80 + 50
            padding = 10

            self.message("Score", x_base, y_base(0) - 30)

            for i in range(self.nb_of_players):

                y = y_base(i)

                player = self.players[i]
                self.message("Player {}".format(player.pid), 45, y + 15, 25)
                self.window.blit(player.image, (130, y))

                self.message("{}".format(player.score), x_base, y + padding)

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

    """ MAIN """

    def run_game(self) -> None:
        """
        Runs the game ...
        """
        # preparing
        self.title_screen()

        while True:

            # reinit variables
            self.obstacles = []
            self.items = []
            self.nb_of_players = self.ask_number_of_player()
            self.create_players(self.nb_of_players)
            self.explain_commands()

            # main game loop
            self.game_loop()

            # sort player list by score for final end board
            self.sort_players()
            self.end_board()

# Runs the game
if __name__ == '__main__':

    game = Game()
    game.run_game()