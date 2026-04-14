from __future__ import annotations
from graphics import arcade_import as arcade
from graphics.views.base_mode import BaseMode
from graphics import styles
from mechanics import nodes, tokens, parse
from copy import deepcopy

######################################## Главный Класс - Режим ########################################

class SandboxMode(BaseMode):
    def __init__(self):
        super().__init__()
        self.root = parse.infix_to_tree('(3 + 4)/sin(x)*7')
        self.panels = []
        
        self.panels_layout = arcade.UIBoxLayout(vertical=True, space_between=20)
        scroll = arcade.UIScrollArea(width=900, height=500)
        scroll.add(self.panels_layout)
        anchor = self.ui.add(arcade.UIAnchorLayout())
        anchor.add(scroll, anchor_x="center", anchor_y="center", align_y=20)
        
        add_btn = arcade.UIFlatButton(text="+", width=50, height=50)
        @add_btn.event("on_click")
        def on_add(event): self.add_panel()
        anchor.add(add_btn, anchor_x="right", anchor_y="bottom", align_x=-20, align_y=-20)
        self.add_panel()
    
    def add_panel(self):
        if self.panels: root = self.panels[0].root
        else: root = deepcopy(self.root)
        panel = ExpressionPanel(self, root)
        self.panels.append(panel)
        self.panels_layout.add(panel)

######################################## Класс, Описывающий Один Пример ########################################

class ExpressionPanel(arcade.UIWidget):
    def __init__(self, sandbox: SandboxMode, root: nodes.Node):
        super().__init__()
        self.sandbox = sandbox
        self.root = root
        self.layout = None
        self.build()
    
    def build(self):
        if self.layout:
            self.layout.kill()
        self.layout = create_horizontal_layout(self, list(self.root))
        self.add(self.layout)
        self.width = self.layout.width
        self.height = self.layout.height

######################################## Класс Для Одной Горизонтальной Группы ########################################

class HorizontalLayout(arcade.UIBoxLayout):
    def __init__(self, expression_panel: ExpressionPanel, scale_coeff: float = 1, space_between: int = 5):
        super().__init__(vertical=False, space_between=space_between)
        self.scale_coeff = scale_coeff
        self.expression_panel = expression_panel

    def scale(self, factor: float):
        self.scale_coeff = self.scale_coeff * factor
        self.space_between = int(self.space_between * factor)
        for child in self.children: child.scale(factor)

    def add(self, child, *args, **kwargs):
        if isinstance(child, arcade.UIWidget): child.scale(self.scale_coeff)
        super().add(child, *args, **kwargs)

######################################## Функция Генерации Горизонтальной Группы ########################################

def create_horizontal_layout(expression_panel: ExpressionPanel, tokens_list: list[tokens.Token], scale_coeff: float = 1) -> HorizontalLayout:
    panel = HorizontalLayout(expression_panel, scale_coeff)
    index = 0
    while index < len(tokens_list):
        token = tokens_list[index]
        if isinstance(token, tokens.Bracket):
            texture = arcade.create_text_sprite(str(token), styles.COLOR_MY_YELLOW, 20).texture
            widget = arcade.UIImage(texture=texture, width=texture.width, height=texture.height)
            panel.add(widget)
            index += 1
            continue
        if isinstance(token, tokens.LayoutBeginToken): 
            index = tokens_list.index(token.pair) + 1; continue
        if isinstance(token, nodes.Node):
            if token not in build_functions: panel.add(NodeButton(expression_panel, token))
            else: index = build_functions[token.__class__](panel, tokens_list, index); continue
        index += 1
    if panel.children:
        width = sum(child.width for child in panel.children) + panel._space_between * (len(panel.children) - 1)
        height = max(child.height for child in panel.children)
        panel.width, panel.height = width, height
    return panel

######################################## Функции Для Не Типпичной Генерации ########################################

