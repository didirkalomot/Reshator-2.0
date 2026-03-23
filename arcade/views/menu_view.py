"""это главное меню, тут можно выйти из игры или выбрать режим игры"""

import arcade
from views.mode1_view import Mode1View
from views.mode2_view import Mode2View

class MenuView(arcade.UIView):
    def __init__(self):
        super().__init__()
        
        anchor = arcade.gui.UIAnchorLayout()
        self.ui.add(anchor)
        
        title = arcade.gui.UILabel(
            text="Решатор",
            font_size=48,
            font_color=arcade.color.WHITE)
        anchor.add(title, anchor_x="center", anchor_y="top", offset_y=-50)
        
        scroll = arcade.gui.UIScrollArea(
            width=self.window.width - 200 if self.window else 800,
            height=400)
        
        grid = arcade.gui.UIGridLayout(
            column_count=2,
            row_count=3,
            horizontal_spacing=20,
            vertical_spacing=20)
        
        btn1 = arcade.gui.UIFlatButton(text="Режим 1: Примеры", width=300)
        @btn1.event("on_click")
        def on_mode1(event): self.window.show_view(Mode1View())
        grid.add(btn1, row=0, column=0)
        
        btn2 = arcade.gui.UIFlatButton(text="Режим 2: Демо", width=300)
        @btn2.event("on_click")
        def on_mode2(event): self.window.show_view(Mode2View())
        grid.add(btn2, row=0, column=1)
        
        btn3 = arcade.gui.UIFlatButton(text="Режим 3", width=300)
        # тут можно добавить метод в декоратором на добовление в кнопку
        grid.add(btn3, row=1, column=0)
        
        btn4 = arcade.gui.UIFlatButton(text="Режим 4", width=300)
        grid.add(btn4, row=1, column=1)
        
        btn5 = arcade.gui.UIFlatButton(text="Режим 5", width=300)
        grid.add(btn5, row=2, column=0)
        
        btn6 = arcade.gui.UIFlatButton(text="Режим 6", width=300)
        grid.add(btn6, row=2, column=1)
        
        scroll.add(grid)
        anchor.add(scroll, anchor_x="center", anchor_y="center")
        
        exit_btn = arcade.gui.UIFlatButton(
            text="Выход",
            width=200,
            style={"bg_color": arcade.color.RED})
        @exit_btn.event("on_click")
        def on_exit(event):
            arcade.exit()
        anchor.add(exit_btn, anchor_x="center", anchor_y="bottom", offset_y=30)