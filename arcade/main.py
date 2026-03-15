import arcade
import parse
from nodes import Node

class BracketToken:
    def __init__(self, symbol: str, position: int):
        self.symbol = symbol
        self.position = position

    def __repr__(self):
        return f"Bracket('{self.symbol}', {self.position})"

WIDTH = 1100
HEIGHT = 600
CENTER = (WIDTH // 2, HEIGHT // 2)

arcade.load_font('resourses\BetterVCR\BetterVCR.ttf') 

FONT_SIZE = 25.0
SYMBOL_SIZE= [24.75, 33]

class ButtonSymbol:
    def __init__(self, text: str, x: float, y: float, node: Node = None, action_name: str = None):
        self.text = text
        self.center_x = x
        self.center_y = y
        self.node = node
        self.action_name = action_name
        self.width = SYMBOL_SIZE[0] * len(text) + 10
        self.height = SYMBOL_SIZE[1] + 10
        self.selected = False

    def draw(self):
        color = arcade.color.YELLOW if self.selected else arcade.color.WHITE
        text = arcade.Text(self.text, self.center_x, self.center_y, color, FONT_SIZE)
        text.draw()
        
    def collides_with_point(self, x: float, y: float) -> bool:
        return (abs(self.center_x - x) < self.width / 2 and
                abs(self.center_y - y) < self.height / 2)

class ExampleSolution(arcade.View):
    def __init__(self, root: Node):
        super().__init__()
        self.root: Node | None = root
        self.buttons: list[ButtonSymbol] = []          
        self.action_buttons: list[ButtonSymbol] = []   
        self.selected_node: Node | None = None
        self.selected_nodes: list[Node] = [] # вот тут хранятся узлы
    
    def make_symbols(self):
        self.buttons.clear()
        if self.root is None: return

        tokens = list(self.root)
        x, y = 50, HEIGHT // 2
        for i, token in enumerate(tokens):
            if isinstance(token, Node):
                btn = ButtonSymbol(str(token), x, y, node=token)
            else:
            # для скобок создаём уникальный объект с позицией
                btn = ButtonSymbol(str(token), x, y, node=BracketToken(token, i))
            self.buttons.append(btn)
            x += btn.width + 5
            if x > WIDTH - 50:
                x = 50
                y -= 50
            
    def reset(self):
        self.make_symbols()
        self.selected_node = None
        self.selected_nodes.clear()
        self.action_buttons.clear()
        
    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        for btn in self.buttons:
            if btn.node in self.selected_nodes: color = arcade.color.ORANGE
            elif btn.selected: color = arcade.color.YELLOW
            else: color = arcade.color.WHITE

            text = arcade.Text(btn.text, btn.center_x, btn.center_y, color, FONT_SIZE)
            text.draw()

        for btn in self.action_buttons:
            btn.draw()   #

        arcade.draw_text("R - рестарт | ESC - выход", 10, HEIGHT-30, arcade.color.WHITE, 16)
          
    def on_update(self, delta_time):pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.reset()
        elif key == arcade.key.ESCAPE:
            self.selected_node = None
            self.action_buttons.clear()
            self.selected_nodes.clear()

    def on_key_release(self, key, modifiers):pass

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in self.buttons + self.action_buttons:
            btn.selected = btn.collides_with_point(x, y)
        
    def on_mouse_release(self, x, y, button, key_modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

    # клик по кнопке действия (только для узлов)
        for btn in self.action_buttons:
            if btn.selected and btn.action_name and isinstance(btn.node, Node):
                btn.node.do_action(btn.action_name)
                self.make_symbols()
                self.action_buttons.clear()
                self.selected_node = None
                self.selected_nodes.clear()
                return

    # все основные кнопки под курсором
        clicked_buttons = [btn for btn in self.buttons if btn.selected]

        if not clicked_buttons:
        # клик в пустоту
            self.selected_node = None
            self.selected_nodes.clear()
            self.action_buttons.clear()
            return

    # обрабатываем первый кликнутый элемент (под курсором обычно одна кнопка)
        btn = clicked_buttons[0]

        if key_modifiers & arcade.key.MOD_CTRL:
        # множественное выделение (и узлы, и скобки)
            if btn.node in self.selected_nodes:
                self.selected_nodes.remove(btn.node)
            else:
                self.selected_nodes.append(btn.node)
            self.action_buttons.clear()
            self.selected_node = None
        else:
        # одиночное выделение – сбрасываем и выделяем только этот элемент
            self.selected_nodes.clear()
            self.selected_nodes.append(btn.node)
            self.selected_node = btn.node if isinstance(btn.node, Node) else None
            self.action_buttons.clear()
        # если это узел – показываем его действия
            if isinstance(btn.node, Node):
                x_pos = btn.center_x + btn.width/2 + 20
                y_pos = btn.center_y
                for i, act in enumerate(btn.node.actions):
                    act_btn = ButtonSymbol(
                        act, x_pos, y_pos - i*40,
                        node=btn.node, action_name=act
                    )
                    self.action_buttons.append(act_btn)

        return  # завершаем, не переходя к клику в пустоту

def main():
    window = arcade.Window(WIDTH, HEIGHT, 'Reshator 3000')

    root = parse.infix_to_tree('(2 + 3 + 4) * (a + b)')
    game = ExampleSolution(root) 
    game.reset()

    window.show_view(game)
    arcade.run()

if __name__ == '__main__':
    main()
        
        
        
