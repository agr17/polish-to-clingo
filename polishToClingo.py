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

'''def equivalence(node):
    # replace a <-> b by (a /\ b) \/ (¬a /\ ¬b) 
    if node.item == "=": # damos por hecho que left y right not null'''



def implication(node):
    # replace a -> b by ¬a \/ b 
    if node.item == ">":
        node.item = "|"
        aux = Node("-") # nodo auxiliar para añadir la negación
        aux.left = node.left
        node.left = aux
    if node.left is not None:
        implication(node.left) # no importa el orden
    if node.right is not None:
        implication(node.right)
    return node

def deMorgan(node):
    if node.item == "-" and (node.left.item == "|" or node.left.item == "&"): # si no es - ya no busca el hijo izquierdo 
        node = node.left
        if node.item == "|":
            node.item = "&"
        else:
            node.item = "|"

        if node.left.item == "-":
            node.left = node.left.left # quitamos la negación ¬(¬a) = a
        else: # añadir ¬
            aux = Node("-")
            aux.left = node.left
            node.left = aux

        if node.right.item == "-":
            node.right = node.right.left # quitamos la negación ¬(¬a) = a
        else:
            aux = Node("-")
            aux.left = node.right
            node.right = aux

    if node.left is not None:
        node.left = deMorgan(node.left) # no importa el orden
    if node.right is not None:
        node.right = deMorgan(node.right)

    return node


pair = {"&","|",">","=","%"}
inpair = {"-","0","1"}

def to_tree(words):

    if len(words) == 1:
        return Node(words[0])

    word = words[0]
    rest = words[1:]

    if word in pair:
        node = Node(word)

        n = 1 # Para controlar que pertenece a la rama izquierda
        aux = 0 # Offset de donde termina la rama izquierda

        for var in rest:
            aux = aux + 1
            if var in pair:
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
    else: # asumir que solo es un -
        node = Node(word)
        node.left = to_tree(rest)
        return node

def process_polish(word):
    if not word.endswith("."):
        print("Entrada invalida, no termina con .")
    else:

        word_splited = word.split()
        return to_tree(word_splited[:len(word_splited)-1]) # Quitar el .

def main():

    word1 = "> | rain - weekend - happy ."
    word2 = "= weekend - workday ."

    tree1 = process_polish(word1)
    tree2 = process_polish(word2) 

    print(preorden(tree1))
    print(preorden(tree2))

    '''print("\nSome errors:\n")
    print(process_polish(""))
    print(process_polish("= weekend - workday "))'''

    print("\nImplications:\n")

    tree1 = implication(tree1)
    tree2 = implication(tree2)

    print(preorden(tree1))
    print(preorden(tree2))

    print("\nDeMorgan:\n")

    tree1 = deMorgan(tree1)

    print(preorden(tree1))

main()