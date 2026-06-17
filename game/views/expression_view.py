from __future__ import annotations
from game import arcade_import as arcade
from game import graphics
from game.views.base_view import BaseView
from mechanics import nodes, tokens, parse, exceptions
from copy import deepcopy

######################################## Класс Режима С Выражением ########################################

class ExpressionView(BaseView):
    def __init__(self, root: nodes.Node, text_info: str='Упростите выражение'):
        super().__init__()
        self.notification = Notification(self.ui)
        self.original_root = deepcopy(root)
        panel_width = graphics.SCREEN_WIDTH - 10
        panel_height = graphics.SCREEN_HEIGHT - 150

        self.expressions = arcade.UIBoxLayout(
            width=panel_width,
            height=0,
            size_hint=(1, None),
            space_between=20,
            align='center')
        self.expressions.size_hint = (1, None)

        self.scroll = arcade.UIScrollArea(
            width=panel_width,
            height=panel_height,
            size_hint=(None, None),
            children=[self.expressions])

        self.anchor.add(self.scroll, anchor_x='center', anchor_y='center', align_x=-80, align_y=-200)

        self.text_info = text_info
        self.btn_info = self.anchor.add(arcade.UIFlatButton(
                                        text='i',
                                        width=50,
                                        style=graphics.BUTTON_UI_STYLE),
                                    anchor_x='right', anchor_y='top',
                                    align_x=-10, align_y=-10)

        @self.btn_info.event('on_click')
        def show_info(e):
            self.anchor.add(graphics.InfoDialog(
<<<<<<< Updated upstream
                            title='Информация о задаче',
                            message_text=self.text_info,
                            button_text='Понятно'))

        print(f'Scrol {self.scroll.width}, {self.scroll.height}')
        print(f'Expessions {self.expressions.width}, {self.expressions.height}')
        self.create_expression(self.original_root)
=======
                title='Информация о задаче',
                message_text=text_info,
                button_text='Понятно'))

        self.btn_create_expr = self.anchor.add(
            arcade.UIFlatButton(
                text='+',
                width=50,
                style=graphics.BUTTON_UI_STYLE),
            anchor_x='right', anchor_y='bottom',
            align_x=-10, align_y=10)

        @self.btn_create_expr.event('on_click')
        def create_expression(e): self.show_input_dialog(self.add_expression)
>>>>>>> Stashed changes

    def show_input_dialog(self, func, title='Введите выражение'):
        dialog = graphics.InputDialog(self, func, title)
        self.anchor.add(dialog, anchor_x='center', anchor_y='center')

    def show_notification(self, text, duration=3.0):
        self.notification.add_notification(text, duration)

    def create_expression(self, root: nodes.Node):
        panel = ExpressionPanel(self, root, depth=0)
        self.expressions.add(panel, align='center')
        self.expressions.fit_content()
        if hasattr(self.scroll, 'do_layout'):
            self.scroll.do_layout()
        else:
            self.scroll.force_update()
        self.scroll.trigger_full_render()

    def update_panel(self, panel):
    # Удаляем старую панель из списка
        if panel in self.expressions.children:
            self.expressions.remove(panel)
    # Создаём новую панель на основе того же корня
        new_panel = ExpressionPanel(self, panel.root, panel.depth)
        self.expressions.add(new_panel, align='center')
        self.expressions.fit_content()
<<<<<<< Updated upstream
    # Обновляем скролл в зависимости от типа
        if hasattr(self.scroll, 'do_layout'):
            self.scroll.do_layout()      # для ScrollContainer
        else:
            self.scroll.force_update()   # для UIScrollArea
            self.scroll.trigger_full_render()


    def compleate_expression(self): pass
=======
        self.scroll.do_layout()
        self.scroll.trigger_full_render()
    # Обновляем ссылку на панель в EquationView, если нужно
        if hasattr(self, 'panel') and self.panel is panel:
            self.panel = new_panel

    def compleate_expression(self):
        self.anchor.add(graphics.InfoDialog('Задача решена', '', 'Ура!'))
>>>>>>> Stashed changes

######################################## Система Уведомлений ########################################

