"""
Main game module.
Controls game's flow and the mechanics.

Pythalex - April 2018
Ludum Dare 41

"""

import os
import pygame

import time
from player import Player

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

    # A list of current obstacles
    obstacles = []

    # default font size
    FONTSIZE = 50

    # clock for FPS fix
    CLOCK = pygame.time.Clock()
    FPS = 60

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

    def create_window(self, width: int, height: int):
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
            self.players.append(Player(self, x_pos, y_pos))

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

    def process_players_inputs(self) -> None:
        """
        Checks players' inputs and call associated methods.
        """
        for player in self.players:
            player.make_action()

    def process_obstacles_movements(self) -> None:
        """
        Makes the obstacles move.
        """
        # TODO: Implement this
        pass

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
        self.window.fill((0, 0, 0))

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
        # TODO: Implement this
        pass

    def game_loop(self) -> None:
        """
        The game loop.
        """

        end = False

        while not end:

            print("{} {}".format(self.players[0].rect, self.players[0].hitboxes[0]))
            print("{} {}".format(self.players[1].rect, self.players[1].hitboxes[0]))
            print("---")

            # Process window events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
            
            # Process players input (moves)
            self.process_players_inputs()

            # Process obstacles movements (falling)
            #self.process_obstacles_movements()

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

            # If only one player remains, he wins
            pid, only_one = self.only_one_alive()
            if only_one:
                print("Bravo player {} !".format(pid))
                end = True

            # If no player still remains, nobody wins
            elif not any(self.still_alive()):
                print("Tout le monde est mort.")
                end = True

            # Draw the background
            self.draw_background()

            # Draw the obstacles
            #self.draw_obstacles()

            # Draw the players
            self.draw_players()

            # Draw foregrounds additionals (if any)
            #self.draw_additionals()

            # Draw everything
            pygame.display.update()

            # Tick
            self.CLOCK.tick(60)
        
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