"""этот модуль - входная точка в программу"""

import game.arcade_import as arcade
from game.views.menu import Menu
from game.graphics import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, 'Решатор')
    menu_view = Menu()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__": main()

