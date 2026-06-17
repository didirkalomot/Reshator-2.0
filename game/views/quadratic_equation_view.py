from __future__ import annotations
from mechanics import parse
from game.views.expression_view import ExpressionView
<<<<<<< Updated upstream

######################################## Режим Со Случайным Примером ########################################

class QuadraticEquationMode(ExpressionView): 
    def __init__(self): 
        string = 'a^2 - a + 10 = 0'
        super().__init__(parse.create_tree(string))
=======
from mechanics import nodes, parse, exceptions
import random

class QuadraticEquationMode(ExpressionView):
    def __init__(self, equation_str: str = None):
        # Если строка не передана, генерируем случайное квадратное уравнение
        if equation_str is None:
            # Генерируем коэффициенты a, b, c (a != 0)
            a = random.randint(1, 5)
            b = random.randint(-10, 10)
            c = random.randint(-10, 10)
            # Формируем строку вида: a*x^2 + b*x + c = 0
            # Упростим: если b или c равны 0, пропускаем соответствующие члены
            parts = []
            if a != 0:
                if a == 1:
                    parts.append("x^2")
                else:
                    parts.append(f"{a}*x^2")
            if b != 0:
                if b == 1:
                    parts.append("+x")
                elif b == -1:
                    parts.append("-x")
                else:
                    if b > 0:
                        parts.append(f"+{b}*x")
                    else:
                        parts.append(f"{b}*x")
            if c != 0:
                if c > 0:
                    parts.append(f"+{c}")
                else:
                    parts.append(f"{c}")
            # Собираем левую часть
            left = "".join(parts)
            if not left:
                left = "0"
            equation_str = f"{left} = 0"

        # Разбиваем на левую и правую части
        if '=' not in equation_str:
            raise ValueError("Уравнение должно содержать '='")
        left_str, right_str = equation_str.split('=')
        left_str = left_str.strip()
        right_str = right_str.strip()

        # Парсим левую и правую части
        try:
            left_root = parse.create_tree(left_str)
            right_root = parse.create_tree(right_str) if right_str else nodes.Number(0)
        except exceptions.ParseError as e:
            # Если парсинг не удался, выведем уведомление и используем заглушку
            print(f"Ошибка парсинга: {e}")
            left_root = nodes.Number(0)
            right_root = nodes.Number(0)

        # Создаём узел равенства
        root = nodes.Equal(left_root, right_root)

        # Вызываем родительский конструктор с корнем и текстом задачи
        super().__init__(root, text_info=f"Решите квадратное уравнение: {equation_str}")

        
>>>>>>> Stashed changes
