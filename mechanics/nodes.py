from __future__ import annotations # это чтобы код видел типы до их объявления
from functools import cached_property # это чтобы первый раз результат свойтсва записался и не срабатывала функция каждый раз
from copy import deepcopy # для глубокого копирования
import math # функции: sin, cos, log, ...
import gc # для метода Node.replace
from mechanics import tokens
#import tokens

######################################## Классы Для Системы Действий ########################################

class Action:
    def __init__(self,
                 func: function,
                 name: str,
                 condition: function = None,
                 interactive: bool = False):
        self.name: str = name
        self.condition: function = condition
        self.interactive: bool = interactive
        self._func = func

    def __call__(self, node, arg_node=None):
        if self.interactive: return self._func(node, arg_node)
        else: return self._func(node)

class Actionable:
    ACTIONS: list[Action] = []
    INHERITED = True

    def __init_subclass__(cls):
        if 'INHERITED' not in cls.__dict__: cls.INHERITED = True
        cls.ACTIONS = []
        for atribute in cls.__dict__.values():
            if isinstance(atribute, Action):
                cls.ACTIONS.append(atribute)
        if cls.INHERITED:
            for base in cls.__bases__:
                if issubclass(base, Actionable):
                    cls.ACTIONS += base.ACTIONS

    @property
    def actions(self) -> tuple[Action, ...]:
        available_actions = []
        for func in self.__class__.ACTIONS:
            if func.condition is None or func.condition(self):
                available_actions.append(func)
        return tuple(available_actions)

def action(name: str, condition: function = None, interactive = False):
    def decorator(func):
        action_func = Action(func, name, condition, interactive)
        return action_func
    return decorator

######################################## Основной Класс Узла ########################################

class Node(Actionable, tokens.VisibleToken):

    __slots__ = ['parent']

    def __init__(self):
        super().__init__()
        self.parent: Operator | None = None

    def __iter__(self): yield self

    def __getitem__(self, key) -> Node | str: return list(iter(self))[key]

    @property
    def visibles(self) -> list[tokens.VisibleToken]:
        return [item for item in self if isinstance(item, tokens.VisibleToken)]

    @property
    def nodes(self) -> list[Node]:
        return [node for node in self if isinstance(node, Node)]

    @property
    def values(self) -> list[Value]:
        return [value for value in self if isinstance(value, Value)]

    @property
    def operators(self) -> list[Operator]:
        return [operator for operator in self if isinstance(operator, Operator)]

    def __str__(self) -> str: return 'node'

    def print_expression(self):
        items = [str(item) for item in self.visibles]
        if not items:
            return
        result = items[0]
        for s in items[1:]:
            result += (' ' if not (s == ')' or result[-1] == '(') else '') + s
        print(result)

    def print_tree(self, prefix): print(f'{prefix}[{self}]')

    def __deepcopy__(self, memo=None):
        cls = self.__class__
        result = cls.__new__(cls)
        result.parent = None
        return result

    def simplify(self): return self

    def __eq__(self, other):
        if not isinstance(other, Node): return False
        left = self.simplify()
        right = other.simplify()
        if type(left) != type(right): return False
        return left._equals(right)

    def _equals(self, other: Node) -> bool: raise NotImplementedError()

    def __ne__(self, other) -> bool: return not self == other

    def replace(self, new):
        if self.parent is not None:
            for i, op in enumerate(self.parent.operands):
                if op is self:
                    self.parent.operands[i] = new
                    new.parent = self.parent
                    self.parent = None
                    return
        for ref in gc.get_referrers(self):
            if isinstance(ref, dict):
                for k, v in list(ref.items()):
                    if v is self:
                        ref[k] = new
            elif isinstance(ref, list):
                for i, v in enumerate(ref):
                    if v is self:
                        ref[i] = new
            elif isinstance(ref, set) and self in ref:
                ref.remove(self)
                ref.add(new)
            elif hasattr(ref, '__dict__'):
                for attr, val in ref.__dict__.items():
                    if val is self:
                        setattr(ref, attr, new)
        new.parent = None

    @staticmethod
    def find_common_parent(*nodes: Node) -> Node | None:
        if not nodes: return None
        if len(nodes) == 1: return nodes[0]
        paths = []
        for node in nodes:
            path = []
            while node:
                path.append(node)
                node = node.parent
            paths.append(path)
        parent = None
        for i in range(-1, -min(len(path) for path in paths) - 1, -1):
            current = paths[0][i]
            if all(path[i] is current for path in paths): parent = current
            else: break
        return parent

    def not_self_already_neg(self): return not (isinstance(self, UnaryMinus) or isinstance(self.parent, UnaryMinus))
    @action('умножить на -1', not_self_already_neg)
    def mult_by_minus_one(self) -> Node: self.replace(UnaryMinus(UnaryMinus(deepcopy(self))))

    @action('разделить на 1', lambda self: not isinstance(self, Div))
    def div_by_one(self) -> Node: self.replace(Div(deepcopy(self), Number(1)))

    def parent_is_factorable_and_grand_is_equal(self):
        parent = self.parent
        return isinstance(parent, Factorable) and isinstance(parent.parent, Equal)
    @action('перенести за равно', parent_is_factorable_and_grand_is_equal)
    def transfer_grandson_via_equals(self): self.parent.parent.transfer_grandson(self)

    @action('перенести за равно', lambda self: isinstance(self.parent, Equal))
    def transfer_child_via_equals(self): self.parent.transfer_child(self)

