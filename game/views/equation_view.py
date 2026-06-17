from game.views.expression_view import ExpressionView
from mechanics import nodes, parse
from game import graphics

class EquationView(ExpressionView):
    def __init__(self, equation_str: str = None):
        # Генерируем случайное уравнение, если строка не передана
        if equation_str is None:
            root = parse.random_equation()
            equation_str = str(root)  # для отображения в заголовке
        else:
            root = parse.create_tree(equation_str)

        if not isinstance(root, nodes.Equal):
            raise ValueError("Уравнение должно содержать '='")

        self.solved = False
        self.panel = None  # будет ссылка на панель с уравнением

        # Вызываем родительский конструктор, передавая корень и текст задачи
        super().__init__(root, text_info=f"Решите уравнение: {equation_str}")

        # После создания панелей сохраняем ссылку на первую (и единственную) панель
        if self.expressions.children:
            self.panel = self.expressions.children[0]

        # Начальная подсказка
        self.show_notification("Упрощайте уравнение, пока не получите x = число.")

    def update_panel(self, panel):
        """Переопределяем, чтобы после обновления панели проверить, решено ли уравнение."""
        super().update_panel(panel)
        # Проверяем только если уравнение ещё не решено и обновляется наша основная панель
        if not self.solved and panel is self.panel:
            self.check_solved(panel.root)

    def check_solved(self, root):
        """Проверяет, приведено ли уравнение к виду x = число (или число = x)."""
        if isinstance(root, nodes.Equal):
            left = root.one
            right = root.two

            # Случай: x = число
            if isinstance(left, nodes.Letter) and isinstance(right, nodes.Number):
                self.solved = True
                self.compleate_equation(f"x = {right.value}")

            # Случай: число = x
            elif isinstance(right, nodes.Letter) and isinstance(left, nodes.Number):
                self.solved = True
                self.compleate_equation(f"x = {left.value}")

            # Случай: число = число (тождество или противоречие)
            elif isinstance(left, nodes.Number) and isinstance(right, nodes.Number):
                if left == right:
                    self.solved = True
                    self.compleate_equation("Уравнение является тождеством (любое x)")
                else:
                    self.show_notification("Уравнение не имеет решений (противоречие)")



    def compleate_equation(self, message):
        """Показывает диалог завершения с результатом."""
        self.anchor.add(
            graphics.InfoDialog(
                title="Уравнение решено!",
                message_text=message,
                button_text="Отлично!"
            )
        )
