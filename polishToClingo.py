import sys

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

def firstStep(node): 
    # replace a <-> b by (a /\ b) \/ (¬a /\ ¬b) 
    if node.item == "=": # damos por hecho que left y right not null
        node.item = "|"

        # Conjunción en la rama izquierda
        aux_left = Node("&")
        aux_left.left = node.left
        aux_left.right = node.right

        # Conjunción de negaciones en la rama derecha
        aux_right = Node("&")

        aux_right.left = Node("-")
        aux_right.left.left = node.left

        aux_right.right = Node("-")
        aux_right.right.left = node.right

        node.left = aux_left
        node.right = aux_right

    # replace a -> b by ¬a \/ b
    elif node.item == ">":
        node.item = "|"
        aux = Node("-") # nodo auxiliar para añadir la negación
        aux.left = node.left
        node.left = aux
    
    # replace a xor b by (a /\ ¬b) \/ (¬a /\ b)  
    elif node.item == "%":
        node.item = "|"

        # Conjunción en la rama izquierda
        aux_left = Node("&")
        aux_left.left = node.left # a
        aux_left.right = Node("-")
        aux_left.right.left = node.right # ¬b

        # Conjunción de la rama derecha
        aux_right = Node("&")
        aux_right.left = Node("-")
        aux_right.left.left = node.left
        aux_right.right = node.right

        node.left = aux_left
        node.right = aux_right

    elif node.item == "1":
        node.item = "#true"
    elif node.item == "0":
        node.item = "#false" 

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
            #node = node.left

            if node.left.item == "|":
                node.item = "&"
            else:
                node.item = "|"

            # Negar hijo izquierdo
            aux_left = Node("-")
            aux_left.left = node.left.left

            # Negar hijo derecho
            aux_right = Node("-")
            aux_right.left = node.left.right
            
            node.left = aux_left
            node.right = aux_right

        elif node.left.item == "-": # ¬(¬a) = a (las que se creen con DeMorgan se deshacen aquí)
            node = node.left.left 

    if node.left is not None:
        node.left = toNNF(node.left) # no importa el orden
    if node.right is not None:
        node.right = toNNF(node.right)

    return node

def cnf(node):
    if node.item == "&":    
        aux_left = cnf(node.left)
        aux_right = cnf(node.right)

        aux_left.extend(aux_right) # se pegan las listas

        return aux_left

    elif node.item == "|":
        aux_left = cnf(node.left)
        aux_right = cnf(node.right)

        l = []

        for i in aux_left:
            for j in aux_right:
                aux = []

                aux.extend(i)
                aux.extend(j)

                l.append(aux)

        return l 

    elif node.item == "-":
        return [["-" + node.left.item]]
    else:
        return [[node.item]]

def toClingo(l):
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

def reductionToCNF(expresion):
    word_splited = expresion.split()
    tree = to_tree(word_splited[:len(word_splited)-1]) # quitamos el punto y construimos arbol

    tree = firstStep(tree)

    while not isNNF(tree):
        tree = toNNF(tree)

    l = cnf(tree)

    return l
    

def main():

    if len(sys.argv) != 2:
        print("Usage: polishToClingo <input file>")
        exit()

    filaname = sys.argv[1]

    f = open(filaname, "r")
    words = set()
    ins = ""

    # inicia bucle infinito para leer línea a línea
    while True: 
        # lee línea
        linea = f.readline()
        if not linea: 
            break  # Si no hay más se rompe bucle

        l = reductionToCNF(linea) # obtenemos la lista de listas
        words_aux, result = toClingo(l)

        words = words | words_aux
        ins = ins + "% " + linea + "\n" + result

    header = "{"
    for x in words:
        header = header + x + ";"
    header = header[:len(header)-1] + "}.\n"
        
    f.close()  # Cierra archivo

    filaname = filaname.split(".")

    f = open(filaname[0] + ".lp" , "w")
    f.write(header)
    f.write(ins)
    f.close()

main()
