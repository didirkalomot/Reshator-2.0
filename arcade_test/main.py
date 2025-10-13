import arcade
import problem

WIDTH = 800
HEIGHT = 600
CENTER = (WIDTH // 2, HEIGHT // 2)

arcade.load_font('resourses/BetterVCR/BetterVCR.ttf')
FONT_SIZE = 25.0

SYMBOL_SIZE= [24.75, 33]


class ButtonSymbol(arcade.Sprite):pass

class ExampleSolution(arcade.View):
    def __init__(self):pass
    
    def make_symbols(self):pass
            
    def reset(self):
        pass

    def on_draw(self):
        self.clear()
          
    def on_update(self, delta_time):pass

    def on_key_press(self, key, modifiers):pass

    def on_key_release(self, key, modifiers):pass

    def on_mouse_motion(self, x, y, dx, dy):pass
        
    def on_mouse_release(self, x, y, button, key_modifiers):pass

def main():
    window = arcade.Window(WIDTH, HEIGHT, 'Reshator 3000')

    game = ExampleSolution() 
    game.reset()

   
    
    window.show_view()
    arcade.run()

if __name__ == '__main__':
    main()
        
        
        
