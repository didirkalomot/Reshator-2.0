import cProfile
import pstats
import io
from problem import create_problem
import ast
import parse  # импортируем модуль parse

def profile_all_functions():
    """Профилирует ВСЕ функции проекта"""
    
    pr = cProfile.Profile()
    pr.enable()
    
    # ТЕСТИРУЕМ ВСЁ:
    
    # 1. Парсинг и создание деревьев - СРАВНЕНИЕ МЕТОДОВ
    expressions = [
        '*(a, +(b, c))',
        '*(*(c, +(1, 2)), *(a, b))', 
        '+(*(x, y), -(z, w))',
        'sin(+(a, b))'
    ]
    
    problems_recursive = []
    problems_iterative = []
    
    # Рекурсивный парсинг
    for expr in expressions * 25:  # 25 раз каждый
        problems_recursive.append(create_problem(expr))  # использует старый рекурсивный
    
    # Итеративный парсинг  
    for expr in expressions * 25:
        try:
            root = parse.create_ast_tree_iterative(expr)  # новый итеративный
            problems_iterative.append(ast.Problem(root))
        except Exception as e:
            print(f"Ошибка в итеративном парсинге '{expr}': {e}")
            # fallback на рекурсивный
            problems_iterative.append(create_problem(expr))
    
    problems = problems_recursive + problems_iterative
    
    # 2. Все методы Problem (остальной код без изменений)
    for A in problems[:10]:
        # Обновление списка
        for _ in range(20):
            A.update_list()
        
        # Свойства
        for _ in range(20):
            _ = A.nodes
            _ = A.values  
            _ = A.operators
            _ = len(A)
            _ = str(A)
        
        # Операции
        if A.operators:
            for op in A.operators[:3]:
                A.work(op)
                if isinstance(op, ast.Commutative):
                    A.commutative(op)
        
        # Дистрибутивность
        if A.values:
            for val in A.values[:2]:
                A.factor_in(val)
                A.factor_in(val, True)
                A.factor_in(val, False)
        
        # Вынос за скобки
        if len(A.values) >= 2:
            try:
                A.factor_out(A.values[0], A.values[1])
            except:
                pass
    
    # 3. Методы узлов AST
    for A in problems[:5]:
        if A.operators:
            op = A.operators[0]
            if hasattr(op, 'associative'):
                for _ in range(10):
                    op.associative()
            if hasattr(op, 'commutative'):
                for _ in range(10):
                    op.commutative()
            for _ in range(5):
                op.solve()
            for _ in range(10):
                _ = op == op
                _ = hash(op)
    
    # 4. Глубокое копирование
    for A in problems[:3]:
        if A.operators:
            for _ in range(5):
                _ = ast.deepcopy(A.operators[0])
    
    pr.disable()
    
    # Сохраняем результаты
    with open('profile_results.txt', 'w') as f:
        ps = pstats.Stats(pr, stream=f)
        ps.sort_stats('cumulative')
        ps.print_stats(100)
    
    print("✅ Профилирование завершено! Смотри profile_results.txt")

profile_all_functions()