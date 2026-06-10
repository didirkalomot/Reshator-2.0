class MyException(Exception):
    HEADER: str = None

    def __init__(self, message: str): self.message = message

    def __str__(self): return f'{self.__class__.HEADER}\n{self.message}' 

class SystemException(MyException): pass

class ParseError(SystemException):
    HEADER = 'Не корректное выражение:'

    def __init__(self, string: str):
        super().__init__(string)

class GameplayException(MyException): pass

class Good(GameplayException):
    HEADER = 'Успешное действие:'

    def __init__(self, action_name: str):
        super().__init__(self, action_name)

class Bad(GameplayException):
    HEADER = 'Неправильное действие:'

    def __init__(self, action_name: str):
        super().__init__(self, action_name)