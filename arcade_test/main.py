import arcade
import problem

WIDTH = 800
HEIGHT = 600
CENTER = (WIDTH // 2, HEIGHT // 2)

class ExampleSymbol():
    def __init__(self, example: problem.Problem, node: problem.Node, x: int, y: int, color = arcade.color.WHITE):
        self.example = example
        self.node = node
        self.sprite: arcade.Sprite = arcade.create_text_sprite(
            str(node),
            color = arcade.color.WHITE,
            font_size = 25.0,
        )
        self.sprite.position = [x, y]

    def click(self):
        if isinstance(self.node, problem.Operator):
            a = self.example.use_operator(self.node)
            print('оператор:', self.node)

        if isinstance(self.node, problem.Value):
            print('значение:', self.node)

class ExampleSolution(arcade.View):
    def __init__(self, example: problem.Problem = problem.Problem(problem.Number(0))):
        super().__init__()
        self.background_color = arcade.color.BLACK
        self.example = example
        self.symbols = []
        self.sprites = arcade.SpriteList()

        self.make_symbols()
    
    ### не работает (позиции не те)
    def make_symbols(self):
        def recursive_make_symbols(node: problem.Node, x, y):
            new_symbol = ExampleSymbol(self.example, node, x, y)
            self.symbols.append(new_symbol)
            self.sprites.append(new_symbol.sprite)

            if node.left != None: 
                recursive_make_symbols(node.left, x - node.recursive_len() * 5, y)
            if node.right != None: 
                recursive_make_symbols(node.right, x + (node.recursive_len() * 5), y)

        self.symbols.clear()
        self.sprites.clear()
        recursive_make_symbols(self.example.root, CENTER[0], CENTER[1])
    ###

    def reset(self):
        pass

    def on_draw(self):
        self.clear()
        self.sprites.draw()
          
    def on_update(self, delta_time):pass

    def on_key_press(self, key, modifiers):pass

    def on_key_release(self, key, modifiers):pass

    def on_mouse_motion(self, x, y, dx, dy):pass

    def on_mouse_press(self, x, y, button, key_modifiers):pass

    def on_mouse_release(self, x, y, button, key_modifiers):pass

def main():
    example = problem.make_problem('((-(3) - 5)+ 3 * 4) / ((34 - 3) * 4)')

    window = arcade.Window(WIDTH, HEIGHT, 'Reshator 3000')
    game = ExampleSolution(example) 
    game.reset()

    window.show_view(game)
    arcade.run()

if __name__ == '__main__':
    main()
        
        
        
