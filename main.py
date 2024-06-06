# Import all modules and libraries necessary
import pygame
import random
import sys
import time

# Import all modules from other files in the game
from game import Game
from images import (Image, load_image, animations, gun_image_collection,
                    carousel_numbers_collection, gameplay_buttons,
                    logo_image_collection, button_image_collection, color_palette,
                    ImageCarousel, Animations)
from sound_effects import (play_mouse_click, play_blood_splatter_sound_effect, play_revolver_sound_effect,
                           sound_effects, play_mouse_hover, sound_channels,
                           SettingSlider)
from text import Text

# Initialize pygame and its mixer for sound effects
pygame.init()
pygame.mixer.init()

# Create the window for the game
window_width = 1280
window_height = 720
game_window = pygame.display.set_mode((window_width, window_height))
window_rect = pygame.Rect(0, 0, window_width, window_height)

# Create the clock for frame rate
clock = pygame.time.Clock()
FPS = 60
clock.tick(FPS)

# Fade In/Fade Out Rate
fade_rate = 4

# Enable multiple inputs from holding down a key
pygame.key.set_repeat(300, 50)

# Game Cursor
cursor = pygame.image.load("images/cursor.png")
pygame.mouse.set_visible(False)

# The game name will now appear in the window
pygame.display.set_caption("Chambers")

back_button_path, back_button_rect = load_image(
    button_image_collection["go_back_button"]["image"],
    "topleft", 975, 580)
back_button_img = Image(back_button_path, back_button_rect, True, True,
                        True, False, None)

# This creates the main_menu background animation. It is drawn down below.
main_menu_animation = Animations(animations["main_menu"], (1280, 720), 0, 0)

icon_image = pygame.image.load(logo_image_collection["chambers_icon"]["image"])
pygame.display.set_icon(icon_image)


def wait_for_spacebar():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


def main_menu_events(rect_list, image_collection):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for rect, data in zip(rect_list, image_collection.values()):
                if rect.collidepoint(mouse_x, mouse_y):
                    play_mouse_click("GUI_Interact", "mouse_click_sfx")
                    if "menu_position" in data:
                        if data["menu_position"] == 1:
                            return data["menu_position"]
                        elif data["menu_position"] == 2:
                            instructions_menu()
                            return
                        elif data["menu_position"] == 3:
                            settings_menu()
                            return
                        elif data["menu_position"] == 4:
                            pygame.quit()
                            sys.exit()
                        else:
                            return None


def give_player_names_events(events, player_name):
    max_characters = 16

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            elif event.unicode.isprintable() and len(player_name) < max_characters:
                player_name += event.unicode

    return player_name


def check_mouse_hover(rect_list, played):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for rect in rect_list:
        if rect.collidepoint(mouse_x, mouse_y):
            if not played:
                play_mouse_hover("GUI_Interact", "mouse_hover_sfx")
            return True
    return False


def draw_mouse_cursor():
    cursor_x, cursor_y = pygame.mouse.get_pos()
    game_window.blit(cursor, (cursor_x, cursor_y))
    pygame.event.set_grab(True)

    if not window_rect.collidepoint(cursor_x, cursor_y):
        # Adjust the mouse position to keep it within the window
        cursor_x = min(max(cursor_x, 0), window_width - 1)
        cursor_y = min(max(cursor_y, 0), window_height - 1)
        pygame.mouse.set_pos((cursor_x, cursor_y))


def back_button(back_button_rect):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if back_button_rect.collidepoint(mouse_x, mouse_y):
                play_mouse_click("GUI_Interact", "mouse_click_sfx")
                main_menu(True)


