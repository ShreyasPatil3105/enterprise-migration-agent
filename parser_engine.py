import ast

class DeadCodeFinder(ast.NodeVisitor):
    def __init__(self):
        self.defined_functions = set()
        self.called_functions = set()

    def visit_FunctionDef(self, node):
        self.defined_functions.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.called_functions.add(node.func.id)
        self.generic_visit(node)

def analyze_file(filepath):
    with open(filepath, "r") as file:
        tree = ast.parse(file.read(), filename=filepath)

    finder = DeadCodeFinder()
    finder.visit(tree)

    unused = finder.defined_functions - finder.called_functions

    print(f"Functions defined: {finder.defined_functions}")
    print(f"Functions called: {finder.called_functions}")
    print(f"Potentially dead code (unused): {unused}")

if __name__ == "__main__":
    analyze_file("sample_code.py")
