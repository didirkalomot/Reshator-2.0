from __future__ import annotations
from game import arcade_import as arcade
from game.views.base_mode import BaseMode
from game import graphics
from mechanics import nodes, tokens, parse
from copy import deepcopy

BUILD_FUNCTIONS = {}

class SandboxMode(BaseMode):
    def __init__(self):
        super().__init__()
        self.expression = ExpressionPanel(self.ui, parse.infix_to_tree('(1 + 2) * 3'))
        anchor = arcade.UIAnchorLayout(width=self.width-100, height=self.height-100)
        anchor.add(self.expression, anchor_x="center", anchor_y="center")
        self.ui.add(anchor)
        self.expression.build()

class ExpressionPanel(arcade.UIBoxLayout):
    def __init__(self, manager: arcade.UIManager, root: nodes.Node):
        super().__init__(vertical=False, space_between=5)
        self.manager = manager
        self.root = root
        
    def build(self):
        self.clear()
        for token in self.root:
            if isinstance(token, tokens.VisibleToken):
                if isinstance(token, tokens.Bracket):
                    self.add(arcade.UIImage(texture=graphics.create_token_texture(token, graphics.YELLOW)))
                elif isinstance(token, nodes.Node):
                    self.add(NodeButton(self, token))
        self.fit_content()

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
                    self.node.work()
                    self.panel.build()
            case arcade.MOUSE_BUTTON_RIGHT:
                self.panel.manager.add(ActionMenu(self.panel, self.node, event.x, event.y))