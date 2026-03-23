"""этот модуль - входная точка в программу"""

import arcade
from views.menu_view import MenuView

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Решатор")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__": main()

