class PythonCodegen:
    operators_mapping = {
        ':=': '=',
        '>': '>',
        '<': '<',
        '=': '==',
        '+': '+',
        '-': '-',
    }

    def generate_py_code(self, ast) -> str:
        if not ast:
            return ""
        elif isinstance(ast, dict):
            if ast.get("type") == "for":
                init = self.generate_py_code(ast["init"])
                cond = self.generate_py_code(ast["cond"])
                next = self.generate_py_code(ast["next"])
                body = self.generate_py_code(ast["body"])
                return f'''{init}\nwhile {cond}:\n{body}\t{next} '''
            elif ast.get('type') == 'print':
                arg = self.generate_py_code(ast["arg"])
                return f'print({arg})'
            elif ast.get("op") is not None:
                left = self.generate_py_code(ast["left"])
                right = self.generate_py_code(ast["right"])
                op = self.operators_mapping[ast['op']]
                return f"{left} {op} {right}"
            elif ast.get("num") is not None:
                return '0x' + str(ast["num"])
            elif ast.get('id') is not None:
                return str(ast['id'])
            else:
                raise ValueError("Undefined AST node type")
        elif isinstance(ast, list):
            result = ""
            for element in ast:
                result += '\t' + self.generate_py_code(element) + "\n"
            return result
        else:
            raise ValueError("Undefined AST node type")