def main_menu(visited):
    game_window.fill((0, 0, 0))

    # This variable is used to determine if a button has been hovered and whether it should play
    # the sound effect. It is used in tandem with check_mouse_hover()
    played = False

    # Alpha values used for fade-in and fade-out effects
    fade_in_alpha = 255
    fade_out_alpha = 0

    logo_path, logo_rect = load_image(logo_image_collection["chambers_logo"]["image"],
                                      "midtop", 640, 0)
    chambers_logo = Image(logo_path, logo_rect, False, False,
                          True, False, None)

    play_path, play_rect = load_image(button_image_collection["play_button"]["image"],
                                      "center", 640, 280)
    play_button_img = Image(play_path, play_rect, True, True,
                            True, False, None)

    instructions_path, instructions_rect = load_image(button_image_collection["instructions_button"]["image"],
                                                      "center", 640, 400)
    instructions_button_img = Image(instructions_path, instructions_rect, True, True,
                                    True, False, None)

    settings_path, settings_rect = load_image(button_image_collection["settings_button"]["image"],
                                              "center", 640, 520)
    settings_button_img = Image(settings_path, settings_rect, True, True,
                                True, False, None)

    quit_path, quit_rect = load_image(button_image_collection["quit_button"]["image"],
                                      "center", 640, 640)
    quit_button_img = Image(quit_path, quit_rect, True, True,
                            True, False, None)

    # This list will store the rectangles of each image in the while loop below
    # The rectangles will then be used to determine where the mouse is clicking so
    # the proper event will trigger.
    main_menu_rects = [play_rect, instructions_rect, settings_rect, quit_rect]

    while True:
        if not visited:
            fade_in_alpha -= (.5 * fade_rate)
            if fade_in_alpha < 0:
                fade_in_alpha = 0
            game_window.fill(color_palette["black"])

            fade_surface = pygame.Surface(game_window.get_size())
            fade_surface.set_alpha(fade_in_alpha)
            fade_surface.fill(color_palette["white"])

        # This draws the animated background for the main menu
        # It is drawn first, so it is in the background.
        main_menu_animation.sprite_group.draw(game_window)
        main_menu_animation.update_frames()

        # Draws the logo image "Chambers" using the load_image function
        # the Image class and the draw method within that class.
        chambers_logo.draw(game_window, None, None, None,
                           None, None, 1)

        # Draws the Play button using the load_image function
        # the Image class and the draw method within that class.
        # Clicking play will start a new game and the user will pick the settings that determine
        # how the game is played
        play_button_img.draw(game_window, color_palette["russian_blue"], 6, color_palette["deep_blue"],
                             color_palette["hushed_yellow"], 8, 1.15, 0, -10, 3)

        # Draws the Instructions button using the load_image function
        # the Image class and the draw method within that class.
        # The instructions will show the user text descriptions on how to play the game
        instructions_button_img.draw(game_window, color_palette["russian_blue"], 6, color_palette["deep_blue"],
                                     color_palette["hushed_yellow"], 8, 1.15, 0, -30, 3)

        # Draws the Settings button using the load_image function
        # the Image class and the draw method within that class.
        # The settings will allow the user to change the overall volume of the game
        settings_button_img.draw(game_window, color_palette["russian_blue"], 6, color_palette["deep_blue"],
                                 color_palette["hushed_yellow"], 8, 1.15, 0, -20, 3)

        # Draws the Quit button using the load_image function
        # the Image class and the draw method within that class.
        # The game will quit when it is clicked on... duh...
        quit_button_img.draw(game_window, color_palette["russian_blue"], 6, color_palette["deep_blue"],
                             color_palette["hushed_yellow"], 8, 1.15, 0, -10, 2)

        played = check_mouse_hover(main_menu_rects, played)
        main_menu_navigation = main_menu_events(main_menu_rects, button_image_collection)

        if not visited:
            game_window.blit(fade_surface, (0, 0))

        draw_mouse_cursor()

        pygame.display.update()
        pygame.display.flip()

        if main_menu_navigation == 1:
            break

    while fade_out_alpha < 255:
        fade_out_alpha += (.5 * fade_rate)

        game_window.fill(color_palette["black"])

        fade_surface = pygame.Surface(game_window.get_size())
        fade_surface.set_alpha(fade_out_alpha)
        fade_surface.fill(color_palette["white"])

        main_menu_animation.sprite_group.draw(game_window)
        main_menu_animation.update_frames()

        game_window.blit(fade_surface, (0, 0))

        pygame.display.update()
        pygame.display.flip()

    find_num_players()


