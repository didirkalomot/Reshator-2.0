from __future__ import annotations
from game import arcade_import as arcade
from game import graphics
from game.views.expression_view import ExpressionView
from mechanics import nodes, parse, exceptions

class QuadraticEquationView(ExpressionView):
    def __init__(self, equation_str: str):
        a, b, c = self.parse.create_tree(equation_str)
        self.a = a
        self.b = b
        self.c = c
        self.discriminant = b*b - 4*a*c
        self.expected_roots = self._compute_roots()
        self.found_roots = []
        self.step = self._initial_step()
        expr_str = equation_str.split('=')[0].strip()
        root = parse.create_tree(expr_str)
        super().__init__(root, f"Решите уравнение: {equation_str}")

    def _parse_equation(self, eq: str):
        import re
        left = eq.replace(' ', '').split('=')[0]
        return (1, -5, 6)

    def _compute_roots(self):
        d = self.discriminant
        if d < 0: return []
        elif d == 0: return [-self.b / (2*self.a)]
        else:
            sqrt_d = d**0.5
            x1 = (-self.b - sqrt_d) / (2*self.a)
            x2 = (-self.b + sqrt_d) / (2*self.a)
            return sorted([x1, x2])

    def _initial_step(self):
        if self.discriminant < 0: return 'discriminant'
        elif self.discriminant == 0: return 'discriminant'
        else: return 'discriminant'

    def get_next_step(self):
        if self.step == 'discriminant': return 'discriminant'
        elif self.step == 'root1': return 'root1'
        elif self.step == 'root2': return 'root2'
        else: return 'done'

    def get_dialog_title(self):
        if self.step == 'discriminant': return f"Введите дискриминант (D = {self.discriminant})"
        elif self.step == 'root1': return "Введите первый корень"
        elif self.step == 'root2': return "Введите второй корень"
        else: return "Задача решена"

    def add_expression(self, root: nodes.Node):
        if self.step == 'done':
            self.show_notification("Задача уже решена!")
            return

        if not isinstance(root, nodes.Number):
            self.show_notification("Пожалуйста, введите число.")
            return

        value = root.value

        if self.step == 'discriminant':
            if abs(value - self.discriminant) < 1e-9:
                self.show_notification("Дискриминант верный!")
                if self.discriminant < 0:
                    self.step = 'done'
                    self.compleate_expression()
                elif self.discriminant == 0:
                    self.step = 'root1'
                    self.show_notification("Теперь введите корень.")
                else:
                    self.step = 'root1'
                    self.show_notification("Теперь введите первый корень.")
            else: self.show_notification(f"Неверный дискриминант. Ожидается {self.discriminant}")
            return

        if self.step in ('root1', 'root2'):
            if value in self.expected_roots and value not in self.found_roots:
                self.found_roots.append(value)
                self.show_notification(f"Корень {value} принят.")
                if set(self.found_roots) == set(self.expected_roots):
                    self.step = 'done'
                    self.compleate_expression()
                else:
                    if self.step == 'root1':
                        self.step = 'root2'
                        self.show_notification("Введите второй корень.")
                    else:
                        self.show_notification("Пожалуйста, введите оставшийся корень.")
            else: self.show_notification("Неверный корень. Попробуйте снова.")
            return

        self.show_notification("Неизвестный шаг. Перезапустите задачу.")

    def compleate_expression(self):
        if self.discriminant < 0: msg = "Корней нет"
        elif self.discriminant == 0: msg = f"Один корень: {self.expected_roots[0]}"
        else: msg = f"Два корня: {self.expected_roots[0]} и {self.expected_roots[1]}"
        self.anchor.add(graphics.InfoDialog(
            title="Задача решена!",
            message_text=msg,
            button_text="Отлично!"))