######################################## Классы Для Значений ########################################

class Value(Node):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value
        super().__init__()

    def __str__(self) -> str: return 'value'

    def _equals(self, other: Value): return self.value == other.value

    def __hash__(self): return hash((self.__class__, self.value))

    def __deepcopy__(self, memo=None):
        result = super().__deepcopy__(memo)
        result.value = deepcopy(self.value, memo)
        return result

    @action('заменить выражением', interactive=True)
    def as_expression(self, node: Node):
        if self == node: self.replace(node)

class Number(Value):
    ONE: Constant
    ZERO: Constant
    E: Constant
    PI: Constant

    def __init__(self, value: float): super().__init__(value)

    def is_integer(self)-> bool: return self.value.is_integer()

    def __str__(self) -> str:
        if self.is_integer(): s = str(int(self.value))
        else: s = str(self.value)
        if len(s) > 5: return s[:5] + '...'
        return s

    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        return NotImplemented

    def __neg__(self): return Number(-self.value)

    def __sub__(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)
        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value)
        return NotImplemented

    def __float__(self): return float(self.value)

    def __int__(self): return int(self.value)

    def __gt__(self, other):    # >
        if isinstance(other, Number):
            return self.value > other.value
        elif isinstance(other, (int, float)):
            return self.value > other
        return NotImplemented

    def __lt__(self, other):    # <
        if isinstance(other, Number):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < other
        return NotImplemented

    def __ge__(self, other):    # >=
        if isinstance(other, Number):
            return self.value >= other.value
        elif isinstance(other, (int, float)):
            return self.value >= other
        return NotImplemented

    def __le__(self, other):    # <=
        if isinstance(other, Number):
            return self.value <= other.value
        elif isinstance(other, (int, float)):
            return self.value <= other
        return NotImplemented

class Constant(Number):
    def __init__(self, number: float, symbol: str = None):
        super().__init__(number)
        #if symbol: self.__str__ = lambda self: symbol
        self.symbol = symbol

    def  __str__(self): return self.symbol if self.symbol else super().__str__()

Number.ZERO = Constant(0)
Number.ONE = Constant(1)
Number.E = Constant(math.e, 'e')
Number.PI = Constant(math.pi, 'pi')

class Letter(Value):
    def __init__(self, value: str):
        if value and value[0].isalpha():
            super().__init__(value)
        else: raise TypeError

    def __str__(self) -> str: return self.value

    def __add__(self, other):
        if self == other: return Mult(2, deepcopy(self))
        return NotImplemented

    def __sub__(self, other):
        if self == other: return Number(0)
        return NotImplemented

    def __mul__(self, other):
        if other == Number.ZERO: return Number(0)
        if self == other: return Pow(self, Number(2))
        if isinstance(other, Pow) and other.one == self:
            return Pow(self, Number(other.two.value + 1))
        return NotImplemented

    def __truediv__(self, other):
        if self == other: return Number(1)
        return NotImplemented

