##################### HELP DO ENUNCIADO #####################
###### Vars
# Redeclaração
# Não-Declaração
# Usada mas não inicializada
# Declarada mas nunca mencionada
# var -> name, type, declaration?, redeclaration?, inicialization?, used

###### Types
# Total de vars declaradas por cada tipo
# type -> nr_variables

###### Instructions
# Nr de instrucoes de cada tipo
# Atribuicao | Leitura e Escrita | Condicional | Ciclico
# inst_type -> nr_instructions

from lark import Lark
from lark.visitors import Interpreter
from grammar import grammar

p = Lark(grammar) # cria um objeto parser

string_test = """
int y; 
int x = 10 + 23; 
x = 10;
dict d = {1: "oi", "teste" : [1,2,3]};
"""

tree = p.parse(string_test) # retorna uma tree

class InterpreterIntervalos(Interpreter):
    def __init__(self):
        # Convem comentarmos a estrutura de cada um destes
        self.symbols = {
            'vars' : {}, 
            'types' : {},
            'instructions' : {
                'assign' : 0,
                'read_write' : 0,
                'conditional' : 0,
                'cycle' : 0
            },
            'errors': {
                'redeclarations' : 0,
                'not_declared' : 0
            }
        }

    def start(self,tree):
        self.visit_children(tree)
        return self.symbols
    
    def expressao(self, tree):
        tree_data = tree.children[0].data

        if tree_data == 'atribuicao':    
            self.symbols['instructions']['assign'] +=1
        elif tree_data == 'operacao':
            self.symbols['instructions']['read_write'] += 1
        elif tree_data == 'condicional':
            self.symbols['instructions']['conditional'] += 1
        elif tree_data == 'ciclo':
            self.symbols['instructions']['cycle'] += 1
        
        self.visit(tree.children[0])

    def declaracao(self,tree):
        var_type = tree.children[0].children[0].value
        var_name = tree.children[1].children[0].value

        # tratar tipo
        if var_type in self.symbols['types'].keys():
            self.symbols['types'][var_type] += 1
        else:
            self.symbols['types'][var_type] = 1
        
        # tratar variavel
        if var_name in self.symbols['vars'].keys():
            self.symbols['errors']['redeclarations'] += 1
            self.symbols['vars'][var_name]['redeclaration?'] = True

        else:
            self.symbols['vars'][var_name] = {
                'type': var_type,
                'declaration?': True,
                'redeclaration?': False,
                'inicialization?': False,
                'used': False
        }

    def inicializacao(self,tree):
        var_type = tree.children[0].children[0].value
        var_name = tree.children[1].children[0].value
        
        # tratar tipo
        if var_type in self.symbols['types'].keys():
            self.symbols['types'][var_type] += 1
        else:
            self.symbols['types'][var_type] = 1
        
        # tratar variavel
        if var_name in self.symbols['vars'].keys():
            self.symbols['errors']['redeclarations'] += 1
            self.symbols['vars'][var_name]['redeclaration?'] = True

        else:
            self.symbols['vars'][var_name] = {
                'type': var_type,
                'declaration?': True,
                'redeclaration?': False,
                'inicialization?': True,
                'used': 0
        }

    def atribuicao(self,tree):
        var_name = tree.children[0].children[0].value

        if var_name not in self.symbols['vars'].keys():
            self.symbols['errors']['not_declared'] += 1
        
        self.symbols['vars'][var_name]['used'] = True

    # Precisamos deste? já tratamos as variaveis antes
    '''def var(self, tree):
        if tree not in self.symbols['vars'].keys():
            self.symbols['vars'][tree] = [tree, '', False, False, False, 0]
        else:
            self.symbols['vars'][tree]['used'] += 1'''


data = InterpreterIntervalos().visit(tree)
print(data)

# estrutura para ser imprimida no html:

# todas as variáveis do programa: var1, var2, var3, var4...
# variáveis declaradas 2 vezes: var1, var2, var3, var4...
# variáveis mencionadas mas nunca declaradas antes: var1, var2, var3, var4...
# variáveis usadas que não foram inicializadas: var1, var2, var3, var4...
# variáveis declaradas mas nunca mencionadas: var1, var2, var3, var4...

# tipos usados no programa
# int: 3 
# char: 2

# total de instruções
# atribuições: 4
# leitura e escrita: 15
# condicional: 7
# ciclos: 2
# total: 28

# ...