def instructions_menu():
    game_window.fill((0, 0, 0))

    played = False

    text_box_path, text_box_rect = load_image(button_image_collection["text_box"]["image"],
                                              "center", 640, 360)
    text_box = Image(text_box_path, text_box_rect, False, False,
                     True, False, None)

    instructions_path, instructions_rect = load_image(
        button_image_collection["instructions_button"]["image"],
        "center", 640, 100)
    instructions_button_img2 = Image(instructions_path, instructions_rect, False, False,
                                     True, False, None)

    instructions_heading_text = Text("Welcome to Chambers", 75, color_palette["hushed_yellow"], 640, 200)
    instructions_heading_text.find_width_center(window_width)

    instructions_text = Text("Each player will receive a revolver with one bullet when it is their turn. \n"
                             "Players must decide to shoot, spin, or target. \n"
                             "      - take aim at your own head and hope for the best. \n"
                             "     - spin the revolver chamber first before shooting. \n"
                             "       - shoot the next player in line. If they do not die... you do. \n",
                             50, color_palette["midnight"], 640, 370)
    instructions_shoot_text1 = Text("Shoot", 50, color_palette["charcoal"], 204, 350)
    instructions_shoot_text2 = Text("Spin", 50, color_palette["hushed_yellow"], 200, 390)
    instructions_shoot_text3 = Text("Target", 50, color_palette["razzmatazz"], 118, 432)

    instructions_ending_text = Text("Good Luck", 55, color_palette["razzmatazz"], 0, 475)
    instructions_ending_text.find_width_center(window_width)

    while True:
        main_menu_animation.sprite_group.draw(game_window)
        main_menu_animation.update_frames()

        text_box.draw(game_window, None, None, None,
                      None, None, 1.88, None)

        instructions_button_img2.draw(game_window, None, None, None,
                                      None, None, 1.25)

        back_button_img.draw(game_window, color_palette["midnight"], 6, color_palette["charcoal"],
                             color_palette["hushed_yellow"], 8, 1.15, None, -13, 3)

        instructions_text.render_multiline_text(game_window)

        instructions_shoot_text1.render(game_window)
        instructions_shoot_text2.render(game_window)
        instructions_shoot_text3.render(game_window)

        instructions_ending_text.render(game_window)

        draw_mouse_cursor()

        instructions_heading_text.type(game_window)

        back_button(back_button_rect)
        rect_list = [back_button_rect]
        played = check_mouse_hover(rect_list, played)

        pygame.display.update()
        pygame.display.flip()


def settings_menu():
    game_window.fill((0, 0, 0))

    played = False

    settings_path, settings_rect = load_image(button_image_collection["settings_button"]["image"],
                                              "center", 640, 100)
    settings_button_img2 = Image(settings_path, settings_rect, False, False,
                                 True, False, None)

    music_text = Text("Main Volume", 40, color_palette["hushed_yellow"], 640, 200)
    sfx_text = Text("SFX", 40, color_palette["hushed_yellow"], 640, 400)

    music_slider = SettingSlider(640, 300)
    sfx_slider = SettingSlider(640, 500)

    while True:
        main_menu_animation.sprite_group.draw(game_window)
        main_menu_animation.update_frames()

        settings_button_img2.draw(game_window, None, None, None,
                                  None, None, 1.25, None)

        back_button_img.draw(game_window, color_palette["midnight"], 6, color_palette["charcoal"],
                             color_palette["hushed_yellow"], 8, 1.15, None, -13, 3)

        music_text.render(game_window, True)
        sfx_text.render(game_window, True)

        mouse_x, _ = pygame.mouse.get_pos()

        music_slider.draw_slider(game_window)
        sfx_slider.draw_slider(game_window)
        music_slider.update_value(mouse_x, sound_channels["music_channel"])
        sfx_slider.update_value(mouse_x, sound_channels["gui_sfx_channel"], sound_channels["game_sfx_channel"])

        draw_mouse_cursor()

        back_button(back_button_rect)
        rect_list = [back_button_rect]
        played = check_mouse_hover(rect_list, played)

        pygame.display.update()
        pygame.display.flip()


