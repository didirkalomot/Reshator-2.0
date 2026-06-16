from game import arcade_import as arcade
from game.views.expression_view import ExpressionView
from mechanics import tokens, parse, exceptions
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

def create_line_texture(
        width: int, 
        height: int, 
        color: arcade.Color = WHITE) -> arcade.Texture:
    sprite = arcade.SpriteSolidColor(width, height, color)
    return sprite.texture

BUTTON_ACTION_MENU_STYLE = {
    'normal': arcade.UIFlatButton.UIStyle(
        font_size=10,
        font_name=FONT_NAME,
        font_color=GREY,
        bg=WHITE,
        border=BLACK,
        border_width=1),
    'hover': arcade.UIFlatButton.UIStyle(
        font_size=10,
        font_name=FONT_NAME,
        font_color=VIOLET,
        bg=WHITE,
        border=BLACK,
        border_width=1),
    'press': arcade.UIFlatButton.UIStyle(
        font_size=10,
        font_name=FONT_NAME,
        font_color=VIOLET,
        bg=VIOLET,
        border=BLACK,
        border_width=1),
    'disabled': arcade.UIFlatButton.UIStyle(
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

class Popup(arcade.UIMouseFilterMixin, arcade.UIBoxLayout):
    def __init__(self, bg_color):
        super().__init__(vertical=True, space_between=15)
        self.with_background(color=bg_color)

    def on_event(self, event):
        if isinstance(event, arcade.UIMousePressEvent):
            if not self.rect.point_in_rect((event.x, event.y)):
                self.parent.remove(self)
                return True
        return super().on_event(event)
    
class InfoDialog(Popup):
    def __init__(self, title, message, button_text='Понятно', bg_color=VIOLET):
        super().__init__(bg_color=bg_color)

        self.add(arcade.UILabel(
            text=title,
            font_name=FONT_NAME,
            font_size=18,
            text_color=WHITE,
            align='center',
            size_hint=(1, None)))
        
        self.add(arcade.UILabel(
            text=message,
            font_name=FONT_NAME,
            font_size=13,
            text_color=WHITE,
            multiline=True,
            width=310,
            size_hint=(1, None)))
        
        btn = self.add(arcade.UIFlatButton(text=button_text, width=120, style=BUTTON_UI_STYLE))
        @btn.event('on_click')
        def on_click(e): self.parent.remove(self)

class InputDialog(Popup):
    def __init__(self, 
                 view: ExpressionView, 
                 func, 
                 title: str='Введите выражение', 
                 bg_color: Color=VIOLET):
        super().__init__(bg_color=bg_color)

        self.add(arcade.UILabel(
            text=title,
            font_name=FONT_NAME,
            font_size=18,
            text_color=WHITE,
            align='center',
            size_hint=(1, None)))

        self.input = self.add(arcade.UIInputText(
            width=280, height=30,
            font_name=FONT_NAME,
            font_size=18,
            multiline=True))

        button_row = arcade.UIBoxLayout(vertical=False, space_between=10)
        ok_btn = arcade.UIFlatButton(text='Готово', width=100)
        cancel_btn = arcade.UIFlatButton(text='Отмена', width=100)

        @ok_btn.event('on_click')
        def on_ok(e):
            expr = self.input.text.strip()
            try: func(parse.create_tree(expr))
            except exceptions.ParseError as err: 
                view.show_notification(str(err))
            self.parent.remove(self)

        @cancel_btn.event('on_click')
        def on_cancel(e): self.parent.remove(self)

        button_row.add(ok_btn)
        button_row.add(cancel_btn)
        self.add(button_row)