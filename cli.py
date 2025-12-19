#!/usr/bin/env python3
import argparse
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import toml
    from src.parser import parse_config
    from src.errors import ConfigSyntaxError, ConfigEvaluationError
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что вы установили зависимости: pip install toml lark")
    print("И что у вас есть файлы src/__init__.py")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Конвертер учебного конфигурационного языка (вариант 30) в TOML'
    )
    parser.add_argument(
        'input',
        help='Путь к входному файлу на учебном языке'
    )
    parser.add_argument(
        '-o', '--output',
        help='Путь к выходному файлу TOML'
    )
    
    args = parser.parse_args()
    
    try:
        print(f"Обработка файла: {args.input}")
        
        if not os.path.exists(args.input):
            raise FileNotFoundError(f"Файл не найден: {args.input}")
        
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = parse_config(content)
        toml_str = toml.dumps(result)
        
        if args.output:
            # Создаем директорию, если её нет
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
            
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(toml_str)
            print(f"Файл сохранен: {args.output}")
        else:
            print(toml_str)
        
    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except ConfigSyntaxError as e:
        print(f"Синтаксическая ошибка: {e}", file=sys.stderr)
        sys.exit(2)
    except ConfigEvaluationError as e:
        print(f"Ошибка вычисления: {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"Ошибка: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(4)

if __name__ == '__main__':
    main()