# Function that finds the number of players that will be playing the game
def find_num_players():
    game_window.fill((0, 0, 0))

    played = False
    num_players_carousel = ImageCarousel(carousel_numbers_collection, game_window, window_width, window_height)
    num_players_info_text = Text("How Many Will Play?", 100, color_palette["razzmatazz"], 640, 500)

    text_box_path, text_box_rect = load_image(button_image_collection["text_box"]["image"],
                                              "center", 640, 545)
    text_box = Image(text_box_path, text_box_rect, False, False,
                     True, False, None)

    # Alpha values used for fade-in and fade-out effects
    fade_in_alpha = 255
    fade_out_alpha = 0

    while True:
        fade_in_alpha -= (.5 * fade_rate)
        if fade_in_alpha < 0:
            fade_in_alpha = 0
        game_window.fill(color_palette["black"])

        fade_surface = pygame.Surface(game_window.get_size())
        fade_surface.set_alpha(fade_in_alpha)
        fade_surface.fill(color_palette["white"])

        main_menu_animation.sprite_group.draw(game_window)
        main_menu_animation.update_frames()

        text_box.draw(game_window, None, None, None,
                      None, None, .90, None)

        num_players_info_text.type(game_window)
        num_players_info_text.find_width_center(window_width)

        right_arrow_rect, left_arrow_rect = num_players_carousel.draw_arrows()

        back_button_img.draw(game_window, color_palette["midnight"], 6, color_palette["charcoal"],
                             color_palette["hushed_yellow"], 8, 1.15, None, -13, 3)

        rect_list = [right_arrow_rect, left_arrow_rect, back_button_rect]
        played = check_mouse_hover(rect_list, played)

        num_players_carousel.draw_carousel()
        num_players = num_players_carousel.image_carousel_events(right_arrow_rect, left_arrow_rect, back_button_rect)

        game_window.blit(fade_surface, (0, 0))
        draw_mouse_cursor()

        if num_players == "go back" or isinstance(num_players, int):
            break

        pygame.display.update()
        pygame.display.flip()

    while fade_out_alpha < 255:
        fade_out_alpha += (.5 * fade_rate)

        game_window.fill(color_palette["black"])

        fade_surface = pygame.Surface(game_window.get_size())
        fade_surface.set_alpha(fade_out_alpha)
        fade_surface.fill(color_palette["white"])

        main_menu_animation.sprite_group.draw(game_window)
        main_menu_animation.update_frames()

        game_window.blit(fade_surface, (0, 0))

        pygame.display.update()
        pygame.display.flip()

    if num_players == "go back":
        main_menu(False)
    elif isinstance(num_players, int):
        give_player_names(num_players)


