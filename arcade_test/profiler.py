import cProfile
import pstats
import io
from problem import create_problem
import ast

def profile_all_functions():
    """Профилирует ВСЕ функции проекта"""
    
    pr = cProfile.Profile()
    pr.enable()
    
    # ТЕСТИРУЕМ ВСЁ:
    
    # 1. Парсинг и создание деревьев
    expressions = [
        '*(a, +(b, c))',
        '*(*(c, +(1, 2)), *(a, b))', 
        '+(*(x, y), -(z, w))',
        'sin(+(a, b))'
    ]
    
    problems = []
    for expr in expressions * 50:  # Многократно
        problems.append(create_problem(expr))
    
    # 2. Все методы Problem
    for A in problems[:10]:  # На подмножестве
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
            # Ассоциативность
            if hasattr(op, 'associative'):
                for _ in range(10):
                    op.associative()
            
            # Коммутативность  
            if hasattr(op, 'commutative'):
                for _ in range(10):
                    op.commutative()
            
            # Решение
            for _ in range(5):
                op.solve()
            
            # Сравнение и хеширование
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
        ps.print_stats(100)  # топ-100 функций
    
    print("✅ Профилирование завершено! Смотри profile_results.txt")


profile_all_functions()