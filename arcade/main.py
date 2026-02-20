# -*- coding: cp1251 -*-

import arcade
import parse
import problem
from nodes import Node
from typing import List, Optional

WIDTH = 800
HEIGHT = 600
CENTER = (WIDTH // 2, HEIGHT // 2)

arcade.load_font('resourses/BetterVCR/BetterVCR.ttf')
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
        arcade.draw_text(self.text, self.center_x, self.center_y, color, FONT_SIZE)

    def collides_with_point(self, x: float, y: float) -> bool:
        #проверка попадания точки в кнопку
        return (abs(self.center_x - x) < self.width/2 and
                abs(self.center_y - y) < self.height/2)

class ExampleSolution(arcade.View):
    def __init__(self):
        super().__init__()
        # Исходное выражение (как в problem.py)
        self.expression_string = '(1 + 34) * ~(sin(x) ^ 2 + cos(x) ^ 2)'
        self.problem: Optional[Node] = None
        self.buttons: List[ButtonSymbol] = []          # кнопки выражения
        self.action_buttons: List[ButtonSymbol] = []   # кнопки доступных действий
        self.selected_node: Optional[Node] = None
    
    def make_symbols(self):
        #Создаёт кнопки для текущего дерева выражения
        self.buttons.clear()
        if self.problem is None:
            return

        tokens = list(self.problem)  # получаем последовательность узлов и скобок
        x, y = 50, HEIGHT // 2
        for token in tokens:
            if isinstance(token, str):
                btn = ButtonSymbol(token, x, y, node=None)
            else:
                btn = ButtonSymbol(str(token), x, y, node=token)
            self.buttons.append(btn)
            x += btn.width + 5
            # простой перенос строки
            if x > WIDTH - 50:
                x = 50
                y -= 50
            
    def reset(self):
         #Сброс к исходному выражению
         self.problem = parse.infix_to_tree(self.expression_string)
         self.make_symbols()
         self.selected_node = None
         self.action_buttons.clear()
        

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        for btn in self.buttons:
            btn.draw()
        for btn in self.action_buttons:
            btn.draw()

        # Подсказки
        arcade.draw_text("R - сброс | ESC - отмена", 10, HEIGHT-30, arcade.color.WHITE, 16)
          
    def on_update(self, delta_time):pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.reset()
        elif key == arcade.key.ESCAPE:
            self.selected_node = None
            self.action_buttons.clear()

    def on_key_release(self, key, modifiers):pass

    def on_mouse_motion(self, x, y, dx, dy):
        # Подсветка кнопок при наведении
        for btn in self.buttons + self.action_buttons:
            btn.selected = btn.collides_with_point(x, y)
        
    def on_mouse_release(self, x, y, button, key_modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

         # 1. Проверяем клик по кнопкам действий
        for btn in self.action_buttons:
            if btn.selected and btn.action_name and btn.node:
                btn.node.do_action(btn.action_name)
                self.make_symbols()               # обновить отображение выражения
                self.action_buttons.clear()       # убрать меню действий
                self.selected_node = None
                return

        # 2. Проверяем клик по основным кнопкам (узлам)
        for btn in self.buttons:
            if btn.selected and btn.node:
                self.selected_node = btn.node
                # Показать доступные действия рядом с кнопкой
                self.action_buttons.clear()
                actions = btn.node.actions
                if actions:
                    x, y = btn.center_x + btn.width/2 + 20, btn.center_y
                    for i, act in enumerate(actions):
                        act_btn = ButtonSymbol(act, x, y - i*40, node=btn.node, action_name=act)
                        self.action_buttons.append(act_btn)
                return

        # 3. Клик мимо – снять выделение
        self.selected_node = None
        self.action_buttons.clear()

def main():
    window = arcade.Window(WIDTH, HEIGHT, 'Reshator 3000')

    game = ExampleSolution() 
    game.reset()

   
    
    window.show_view(game)
    arcade.run()

if __name__ == '__main__':
    main()
        
        
        
