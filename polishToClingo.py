#!/usr/bin/python3

class Node:

    def __init__(self, item):
        self.item = item
        self.left = None
        self.right = None

# El recorrido en preorden devuelve la expresión en notación polaca
def PreOrder(node):
    nodeList = []
    if node is not None:
        nodeList = nodeList + PreOrder(node.left)
        nodeList.insert(0, node.item)
        nodeList = nodeList + PreOrder(node.right)
    return nodeList

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
        tree = to_tree(word_splited[:len(word_splited)-1]) # Quitar el .
        print(PreOrder(tree))


def main():

    word1 = "> | rain - weekend - happy ."
    word2 = "= weekend - workday ."

    process_polish(word1)
    process_polish(word2)
    print("\nSome errors:\n")
    process_polish("")
    process_polish("= weekend - workday ")

main()