######################################## Класс Для Операторов ########################################

class Operator(Node):
    ARITY = 2
    PRIORITY = 1

    __slots__ = ['operands']

    def __init__(self, *operands: Node):
        self.operands: list[Node] = list(operands)
        for node in self.operands: node.parent = self
        super().__init__()

    @property
    def arity(self) -> int:
        if self.__class__.Arity is None: return len(self.operands)
        else: return self.__class__.Arity

    @cached_property
    def priority(self) -> int: return self.__class__.PRIORITY

    def simplify(self) -> Node:
        simplified_operands = [op.simplify() for op in self.operands]
        candidate = type(self)(*simplified_operands)
        res = candidate.result()
        if res is not NotImplemented: return res
        return candidate

    def _equals(self, other: Operator):
        if len(self.operands) != len(other.operands): return False
        return all(a == b for a, b in zip(self.operands, other.operands))

    def __hash__(self):
        return hash((self.__class__,) + tuple(
            op.value if isinstance(op, Value) else op.__class__
            for op in self.operands))

    def __deepcopy__(self, memo=None):
        result = super().__deepcopy__(memo)
        result.operands = deepcopy(self.operands, memo)
        for op in result.operands:
            op.parent = result
        return result

    def __str__(self): return 'operator'

    def print_tree(self, prefix=''):
        print(f'{prefix}[{self}]')
        for i, oper in enumerate(self.operands):
            if i == len(self.operands) - 1: oper.print_tree(prefix + '└── ')
            else: oper.print_tree(prefix + '├── ')

    def is_child(self, node: Node) -> bool: return node in self.operands

    def result(self) -> Value: return NotImplemented

    @action('выполнить', lambda self: self.result() is not NotImplemented)
    def work(self):
        if (result := self.result()) is not NotImplemented: self.replace(result)

######################################## Миксины Для Операторов ########################################

class Prefix:
    ARITY = 1

    @property
    def one(self) -> Node: return self.operands[0]

    @one.setter
    def one(self, value: Node):
        self.operands[0] = value
        value.parent = self

    def __iter__(self):
        left_bracket, right_bracket = tokens.function_brackets.create_pair()
        yield self
        yield left_bracket
        for op in self.operands: yield from op
        yield right_bracket

class Infix:
    ARITY = 2
    ASSOCIATIVITY_LEFT = True

    @property
    def one(self) -> Node: return self.operands[0]

    @one.setter
    def one(self, value: Node):
        self.operands[0] = value
        value.parent = self

    @property
    def two(self) -> Node: return self.operands[1]

    @two.setter
    def two(self, value: Node):
        self.operands[1] = value
        value.parent = self

    @cached_property
    def associativity_left(self) -> bool: return self.__class__.ASSOCIATIVITY_LEFT

    def _needs_brackets(self, child: Node, is_left: bool) -> bool:
        if not isinstance(child, Operator): return False
        if child.priority >= self.priority: return True
        #if child.priority == self.priority:
            #if child.__class__ != self.__class__: return True
            #return self.associativity_left != is_left
        return False

    def __iter__(self):
        left, right = self.operands
        def wrap(operand, need_parens):
            if need_parens:
                left_bracket, right_bracket = tokens.brackets.create_pair()
                yield left_bracket
                yield from operand
                yield right_bracket
            else: yield from operand

        yield from wrap(left, self._needs_brackets(left, True))
        yield self
        yield from wrap(right, self._needs_brackets(right, False))

    def other_operand(self, node: Node) -> Node:
        if not self.is_child(node): raise ValueError()
        return self.two if node is self.one else self.one

class Postfix:
    ARITY = 1

    @property
    def one(self) -> Node: return self.operands[0]

    @one.setter
    def one(self, value: Node):
        self.operands[0] = value
        value.parent = self

    def __iter__(self):
        left_bracket, right_bracket = tokens.function_brackets.create_pair()
        yield left_bracket
        for op in self.operands: yield from op
        yield right_bracket
        yield self

