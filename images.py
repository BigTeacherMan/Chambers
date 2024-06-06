import pygame
from sound_effects import play_mouse_click
from text import Text

color_palette = {
    "silver": (203, 211, 219),
    "russian_blue": (122, 143, 159),
    "midnight": (46, 55, 67),
    "charcoal": (37, 39, 43),
    "hazy_blue": (70, 96, 132),
    "deep_blue": (7, 15, 45),
    "razzmatazz": (231, 14, 90),
    "hushed_yellow": (225, 225, 0),
    "black": (255, 255, 255),
    "white": (0, 0, 0),
}

# Individualized nested dictionaries that contain the associated images for each category
gun_image_collection = {
    "gun_4_chambers": {
        "image": "images/carousel/gun_chamber_4.png",
        "text": "Four",
        "value": 4,
        "carousel_position": 1,
    },
    "gun_5_chambers": {
        "image": "images/carousel/gun_chamber_5.png",
        "text": "Five",
        "value": 5,
        "carousel_position": 2,
    },
    "gun_6_chambers": {
        "image": "images/carousel/gun_chamber_6.png",
        "text": "Six",
        "value": 6,
        "carousel_position": 3,
    },
    "gun_7_chambers": {
        "image": "images/carousel/gun_chamber_7.png",
        "text": "Seven",
        "value": 7,
        "carousel_position": 4,
    },
}

carousel_numbers_collection = {
    2: {
        "image": "images/carousel/two_carousel.png",
        "text": "Two",
        "carousel_position": 1,
        "value": 2,
    },
    3: {
        "image": "images/carousel/three_carousel.png",
        "text": "Three",
        "carousel_position": 2,
        "value": 3,
    },
    4: {
        "image": "images/carousel/four_carousel.png",
        "text": "Four",
        "carousel_position": 3,
        "value": 4,
    },
    5: {
        "image": "images/carousel/five_carousel.png",
        "text": "Five",
        "carousel_position": 4,
        "value": 5,
    },
    6: {
        "image": "images/carousel/six_carousel.png",
        "text": "Six",
        "carousel_position": 5,
        "value": 6,
    },
    7: {
        "image": "images/carousel/seven_carousel.png",
        "text": "Seven",
        "carousel_position": 6,
        "value": 7,
    },
}

logo_image_collection = {
    "chambers_logo": {
        "image": "images/chambers_title.png",
    },
    "chambers_icon": {
        "image": "images/chambers_icon.png",
    },
    "chambers_cursor": {
        "image": "images/cursor.png",
    },
}

button_image_collection = {
    "play_button": {
        "image": "images/buttons/play_button.png",
        "menu_position": 1,
    },
    "instructions_button": {
        "image": "images/buttons/instructions_button.png",
        "menu_position": 2,
    },
    "settings_button": {
        "image": "images/buttons/settings_button.png",
        "menu_position": 3,
    },
    "quit_button": {
        "image": "images/buttons/quit_button.png",
        "menu_position": 4,
    },
    "go_back_button": {
        "image": "images/buttons/go_back_button.png",
    },
    "confirm_button": {
        "image": "images/buttons/confirm_button.png",
    },
    "left_arrow": {
        "image": "images/carousel/left_arrow.png",
    },
    "right_arrow": {
        "image": "images/carousel/right_arrow.png",
    },
    "text_box": {
        "image": "images/text_box.png",
    },
}

gameplay_buttons = {
    "shoot_button": {
        "image": "images/buttons/shoot_button.png",
    },
    "spin_button": {
        "image": "images/buttons/spin_button.png",
    },
    "target_button": {
        "image": "images/buttons/target_button.png",
    },
}

animations = {
    "main_menu": "animations/main_menu_background.png",
    "character": "animations/character.png",
}


def load_image(path, rect_location, x_pos=0, y_pos=0):
    image = pygame.image.load(path)
    image_rect = image.get_rect(**{rect_location: (x_pos, y_pos)})
    return path, image_rect


