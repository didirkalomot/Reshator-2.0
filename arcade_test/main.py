import arcade

WIDTH = 800
HEIGHT = 600
CENTER = (WIDTH // 2, HEIGHT // 2)

class MyGamge(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.GREEN)

    def setup(self):
        self.sprites = arcade.SpriteList()
        self.score = 0
        self.player_sprite = arcade.Sprite('arcade_test/icon.png', 1)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.sprites.append(self.player_sprite)

    def on_draw(self):
        arcade.start_render()
        self.sprites.draw()

    def update(self, delta_time):pass

def main():
    game = MyGamge(WIDTH, HEIGHT)
    game.setup()
    arcade.run()

if __name__ == '__main__':
    main()