from game import arcade_import as arcade
from game.views.base import BaseMode
from game import graphics

class GifWidget(arcade.UIWidget):
    def __init__(self, gif_sprite: arcade.TextureAnimationSprite):
        super().__init__(size_hint=(None, None),
                         width=gif_sprite.width,
                         height=gif_sprite.height)
        self.gif_sprite = gif_sprite

    def do_render(self, surface):
        # Отрисовываем текущий кадр анимации
        surface.draw_sprite(0, 0, self.width, self.height, self.gif_sprite)

    def on_update(self, delta_time: float):
        # Обновляем анимацию спрайта (переход к следующему кадру)
        # В новых версиях Arcade используется update_animation(delta_time)
        self.gif_sprite.update_animation(delta_time)
        # Говорим GUI, что виджет нужно перерисовать
        self.trigger_render()


class learning(BaseMode):
    TUTORIAL_ITEMS = [
        ('resources/action_tutorial.gif',
         'При нажатии правой кнопкой мыши по объекту будет выведен список его свойств, которые можно выполнить'),
        ('resources/work_tutorial.gif',
         'При нажатии левой кнопкой мыши по оператору он выполнится, если это возможно')]

    def __init__(self):
        super().__init__()
        self.background_color = graphics.VIOLET
        self.animated_widgets = []

        anchor = self.ui.add(arcade.UIAnchorLayout())

        title = arcade.UILabel(
            text='Обучение',
            font_name=graphics.FONT_NAME,
            font_size=48,
            text_color=arcade.color.WHITE)
        anchor.add(title, anchor_x='center', anchor_y='top', align_y=-30)

        scroll = arcade.UIScrollArea(width=800, height=500)
        scroll.add(self.build_tutorial_grid())
        anchor.add(scroll, anchor_x='center', anchor_y='center', align_y=-70)

    def build_tutorial_grid(self):
        vertical_layout = arcade.UIBoxLayout(vertical=True, space_between=20)
        for gif_path, description in self.TUTORIAL_ITEMS:
            row = self.create_tutorial_row(gif_path, description)
            vertical_layout.add(row)
        return vertical_layout

    def create_tutorial_row(self, gif_path: str, description: str):
        gif_sprite = arcade.load_animated_gif(gif_path)
        gif_sprite.scale = 0.3
        gif_widget = GifWidget(gif_sprite)
        self.animated_widgets.append(gif_widget)

        text_label = arcade.UILabel(
            text=description,
            font_name=graphics.FONT_NAME,
            font_size=16,
            width=400,
            multiline=True,
            text_color=arcade.color.WHITE)

        row = arcade.UIBoxLayout(vertical=False, space_between=15)
        spacer = arcade.UIWidget(width=50, height=1)
        row.add(spacer)
        row.add(gif_widget)
        row.add(text_label)
        return row

    def on_update(self, delta_time: float):
        for widget in self.animated_widgets: widget.on_update(delta_time)
        if hasattr(super(), 'on_update'): super().on_update(delta_time)