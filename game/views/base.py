from __future__ import annotations
from game import arcade_import as arcade
from game import graphics
from mechanics import nodes, tokens, parse, exceptions
from copy import deepcopy

######################################## Базовый Класс Режима ########################################

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

######################################## Класс Режима С Выражением ########################################

class ExpressionMode(BaseMode):
    def __init__(self, root_or_str: nodes.Node | str):
        super().__init__()
        if isinstance(root_or_str, nodes.Node): self.original_root = root_or_str
        else: self.original_root = parse.create_tree(root_or_str)
        self.expression = ExpressionPanel(self, deepcopy(self.original_root))
        anchor = arcade.UIAnchorLayout()
        anchor.add(self.expression, anchor_x='center', anchor_y='center')
        self.ui.add(anchor)
        self.notification = Notification(self.ui)

    def show_input_dialog(self, action, node):
        dialog = InputDialog(action, node, self)
        anchor = self.ui.add(arcade.UIAnchorLayout())
        anchor.add(dialog, anchor_x="center", anchor_y="center")

    def show_notification(self, text, duration=3.0):
        self.notification.add_notification(text, duration) 

######################################## Ввод Выражения ########################################
    
class InputDialog(arcade.UIBoxLayout):
    def __init__(self, 
                 action: nodes.Action, 
                 node: nodes.Node, 
                 view: ExpressionMode, 
                 title: str = 'Введите выражение'):
        super().__init__(vertical=True, space_between=10, width=300)
        self.add(arcade.UILabel(text=title, font_size=18, text_color=arcade.color.WHITE))
        self.input = arcade.UIInputText(width=280, height=30)
        self.add(self.input)
        row = arcade.UIBoxLayout(vertical=False, space_between=10)
        ok_btn = arcade.UIFlatButton(text='Готово', width=100)
        cancel_btn = arcade.UIFlatButton(text='Отмена', width=100)

        @ok_btn.event('on_click')
        def on_ok(e):
            expr = self.input.text.strip()
            try:
                tree = parse.create_tree(expr)
                action(node, tree)
                view.expression.build()
            except exceptions.ParseError as err: view.show_notification(err, 2)
            self.parent.remove(self)
            
        @cancel_btn.event('on_click')
        def on_cancel(e): self.parent.remove(self)

        row.add(ok_btn)
        row.add(cancel_btn)
        self.add(row)
        self.bg_color = (40, 40, 40, 220)
        self.with_padding(all=10)

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
            arcade.unschedule(self._timer)

        # Создаём новый виджет (внутренний класс или просто локальный)
        self._widget = self._make_widget(text)
        anchor = self.ui.add(arcade.UIAnchorLayout())
        anchor.add(self._widget, anchor_x="right", anchor_y="bottom", offset_x=-20, offset_y=20)
        self._timer = arcade.clock.schedule_once(lambda dt: self._fade_out(), duration)

    def _make_widget(self, text):
        class _Widget(arcade.UIWidget):
            def __init__(self):
                super().__init__(width=300, height=50)
                self.label = arcade.UILabel(text=text, font_size=14, text_color=arcade.color.WHITE,
                                            width=290, multiline=True)
                self.label.position = (5, 5)
                self.add(self.label)
                self.bg_color = (0, 0, 0, 200)
                self._alpha = 255

            def set_alpha(self, alpha):
                self._alpha = alpha
                r, g, b, _ = self.bg_color
                self.bg_color = (r, g, b, alpha)
                self.label.color = (255, 255, 255, alpha)

            def do_render(self, surface):
                surface.fill(self.bg_color)
                super().do_render(surface)
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
                self.ui.remove(self._widget)
                self._widget = None
                return False
            self._widget.set_alpha(int(current_alpha))
            return True
        arcade.clock.schedule_interval(update, 0.5 / steps, steps)

######################################## Панель Отображения Примера ########################################

class ExpressionPanel(arcade.UIBoxLayout):
    def __init__(self, 
                 view: ExpressionMode, 
                 root: nodes.Node, 
                 font_size: float = 1):
        super().__init__(vertical=False, space_between=5)
        self.view = view
        self.root = root
        self.font_size = font_size
        self.build()

    def build(self):
        self.clear()
        main_build(self, self.root, self.font_size)
        self.do_layout()

######################################## Кнопка Одного Узла ########################################

class NodeButton(arcade.UITextureButton):
    def __init__(self, 
                 view: ExpressionMode, 
                 node: nodes.Node, 
                 font_size_or_texture: float | arcade.Texture = 1):
        if isinstance(font_size_or_texture, arcade.Texture): super().__init__(texture=font_size_or_texture)
        else: super().__init__(texture=graphics.create_token_texture(node, graphics.WHITE, font_size_or_texture)) 
        self.view = view
        self.node = node
        self.interaction_buttons = (arcade.MOUSE_BUTTON_LEFT, arcade.MOUSE_BUTTON_RIGHT)
        
    def on_click(self, event):
        match event.button:
            case arcade.MOUSE_BUTTON_LEFT: 
                if isinstance(self.node, nodes.Operator):
                    self.node.work(self.node)
                    self.view.expression.build()
            case arcade.MOUSE_BUTTON_RIGHT:
                if self.node.actions: 
                    self.view.ui.add(ActionMenu(self.view, self.node, event.x, event.y))

######################################## Список Свойств Узла ########################################

class ActionMenu(arcade.UIMouseFilterMixin, arcade.UIBoxLayout):
    def __init__(self, view: ExpressionMode, node: nodes.Node, x: int, y: int):
        super().__init__(vertical=True, space_between=1)
        self.x, self.y = x, y
        w, h = max([len(func.name) for func in node.actions]) * 13, 25
        for func in node.actions:
            btn = arcade.UIFlatButton(
                width=w, height=h, text=func.name, 
                style=graphics.BUTTON_ACTION_MENU_STYLE)
            btn.on_click = lambda e, f=func, n=node, v=view: (f(n), v.expression.build(), v.ui.remove(self))
            self.add(btn)

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
                bracket = arcade.UIImage(
                        texture=graphics.create_token_texture(
                            token, 
                            graphics.YELLOW, 
                            font_size))
                panel.add(bracket)
            elif isinstance(token, nodes.Node):
                panel.add(NodeButton(panel.view, token, font_size))
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
    base_panel = ExpressionPanel(panel.view, root.one, font_size * 0.8)
    grid.add(log_btn, column=0, row=0, row_span=2)
    grid.add(base_panel, column=1, row=1)
    panel.add(grid)

def div_build(panel: ExpressionPanel, root: nodes.Div, font_size: float):
    fraction = arcade.UIBoxLayout(vertical=True, space_between=5)
    numerator = ExpressionPanel(panel.view, root.one, font_size * 0.8)
    denominator = ExpressionPanel(panel.view, root.two, font_size * 0.8)
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
    exp_panel = ExpressionPanel(panel.view, root.two, font_size * 0.8)
    top_right.add(pow_btn)
    top_right.add(exp_panel)
    base_panel = ExpressionPanel(panel.view, root.one, font_size)
    grid.add(base_panel, column=0, row=0, row_span=2)
    grid.add(top_right, column=1, row=0)
    panel.add(grid)

NESTED_OPERATORS: dict[type[nodes.Operator], function] = {    
    nodes.Log : log_build,
    nodes.Div : div_build,
    nodes.Pow : pow_build
}