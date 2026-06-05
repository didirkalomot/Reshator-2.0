from __future__ import annotations
from game import arcade_import as arcade
from game.views.base_mode import BaseMode
from game import graphics
from mechanics import nodes, tokens, parse

# =============================================================================
# СИСТЕМА ФУНКЦИЙ ГЕНЕРАЦИИ ДЛЯ СПЕЦИАЛЬНЫХ ОПЕРАТОРОВ
# =============================================================================

BUILD_FUNCTIONS: dict[type, function] = {}


def register_build_function(token_class: type):
    """Декоратор для регистрации функции построения."""
    def decorator(func: function):
        BUILD_FUNCTIONS[token_class] = func
        return func
    return decorator


class SandboxMode(BaseMode):
    """Класс окна песочницы."""
    def __init__(self):
        super().__init__()
        # Пример выражения: 1 / 2. Замени строку на любую другую для теста.
        self.expression = ExpressionPanel(self.ui, parse.infix_to_tree('1 / 2'))
        
        anchor = arcade.UIAnchorLayout(width=self.width-100, height=self.height-100)
        anchor.add(self.expression, anchor_x="center", anchor_y="center")
        self.ui.add(anchor)
        
        self.expression.build()


class ExpressionPanel(arcade.UIBoxLayout):
    """Панель для отображения математического выражения."""
    def __init__(self, manager: arcade.UIManager, root: nodes.Node):
        super().__init__(vertical=False, space_between=5)
        self.manager = manager
        self.root = root
        
    def build(self):
        """Очищает панель и строит выражение заново."""
        self.clear()
        build_expression(self, list(self.root))
        self.fit_content()


def _create_fake_panel():
    """Создаёт заглушку панели для рекурсивных вызовов."""
    class FakePanel:
        def __init__(self):
            self.children = []
        def add(self, child):
            self.children.append(child)
        def clear(self):
            self.children = []
    return FakePanel()


def build_expression(panel: ExpressionPanel, token_list: list, 
                     start_index: int = 0, end_index: int | None = None) -> int:
    """Рекурсивная функция построения UI из списка токенов."""
    if end_index is None:
        end_index = len(token_list)
    
    index = start_index
    while index < end_index:
        token = token_list[index]
        
        # Обработка начала layout-скобки [
        if isinstance(token, tokens.LayoutBeginToken):
            pair_index = index + 1
            while pair_index < end_index and token_list[pair_index] is not token.pair:
                pair_index += 1
            
            build_expression(panel, token_list, index + 1, pair_index)
            index = pair_index + 1
            continue
        
        # Обработка конца layout-скобки ]
        if isinstance(token, tokens.LayoutEndToken):
            return index + 1
        
        # Проверка специальных операторов
        token_type = type(token)
        if token_type in BUILD_FUNCTIONS:
            index = BUILD_FUNCTIONS[token_type](index, token_list, panel)
            continue
        
        # Обычные токены
        if isinstance(token, tokens.VisibleToken):
            if isinstance(token, tokens.Bracket):
                panel.add(arcade.UIImage(texture=graphics.create_token_texture(token, graphics.YELLOW)))
            elif isinstance(token, nodes.Node):
                panel.add(NodeButton(panel, token))
        
        index += 1
    
    return index


# =============================================================================
# ФУНКЦИИ ГЕНЕРАЦИИ (ДРОБИ, СТЕПЕНИ, ЛОГАРИФМЫ)
# =============================================================================

@register_build_function(nodes.Div)
def build_div(index: int, token_list: list, panel: ExpressionPanel) -> int:
    """Построение дроби: вертикальный контейнер (числитель, черта, знаменатель)."""
    div_node = token_list[index]
    
    # Поиск числителя (идём назад до скобки)
    numerator_end_index = index - 1
    while numerator_end_index >= 0 and not isinstance(token_list[numerator_end_index], tokens.LayoutEndToken):
        numerator_end_index -= 1
    
    if numerator_end_index >= 0 and isinstance(token_list[numerator_end_index], tokens.LayoutEndToken):
        numerator_begin_token = token_list[numerator_end_index].pair
        numerator_start_index = token_list.index(numerator_begin_token)
    else:
        numerator_start_index = index - 1
        numerator_end_index = index - 1
    
    # Поиск знаменателя (идём вперёд)
    denominator_start_index = index + 1
    while denominator_start_index < len(token_list) and not isinstance(token_list[denominator_start_index], tokens.LayoutBeginToken):
        denominator_start_index += 1
    
    denominator_end_index = denominator_start_index + 1
    while denominator_end_index < len(token_list) and not isinstance(token_list[denominator_end_index], tokens.LayoutEndToken):
        denominator_end_index += 1
    
    # Сборка UI
    fraction_container = arcade.UIBoxLayout(vertical=True, space_between=2)
    
    numerator_temp_panel = _create_fake_panel()
    build_expression(numerator_temp_panel, token_list, numerator_start_index + 1, numerator_end_index)
    for child in numerator_temp_panel.children:
        fraction_container.add(child)
    
    divider = arcade.UISpace(width=50, height=2)
    divider._background_color = graphics.WHITE
    fraction_container.add(divider)
    
    denominator_temp_panel = _create_fake_panel()
    build_expression(denominator_temp_panel, token_list, denominator_start_index + 1, denominator_end_index)
    for child in denominator_temp_panel.children:
        fraction_container.add(child)
    
    panel.add(fraction_container)
    return denominator_end_index + 1