def give_player_names(num_players):
    game_window.fill((0, 0, 0))

    played = False
    player_names = {}
    player_count = 1
    player_name = ""

    # Alpha values used for fade-in and fade-out effects
    fade_in_alpha = 255
    fade_out_alpha = 0

    names_info_text = Text("Enter the Players' Names", 100, color_palette["razzmatazz"], 640, 475)
    names_info_text2 = Text("Press Enter to Confirm", 35, color_palette["charcoal"], 640, 230)
    player_num_text = Text(f"Player {player_count}", 100, color_palette["silver"], 0, 125)
    player_name_text = Text("", 100, color_palette["hushed_yellow"], 640, 355)

    text_box_path, text_box_rect = load_image(button_image_collection["text_box"]["image"],
                                              "center", 640, 360)
    text_box = Image(text_box_path, text_box_rect, False, False,
                     True, False, None)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(mouse_x, mouse_y):
                    play_mouse_click("GUI_Interact", "mouse_click_sfx")
                    player_names.clear()
                    while fade_out_alpha < 255:
                        fade_out_alpha += (.5 * fade_rate)

                        game_window.fill(color_palette["black"])

                        fade_surface = pygame.Surface(game_window.get_size())
                        fade_surface.set_alpha(fade_out_alpha)
                        fade_surface.fill(color_palette["white"])

                        main_menu_animation.sprite_group.draw(game_window)
                        main_menu_animation.update_frames()

                        game_window.blit(fade_surface, (0, 0))

                        pygame.display.update()
                        pygame.display.flip()
                    find_num_players()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_names[player_count] = player_name
                    player_name = ""
                    player_count += 1
                    player_num_text.set_text(f"Player {player_count}")
                if event.key == pygame.K_ESCAPE:
                    quit()

        fade_in_alpha -= (.5 * fade_rate)
        if fade_in_alpha < 0:
            fade_in_alpha = 0
        game_window.fill(color_palette["black"])

        fade_surface = pygame.Surface(game_window.get_size())
        fade_surface.set_alpha(fade_in_alpha)
        fade_surface.fill(color_palette["white"])

        main_menu_animation.sprite_group.draw(game_window)
        main_menu_animation.update_frames()

        names_info_text.type(game_window)
        names_info_text.find_width_center(window_width)

        names_info_text2.type(game_window)
        names_info_text2.find_width_center(window_width)

        player_num_text.find_width_center(window_width)
        player_num_text.render(game_window)

        text_box.draw(game_window, None, None, None,
                      None, None, 1, None)

        player_name = give_player_names_events(events, player_name)
        player_name_text.set_text(player_name)
        player_name_text.render(game_window, True)

        back_button_img.draw(game_window, color_palette["midnight"], 6, color_palette["charcoal"],
                             color_palette["hushed_yellow"], 8, 1.15, None, -13, 3)

        rect_list = [back_button_rect]
        played = check_mouse_hover(rect_list, played)

        game_window.blit(fade_surface, (0, 0))
        draw_mouse_cursor()

        if len(player_names) == num_players:
            break

        pygame.display.update()
        pygame.display.flip()

    while fade_out_alpha < 255:
        fade_out_alpha += (.5 * fade_rate)

        game_window.fill(color_palette["black"])

        fade_surface = pygame.Surface(game_window.get_size())
        fade_surface.set_alpha(fade_out_alpha)
        fade_surface.fill(color_palette["white"])

        main_menu_animation.sprite_group.draw(game_window)
        main_menu_animation.update_frames()

        game_window.blit(fade_surface, (0, 0))

        pygame.display.update()
        pygame.display.flip()

    find_chamber_size(num_players, player_names)


