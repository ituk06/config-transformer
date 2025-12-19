import unittest
import sys
import os

# Добавляем корневую директорию в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.parser import parse_config
    from src.errors import ConfigSyntaxError
except ImportError as e:
    print(f"Ошибка импорта в тестах: {e}")
    print("Убедитесь, что есть файл src/__init__.py")
    raise

class TestParser(unittest.TestCase):
    
    def test_simple_dict(self):
        """Тест простого словаря"""
        config = """
        table(
            port => 8080,
            host => @"localhost"
        )
        """
        result = parse_config(config)
        self.assertEqual(result, {
            'port': 8080,
            'host': 'localhost'
        })
    
    def test_array(self):
        """Тест массива"""
        config = """{1, 2, 3, @"four"}"""
        result = parse_config(config)
        self.assertEqual(result, [1, 2, 3, 'four'])
    
    def test_constants(self):
        """Тест констант"""
        config = """
        var port := 8080;
        var host := @"127.0.0.1";
        
        table(
            server_port => |port|,
            server_host => |host|
        )
        """
        result = parse_config(config)
        self.assertEqual(result, {
            'server_port': 8080,
            'server_host': '127.0.0.1'
        })
    
    def test_expression_addition(self):
        """Тест выражения сложения"""
        config = """
        var base := 8000;
        var offset := 80;
        
        table(
            port => |base + offset|
        )
        """
        result = parse_config(config)
        self.assertEqual(result, {'port': 8080})
    
    def test_expression_subtraction(self):
        """Тест выражения вычитания"""
        config = """
        table(
            result => |10 - 3|
        )
        """
        result = parse_config(config)
        self.assertEqual(result, {'result': 7})
    
    def test_expression_multiplication(self):
        """Тест выражения умножения"""
        config = """
        table(
            result => |5 * 4|
        )
        """
        result = parse_config(config)
        self.assertEqual(result, {'result': 20})
    
    def test_expression_division(self):
        """Тест выражения деления"""
        config = """
        table(
            result => |10 / 2|
        )
        """
        result = parse_config(config)
        self.assertEqual(result, {'result': 5})
    
    def test_print_function(self):
        """Тест функции print()"""
        config = """
        table(
            message => |print(@"test")|
        )
        """
        result = parse_config(config)
        self.assertEqual(result, {'message': 'test'})
    
    def test_chr_function(self):
        """Тест функции chr()"""
        config = """
        table(
            char => |chr(65)|
        )
        """
        result = parse_config(config)
        self.assertEqual(result, {'char': 'A'})
    
    def test_nested_dict(self):
        """Тест вложенного словаря"""
        config = """
        table(
            database => table(
                host => @"localhost",
                port => 5432
            ),
            cache => table(
                enabled => true,
                size => 1024
            )
        )
        """
        result = parse_config(config)
        self.assertEqual(result['database']['host'], 'localhost')
        self.assertEqual(result['database']['port'], 5432)
        self.assertEqual(result['cache']['enabled'], True)
        self.assertEqual(result['cache']['size'], 1024)
    
    def test_invalid_syntax(self):
        """Тест на некорректный синтаксис"""
        config = "table( port => ; )"
        with self.assertRaises(ConfigSyntaxError):
            parse_config(config)
    
    def test_comments(self):
        """Тест комментариев"""
        config = """
        #[
        Многострочный
        комментарий
        ]#
        
        table(
            key => @"value"
        )
        """
        result = parse_config(config)
        self.assertEqual(result, {'key': 'value'})
    
    def test_expression_with_variable(self):
        """Тест выражения с переменной"""
        config = """
        var count := 5;
        var multiplier := 2;
        
        table(
            total => |count * multiplier|
        )
        """
        result = parse_config(config)
        self.assertEqual(result, {'total': 10})
    
    def test_complex_expression(self):
        """Тест сложного выражения"""
        config = """
        var a := 10;
        var b := 2;
        
        table(
            result => |(a + b) * 3 / 4 - 1|
        )
        """
        result = parse_config(config)
        # (10 + 2) * 3 / 4 - 1 = 12 * 3 / 4 - 1 = 36 / 4 - 1 = 9 - 1 = 8
        self.assertEqual(result, {'result': 8})
    
    def test_array_in_dict(self):
        """Тест массива внутри словаря"""
        config = """
        table(
            servers => {@"server1", @"server2", @"server3"},
            ports => {80, 443, 8080}
        )
        """
        result = parse_config(config)
        self.assertEqual(result['servers'], ['server1', 'server2', 'server3'])
        self.assertEqual(result['ports'], [80, 443, 8080])
    
    def test_boolean_values(self):
        """Тест булевых значений"""
        config = """
        table(
            enabled => true,
            disabled => false
        )
        """
        result = parse_config(config)
        self.assertEqual(result, {'enabled': True, 'disabled': False})
    
    def test_string_concatenation_in_expression(self):
        """Тест конкатенации строк в выражении"""
        config = """
        var prefix := @"Hello, ";
        var name := @"World";
        
        table(
            greeting => |prefix + name|
        )
        """
        result = parse_config(config)
        self.assertEqual(result, {'greeting': 'Hello, World'})

if __name__ == '__main__':
    unittest.main()