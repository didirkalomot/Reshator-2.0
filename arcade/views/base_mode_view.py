"""в этом модуле базовый класс для тех view, 
которые описывают режим игры, для их общей логики
сейчас это кнопка для возврата в меню"""

import arcade
from views.menu_view import MenuView

class BaseModeView(arcade.UIView):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_SLATE_GRAY
        
        button = arcade.gui.UIFlatButton(
            text="← Меню",
            width=100,
            style={"bg_color": arcade.color.YELLOW_ORANGE})
        @button.event("on_click")
        def on_click(event): self.window.show_view(MenuView())
        anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        anchor.add(button, anchor_x="left", anchor_y="top", offset_x=10, offset_y=-10)