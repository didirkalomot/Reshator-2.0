from game.views.expression_view import ExpressionView
from game import graphics
from mechanics import nodes, parse

class EquationView(ExpressionView):
    def __init__(self, equation_str: str = None):
        if equation_str is None:
            root = parse.random_equation()
        else:
            root = parse.create_tree(equation_str)

        if not isinstance(root, nodes.Equal):
            raise ValueError("Уравнение должно содержать '='")

        self.solved = False
        # Сохраняем ссылку на корень для проверки
        self.root = root
        text_info = f"Решите уравнение: {str(root)}"

        super().__init__(root, text_info)

        # Сохраняем ссылку на основную панель (первую и единственную)
        if self.expressions.children:
            self.main_panel = self.expressions.children[0]
        else:
            self.main_panel = None

        self.show_notification("Упрощайте уравнение, пока не получите x = число.")

    def update_panel(self, panel):
        # Обновляем панель через родительский метод
        new_panel = super().update_panel(panel)
        # Обновляем ссылку на основную панель, если это она
        if panel is self.main_panel:
            self.main_panel = new_panel
            # Проверяем, решено ли уравнение
            if not self.solved:
                self.check_solved(new_panel.root)
        return new_panel

    def check_solved(self, root):
        if isinstance(root, nodes.Equal):
            left = root.one
            right = root.two

            print(f"Проверка: left={left}, right={right}")

            # Проверяем, что одна сторона — буква, другая — число
            if isinstance(left, nodes.Letter) and isinstance(right, nodes.Number):
                self.solved = True
                print("Условие выполнено! Вызываем complete_expression")
                self.complete_expression(f"x = {right.value}")
            elif isinstance(right, nodes.Letter) and isinstance(left, nodes.Number):
                self.solved = True
                print("Условие выполнено! Вызываем complete_expression")
                self.complete_expression(f"x = {left.value}")
            elif isinstance(left, nodes.Number) and isinstance(right, nodes.Number):
                if left == right:
                    self.solved = True
                    print("Условие выполнено! Вызываем complete_expression")
                    self.complete_expression("Тождество (любое x)")
                else:
                    self.show_notification("Противоречие, решений нет")