class Associative(Actionable): # Infix
    def both_operands_is_self_class(self):
        return all(isinstance(oper, self.__class__) for oper in self.operands)
    @action('ассоциативность влево', both_operands_is_self_class)
    def associative_left(self):
        """a ∘ (b ∘ c) → (a ∘ b) ∘ c"""
        if isinstance(self.two, self.__class__):
            self.one = self.__class__(self.one, self.two.one)
            self.two = self.two.two

    @action('ассоциативность вправо', both_operands_is_self_class)
    def associative_right(self):
        """(a ∘ b) ∘ c → a ∘ (b ∘ c)"""
        if isinstance(self.one, self.__class__):
            self.two = self.__class__(self.one.two, self.two)
            self.one = self.one.one

    def only_one_operand_is_self_class(self):
        return isinstance(self.one, self.__class__) != isinstance(self.two, self.__class__)
    @action('ассоциативность', only_one_operand_is_self_class)
    def associative(self):
        if isinstance(self.one, self.__class__):  self.associative_right(self)
        else: self.associative_left(self)

    def to_list(self) -> list[Node]:
        operands = []
        def collect(n):
            if isinstance(n, self.__class__):
                for op in n.operands: collect(op)
            else: operands.append(n)
        collect(self)
        return operands

    @classmethod
    def from_list(cls, operands) -> Node | None:
        if not operands: return None
        if len(operands) == 1: return operands[0]
        if cls.ASSOCIATIVITY_LEFT:
            result = operands[0]
            for op in operands[1:]: result = cls(result, op)
        else:
            result = operands[-1]
            for i in range(len(operands)-2, -1, -1):
                result = cls(operands[i], result)
        return result

    def __hash__(self): return hash((self.__class__, *self.to_list()))

    def _equals(self, other: Associative) -> bool: return self.to_list() == other.to_list()

class Commutative(Actionable): # Infix
    def __hash__(self):
        return hash(( self.__class__, *sorted(
            str(op.value) if isinstance(op, Value) else op.__class__.__name__
            for op in self.operands)))

    def _equals(self, other: Commutative) -> bool:
        return sorted(self.operands, key=hash) == sorted(other.operands, key=hash)

    @action('коммутативность')
    def commutative(self: Infix):
        """a ∘ b → b ∘ a - поменять операнды местами"""
        self.one, self.two = self.two, self.one

class AssociativeCommutative(Associative, Commutative): # Infix
    def _key(self):
        return sorted(
            str(op.value) if isinstance(op, Value) else op.__class__.__name__
            for op in self.to_list())

    def __hash__(self): return hash((self.__class__, *self._key()))

    def _equals(self, other: AssociativeCommutative): return self._key() == other._key()

class Factorable(Actionable): # Infix
    def both_operands_is_muls(self) -> bool: return all(isinstance(oper, Mult) for oper in self.operands)

    def get_common_factor(self) -> Node | None:
        if not self.both_operands_is_muls(): return None
        common = set(self.one.operands) & set(self.two.operands)
        return common.pop() if common else None

    def has_common_factor(self) -> bool: return bool(self.get_common_factor())

    @action('вынести общий множитель', has_common_factor)
    def factor_out(self):
        if not self.both_operands_is_muls(): return
        common = self.get_common_factor()
        if common is None: return
        left_rest, right_rest = (mult.one if mult.one != common else mult.two for mult in self.operands)
        new_sum = self.__class__(left_rest, right_rest)
        new_mult = Mult(new_sum, common)
        self.replace(new_mult)

    def both_operands_is_div(self) -> bool: return all(isinstance(oper, Div) for oper in self.operands)

    def get_common_denominator(self) -> Node | None:
        if not self.both_operands_is_div(): return
        return self.one.one if self.one.two == self.two.two else None

    def has_common_denominator(self) -> bool: return bool(self.get_common_denominator())

    @action('вынести общий знаменатель', has_common_denominator)
    def denominator_out(self):
        if not self.both_operands_is_div(): return
        common = self.get_common_denominator()
        if common is None: return
        new_sum = self.__class__(self.one.one, self.two.one)
        new_div = Div(new_sum, common)
        self.replace(new_div)

######################################## Итоговые Классы Операторов ########################################