class Notification:
    def __init__(self, ui: arcade.UIManager):
        self.ui = ui
        self._widget = None
        self._timer = None

    def add_notification(self, text: str, duration=3.0):
        # Удаляем предыдущее уведомление
        if self._widget and self._widget.parent:
            self.ui.remove(self._widget)
        if self._timer:
            try:
                arcade.unschedule(self._timer)
            except:
                pass

        # Создаём новый виджет
        self._widget = self._make_widget(text)
        anchor = self.ui.add(arcade.UIAnchorLayout())
        anchor.add(self._widget, anchor_x='right', anchor_y='bottom', align_x=-20, align_y=-20)
        self._timer = arcade.schedule_once(lambda dt: self._fade_out(), duration)

    def _make_widget(self, text):
        class _Widget(arcade.UIWidget):
            def __init__(self):
                super().__init__(width=300, height=50)
                self.label = arcade.UILabel(
                    text=text,
                    font_size=14,
                    text_color=arcade.color.WHITE,
                    width=290,
                    multiline=True
                )
                self.label.x = 5
                self.label.y = 5
                self.add(self.label)
                self.bg_color = (0, 0, 0, 200)
                self._alpha = 255

            def set_alpha(self, alpha):
                self._alpha = alpha
                r, g, b, _ = self.bg_color
                self.bg_color = (r, g, b, alpha)
                # Меняем прозрачность текста
                self.label.color = (255, 255, 255, alpha)

            def do_render(self, surface):
                # Рисуем фон через arcade (surface не используется)
                # Вместо surface.fill используем arcade.draw_rectangle_filled
                # Но для простоты можно использовать UIWidget с background_color
                # Однако мы используем кастомный рендеринг, поэтому перерисуем фон
                # в стандартном методе on_draw? Вместо do_render лучше переопределить on_draw
                pass

            def on_draw(self):
                # Рисуем фон и текст
                arcade.draw_rectangle_filled(
                    self.x + self.width/2,
                    self.y + self.height/2,
                    self.width,
                    self.height,
                    self.bg_color
                )
                # Текст рисуется автоматически через self.label, так как он добавлен как дочерний

        return _Widget()

    def _fade_out(self):
        if not self._widget or not self._widget.parent:
            self._widget = None
            return
        steps = 30
        alpha_step = 255 / steps
        current_alpha = 255

        def update(dt):
            nonlocal current_alpha
            current_alpha -= alpha_step
            if current_alpha <= 0:
                if self._widget and self._widget.parent:
                    self.ui.remove(self._widget)
                self._widget = None
                return False
            if self._widget:
                self._widget.set_alpha(int(current_alpha))
            return True

        self._timer = arcade.schedule(update, 0.5 / steps)

######################################## Панель Отображения Примера ########################################

class ExpressionPanel(arcade.UIBoxLayout):
    def __init__(self, view: ExpressionView, root: nodes.Node, depth: int = 0):
        self.depth = depth
        self.font_size = graphics.get_font_size(depth)   # абсолютный размер
        super().__init__(
            vertical=False,
            space_between=2,
            size_hint=(None, None),
            size_hint_min=(100, 30)
        )
        self.view = view
        self.root = root
        self.build()
        print(f'Panel {self.width}, {self.height}')

    def build(self):
        self.clear()
        main_build(self, self.root, self.font_size)
        self.fit_content()
        self.trigger_full_render()

######################################## Кнопка Одного Узла ########################################

class NodeButton(arcade.UITextureButton):
    def __init__(self, panel: ExpressionPanel, node: nodes.Node, font_size_or_texture: int | arcade.Texture = None):
        if isinstance(font_size_or_texture, arcade.Texture):
            texture = font_size_or_texture
        else:
            # Если не передано – берём размер из панели
            sz = font_size_or_texture if font_size_or_texture is not None else panel.font_size
            # Гарантируем, что размер в допустимых пределах
            sz = max(8, min(24, sz))
            texture = graphics.create_token_texture(node, graphics.WHITE, sz)
        super().__init__(texture=texture)
        self.size_hint = (None, None)
        self.width = texture.width
        self.height = texture.height
        self.panel = panel
        self.node = node
        self.interaction_buttons = (arcade.MOUSE_BUTTON_LEFT, arcade.MOUSE_BUTTON_RIGHT)

    def on_click(self, event):
        match event.button:
            case arcade.MOUSE_BUTTON_LEFT:
                if isinstance(self.node, nodes.Operator):
                    self.node.work(self.node)
                    self.panel.view.update_panel(self.panel)
            case arcade.MOUSE_BUTTON_RIGHT:
                if self.node.actions:
                    x = event.x - 50
                    y = event.y + 300
                    self.panel.view.ui.add(ActionMenu(self.panel, self.node, x, y))

