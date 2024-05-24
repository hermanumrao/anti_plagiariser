import ast
import random
import sys

def name_randomizer(li):
    dic={}
    for i in range(0,len(li)):
        if len(li[i]) >5 :
            x=random.randint(0,2)
            if x==0:
                if li[i][0:1] not in dic.values():
                    dic[li[i]]=li[i][0:1]
                else :
                    x+=1
            elif x==1:
                if li[i][0:len(li[i])] not in dic.values():
                    dic[li[i]]=li[i][0:1]
                else :
                    x+=1
            else :
                a=li[i].split('_')[-1]
                if a not in dic.values():
                    dic[li[i]]=a
                else :
                    x+=1
    return dic

def replace_words(text, replacements):
    result = []
    i = 0
    text_length = len(text)
    
    while i < text_length:
        # Identify the start of a word
        if text[i].isalnum():
            start = i
            while i < text_length and text[i].isalnum():
                i += 1
            word = text[start:i]
            # Replace the word if it exists in the replacements dictionary
            result.append(replacements.get(word, word))
        else:
            # Append non-alphanumeric characters as they are
            result.append(text[i])
            i += 1
    
    return ''.join(result)

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

    d=name_randomizer(list(analyzer.functions))
    d.update(name_randomizer(list(analyzer.classes)))
    d.update(name_randomizer(list(analyzer.variables)))
    return d

def main(argv):
    if len(argv) <1 or len(argv)>3:
        print("improper usage, \n right usage is python_fix <input.py> <output.py>")
        exit()
    else:
        inp=argv[1]
        if len(argv)==3:
            outp=argv[2]
        else:
            outp="output.py"

    file_in = open(inp, 'r')
    file_out = open(outp, 'w')
    text=""
    dic=analyze_code(file_in.read()) 
    file_in.seek(0)
    print(dic)
    print(dic.keys())
    for line in file_in.readlines():
        if '#' in line:
            line = line.split('#')[0] + '\n'
        line=replace_words(line,dic)
        text+=line
    print(text)
    file_out.writelines(text)
    file_in.close()
    file_out.close()

if __name__ == "__main__":
   main(sys.argv) 
