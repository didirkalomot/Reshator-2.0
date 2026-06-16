from __future__ import annotations
from game import arcade_import as arcade
from game import graphics

######################################## Базовый Класс Режима ########################################

class BaseView(arcade.UIView):
    def __init__(self):
        super().__init__()
        self.background_color = graphics.BLACKBOARD
        button = arcade.UIFlatButton(text='меню', width=100, style=graphics.BUTTON_UI_STYLE)
        from game.views.menu_view import Menu
        @button.event('on_click')
        def on_click(event): self.window.show_view(Menu())
        self.anchor = self.ui.add(arcade.UIAnchorLayout())
        self.anchor.add(button, anchor_x='left', anchor_y='top', align_x=10, align_y=-10)