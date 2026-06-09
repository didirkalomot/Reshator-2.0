"""этот модуль - входная точка в программу"""

import game.arcade_import as arcade
from game.views.menu import Menu

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, 'Решатор')
    menu_view = Menu()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__": main()

