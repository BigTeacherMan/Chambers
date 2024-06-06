import pygame
import random

from text import Text
from sound_effects import play_mouse_click

from sound_effects import play_revolver_sound_effect

from images import color_palette


class Game:
    def __init__(self, num_players, player_names, chamber_size, game_window):
        self.num_players = num_players
        self.alive_players = player_names.values()
        self.chamber_size = chamber_size
        self.game_window = game_window
        self.current_player = list(self.alive_players)[0]
        self.bullet_chamber = random.randint(1, self.chamber_size)
        self.current_chamber = random.randint(1, self.chamber_size)
        self.dead_players = []

    def start_turn(self):
        next_turn_text = Text(f"It is {self.current_player}'s turn...", 75, color_palette["silver"],
                              640, 540)

        next_turn_text.type(self.game_window)

    def shoot_gun(self):
        self.current_chamber = self.current_chamber + 1
        if self.current_chamber > self.chamber_size:
            self.current_chamber = 1

        if self.current_chamber == self.bullet_chamber:
            print(f"{self.current_player} is dead!")

    def spin_chamber(self):
        self.current_chamber = random.randint(1, self.chamber_size)
        play_revolver_sound_effect("revolver_collection", "revolver_spin_sfx")

    def target_next_player(self):
        next_player = (self.current_player + 1) % self.alive_players
        shoot_player_text = Text(f"{self.current_player} takes aim at {next_player}!", 75,
                                 color_palette["silver"], 640, 540)
        shoot_player_text.type(self.game_window)
        if self.current_chamber == self.bullet_chamber:
            print(f"{next_player} is dead!")

    def play_game_events(self, rect_list):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for rect in rect_list:
                    if rect.collidepoint(mouse_x, mouse_y):
                        play_mouse_click("GUI_Interact", "mouse_click_sfx")
                        if rect == rect_list[0]:
                            self.shoot_gun()
                        if rect == rect_list[1]:
                            self.spin_chamber()
                        if rect == rect_list[2]:
                            self.target_next_player()




