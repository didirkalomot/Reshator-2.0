from graphics import arcade_import as arcade
from arcade.color import *

COLOR_BLACKBOARD = arcade.Color(25, 112, 39)
COLOR_MY_VIOLET = arcade.Color(80, 25, 112)
COLOR_MY_RED = arcade.Color(112, 25, 47)
COLOR_MY_ORANGE = arcade.Color(202, 137, 47)
COLOR_MY_YELLOW = arcade.Color(234, 200, 26)

BUTTON_CHOOSE_MODE = {
    "normal": {
        "bg_color": COLOR_MY_VIOLET,
        "font_color": COLOR_MY_YELLOW,
        "font_size": 16,
    },
    "hover": { 
        "bg_color": (100, 100, 100),
        "font_color": (255, 255, 255),
        "font_size": 16,
    },
    "press": {
        "bg_color": (50, 50, 50),
        "font_color": (200, 200, 200),
        "font_size": 16,
        #"border_width": 1,
        #"border_color": (80, 80, 80)
    }
}

BUTTON_EXIT = {
    "normal": {
        "bg_color": (80, 80, 80),
        "font_color": (255, 255, 255),
        "font_size": 16,
        "border_width": 1,
        "border_color": (120, 120, 120)
    },
    "hover": { 
        "bg_color": (100, 100, 100),
        "font_color": (255, 255, 255),
        "font_size": 16,
        "border_width": 1,
        "border_color": (140, 140, 140)
    },
    "press": {
        "bg_color": (50, 50, 50),
        "font_color": (200, 200, 200),
        "font_size": 16,
        "border_width": 1,
        "border_color": (80, 80, 80)
    }
}

BUTTON_GOTO_MENU = {
    "normal": {
        "bg_color": (80, 80, 80),
        "font_color": (255, 255, 255),
        "font_size": 16,
        "border_width": 1,
        "border_color": (120, 120, 120)
    },
    "hover": { 
        "bg_color": (100, 100, 100),
        "font_color": (255, 255, 255),
        "font_size": 16,
        "border_width": 1,
        "border_color": (140, 140, 140)
    },
    "press": {
        "bg_color": (50, 50, 50),
        "font_color": (200, 200, 200),
        "font_size": 16,
        "border_width": 1,
        "border_color": (80, 80, 80)
    }
}