def find_chamber_size(num_players, player_names):
    game_window.fill((0, 0, 0))

    played = False
    chamber_size_carousel = ImageCarousel(gun_image_collection, game_window, window_width, window_height)
    chamber_size_info_text = Text("Pick a Chamber Size", 100, color_palette["razzmatazz"], 640, 500)

    text_box_path, text_box_rect = load_image(button_image_collection["text_box"]["image"],
                                              "center", 640, 545)
    text_box = Image(text_box_path, text_box_rect, False, False,
                     True, False, None)

    # Alpha values used for fade-in and fade-out effects
    fade_in_alpha = 255
    fade_out_alpha = 0

    while True:
        fade_in_alpha -= (.5 * fade_rate)
        if fade_in_alpha < 0:
            fade_in_alpha = 0
        game_window.fill(color_palette["black"])

        fade_surface = pygame.Surface(game_window.get_size())
        fade_surface.set_alpha(fade_in_alpha)
        fade_surface.fill(color_palette["white"])

        main_menu_animation.sprite_group.draw(game_window)
        main_menu_animation.update_frames()

        text_box.draw(game_window, None, None, None,
                      None, None, .90, None)

        chamber_size_info_text.render(game_window)
        chamber_size_info_text.find_width_center(window_width)

        right_arrow_rect, left_arrow_rect = chamber_size_carousel.draw_arrows()

        back_button_img.draw(game_window, color_palette["midnight"], 6, color_palette["charcoal"],
                             color_palette["hushed_yellow"], 8, 1.15, None, -13, 3)

        rect_list = [right_arrow_rect, left_arrow_rect, back_button_rect]
        played = check_mouse_hover(rect_list, played)

        chamber_size_carousel.draw_carousel()
        chamber_size = chamber_size_carousel.image_carousel_events(right_arrow_rect, left_arrow_rect, back_button_rect)

        game_window.blit(fade_surface, (0, 0))
        draw_mouse_cursor()

        if chamber_size == "go back" or isinstance(chamber_size, int):
            break

        pygame.display.update()
        pygame.display.flip()

    while fade_out_alpha < 255:
        fade_out_alpha += (.5 * fade_rate)

        game_window.fill(color_palette["black"])

        fade_surface = pygame.Surface(game_window.get_size())
        fade_surface.set_alpha(fade_out_alpha)
        fade_surface.fill(color_palette["white"])

        main_menu_animation.sprite_group.draw(game_window)
        main_menu_animation.update_frames()

        game_window.blit(fade_surface, (0, 0))

        pygame.display.update()
        pygame.display.flip()

    if chamber_size == "go back":
        give_player_names(num_players)
    elif isinstance(chamber_size, int):
        play_game(num_players, player_names, chamber_size)


def play_game(num_players, player_names, chamber_size):
    game_window.fill((0, 0, 0))
    played = False

    game = Game(num_players, player_names, chamber_size, game_window)

    # character = Animations(animations["character"], (650, 500), 640, 350)

    shoot_button_path, shoot_button_rect = load_image(gameplay_buttons["shoot_button"]["image"],
                                                      "center", 240, 100)
    shoot_button = Image(shoot_button_path, shoot_button_rect, True, True, True,
                         False, False)

    spin_button_path, spin_button_rect = load_image(gameplay_buttons["spin_button"]["image"],
                                                    "center", 640, 100)
    spin_button = Image(spin_button_path, spin_button_rect, True, True, True,
                        False, False)

    target_button_path, target_button_rect = load_image(gameplay_buttons["target_button"]["image"],
                                                        "center", 1040, 100)
    target_button = Image(target_button_path, target_button_rect, True, True, True,
                          False, False)

    text_box_path, text_box_rect = load_image(button_image_collection["text_box"]["image"],
                                              "center", 640, 545)
    text_box = Image(text_box_path, text_box_rect, False, False,
                     True, False, None)

    rect_list = [shoot_button_rect, spin_button_rect, target_button_rect]

    fade_in_alpha = 255
    fade_out_alpha = 0

    while True:
        fade_in_alpha -= (.5 * (fade_rate + 5))
        if fade_in_alpha < 0:
            fade_in_alpha = 0
        game_window.fill(color_palette["black"])

        fade_surface = pygame.Surface(game_window.get_size())
        fade_surface.set_alpha(fade_in_alpha)
        fade_surface.fill(color_palette["white"])

        shoot_button.draw(game_window, color_palette["russian_blue"], 6, color_palette["deep_blue"],
                          color_palette["hushed_yellow"], 8, 1.15, 0, -10, 3)
        spin_button.draw(game_window, color_palette["russian_blue"], 6, color_palette["deep_blue"],
                         color_palette["hushed_yellow"], 8, 1.15, 0, -10, 3)
        target_button.draw(game_window, color_palette["russian_blue"], 6, color_palette["deep_blue"],
                           color_palette["hushed_yellow"], 8, 1.15, 0, -10, 3)

        text_box.draw(game_window, None, None, None,
                      None, None, 1.15, None)

        game.play_game_events(rect_list)
        game.start_turn()

        game_window.blit(fade_surface, (0, 0))
        draw_mouse_cursor()

        played = check_mouse_hover(rect_list, played)

        pygame.display.update()
        pygame.display.flip()


