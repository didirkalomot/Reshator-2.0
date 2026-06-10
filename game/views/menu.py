'''это главное меню, тут можно выйти из игры или выбрать режим игры'''

from game import arcade_import as arcade
from game import graphics
from game.views.sandbox_mode import SandboxMode
from game.views.learning_mode import learning
from game.views.base_mode import BaseMode

BUTTON_MODE_WIDTH = 200
BUTTON_MODE_HEIGHT = 50

class Menu(arcade.UIView):
    MODES = [
        (learning, 'Обучение'),
        (SandboxMode, 'Песочница'),
        (BaseMode, 'Режим 3'),
        (BaseMode, 'Режим 4')]
        # следующий режим
        
    def __init__(self):
        super().__init__()
        self.background_color = graphics.BLACKBOARD
        
        anchor = self.ui.add(arcade.UIAnchorLayout())
        
        # Заголовок
        title = arcade.UILabel(
            text='Решатор',
            font_name=graphics.FONT_NAME,
            font_size=48,
            text_color=arcade.color.WHITE)
        anchor.add(title, anchor_x='center', anchor_y='top', align_y=-30)
        
        # Область прокрутки
        scroll = arcade.UIScrollArea(width=700, height=400)
        scroll.add(self.build_modes_grid())
        anchor.add(scroll, anchor_x='center', align_x=140, anchor_y='center', align_y=-70)
        
        # Кнопка выхода
        exit_btn = arcade.UIFlatButton(text='Выход', width=200, height=50, style=graphics.BUTTON_UI_STYLE)
        @exit_btn.event('on_click')
        def on_exit(event): arcade.exit()
        anchor.add(exit_btn, anchor_x='center', anchor_y='bottom', align_y=30)
    
    def build_modes_grid(self): #Строит сетку кнопок 2xN
        vertical_layout = arcade.UIBoxLayout(vertical=True, space_between=20)
        for i in range(0, len(self.MODES), 2):
            row = self.create_row(
                self.MODES[i],
                self.MODES[i + 1] if i + 1 < len(self.MODES) else None)
            vertical_layout.add(row)
        return vertical_layout
    
    def create_row(self, mode1, mode2=None): # Создает одну строку
        row = arcade.UIBoxLayout(vertical=False, space_between=20)
        row.add(self.create_button(mode1[0], mode1[1])) # Первая кнопка
        if mode2: row.add(self.create_button(mode2[0], mode2[1])) # Вторая кнопка или пустышка
        else: row.add(arcade.UIWidget(width=BUTTON_MODE_WIDTH, height=BUTTON_MODE_HEIGHT))        
        return row
    
    def create_button(self, view_class, text): #Создает одну кнопку для режима игры
        btn = arcade.UIFlatButton(
            text=text,
            width=BUTTON_MODE_WIDTH,
            height=BUTTON_MODE_HEIGHT,
            style=graphics.BUTTON_UI_STYLE,
            font_size=18)
        @btn.event('on_click')
        def on_click(event, vc=view_class): self.window.show_view(vc())
        return btn