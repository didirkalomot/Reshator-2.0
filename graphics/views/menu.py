"""это главное меню, тут можно выйти из игры или выбрать режим игры"""

from graphics import arcade_import as arcade
from graphics import styles
from graphics.views.sandbox_mode import SandboxMode
from graphics.views.mode2 import Mode2
from graphics.views.base_mode import BaseMode

class Menu(arcade.UIView):
    # Список режимов: (View_класс, текст_на_кнопке)
    MODES = [
        (SandboxMode, "Песочница"),
        (Mode2, "Режим 2"),
        (BaseMode, "Режим 3"),
        (BaseMode, "Режим 4"),
        # следующий режим
    ]
    
    def __init__(self):
        super().__init__()
        self.background_color = styles.COLOR_BLACKBOARD
        
        anchor = self.ui.add(arcade.UIAnchorLayout())
        
        # Заголовок
        title = arcade.UILabel(
            text="Решатор",
            font_size=48,
            text_color=arcade.color.WHITE)
        anchor.add(title, anchor_x="center", anchor_y="top", align_y=-50)
        
        # Область прокрутки
        scroll = arcade.UIScrollArea(width=700, height=400)
        scroll.add(self._build_modes_grid())
        anchor.add(scroll, anchor_x="center", anchor_y="center")
        
        # Кнопка выхода
        exit_btn = arcade.UIFlatButton(text="Выход", width=200, height=50)
        @exit_btn.event("on_click")
        def on_exit(event): arcade.exit()
        anchor.add(exit_btn, anchor_x="center", anchor_y="bottom", align_y=30)
    
    def _build_modes_grid(self): #Строит сетку кнопок 2xN
        vertical_layout = arcade.UIBoxLayout(vertical=True, space_between=20)
        for i in range(0, len(self.MODES), 2):
            row = self._create_row(
                self.MODES[i],
                self.MODES[i + 1] if i + 1 < len(self.MODES) else None)
            vertical_layout.add(row)
        return vertical_layout
    
    def _create_row(self, mode1, mode2=None): # Создает одну строку
        row = arcade.UIBoxLayout(vertical=False, space_between=20)
        row.add(self._create_button(mode1[0], mode1[1])) # Первая кнопка
        if mode2: row.add(self._create_button(mode2[0], mode2[1])) # Вторая кнопка или пустышка
        else: row.add(arcade.UIWidget(width=300, height=80))        
        return row
    
    def _create_button(self, view_class, text): #Создает одну кнопку для режима игры
        btn = arcade.UIFlatButton(
            text=text,
            width=300,
            height=80,
            style=styles.BUTTON_CHOOSE_MODE,
            font_size=18)
        @btn.event("on_click")
        def on_click(event, vc=view_class): self.window.show_view(vc())
        return btn