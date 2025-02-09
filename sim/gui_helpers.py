import pygame as pg
import random
from bt import SPOT_CLEANING, GENERAL_CLEANING, BATTERY_LEVEL
from sim.sim_colors import color_dict
from sim import SpotSelector
from sim.sim_config import ROBOT_RADIUS, TOP_BAR_HEIGHT, BATTERY_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
from sim import sim_globals
from sim.sim_globals import gui_objects, screen, font, current_blackboard
from sim.sim_dust_functions import add_dirt_at



def play_pause():
    if sim_globals.is_playing:
        sim_globals.is_playing = False
        gui_objects["is_playing"].button_text_surf = sim_globals.font.render('Play', True, (20, 20, 20))
        gui_objects["is_playing"].update_colors(color_dict["RED"])
    else:
        sim_globals.is_playing = True
        gui_objects["is_playing"].button_text_surf = sim_globals.font.render('Pause', True, (20, 20, 20))
        gui_objects["is_playing"].update_colors(color_dict["GREEN"])


def spot_cleaning():
    if not current_blackboard.get_in_environment(SPOT_CLEANING, False):
        sim_globals.game_objects.append(
            SpotSelector(screen=sim_globals.screen, robot_radius=ROBOT_RADIUS, font=sim_globals.font, current_blackboard=current_blackboard,
                         game_objects=sim_globals.game_objects, gui_objects=sim_globals.gui_objects, on_click_function=add_dirt_at))
        gui_objects["spot_cleaning_btn"].update_colors(color_dict["GREEN"])
        gui_objects["spot_cleaning_btn"].button_text_surf = sim_globals.font.render('Spot Clean: On', True, (20, 20, 20))


def general_cleaning():
    if not current_blackboard.get_in_environment(GENERAL_CLEANING, False):
        current_blackboard.set_in_environment(GENERAL_CLEANING, True)
        gui_objects["general_cleaning_btn"].update_colors(color_dict["GREEN"])
        gui_objects["general_cleaning_btn"].button_text_surf = sim_globals.font.render('General Clean: On ', True, (20, 20, 20))


def update_general_cleaning():
    if not current_blackboard.get_in_environment(GENERAL_CLEANING, False):
        gui_objects["general_cleaning_btn"].update_colors(color_dict["RED"])
        gui_objects["general_cleaning_btn"].button_text_surf = sim_globals.font.render('General Clean: Off', True, (20, 20, 20))
    else:
        gui_objects["general_cleaning_btn"].update_colors(color_dict["GREEN"])
        gui_objects["general_cleaning_btn"].button_text_surf = sim_globals.font.render('General Clean: On ', True, (20, 20, 20))


def draw_battery():
    # Battery container
    battery_rect = pg.Rect(0, TOP_BAR_HEIGHT, BATTERY_WIDTH, SCREEN_HEIGHT - TOP_BAR_HEIGHT)

    pg.draw.rect(sim_globals.screen, color_dict["DARK_GRAY"], battery_rect)

    # Battery level
    battery_level = current_blackboard.get_in_environment(BATTERY_LEVEL, 0)
    level_height = ((SCREEN_HEIGHT - TOP_BAR_HEIGHT) * (battery_level / 100))
    level_rect = pg.Rect(4, TOP_BAR_HEIGHT + (SCREEN_HEIGHT - TOP_BAR_HEIGHT - level_height), BATTERY_WIDTH - 8,
                         level_height)

    # Color based on level
    if battery_level > 60:
        color = color_dict["GREEN"]
    elif battery_level > 30:
        color = color_dict["ORANGE"]
    else:
        color = color_dict["RED"]

    # Draw the battery
    pg.draw.rect(sim_globals.screen, color, level_rect)

    # Battery percentage
    text_surface = sim_globals.font.render(f"{int(battery_level)}%", True, color_dict["BLACK"])
    text_rect = text_surface.get_rect()
    # Rotate text
    text_surface = pg.transform.rotate(text_surface, 90)
    text_rect = text_surface.get_rect(center=(BATTERY_WIDTH // 2, SCREEN_HEIGHT - (level_height // 2)))
    sim_globals.screen.blit(text_surface, text_rect)

roomba_img = pg.image.load("sim/assets/roomba_dock.png")
roomba_rect = roomba_img.get_rect()
roomba_rect.bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT)
def draw_dock():
    sim_globals.screen.blit(roomba_img, roomba_rect)