@register_build_function(nodes.Pow)
def build_pow(index: int, token_list: list, panel: ExpressionPanel) -> int:
    """Построение степени: основание + приподнятый показатель."""
    pow_node = token_list[index]
    
    exponent_start_index = index + 1
    while exponent_start_index < len(token_list) and not isinstance(token_list[exponent_start_index], tokens.LayoutBeginToken):
        exponent_start_index += 1
    
    exponent_end_index = exponent_start_index + 1
    while exponent_end_index < len(token_list) and not isinstance(token_list[exponent_end_index], tokens.LayoutEndToken):
        exponent_end_index += 1
    
    pow_container = arcade.UIBoxLayout(vertical=False, space_between=0)
    base_button = NodeButton(panel, pow_node.one)
    pow_container.add(base_button)
    
    exponent_wrapper = arcade.UIBoxLayout(vertical=True, space_between=0)
    spacer = arcade.UISpace(width=1, height=5)
    exponent_wrapper.add(spacer)
    
    exponent_temp_panel = _create_fake_panel()
    build_expression(exponent_temp_panel, token_list, exponent_start_index + 1, exponent_end_index)
    for child in exponent_temp_panel.children:
        exponent_wrapper.add(child)
    
    pow_container.add(exponent_wrapper)
    panel.add(pow_container)
    return exponent_end_index + 1


@register_build_function(nodes.Log)
def build_log(index: int, token_list: list, panel: ExpressionPanel) -> int:
    """Построение логарифма: log(аргумент) с основанием снизу."""
    log_node = token_list[index]
    
    args_start_index = index + 1
    while args_start_index < len(token_list) and not isinstance(token_list[args_start_index], tokens.FunctionBracketLeftToken):
        args_start_index += 1
    
    args_end_index = args_start_index + 1
    bracket_depth = 1
    while args_end_index < len(token_list) and bracket_depth > 0:
        if isinstance(token_list[args_end_index], tokens.FunctionBracketLeftToken):
            bracket_depth += 1
        elif isinstance(token_list[args_end_index], tokens.FunctionBracketRightToken):
            bracket_depth -= 1
        args_end_index += 1
    
    log_container = arcade.UIBoxLayout(vertical=True, space_between=0)
    top_row = arcade.UIBoxLayout(vertical=False, space_between=2)
    
    log_button = NodeButton(panel, log_node)
    top_row.add(log_button)
    
    arg_temp_panel = _create_fake_panel()
    build_expression(arg_temp_panel, token_list, args_start_index + 1, args_end_index - 1)
    for child in arg_temp_panel.children:
        top_row.add(child)
    
    log_container.add(top_row)
    
    base_label = arcade.UILabel(text=str(log_node.one), font_size=10, color=graphics.WHITE)
    log_container.add(base_label)
    
    panel.add(log_container)
    return args_end_index


@register_build_function(nodes.Equal)
def build_equal(index: int, token_list: list, panel: ExpressionPanel) -> int:
    """Построение знака равенства."""
    equal_node = token_list[index]
    panel.add(NodeButton(panel, equal_node))
    return index + 1


# =============================================================================
# ВСПОМОГАТЕЛЬНЫЕ КЛАССЫ
# =============================================================================

class ActionMenu(arcade.UIMouseFilterMixin, arcade.UIBoxLayout):
    def __init__(self, panel: ExpressionPanel, node: nodes.Node, x: int, y: int):
        super().__init__(vertical=True, space_between=1)
        self.x, self.y = x, y
        w, h = max([len(func.name) for func in node.actions]) * 13, 25
        for func in node.actions:
            btn = arcade.UIFlatButton(width=w, height=h, text=func.name, style=graphics.BUTTON_ACTION_MENU_STYLE)
            btn.on_click = lambda e, f=func, n=node, p=panel: (f(n), p.build(), p.manager.remove(self))
            self.add(btn)

    def on_event(self, event):
        if isinstance(event, arcade.UIMousePressEvent):
            if self.rect.point_in_rect((event.x, event.y)):
                return super().on_event(event)
            self.parent.remove(self)
            return True
        return super().on_event(event)


class NodeButton(arcade.UITextureButton):
    def __init__(self, panel: ExpressionPanel, node: nodes.Node):
        super().__init__(texture=graphics.create_token_texture(node))
        self.panel = panel
        self.node = node
        self.interaction_buttons = (arcade.MOUSE_BUTTON_LEFT, arcade.MOUSE_BUTTON_RIGHT)

    def on_click(self, event):
        match event.button:
            case arcade.MOUSE_BUTTON_LEFT: 
                if isinstance(self.node, nodes.Operator):
                    self.node.work(self.node)
                    self.panel.build()
            case arcade.MOUSE_BUTTON_RIGHT:
                if self.node.actions:
                    self.panel.manager.add(ActionMenu(self.panel, self.node, event.x, event.y))
