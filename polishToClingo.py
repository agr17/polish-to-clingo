#!/usr/bin/python3

class Node:

    def __init__(self, item):
        self.item = item
        self.left = None
        self.right = None

# El recorrido en preorden devuelve la expresión en notación polaca
def preorden(node):
    nodeList = []
    if node is not None:
        nodeList = nodeList + preorden(node.left)
        nodeList.insert(0, node.item)
        nodeList = nodeList + preorden(node.right)
    return nodeList

def firstStep(node): # FALTA XOR
    # replace a <-> b by (a /\ b) \/ (¬a /\ ¬b) 
    if node.item == "=": # damos por hecho que left y right not null
        node.item = "|"

        # Conjunción en la rama izquierda
        aux_left = Node("&")
        aux_left.left = node.left
        aux_left.right = node.right

        # Conjunción de negaciones en la rama derecha
        aux_right = Node("&")

        if node.left.item == "-":
            aux_right.left = node.left.left
        else:
            aux_right.left = Node("-")
            aux_right.left.left = node.left
        
        if node.right.item == "-":
            aux_right.right = node.right.left
        else:
            aux_right.right = Node("-")
            aux_right.right.left = node.left

        node.left = aux_left
        node.right = aux_right

    # replace a -> b by ¬a \/ b
    elif node.item == ">":
        node.item = "|"
        aux = Node("-") # nodo auxiliar para añadir la negación
        aux.left = node.left
        node.left = aux

    if node.left is not None:
        firstStep(node.left) # no importa el orden
    if node.right is not None:
        firstStep(node.right)
    return node

def isNNF(node):
    if node.item == "-" and (node.left.item == "|" or node.left.item == "&" or node.left.item == "-"):
        return False
    aux = True
    if node.left is not None:
        aux = aux and isNNF(node.left) # no importa el orden
    if node.right is not None:
        aux = aux and isNNF(node.right)
    return aux

def toNNF(node):
    if node.item == "-": 
        if node.left.item == "|" or node.left.item == "&": # DeMorgan
            node = node.left

            if node.item == "|":
                node.item = "&"
            else:
                node.item = "|"

            # Negar hijo izquierdo
            aux = Node("-")
            aux.left = node.left
            node.left = aux
      
            # Negar hijo derecho
            aux = Node("-")
            aux.left = node.right
            node.right = aux

        elif node.left.item == "-": # ¬(¬a) = a (las que se creen con DeMorgan se deshacen aquí)
            node = node.left.left 

    if node.left is not None:
        node.left = toNNF(node.left) # no importa el orden
    if node.right is not None:
        node.right = toNNF(node.right)

    return node

def isCNF(node): # se da por hecho que se han seguido todos los pasos previos
    if node.item == "|" and ( node.left.item == "&" or node.right.item == "&" ):
        return False

    if node.item == "-": # está en NNF, la negación solo puede ir con atomos
        node.item = "-" + node.left.item # por tanto, se juntan en un mismo nodo
        node.left = None

    aux = True

    if node.left is not None:
        aux = aux and isCNF(node.left) # no importa el orden
    if node.right is not None:
        aux = aux and isCNF(node.right)
    return aux
    

def toCNF(node): # ¿Con esta llega? Solo hace distributiva
    aux_left = None
    aux_right = None
    
    if node.item == "|": # Se puede reducir, aux = node.right/left según donde esté &!
        if node.left.item == "&":

            aux_left = Node("|")
            aux_left.left = node.right
            aux_left.right = node.left.left

            aux_right = Node("|")
            aux_right.left = node.right
            aux_right.right = node.left.right

        elif node.right.item == "&":

            aux_left = Node("|")
            aux_left.left = node.left
            aux_left.right = node.right.left

            aux_right = Node("|")
            aux_right.left = node.left
            aux_right.right = node.right.right

        if aux_left is not None: # ¿Cambiar por un else + break? Break solo para loops...
            node.item = "&"
            node.left = aux_left
            node.right = aux_right

    if node.left is not None:
        node.left = toCNF(node.left)  
    if node.right is not None:
        node.right = toCNF(node.right)

    return node

def asociative(node):
    if node.item == "&":
        node.left = asociative(node.left)
        node.right = asociative(node.right)
    elif node.item == "|":
        if node.left.item != ("|" or "-") and node.right.item != ("|" or "-"):
            node.item = [node.left.item, node.right.item] 
            node.left = None
            node.right = None
        elif node.left.item != ("|" or "-"):
            node = [node.left.item,asociative(node.right)]
            node.left = None
            node.right = None
        elif node.right.item != ("|" or "-"):
            node = [asociative(node.left),node.right.item]
            node.left = None
            node.right = None
        else:
            node = [asociative(node.left),asociative(node.right)]
            node.left = None
            node.right = None
    else:
        node.item = [node.item]
    return node

def toClingo(tree):
    l = preorden(tree)
    words = set()
    result = ""

    for x in l:
        if x != "&":
            aux = ":- "
            for y in x:
                if y.startswith("-"):
                    aux = aux + y[1:] + ", "
                    words.add(y[1:])
                else:
                    aux = aux + "not " + y + ", "
                    words.add(y)
            
            result = result + aux[:len(aux)-2] + ".\n" # quitamos la última ,

    return (words,result + "\n")

            

PAIR = {"&","|",">","=","%"} # Constante, estas operaciones son BINARIAS

def to_tree(words):

    if len(words) == 1:
        return Node(words[0])

    word = words[0]
    rest = words[1:]

    if word in PAIR:
        node = Node(word)

        n = 1 # Para controlar que pertenece a la rama izquierda
        aux = 0 # Offset para ver donde termina la rama izquierda

        for var in rest:
            aux = aux + 1
            if var in PAIR:
                n = n + 1
            else: 
                if var == "-":
                    n = n
                else:
                    n = n - 1
            
            if n == 0:
                break
        
        node.left = to_tree(rest[:aux])
        node.right = to_tree(rest[aux:])

        return node
    else: 
        node = Node(word)
        node.left = to_tree(rest)
        return node            

def process_polish(word):
    if not word.endswith("."):
        print("Entrada invalida, no termina con .")
    else:

        word_splited = word.split()
        return to_tree(word_splited[:len(word_splited)-1]) # Quitar el .

def reductionToCNF(expresion):
    word_splited = expresion.split()
    tree = to_tree(word_splited[:len(word_splited)-1])

    tree = firstStep(tree)

    while not isNNF(tree):
        tree = toNNF(tree)

    while not isCNF(tree):
        tree = toCNF(tree)

    tree = asociative(tree)

    return tree
    

def main():

    filaname = "polish.txt"

    f = open(filaname, "r")
    words = set()
    ins = ""

    # inicia bucle infinito para leer línea a línea
    while True: 
        # lee línea
        linea = f.readline()
        if not linea: 
            break  # Si no hay más se rompe bucle

        tree = reductionToCNF(linea)
        words_aux, result = toClingo(tree)

        words = words | words_aux
        ins = ins + "% " + linea +result

    header = "{"
    for x in words:
        header = header + x + ";"
    header = header[:len(header)-1] + "}.\n"
        
    f.close()  # Cierra archivo

    filaname = filaname.split(".")

    f = open(filaname[0] + ".lp" , "x")
    f.write(header)
    f.write(ins)
    f.close()

main()