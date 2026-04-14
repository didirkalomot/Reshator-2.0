"""в этом модуле базовый класс для тех view, 
которые описывают режим игры, для их общей логики
сейчас это кнопка для возврата в меню"""

from graphics import arcade_import as arcade

class BaseMode(arcade.UIView):
    def __init__(self):
        super().__init__()
        print("----------------------------------")
        self.background_color = arcade.color.DARK_SLATE_GRAY
        button = arcade.UIFlatButton(
            text="← Меню",
            width=100,
            style={
                "normal": {"bg_color": arcade.color.YELLOW_ORANGE},
                "hover": {"bg_color": arcade.color.ORANGE},
                "press": {"bg_color": arcade.color.DARK_ORANGE}})
        from graphics.views.menu import Menu
        @button.event("on_click")
        def on_click(event): self.window.show_view(Menu())
        anchor = self.ui.add(arcade.UIAnchorLayout())
        anchor.add(button, anchor_x="left", anchor_y="top", align_x=10, align_y=-10)