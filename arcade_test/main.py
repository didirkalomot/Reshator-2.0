import arcade
import problem

WIDTH = 800
HEIGHT = 600
CENTER = (WIDTH // 2, HEIGHT // 2)

arcade.load_font('resourses/BetterVCR/BetterVCR.ttf')

FONT_SIZE = 25.0

class ButtonSymbol(arcade.Sprite):
    def __init__(self, example: problem.ProblemList, node: problem.Node, x, y, depth = 1):
        text_sprite = arcade.create_text_sprite(
            text=str(node),
            color=arcade.color.WHITE,
            font_size=FONT_SIZE / depth,
            font_name='Better VCR',
            anchor_x='center'
        )
        super().__init__(
            text_sprite.texture, 
            text_sprite.scale,
            x, y,
            )

        self.example = example
        self.node = node

    def click(self):
        if isinstance(self.node, problem.Operator):
            self.example.use_operator(self.node)
            print('оператор:', self.node)

        if isinstance(self.node, problem.Value):
            print('значение:', self.node)

class ExampleSolution(arcade.View):
    def __init__(self, example: problem.ProblemList = problem.ProblemList(problem.Number(0))):
        super().__init__()
        self.background_color = arcade.color.BLACK
        self.example = example
        self.sprites = arcade.SpriteList()
        self.make_symbols()
    
    def make_symbols(self):
        len_example =  self.example.len_string() * 50.0
        current_x, current_y = CENTER[0] - len_example / 2, CENTER[1]
        current_depth = 1
        for node in self.example:
            self.sprites.append(
                ButtonSymbol(self.example, node, current_x, current_y)
            )
            current_x += 100.0
            

    def reset(self):
        pass

    def on_draw(self):
        self.clear()
        self.sprites.draw()
          
    def on_update(self, delta_time):pass

    def on_key_press(self, key, modifiers):pass

    def on_key_release(self, key, modifiers):pass

    def on_mouse_motion(self, x, y, dx, dy):pass
        
    def on_mouse_release(self, x, y, button, key_modifiers):pass

def main():
    window = arcade.Window(WIDTH, HEIGHT, 'Reshator 3000')


    #example = problem.make_problem('((-(3) - 5)+ 3 * 4) / ((34 - 3) * 4)')
    example = problem.make_problem_list('(-(3) - 5) + 3 * 4')
    game = ExampleSolution(example) 
    game.reset()

   
    
    window.show_view(game)
    arcade.run()

if __name__ == '__main__':
    main()
        
        
        