def create_div_button(
        panel: HorizontalLayout, 
        tokens_list: list[tokens.Token], 
        index_div: int) -> int:
    index_pair_prev_bracket_layout = tokens_list.index(tokens_list[index_div - 1].pair)
    index_pair_next_bracket_laout = tokens_list.index(tokens_list[index_div + 1].pair)
    numerator = tokens_list[index_pair_prev_bracket_layout + 1:index_div - 1]
    denominator = tokens_list[index_div + 1:index_pair_next_bracket_laout]
    numerator = create_horizontal_layout(panel.expression_panel, numerator, panel.scale_coeff * 0.5)
    denominator = create_horizontal_layout(panel.expression_panel, denominator, panel.scale_coeff * 0.5)
    div = tokens_list[index_div]
    panel.add(DivButton(panel.expression_panel, div, numerator, denominator))
    return index_pair_next_bracket_laout + 1

def create_pow_button(
        panel: HorizontalLayout,
        tokens_list: list[tokens.Token],
        index_pow: int) -> int:
    idex_pair_bracket_layout = tokens_list.index(tokens_list[index_pow + 1].pair)
    exponent = tokens_list[index_pow + 1:idex_pair_bracket_layout]
    power = tokens_list[index_pow]
    panel.add(PowButton(panel.expression_panel, power, exponent))
    return idex_pair_bracket_layout + 1

build_functions = { 
    nodes.Div : create_div_button,
    nodes.Pow : create_pow_button
}

######################################## Класс Для Меню Actions ########################################

class ActionsMenu(arcade.UIBoxLayout):
    def __init__(self, node: nodes.Node, panel: ExpressionPanel):
        super().__init__(vertical=True, space_between=2)
        self.node = node
        self.panel = panel
        for name in node.actions:
            btn = arcade.UIFlatButton(text=name, width=150, height=30, font_size=12)
            @btn.event("on_click")
            def on_click(event, n=name):
                self.node.do_action(n)
                self.kill()
                self.panel.rebuild()
            self.add(btn)

######################################## Класс - Кнопка Для Одного Узла ########################################

class NodeButton(arcade.UIFlatButton):
    def __init__(self, expression_panel: ExpressionPanel, node: nodes.Node):
        texture = arcade.create_text_sprite(str(node), font_size=20).texture
        super().__init__(texture=texture, width=texture.width, height=texture.height)
        self.expression_panel = expression_panel
        self.node = node
        self.menu = None
    
    def on_click(self, event):
        if isinstance(self.node, nodes.Operator):
            self.node.work(); self.expression_panel.build()
    
    def on_right_click(self, event):
        if self.menu:
            self.menu.kill()
            self.menu = None
        else:
            self.menu = ActionsMenu(self.expression_panel, self.node)
            self.expression_panel.sandbox.ui.add(self.menu)
            self.menu.position = (self.right + 5, self.top)

######################################## Не Типичные Классы - Кнопки ########################################

class DivButton(NodeButton):
    def __init__(self, panel: ExpressionPanel, node: nodes.Div, numerator: HorizontalLayout, denominator: HorizontalLayout):
        texture = arcade.SpriteSolidColor(max(numerator.width, denominator.width), 3, color=styles.BLACK).texture
        super(arcade.UIFlatButton).__init__(texture=texture, width=texture.width, height=texture.height)

        self.panel = panel; self.node = node; self.menu = None
        self.numerator: HorizontalLayout = numerator
        self.denominator: HorizontalLayout = denominator

        self.numerator.x = self.x + (self.width - self.numerator.width) / 2
        self.numerator.y = self.y + self.height + 5
        self.denominator.x = self.x + (self.width - self.denominator.width) / 2
        self.denominator.y = self.y - self.denominator.height - 5

class PowButton(NodeButton):
    def __init__(self, panel: ExpressionPanel, node: nodes.Pow, exponent: HorizontalLayout):
        texture = arcade.create_text_sprite('^', font_size=10, color=styles.BLACK).texture
        super(arcade.UIFlatButton).__init__(texture=texture, width=texture.width, height=texture.height)
        
        self.panel = panel
        self.node = node
        self.menu = None
        self.exponent = exponent
        
        self.y += 5
        self.exponent.x = self.x + self.width + 5
        self.exponent.y = self.y + self.height * 0.5