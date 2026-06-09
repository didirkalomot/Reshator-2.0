from __future__ import annotations
from game import arcade_import as arcade
from game.views.base_mode import BaseMode
from game import graphics
from mechanics import nodes, tokens, parse
from copy import deepcopy

######################################## Основные Классы ########################################

class SandboxMode(BaseMode):
    def __init__(self):
        super().__init__()
        string = '(x * x) / (2 + 4 + x)'
        self.expression = ExpressionPanel(self.ui, parse.create_tree(string))
        anchor = arcade.UIAnchorLayout()
        anchor.add(self.expression, anchor_x='center', anchor_y='center')
        self.ui.add(anchor)

class ExpressionPanel(arcade.UIBoxLayout):
    def __init__(self, 
                 ui: arcade.UIManager, 
                 root: nodes.Node, 
                 font_size: float = 1,
                 main_panel: ExpressionPanel = None):
        super().__init__(vertical=False, space_between=5)
        self.ui = ui
        self.root = root
        self.font_size = font_size
        self.main_panel = main_panel or self
        self.build()

    def build(self):
        self.clear()
        main_build(self, self.root, self.font_size)
        self.do_layout()

class NodeButton(arcade.UITextureButton):
    def __init__(self, 
                 panel: ExpressionPanel, 
                 node: nodes.Node, 
                 font_size_or_texture: float | arcade.Texture = 1):
        if isinstance(font_size_or_texture, arcade.Texture): super().__init__(texture=font_size_or_texture)
        else: super().__init__(texture=graphics.create_token_texture(node, graphics.WHITE, font_size_or_texture)) 
        self.panel = panel
        self.node = node
        self.interaction_buttons = (arcade.MOUSE_BUTTON_LEFT, arcade.MOUSE_BUTTON_RIGHT)
        
    def on_click(self, event):
        match event.button:
            case arcade.MOUSE_BUTTON_LEFT: 
                if isinstance(self.node, nodes.Operator):
                    self.node.work(self.node)
                    self.panel.main_panel.build()
            case arcade.MOUSE_BUTTON_RIGHT:
                if self.node.actions: 
                    self.panel.ui.add(ActionMenu(self.panel, self.node, event.x, event.y))

class ActionMenu(arcade.UIMouseFilterMixin, arcade.UIBoxLayout):
    def __init__(self, panel: ExpressionPanel, node: nodes.Node, x: int, y: int):
        super().__init__(vertical=True, space_between=1)
        self.x, self.y = x, y
        w, h = max([len(func.name) for func in node.actions]) * 13, 25
        for func in node.actions:
            btn = arcade.UIFlatButton(
                width=w, height=h, text=func.name, 
                style=graphics.BUTTON_ACTION_MENU_STYLE)
            btn.on_click = lambda e, f=func, n=node, p=panel: (f(n), p.main_panel.build(), p.ui.remove(self))
            self.add(btn)

    def on_event(self, event):
        if isinstance(event, arcade.UIMousePressEvent):
            if self.rect.point_in_rect((event.x, event.y)):
                return super().on_event(event)
            self.parent.remove(self)
            return True
        return super().on_event(event)

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
    base_panel = ExpressionPanel(panel.ui, root.one, font_size * 0.8, panel.main_panel)
    grid.add(log_btn, column=0, row=0, row_span=2)
    grid.add(base_panel, column=1, row=1)
    panel.add(grid)

def div_build(panel: ExpressionPanel, root: nodes.Div, font_size: float):
    fraction = arcade.UIBoxLayout(vertical=True, space_between=5)
    numerator = ExpressionPanel(panel.ui, root.one, font_size * 0.8, panel.main_panel)
    denominator = ExpressionPanel(panel.ui, root.two, font_size * 0.8, panel.main_panel)
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
    exp_panel = ExpressionPanel(panel.ui, root.two, font_size * 0.8, panel.main_panel)
    top_right.add(pow_btn)
    top_right.add(exp_panel)
    base_panel = ExpressionPanel(panel.ui, root.one, font_size, panel.main_panel)
    grid.add(base_panel, column=0, row=0, row_span=2)
    grid.add(top_right, column=1, row=0)
    panel.add(grid)

NESTED_OPERATORS: dict[type[nodes.Operator], function] = {    
    nodes.Log : log_build,
    nodes.Div : div_build,
    nodes.Pow : pow_build
}

