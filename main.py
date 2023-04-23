from parser import get_ast_from_prog_text
from codegen import PythonCodegen
import json
import os


def execute_py_code(code: str):
    with open('output_code.py', 'w') as f:
        f.write(code)
    os.system("python3 output_code.py")


def main():
    prog_text = open('prog').read()

    ast = get_ast_from_prog_text(prog_text)

    output_source_code = PythonCodegen().generate_py_code(ast)

    print("Получившаяся программа на python:")
    print(output_source_code)

    execute_py_code(output_source_code)


main()