######################################## Список Свойств Узла ########################################

from functools import partial

class ActionMenu(arcade.UIMouseFilterMixin, arcade.UIBoxLayout):
    def __init__(self, panel: ExpressionPanel, node: nodes.Node, x: int, y: int):
        w, h = max([len(func.name) for func in node.actions]) * 13, 25
        super().__init__(x = x, y = y, width=w, height=h, vertical=True, space_between=1)
        for action in node.actions:
            btn = arcade.UIFlatButton(
                width=w, height=h, text=action.name,
                style=graphics.BUTTON_ACTION_MENU_STYLE)
            # Используем partial для передачи аргументов
            btn.on_click = partial(self._on_action_click, action, node, panel)
            self.add(btn)

    def _on_action_click(self, action: nodes.Action, node: nodes.Node, panel: ExpressionPanel, event):
        if action.interactive:
            panel.view.show_input_dialog(lambda root: action(node, root))
        else:
            action(node)
        panel.view.update_panel(panel)
        panel.view.ui.remove(self)

    def on_event(self, event):
        if isinstance(event, arcade.UIMousePressEvent):
            if self.rect.point_in_rect((event.x, event.y)):
                return super().on_event(event)
            self.parent.remove(self)
            return True
        return super().on_event(event)

######################################## Главная Функция Построения Выражения ########################################

def main_build(panel: ExpressionPanel, root: nodes.Node, font_size: float):
    i = 0
    toks  = list(root)
    lenth = len(toks)
    while i < lenth:
        token = toks[i]
        if isinstance(token, tokens.VisibleToken):
            if isinstance(token, tokens.Bracket):
                bracket_texture = graphics.create_token_texture(token, graphics.YELLOW, font_size)
                bracket = arcade.UIImage(texture=bracket_texture)
                bracket.size_hint = (None, None)
                bracket.width = bracket_texture.width
                bracket.height = bracket_texture.height
                panel.add(bracket)
            elif isinstance(token, nodes.Node):
                panel.add(NodeButton(panel, token, font_size))
        elif isinstance(token, tokens.NestedBeginToken):
            operator = token.operator
            NESTED_OPERATORS[type(operator)](panel, operator, font_size)
            i = toks.index(token.pair)
        i+=1

def log_build(panel: ExpressionPanel, root: nodes.Log, font_size: float):
    grid = arcade.UIGridLayout(
        column_count=2,
        row_count=2,
        horizontal_spacing=5,
        vertical_spacing=2)
    log_btn = NodeButton(panel, root, font_size)
    base_panel = ExpressionPanel(panel.view, root.one, panel.depth + 1)   # depth+1
    grid.add(log_btn, column=0, row=0, row_span=2)
    grid.add(base_panel, column=1, row=1)
    panel.add(grid)

def div_build(panel: ExpressionPanel, root: nodes.Div, font_size: float):
    fraction = arcade.UIBoxLayout(vertical=True, space_between=5)
    numerator = ExpressionPanel(panel.view, root.one, panel.depth + 1)
    denominator = ExpressionPanel(panel.view, root.two, panel.depth + 1)
    line_texture = graphics.create_line_texture(1, 5 * font_size, arcade.color.WHITE)
    line_button = NodeButton(panel, root, font_size_or_texture=line_texture)
    line_button.size_hint = (1, None)
    fraction.add(numerator)
    fraction.add(line_button)
    fraction.add(denominator)
    panel.add(fraction)

def pow_build(panel: ExpressionPanel, root: nodes.Pow, font_size: float):
    grid = arcade.UIGridLayout(
        column_count=2,
        row_count=2,
        horizontal_spacing=5,
        vertical_spacing=2)
    top_right = arcade.UIBoxLayout(vertical=False, space_between=2)
    pow_btn = NodeButton(panel, root, font_size * 0.8)
    exp_panel = ExpressionPanel(panel.view, root.two, panel.depth + 1)
    top_right.add(pow_btn)
    top_right.add(exp_panel)
    base_panel = ExpressionPanel(panel.view, root.one, panel.depth + 1)
    grid.add(base_panel, column=0, row=0, row_span=2)
    grid.add(top_right, column=1, row=0)
    panel.add(grid)

NESTED_OPERATORS: dict[type[nodes.Operator], function] = {
    nodes.Log : log_build,
    nodes.Div : div_build,
    nodes.Pow : pow_build
}
