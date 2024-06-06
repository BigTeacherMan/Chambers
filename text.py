import pygame

from sound_effects import sound_effects, sound_channels


class Text:
    def __init__(self, text, font_size, color, x_pos, y_pos):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = pygame.font.Font("font/Chambers-Regular.ttf", self.font_size)
        self.rendered_lines = []
        self.line_rects = []
        self.typing_index = 0  # Index to track the current character being typed
        self.typing_speed = 100  # Typing speed in milliseconds
        self.typing_timer = 0  # Time of the last update
        self.rendered_text = ""

    def type(self, game_window):
        current_time = pygame.time.get_ticks()
        if current_time - self.typing_timer > self.typing_speed:
            self.typing_timer = current_time

            if self.typing_index < len(self.text):
                sound_channels["game_sfx_channel"].play(sound_effects["GUI_Interact"]["typing_sound_sfx"])  # Play typing sound for each character
                self.rendered_text += self.text[self.typing_index]  # Get text up to the current character
                self.typing_index += 1
                self.typing_timer = current_time

        text_surface = self.font.render(self.rendered_text, True, self.color)
        text_rect = text_surface.get_rect(topleft=(self.x_pos, self.y_pos))
        game_window.blit(text_surface, text_rect)

    def render(self, game_window, center_align=False):
        text = self.font.render(self.text, True, self.color)

        if center_align:
            centered_text = self.font.render(self.text, True, self.color)
            rect = centered_text.get_rect()
            rect.center = (self.x_pos, self.y_pos)
            game_window.blit(text, rect)

        else:
            game_window.blit(text, (self.x_pos, self.y_pos))

    def render_multiline_text(self, surface):
        lines = self.text.splitlines()
        self.rendered_lines = []
        self.line_rects = []
        for line in lines:
            line_surface = self.font.render(line, True, self.color)
            line_rect = line_surface.get_rect()
            self.rendered_lines.append(line_surface)
            self.line_rects.append(line_rect)

        # Calculate the total height of all lines
        total_height = sum(line_rect.height for line_rect in self.line_rects)

        # Calculate the y-coordinate to center the text vertically
        y_center = self.y_pos - total_height // 2

        # Render each line centered horizontally and aligned vertically
        for i, (line_surface, line_rect) in enumerate(zip(self.rendered_lines, self.line_rects)):
            # Calculate the x-coordinate to center the line horizontally
            x_center = self.x_pos - line_rect.width // 2
            surface.blit(line_surface, (x_center, y_center + i * line_rect.height))

    def set_text(self, new_text):
        self.text = new_text

    def find_width_center(self, window_width):
        text_width, _ = self.font.size(self.text)
        self.x_pos = (window_width - text_width) // 2

    def find_height_center(self, window_height):
        text_width, _ = self.font.size(self.text)
        self.y_pos = (window_height - text_width) // 2

