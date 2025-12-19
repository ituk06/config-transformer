class Evaluator:
    def __init__(self, variables):
        self.variables = variables
    
    def evaluate(self, node):
        if isinstance(node, tuple):
            op = node[0]
            
            if op == 'add':
                left = self.evaluate(node[1])
                right = self.evaluate(node[2])
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            
            elif op == 'sub':
                left = self.evaluate(node[1])
                right = self.evaluate(node[2])
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left - right
                raise ValueError(f"Вычитание для типов {type(left)} и {type(right)} не поддерживается")
            
            elif op == 'mul':
                left = self.evaluate(node[1])
                right = self.evaluate(node[2])
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left * right
                raise ValueError(f"Умножение для типов {type(left)} и {type(right)} не поддерживается")
            
            elif op == 'div':
                left = self.evaluate(node[1])
                right = self.evaluate(node[2])
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    if right == 0:
                        raise ValueError("Деление на ноль")
                    return left / right
                raise ValueError(f"Деление для типов {type(left)} и {type(right)} не поддерживается")
            
            elif op == 'func_call':
                func_name = node[1]
                arg = self.evaluate(node[2])
                
                if func_name == 'print':
                    return str(arg)
                elif func_name == 'chr':
                    if isinstance(arg, int):
                        return chr(arg)
                    raise ValueError(f"chr() ожидает целое число, получен {type(arg)}")
                else:
                    raise ValueError(f"Неизвестная функция: {func_name}")
            
            elif op == 'var':
                var_name = node[1]
                if var_name in self.variables:
                    return self.variables[var_name]
                raise ValueError(f"Неизвестная переменная: {var_name}")
        
        return node