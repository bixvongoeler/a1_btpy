from sim import sim_globals
from sim.sim_config import SCREEN_WIDTH, TOP_BAR_HEIGHT
from sim.gui_button import Button
from sim.gui_slider import Slider
from sim.gui_helpers import play_pause, spot_cleaning, general_cleaning
from sim.sim_dust_functions import add_dirt
from sim.sim_colors import color_dict

ELEM_HEIGHT = TOP_BAR_HEIGHT - (4 * 2)

def create_gui_elements():
    # GUI Elements
    play_btn = Button(name="is_playing", x=4, y=4, width=75, height=ELEM_HEIGHT, font=sim_globals.font, screen=sim_globals.screen,
                      container=sim_globals.gui_objects,
                      color=color_dict["RED"], button_text='Play', on_click_function=play_pause)
    add_dirt_btn = Button(name="add_dirt_btn", x=117, y=4, width=80, height=ELEM_HEIGHT, font=sim_globals.font, screen=sim_globals.screen,
                          container=sim_globals.gui_objects,
                          color=color_dict["BROWN"], button_text='Add Dirt', on_click_function=add_dirt)
    spot_cleaning_btn = Button(name="spot_cleaning_btn", x=201, y=4, width=130, height=ELEM_HEIGHT, font=sim_globals.font,
                               screen=sim_globals.screen, container=sim_globals.gui_objects,
                               color=color_dict["RED"], button_text='Spot Clean: Off', on_click_function=spot_cleaning)
    general_cleaning_btn = Button(name="general_cleaning_btn", x=335, y=4, width=170, height=ELEM_HEIGHT, font=sim_globals.font,
                                  screen=sim_globals.screen, container=sim_globals.gui_objects,
                                  color=color_dict["RED"], button_text='General Clean: Off',
                                  on_click_function=general_cleaning)
    speed_slider = Slider(name="speed_slider", x=509, y=4, width=SCREEN_WIDTH - 509 - 4, puck_width=20, height=ELEM_HEIGHT,
                          value=sim_globals.simulation_speed,
                          v_min=0, v_max=80, font=sim_globals.font, screen=sim_globals.screen, container=sim_globals.gui_objects, color=color_dict["BLUE"],
                          l_text='Faster', r_text='Slower')