if __name__ == "__main__":
    main_menu(False)

"""
def take_turn(current_player, bullet_chamber, alive_players):
    # AI responses
    # player_response = generate_response(current_player, prompts)
    # print(player_response)
    player_response = next_turn_responses(current_player)
    print(player_response)
    time.sleep(2)


    def is_player_dead():
        if bullet_chamber == current_chamber:
            time.sleep(2)
            play_blood_splatter_sound_effect()
            print("BLAM!")
            time.sleep(2)
            print("Player", current_player, "is dead!")
            players_to_remove.append(current_player)
            time.sleep(2)
            last_player_dead = True
        else:
            time.sleep(2)
            play_revolver_sound_effect("revolver_collection", "revolver_fire_empty_sfx")
            print("WHEW!")
            time.sleep(2)
            print("Player", current_player, "is still alive!")
            time.sleep(2)
            alive_response = alive_responses(current_player)
            print(alive_response)
            last_player_dead = False
        return last_player_dead

    def spin_chamber():
        print("Player", current_player, "spins the chamber of the gun!")
        current_chamber = random.randint(1, bullet_chamber)
        play_revolver_sound_effect("revolver_collection", "revolver_spin_sfx")
        for _ in range(3):
            time.sleep(random.randint(1, 3))
            print(".")
        is_player_dead()

    def shoot_without_spinning():
        print("Player", current_player, "doesn't spin the chamber!")
        for _ in range(3):
            time.sleep(random.randint(1, 3))
            print(".")
        is_player_dead()

    def shoot_next_player():
        next_player = (current_player + 1) % alive_players
        print("Player", current_player, "takes aim at", next_player, "!")
        last_player_dead = True

        for _ in range(3):
            time.sleep(random.randint(1, 3))
            print(".")
        if bullet_chamber == current_chamber:
            time.sleep(2)
            play_blood_splatter_sound_effect()
            print("BLAM!")
            time.sleep(2)
            print("Player", current_player, "shot", next_player, "!")
            players_to_remove.append(next_player)
            time.sleep(2)

        else:
            time.sleep(2)
            play_revolver_sound_effect("revolver_collection", "revolver_fire_empty_sfx")
            print("WHEW!")
            time.sleep(2)
            print("Player", next_player, "is still alive!")
            time.sleep(2)
            print("Player", current_player, "must now die!")
            time.sleep(2)
            play_blood_splatter_sound_effect()
        return last_player_dead


def play_russian_roulette():
    alive_players = find_num_players()
    random.shuffle(alive_players)
    print(alive_players)
    bullet_chamber = random.randint(1, find_chamber_size())

    while len(alive_players) > 1:
        players_to_remove = []
        last_player_dead = False
        for current_player in alive_players:
            print("It is Player", str(current_player) + "'s turn!")
            if last_player_dead:
                play_revolver_sound_effect("revolver_collection", "revolver_reload_sfx")
            wait_for_spacebar()
            take_turn(current_player, bullet_chamber, alive_players)



            if bullet_chamber == current_chamber:
                time.sleep(2)
                play_blood_splatter_sound_effect()
                print("BLAM!")
                time.sleep(2)
                print("Player", current_player, "is dead!")
                players_to_remove.append(current_player)
                time.sleep(2)
                last_player_dead = True
            else:
                time.sleep(2)
                last_player_dead = False
                play_revolver_sound_effect("revolver_collection", "revolver_fire_empty_sfx")
                print("WHEW!")
                time.sleep(2)
                print("Player", current_player, "is still alive!")
                time.sleep(2)


# Remove dead players from the alive_players list after the iteration
for player_to_remove in players_to_remove:
    alive_players.remove(player_to_remove)

print("Game Over! Player", alive_players[0], "wins!")


"""
