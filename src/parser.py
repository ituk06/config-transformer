import toml
from lark import Lark, Transformer, v_args
from lark.exceptions import LarkError
from .evaluator import Evaluator
from .errors import ConfigSyntaxError

class ConfigTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.variables = {}
        self.evaluator = Evaluator(self.variables)
    
    def start(self, items):
        result = {}
        for item in items:
            if item is not None:
                if isinstance(item, tuple) and len(item) == 2:
                    key, value = item
                    result[key] = value
                elif isinstance(item, dict):
                    result.update(item)
        return result
    
    def const_decl(self, items):
        name = str(items[0])
        value = items[1]
        self.variables[name] = value
        return None
    
    def dict(self, items):
        result = {}
        for item in items:
            if item is not None:
                key, value = item
                result[key] = value
        return result
    
    def pair(self, items):
        key = str(items[0])
        value = items[1]
        return (key, value)
    
    def array(self, items):
        return list(items)
    
    @v_args(inline=True)
    def string(self, s):
        s = str(s)
        if s.startswith('@'):
            return s[2:-1]  # Убираем @" и "
        else:
            return s[1:-1]  # Убираем " и "
    
    @v_args(inline=True)
    def bool(self, b):
        return b == "true"
    
    @v_args(inline=True)
    def number(self, n):
        try:
            return int(n)
        except ValueError:
            return float(n)
    
    def const_expr(self, items):
        expr_tree = items[0]
        return self.evaluator.evaluate(expr_tree)
    
    # Операции
    def add(self, items):
        return ('add', items[0], items[1])
    
    def sub(self, items):
        return ('sub', items[0], items[1])
    
    def mul(self, items):
        return ('mul', items[0], items[1])
    
    def div(self, items):
        return ('div', items[0], items[1])
    
    def func_call(self, items):
        func_name = str(items[0])
        arg = items[1]
        return ('func_call', func_name, arg)
    
    def var(self, items):
        var_name = str(items[0])
        return ('var', var_name)
    
    @v_args(inline=True)
    def CNAME(self, name):
        return str(name)

def parse_config(text: str) -> dict:
    with open('src/grammar.lark', 'r', encoding='utf-8') as f:
        grammar = f.read()
    
    parser = Lark(
        grammar,
        parser='lalr',
        transformer=ConfigTransformer(),
        propagate_positions=False
    )
    
    try:
        result = parser.parse(text)
        return result
    except LarkError as e:
        raise ConfigSyntaxError(f"Синтаксическая ошибка: {e}")
    except Exception as e:
        raise ConfigSyntaxError(f"Ошибка обработки: {e}")