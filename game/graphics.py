from game import arcade_import as arcade
from mechanics import tokens
from arcade.color import *

BLACKBOARD = arcade.Color(10, 64, 15)
TURQUOISE = arcade.Color(0, 104, 90)
VIOLET = arcade.Color(80, 25, 112)
RED = arcade.Color(112, 25, 47)
ORANGE = arcade.Color(138, 85, 47)
YELLOW = arcade.Color(234, 200, 26)
GREY = arcade.Color(150, 150, 150)
WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FONT_NAME = 'Better VCR'
FONT_SIZE = 30
CHAR_WIDTH = 31
CHAR_HEIGHT = 61

def create_token_texture(
        token: tokens.VisibleToken, 
        color: arcade.Color = WHITE, 
        font_size: float = 1) -> arcade.Texture:
    sprite = arcade.create_text_sprite(
        str(token), 
        color, 
        FONT_SIZE * font_size, 
        font_name=FONT_NAME)
    return sprite.texture

def create_line_texture(width: int, 
                        height: int, 
                        color: arcade.Color = WHITE) -> arcade.Texture:
    sprite = arcade.SpriteSolidColor(width, height, color)
    return sprite.texture

BUTTON_ACTION_MENU_STYLE = {
    "normal": arcade.UIFlatButton.UIStyle(
        font_size=10,
        font_name=FONT_NAME,
        font_color=GREY,
        bg=WHITE,
        border=BLACK,
        border_width=1),
    "hover": arcade.UIFlatButton.UIStyle(
        font_size=10,
        font_name=FONT_NAME,
        font_color=VIOLET,
        bg=WHITE,
        border=BLACK,
        border_width=1),
    "press": arcade.UIFlatButton.UIStyle(
        font_size=10,
        font_name=FONT_NAME,
        font_color=VIOLET,
        bg=VIOLET,
        border=BLACK,
        border_width=1),
    "disabled": arcade.UIFlatButton.UIStyle(
        font_size=10,
        font_name=FONT_NAME,
        font_color=WHITE,
        bg=GREY,
        border=BLACK,
        border_width=1)
}

BUTTON_UI_STYLE = {
    'normal': arcade.UIFlatButton.UIStyle(
        font_size=15,
        font_name=FONT_NAME,
        font_color=WHITE,
        bg=BLACKBOARD,
        border=WHITE,
        border_width=2),
    'hover': arcade.UIFlatButton.UIStyle(
        font_size=15,
        font_name=FONT_NAME,
        font_color=ORANGE,
        bg=BLACKBOARD,
        border=GRAY,
        border_width=2),
    'press': arcade.UIFlatButton.UIStyle(
        font_size=15,
        font_name=FONT_NAME,
        font_color=ORANGE,
        bg=BLACK,
        border=BLACK,
        border_width=2),
    'disable': arcade.UIFlatButton.UIStyle(
        font_size=15,
        font_name=FONT_NAME,
        font_color=ORANGE,
        bg=BLACK,
        border=BLACK,
        border_width=2)
}