class Plus(Factorable, AssociativeCommutative, Infix, Operator):
    PRIORITY = 5

    def __init__(self, addend1, addend2): super().__init__(addend1, addend2)

    def __str__(self): return '+'

    def operands_are_logs_with_equal_base(self) -> bool:
        return all(isinstance(op, Log) for op in self.operands) and self.one.one == self.two.one
    @action('свернуть сумму логарифмов', operands_are_logs_with_equal_base)
    def plus_to_log(self):
        new_arg = Mult(self.one.two, self.two.two)
        new_log = self.one.create_same(new_arg)
        self.replace(new_log)

    def result(self) -> Node:
        if self.one == Number.ZERO: return self.two
        if self.two == Number.ZERO: return self.one
        try: return self.one + self.two
        except TypeError: return NotImplemented

class BinaryMinus(Factorable, Infix, Operator):
    PRIORITY = 5

    def __init__(self, minuend, subtrahend): super().__init__(minuend, subtrahend)

    def __str__(self): return '-'

    @action('представить как сумму')
    def as_plus(self):
        if isinstance(self.two, Number): self.replace(Plus(self.one, -self.two))
        elif isinstance(self.two, UnaryMinus): self.replace(Plus(self.one, self.two.one))
        else: self.replace(Plus(self.one, UnaryMinus(self.two)))

    def operands_are_logs_with_equal_base(self) -> bool:
        return all(isinstance(op, Log) for op in self.operands) and self.one.one == self.two.one
    @action('свернуть разность логарифмов', operands_are_logs_with_equal_base)
    def minus_to_log(self):
        new_arg = Div(self.one.two, self.two.two)
        new_log = self.one.create_same(new_arg)
        self.replace(new_log)

    def result(self) -> Node:
        if self.one == Number.ZERO: return UnaryMinus(self.two)
        if self.two == Number.ZERO: return self.one
        try: return self.one - self.two
        except TypeError: return NotImplemented

class Mult(AssociativeCommutative, Infix, Operator):
    PRIORITY = 4

    def __init__(self, factor1, factor2): super().__init__(factor1, factor2)

    def __str__(self): return '*'

    def both_operands_is_factorable(self) -> bool:
        return all(isinstance(oper, Factorable) for oper in self.operands)
    @action('раскрыть скобку слева', both_operands_is_factorable)
    def factor_in_left(self):
        if not isinstance(self.one, Plus): return
        for i, operand in enumerate(self.one.operands):
            self.one.operands[i] = Mult(operand, deepcopy(self.two))
        self.replace(self.one)

    @action('раскрыть скобку справа', both_operands_is_factorable)
    def factor_in_right(self) -> Node:
        if not isinstance(self.two, Plus): return
        for i, operand in enumerate(self.two.operands):
            self.two.operands[i] = Mult(deepcopy(self.one), operand)
        self.replace(self.two)

    def only_one_operand_is_factorable(self) -> bool:
        return isinstance(self.one, Factorable) != isinstance(self.two, Factorable)
    @action('раскрыть скобку', only_one_operand_is_factorable)
    def factor_in(self) -> Node:
        if isinstance(self.one, Factorable): self.factor_in_left(self)
        else: self.factor_in_right(self)

    def result(self) -> Node:
        if self.one == Number.ONE: return self.two
        if self.two == Number.ONE: return self.one
        if isinstance(self.one, Div) and isinstance(self.two,  Div):
            return Div(Mult(self.one.one, self.two.one), Mult(self.one.two, self.two.two))
        if isinstance(self.one, Div) and not isinstance(self.two, Div):
            return Div(Mult(self.one.one, self.two), self.one.two)
        if isinstance(self.two, Div) and not isinstance(self.one, Div):
            return Div(Mult(self.one, self.two.one), self.two.two)
        try: return self.one * self.two
        except TypeError: return NotImplemented

