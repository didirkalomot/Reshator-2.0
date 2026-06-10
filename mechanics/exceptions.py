class MyException(Exception):
    HEADER: str = None
    def __init__(self, message: str): self.message = message
    def __str__(self): return f'{self.__class__.HEADER}:\n{self.message}' 

class SystemException(MyException): pass

class ParseError(SystemException):
    HEADER = 'Не корректное выражение'
    def __init__(self, string: str): super().__init__(string)

class GameplayException(MyException): pass

class Good(GameplayException):
    HEADER = 'Успешное действие'
    def __init__(self, action_name: str): super().__init__(action_name)

class Bad(GameplayException):
    HEADER = 'Неправильное действие'
    def __init__(self, action_name: str): super().__init__(action_name)

class NotCorrectLogBase(Bad):
    HEADER = 'Не допустимое основание логарифма'
    def __init__(self, base: str): super().__init__(base)

class NotCorrectLogArg(Bad):
    HEADER = 'Не допустимый аргумент логарифма'
    def __init__(self, arg: str): super().__init__(arg)

class InvalidOperandError(Bad):
    HEADER = 'Недопустимый операнд'
    def __init__(self, operand: str): super().__init__(operand)

class InvalidOrderError(Bad):
    HEADER = 'Неправильный порядок действий'
    def __init__(self, this, other): super().__init__(f'{this} выполняется после {other}')