class Image:
    def __init__(self, image_path, rect, can_hover, has_border, scalable, has_opacity, text):
        self.image_path = image_path
        self.rect = rect
        self.can_hover = can_hover
        self.has_border = has_border
        self.scalable = scalable
        self.has_opacity = has_opacity
        self.text = text
        self.hovered = False
        self.original_image = pygame.image.load(image_path)
        self.modified_image = self.original_image.copy()

    def draw(self, game_window, border_color=(0, 0, 0), border_width=0,
             background_color=(0, 0, 0), hover_color=(0, 0, 0), hover_width=0,
             scale=0.0, opacity=0, polygon_angle=0, polygon_angle2=0):

        if self.has_border:
            bordered_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            bordered_surface.fill(border_color)

            points1 = [(0, 0), (0, self.rect.height), (self.rect.width, 0)]
            points2 = [(self.rect.width, self.rect.height), (self.rect.width, polygon_angle2),
                       (polygon_angle, self.rect.height)]

            # Create a darker shade for the bottom and right borders
            darker_color = (max(0, border_color[0] - 50), max(0, border_color[1] - 50), max(0, border_color[2] - 50))

            # Fill the bottom and right sides with the darker shade
            pygame.draw.polygon(bordered_surface, border_color, points1)
            pygame.draw.polygon(bordered_surface, darker_color, points2)

            inner_surface = pygame.Surface((self.rect.width - border_width * 2, self.rect.height - border_width * 2))
            inner_surface.fill(background_color)
            bordered_surface.blit(inner_surface, (border_width, border_width))

            game_window.blit(bordered_surface, self.rect.topleft)

        self.check_hover(self.can_hover)

        if self.hovered and self.can_hover:

            # This code draws the actual hover border when the images are hovered over.
            pygame.draw.rect(game_window, hover_color, self.rect, hover_width)

            if self.scalable:
                scaled_width = int(self.original_image.get_width() * scale)
                scaled_height = int(self.original_image.get_height() * scale)
                scaled_image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))

                if self.has_opacity:
                    scaled_image.set_alpha(opacity)
                    scaled_rect = scaled_image.get_rect()
                    scaled_rect.center = self.rect.center
                    game_window.blit(scaled_image, scaled_rect.topleft)
                else:
                    scaled_rect = scaled_image.get_rect()
                    scaled_rect.center = self.rect.center
                    game_window.blit(scaled_image, scaled_rect.topleft)

                if self.text:
                    self.text.render(game_window)

        elif self.scalable and not self.has_opacity and not self.can_hover:
            scaled_width = int(self.original_image.get_width() * scale)
            scaled_height = int(self.original_image.get_height() * scale)
            scaled_image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))

            scaled_rect = scaled_image.get_rect()
            scaled_rect.center = self.rect.center
            game_window.blit(scaled_image, scaled_rect.topleft)

        elif self.scalable and self.has_opacity and not self.can_hover:
            scaled_width = int(self.original_image.get_width() * scale)
            scaled_height = int(self.original_image.get_height() * scale)
            scaled_image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))

            scaled_image.set_alpha(opacity)
            scaled_rect = scaled_image.get_rect()
            scaled_rect.center = self.rect.center
            game_window.blit(scaled_image, scaled_rect.topleft)

        else:
            game_window.blit(self.original_image, self.rect.topleft)

    def check_hover(self, can_hover):
        if can_hover:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.hovered = self.rect.collidepoint(mouse_x, mouse_y)


class Animations(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, frame_dimensions, x_pos, y_pos, frame_delay=5):
        super().__init__()
        self.frames = []
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_frame = 0
        self.frame_delay = frame_delay
        self.frame_countdown = frame_delay
        self.sprite_group = pygame.sprite.Group()
        self.load_frames(sprite_sheet_path, frame_dimensions)

    def load_frames(self, sprite_sheet_path, frame_dimensions):
        sprite_sheet = pygame.image.load(sprite_sheet_path)
        width, height = sprite_sheet.get_size()
        frame_width, frame_height = frame_dimensions
        rows = height // frame_height
        cols = width // frame_width
        for row in range(rows):
            for col in range(cols):
                frame_surface = pygame.Surface(frame_dimensions, pygame.SRCALPHA)
                frame_surface.blit(sprite_sheet, (0, 0), (col * frame_width, row * frame_height,
                                                          frame_width, frame_height))
                self.frames.append(frame_surface)
                sprite = pygame.sprite.Sprite()
                sprite.image = frame_surface
                sprite.rect = frame_surface.get_rect(topleft=(self.x_pos, self.y_pos))
                self.sprite_group.add(sprite)

    def update_frames(self):
        self.frame_countdown -= 1
        if self.frame_countdown <= 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            for sprite, frame in zip(self.sprite_group.sprites(), self.frames):
                sprite.image = self.frames[self.current_frame]
            self.frame_countdown = self.frame_delay