class Div(Infix, Operator):
    PRIORITY = 4

    def __init__(self, dividend, divisor): super().__init__(dividend, divisor)

    def __str__(self): return '/'

    def __iter__(self):
        div_begin, div_end = tokens.nested_bounds.create_pair(self)
        yield div_begin
        yield from self.one
        yield self
        yield from self.two
        yield div_end

    @action('раскрыть числитель', lambda self: isinstance(self.one, Factorable))
    def expand_numerator(self):
        if isinstance(self.one, Plus):
            new_operands = [Div(operand, deepcopy(self.two)) for operand in self.one.operands]
            self.replace(Plus.from_list(new_operands))
        elif isinstance(self.one, BinaryMinus):
            left = Div(self.one.one, deepcopy(self.two))
            right = Div(self.one.two, deepcopy(self.two))
            self.replace(BinaryMinus(left, right))

    def denominator_is_mult(self) -> bool: return isinstance(self.two, Mult)
    @action('раскрыть деление на произведение', denominator_is_mult)
    def expand_denominator_product(self):
        left = Div(deepcopy(self.one), deepcopy(self.two.one))
        right = Div(deepcopy(self.one), deepcopy(self.two.two))
        self.replace(Mult(left, right))

    def result(self) -> Node:
        if self.one == Number.ZERO: return Number(0)
        if self.two == Number.ONE: return self.one
        try: return self.one / self.two
        except TypeError: return NotImplemented

class Pow(Infix, Operator):
    PRIORITY = 2
    ASSOCIATIVITY_LEFT = False

    def __init__(self, base, degree): super().__init__(base, degree)

    def __str__(self): return '^'

    def __iter__(self):
        pow_begin, pow_end = tokens.nested_bounds.create_pair(self)
        yield pow_begin
        yield from self.one
        yield self
        yield from self.two
        yield pow_end

    def exponent_is_int_and_positive(self) -> bool:
        return isinstance(self.two, Number) and self.two.is_integer() and self.two > 1
    @action('представить как умножение', exponent_is_int_and_positive)
    def as_mult(self):
        base = self.one
        new_exp = Number(self.two.value - 1)
        if new_exp.value == 1: self.replace(Mult(deepcopy(base), deepcopy(base)))
        else: self.replace(Mult(deepcopy(base), Pow(deepcopy(base), new_exp)))

    @action('перенос степени в знаменатель')
    def as_div(self): self.replace(Div(Number.ONE, Pow(self.one, UnaryMinus(self.two))))

    @action('раскрыть умножение', lambda self: isinstance(self.one, Mult))
    def mult_out(self):
        self.replace(Mult(Pow(self.one.one, self.two), Pow(self.one.two, deepcopy(self.two))))

    def result(self) -> Node:
        if self.two == Number.ONE: return self.one
        try: return self.one ** self.two
        except TypeError: return NotImplemented

class UnaryMinus(Prefix, Operator):
    ARITY = 1
    PRIORITY = 3

    def __init__(self, operand): super().__init__(operand)

    def __str__(self): return '-'

    def result(self) -> Node:
        if isinstance(self.one, UnaryMinus): return self.one.one
        if isinstance(self.one, Plus):
            return BinaryMinus(UnaryMinus(self.one.one), self.one.two)
        try: return -self.one
        except TypeError: return NotImplemented

class Sin(Prefix, Operator):
    ARITY = 1
    PRIORITY = 1

    def __int__(self, x): super().__init__(x)

    def __str__(self): return 'sin'

    def result(self) -> Node:
        try: return Number(math.sin(self.one))
        except TypeError: return NotImplemented

class Cos(Prefix, Operator):
    ARITY = 1
    PRIORITY = 1

    def __init__(self, x): super().__init__(x)

    def __str__(self): return 'cos'

    def result(self) -> Node:
        try: return Number(math.cos(self.one))
        except TypeError: return NotImplemented

