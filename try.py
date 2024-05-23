import ast

def name_randomizer(li):
    for identifier in li:


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []
        self.variables = set()
        self.assignments = set()

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.variables.add(node.id)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.assignments.add(target.id)
            elif isinstance(target, ast.Tuple):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        self.assignments.add(elt.id)
        self.generic_visit(node)

def analyze_code(file):
    tree = ast.parse(file)


    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    
    print(f"Functions: {analyzer.functions}")
    print(f"Classes: {analyzer.classes}")
    print(f"Variables: {list(analyzer.variables)}")
    print(f"Assignments: {list(analyzer.assignments)}")

    d=name_randomizer(analyzer.functions) 

if __name__ == "__main__":
    file_path = 'input.py'  # Replace with your .py file path
    file_in = open('input.py', 'r')
    file_out = open('output.py', 'w')
    text=""
    for line in file_in:
        if '#' in line:
            line = line.split('#')[0] + '\n'
        text=text+line
    
    analyze_code(text) 
    file_in.close()
    file_out.close()