class ImageCarousel:
    def __init__(self, image_collection, window, window_width, window_height, current_image=2):
        self.image_collection = image_collection
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.current_image = current_image
        self.image_rects = []

    def draw_arrows(self):
        right_arrow_path, right_arrow_rect = load_image(button_image_collection["right_arrow"]["image"],
                                                        "center", 1040, 300)
        left_arrow_path, left_arrow_rect = load_image(button_image_collection["left_arrow"]["image"],
                                                      "center", 240, 300)
        right_arrow = Image(right_arrow_path, right_arrow_rect, True, False,
                            True, False, None)
        left_arrow = Image(left_arrow_path, left_arrow_rect, True, False,
                           True, False, None)

        right_arrow_faded = Image(right_arrow_path, right_arrow_rect, False, False,
                                  True, True, None)
        left_arrow_faded = Image(left_arrow_path, left_arrow_rect, False, False,
                                 True, True, None)

        if 1 < self.current_image < len(self.image_collection):
            right_arrow.draw(self.window, None, 6, None,
                             color_palette["hushed_yellow"], 8, 1.15)

            left_arrow.draw(self.window, None, 6, None,
                            color_palette["hushed_yellow"], 8, 1.15)

        elif self.current_image == 1:
            right_arrow.draw(self.window, None, 6, None,
                             color_palette["hushed_yellow"], 8, 1.15)

            left_arrow_faded.draw(self.window, None, 0, None,
                                  None, 0, .75, 80)

        elif self.current_image == len(self.image_collection):
            left_arrow.draw(self.window, None, 6, None,
                            color_palette["hushed_yellow"], 8, 1.15)

            right_arrow_faded.draw(self.window, None, 0, None,
                                   None, 0, .75, 80)

        return right_arrow_rect, left_arrow_rect

    def image_carousel_events(self, right_arrow_rect, left_arrow_rect, back_button_rect):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if left_arrow_rect.collidepoint(mouse_x, mouse_y) and self.current_image > 1:
                    play_mouse_click("GUI_Interact", "mouse_click_sfx")
                    self.current_image -= 1
                elif right_arrow_rect.collidepoint(mouse_x, mouse_y) and self.current_image < len(
                        self.image_collection):
                    play_mouse_click("GUI_Interact", "mouse_click_sfx")
                    self.current_image += 1
                elif back_button_rect.collidepoint(mouse_x, mouse_y):
                    play_mouse_click("GUI_Interact", "mouse_click_sfx")
                    return "go back"
                for i, (rect, data) in enumerate(zip(self.image_rects, self.image_collection.values())):
                    if (i + 1) == self.current_image and rect.collidepoint(mouse_x, mouse_y):
                        play_mouse_click("GUI_Interact", "mouse_click_sfx")
                        value = data["value"]
                        return int(value)

    def draw_carousel(self):
        start_x = 640
        for image in self.image_collection.values():
            image_text = image["text"]
            image_path = image["image"]
            image_loaded = pygame.image.load(image_path)
            num_players_text = Text(str(image_text), 80, (200, 200, 200), 0, 0)
            num_players_text.find_width_center(window_width=1280)
            num_players_text.find_height_center(window_height=720)

            if self.current_image == image["carousel_position"]:
                image_rect = image_loaded.get_rect(center=(start_x, 300))
                carousel_image = Image(image_path, image_rect, True,
                                       False, True, True, num_players_text)
                carousel_image.draw(self.window, (0, 0, 0), 0, None,
                                    (0, 0, 0), 0, 1.25, 125, )
                self.image_rects.append(image_rect)
            elif image["carousel_position"] == (self.current_image + 1):
                image_rect = image_loaded.get_rect(center=((start_x + 175), 300))
                carousel_image = Image(image_path, image_rect, False,
                                       False, True, True, num_players_text)
                carousel_image.draw(self.window, (0, 0, 0), 0, (0, 0, 0),
                                    (0, 0, 0), 0, .75, 50, )
            elif image["carousel_position"] == (self.current_image - 1):
                image_rect = image_loaded.get_rect(center=((start_x - 175), 300))
                carousel_image = Image(image_path, image_rect, False,
                                       False, True, True, num_players_text)
                carousel_image.draw(self.window, (0, 0, 0), 0, (0, 0, 0),
                                    (0, 0, 0), 0, .75, 50, )