class Log(Prefix, Operator):
    ARITY = 2
    PRIORITY = 1

    def create_same(self, arg): return self.__class__(self.one, arg)

    @property
    def two(self): return self.operands[1]

    def __init__(self, base: Node, arg: Node):
        if isinstance(base, Number):
            if base <= 0 or base == 1: raise ValueError(f'основание логарифма: {base}')
        if isinstance(arg, Number) and arg <= 0: raise ValueError(f'аргумент логарифма: {base}')
        super().__init__(base, arg)

    def __str__(self): return 'log'

    def __iter__(self):
        log_begin, log_end = tokens.nested_bounds.create_pair(self)
        arg_begin, arg_end = tokens.function_brackets.create_pair()
        yield log_begin
        yield self
        yield from self.one
        yield log_end
        yield arg_begin
        yield from self.two
        yield arg_end

    @action('разложить логарифм произведения', lambda self: isinstance(self.two, Mult))
    def arg_mult_to_pluse(self):
        self.replace(Plus(self.create_same(self.two.one), self.create_same(self.two.two)))

    @action('разложить логарифм деления', lambda self: isinstance(self.two, Div))
    def arg_div_to_minus(self):
        self.replace(BinaryMinus(self.create_same(self.two.one), self.create_same(self.two.two)))

    @action('вынести степень аргумента', lambda self: isinstance(self.two, Pow))
    def arg_pow_to_mult(self):
        self.replace(Mult(self.two.two, self.create_same(self.two.one)))

    @action('внести множитель логарифма', lambda self: isinstance(self.parent, Mult))
    def mult_to_arg_pow(self):
        factor = self.parent.other_operand(self)
        new_log = self.create_same(Pow(self.two, factor))
        self.parent.replace(new_log)

    @action('вынести степень основания', lambda self: isinstance(self.one, Pow))
    def base_pow_to_mult(self):
        self.replace(Mult(Div(Number.ONE, self.one.two), Log(self.one.one, self.two)))

    @action('переход к новому основанию', interactive=True)
    def change_base(self, new_base: Node):
        self.replace(Div(Log(new_base, self.two), Log(new_base, self.one)))

    @action('запись в виде lg', lambda self: self.one == 10)
    def as_lg(self): self.replace(Lg(self.two))

    @action('запись в виде ln', lambda self: self.one == Number.E)
    def as_ln(self): self.replace(Ln(self.two))

    def result(self) -> Node:
        if self.one == self.two: return Number.ONE
        if self.two == Number.ONE: return Number.ZERO
        if isinstance(self.two, Pow) and self.one == self.two.two: return self.two.two
        try: return Number(math.log(self.two.value, self.one.value))
        except (TypeError, AttributeError): return NotImplemented

class ConstBaseLog(Log): # вспомогательный класс
    BASE: Number = None

    def create_same(self, arg): return self.__class__(arg)

    def __init__(self, arg): super().__init__(self.__class__.BASE, arg)

    def __iter__(self):
        arg_begin, arg_end = tokens.function_brackets.create_pair()
        yield self
        yield arg_begin
        yield from self.two
        yield arg_end

    @action('запись в виде обычного логарифма')
    def as_full_log(self):
        self.replace(Log(self.one, self.two))

class Lg(ConstBaseLog):
    ARITY = 1
    PRIORITY = 1
    BASE = Number(10)

    def __str__(self): return 'lg'

class Ln(ConstBaseLog):
    ARITY = 1
    PRIORITY = 1
    BASE = Number.E

    def __str__(self): return 'ln'

######################################## Класс Равенства ########################################

class Equal(Commutative, Infix, Operator):
    PRIORITY = 100
    INHERITED = False # отказ от наследования действий

    def __init__(self, left_hand_side, right_hand_side):
        super().__init__(left_hand_side, right_hand_side)

    def __str__(self): return "="

    def transfer_grandson(self, node: Node):
        parent = node.parent
        grand = parent.parent
        if isinstance(parent, Factorable) and grand is self:
            if isinstance(parent, BinaryMinus): parent.as_plus()
            other = parent.other_operand(node)
            if grand.one is parent:
                grand.one = other
                grand.two = Plus(self.two, UnaryMinus(node))
            else:
                grand.two = other
                grand.one = Plus(UnaryMinus(node), self.one)

    def transfer_child(self, node: Node):
        if self.is_child(node):
            other = self.other_operand(node)
            if node is self.one:
                self.one = Number.ZERO
                self.two = Plus(UnaryMinus(node), other)
            else:
                self.two = Number.ZERO
                self.one = BinaryMinus(other, node)

    @action('поменять левую и правую части')
    def swap_left_and_right(self): super().commutative(self)

    @action('умножить на -1')
    def multiply_by_minus_one(self):
        self.one = UnaryMinus(self.one)
        self.two = UnaryMinus(self.two)

    @action('умножить обе части', interactive=True)
    def multiply_both_sides(self, multiplier: Node):
        self.one = Mult(self.one, multiplier)
        self.two = Mult(self.two, multiplier)

    @action('прибавить к обоим частям', interactive=True)
    def add_both_sides(self, addend: Node):
        self.one = Plus(self.one, addend)
        self.two = Plus(self.two, addend)
