import pygame
import random

pygame.mixer.init()

# The different channels that will be dedicated to playing specific sound effects
sound_channels = {
    "music_channel": pygame.mixer.Channel(0),
    "gui_sfx_channel": pygame.mixer.Channel(1),
    "game_sfx_channel": pygame.mixer.Channel(2),
}

slider_images = {
    "settings_bar": "images/settings_bar.png",
    "slider_knob": "images/slider_knob.png",
}

# Nested Dictionary to store all sound effects in unique categories:
# 1. gun sounds
# 2. blood splatters
# 3. GUI interaction
sound_effects = {
    "revolver_collection": {
        "revolver_spin_sfx": pygame.mixer.Sound("sfx/revolver-spin.wav"),
        "revolver_reload_sfx": pygame.mixer.Sound("sfx/revolver-reload.wav"),
        "revolver_fire_empty_sfx": pygame.mixer.Sound("sfx/revolver-fire-empty.wav"),
        "revolver_fire_loaded_sfx": pygame.mixer.Sound("sfx/revolver-fire-loaded.wav"),
    },
    "blood_splatter_collection": {
        "blood_splatter_sfx": pygame.mixer.Sound("sfx/blood-splatter.wav"),
        "blood_splatter2_sfx": pygame.mixer.Sound("sfx/blood-splatter2.wav"),
        "blood_splatter3_sfx": pygame.mixer.Sound("sfx/blood-splatter3.wav"),
        "blood_splatter4_sfx": pygame.mixer.Sound("sfx/blood-splatter4.wav"),
        "blood_splatter5_sfx": pygame.mixer.Sound("sfx/blood-splatter5.wav"),
        "blood_splatter6_sfx": pygame.mixer.Sound("sfx/blood-splatter6.wav"),
        "blood_splatter7_sfx": pygame.mixer.Sound("sfx/blood-splatter7.wav"),
    },
    "GUI_Interact": {
        "mouse_hover_sfx": pygame.mixer.Sound("sfx/mouse-hover.wav"),
        "mouse_click_sfx": pygame.mixer.Sound("sfx/mouse-click.wav"),
        "typing_sound_sfx": pygame.mixer.Sound("sfx/typing-sound.wav"),
    }
}


def play_revolver_sound_effect(collection, sound_effect):
    sound_effect_to_play = sound_effects.get(collection, {}).get(sound_effect)
    if sound_effect_to_play:
        sound_channels["game_sfx_channel"].queue(sound_effect)


def play_blood_splatter_sound_effect():
    random_sound_effect = random.choice(list(sound_effects["blood_splatter_collection"].keys()))
    sound_effect = sound_effects["blood_splatter_collection"][random_sound_effect]
    if sound_effect:
        sound_channels["game_sfx_channel"].play(sound_effect)


def play_mouse_click(collection, sound_effect):
    sound_effect_to_play = sound_effects.get(collection, {}).get(sound_effect)
    sound_effect_to_play.set_volume(0.2)
    if sound_effect_to_play:
        sound_channels["gui_sfx_channel"].play(sound_effect_to_play)


def play_mouse_hover(collection, sound_effect):
    sound_effect_to_play = sound_effects.get(collection, {}).get(sound_effect)
    sound_effect_to_play.set_volume(0.15)
    if sound_effect_to_play:
        sound_channels["gui_sfx_channel"].play(sound_effect_to_play)


class SettingSlider:
    def __init__(self, x, y, default_value=0.5):
        self.x = x
        self.y = y
        self.value = default_value
        self.dragging = False

        # Load slider images
        self.slider_bar_image = pygame.image.load(slider_images["settings_bar"]).convert_alpha()
        self.slider_knob_image = pygame.image.load(slider_images["slider_knob"]).convert_alpha()
        self.slider_knob_width = self.slider_knob_image.get_width()

        # Calculate the position to draw the slider bar
        self.slider_bar_x = self.x - self.slider_bar_image.get_width() // 2

        self.bar_length = self.slider_bar_image.get_width() // 2 - 70

    def draw_slider(self, game_window):
        # Draw slider track
        game_window.blit(self.slider_bar_image, (self.slider_bar_x, self.y - self.slider_bar_image.get_height() // 2))

        # Calculate slider position based on value
        slider_pos = self.x + int(self.value * self.bar_length) - self.slider_knob_width // 2

        # Draw slider knob
        game_window.blit(self.slider_knob_image, (slider_pos, self.y - self.slider_knob_image.get_height() // 2))

    def update_value(self, mouse_x, *sound_channel):
        # Calculate new value based on mouse position
        self.value = (mouse_x - self.x + self.slider_knob_width // 2) / self.bar_length
        self.value = min(1, max(0, self.value))  # Clamp value between 0 and 1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (self.x <= mouse_x <= self.x + self.bar_length and abs(mouse_y - self.y)
                    <= self.slider_knob_image.get_height() // 2):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, _ = pygame.mouse.get_pos()
            self.update_value(mouse_x)



