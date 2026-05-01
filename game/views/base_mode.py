"""в этом модуле базовый класс для тех view, 
которые описывают режим игры, для их общей логики
сейчас это кнопка для возврата в меню"""

from game import arcade_import as arcade
from game import graphics

class BaseMode(arcade.UIView):
    def __init__(self):
        super().__init__()
        self.background_color = graphics.BLACKBOARD
        button = arcade.UIFlatButton(text="меню", width=100, style=graphics.BUTTON_UI_STYLE)
        from game.views.menu import Menu
        @button.event("on_click")
        def on_click(event): self.window.show_view(Menu())
        anchor = self.ui.add(arcade.UIAnchorLayout())
        anchor.add(button, anchor_x="left", anchor_y="top", align_x=10, align_y=-10)