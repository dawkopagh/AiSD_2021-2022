from copy import deepcopy


class Root:
    def __init__(self):
        self.head = None

    def search(self, key, node = None):
        if node == None:
            node = self.head
        if node.key == key:
            return node.value
        elif node.key > key and node.branchLEFT is not None:
            res = self.search(key, node.branchLEFT)
        elif node.key < key and node.branchRIGHT is not None:
            res = self.search(key, node.branchRIGHT)

        elif node.branchRIGHT is None and node.branchLEFT is None:
            return None
        return res

    def insert(self, key, value):
        previous_node = None
        current_node = self.head
        while current_node is not None:
            if current_node.key == key:
                current_node.value = value
                return None
            elif current_node.key > key:
                previous_node = current_node
                current_node = current_node.branchLEFT
            elif current_node.key < key:
                previous_node = current_node
                current_node = current_node.branchRIGHT
        if previous_node is None:
            self.head = Branch(key,value)
        elif key > previous_node.key:
            previous_node.branchRIGHT = Branch(key,value)
        elif key < previous_node.key:
            previous_node.branchLEFT = Branch(key,value)

    def delete(self, key):
        previous_node = None
        current_node = self.head
        while current_node is not None:
            if current_node.key == key:
                break
            elif current_node.key > key and current_node.branchLEFT is not None:
                previous_node = current_node
                current_node = current_node.branchLEFT
            elif current_node.key < key and current_node.branchRIGHT is not None:
                previous_node = current_node
                current_node = current_node.branchRIGHT

        if current_node.key == key:
            if current_node.branchRIGHT is None and current_node.branchLEFT is None:
                if key > previous_node.key:
                    previous_node.branchRIGHT = None
                elif key < previous_node.key:
                    previous_node.branchLEFT = None
            elif current_node.branchLEFT is None and current_node.branchRight is not None:
                if previous_node.branchLEFT == current_node:
                    previous_node.branchLEFT = current_node.branchRIGHT
                elif previous_node.branchRIGHT == current_node:
                    previous_node.branchRIGHT = current_node.branchRIGHT
            elif current_node.branchRIGHT is None and current_node.branchLEFT is not None:
                if previous_node.branchLEFT == current_node:
                    previous_node.branchLEFT = current_node.branchLEFT
                elif previous_node.branchRIGHT == current_node:
                    previous_node.branchRIGHT = current_node.branchLEFT
            elif current_node.branchLEFT is not None and current_node.branchRIGHT is not None: #zastępujemy minimalnym elementem z prawego poddrzewa
                minNode = current_node.branchRIGHT
                delete_node = current_node
                while minNode.branchLEFT is not None:
                    delete_node = minNode
                    minNode = minNode.branchLEFT
                current_node.key = minNode.key
                current_node.value = minNode.value
                if current_node.branchRIGHT == minNode:
                    if minNode.branchRIGHT is None:
                        current_node.branchRIGHT = None
                    else:
                        current_node.branchRIGHT = minNode.branchRIGHT
                else:
                    delete_node.branchLEFT = None

    def height(self, node, levels=0):
        current_node = node
        if current_node.branchRIGHT is None and current_node.branchLEFT is not None:
            levels = self.height(current_node.branchLEFT, levels+1)
        elif current_node.branchLEFT is None and current_node.branchRIGHT is not None:
            levels = self.height(current_node.branchRIGHT, levels+1)
        elif current_node.branchLEFT is not None and current_node.branchRIGHT is not None:
            branchLEFT_level = self.height(current_node.branchLEFT, levels+1)
            branchRIGHT_level = self.height(current_node.branchRIGHT, levels+1)
            if branchRIGHT_level > branchLEFT_level:
                levels = branchRIGHT_level
            else:
                levels = branchLEFT_level
        return levels

    def print_tree(self):
        print("==============")
        self._print_tree(self.head, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node != None:
            self._print_tree(node.branchRIGHT, lvl + 5)

            print()
            print(lvl * " ", node.key, node.value)

            self._print_tree(node.branchLEFT, lvl + 5)

    def print_tree_list(self, node, result=None):
        if result is None:
            result = []
        if node.branchLEFT is not None:
            self.print_tree_list(node.branchLEFT, result)
        if node.branchRIGHT is not None:
            result.append(str(node.key) + ":" + str(node.value))
            self.print_tree_list(node.branchRIGHT, result)
        if node.key is not None and node.value is not None and (str(node.key) + ":" + str(node.value)) not in result:
            result.append(str(node.key) + ":" + str(node.value))
        return result


class Branch:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.branchLEFT = None
        self.branchRIGHT = None
        self.height = 0

class AVL(Root):
    def nodeHeight(self, node):
        if not node:
            return 0
        else:
            return self.height(node)

    def insert(self, key, value, node = None):

        if not node:
            self.head = Branch(key, value)
        elif key < node.key:
            node.leftBRANCH = self.insert(key, value, node.leftBRANCH)
        elif key > node.key:
            node.rightBRANCH = self.insert(key, value, node.rightBRANCH)

        node.height = 1 + max(self.nodeHeight(node.branchLEFT), self.nodeHeight(node.branchRIGHT))

        balanceCoeff = self.nodeHeight(node.branchLEFT) - self.nodeHeight(node.branchRIGHT)

        if balanceCoeff > 1:
            if key < node.branchLEFT.key: #rotuj w prawo
                self.rightRotation(node)
            else: #rotuj w lewo, rotuj w prawo
                node.branchLEFT = self.leftRotation(node.branchLEFT)
                self.rightRotation(node)

        if balanceCoeff < -1:
            if key > node.branchRIGHT.key: #rotuj w lewo
                self.leftRotation(node)
            else: #rotuj w prawo,lewo
                node.branchRIGHT = self.rightRotation(node.branchRIGHT)
                self.leftRotation(node)

    def rightRotation(self, node):
        buff = node.branchLEFT
        buff2 = buff.branchRIGHT
        buff.branchRIGHT = node
        node.branchLEFT = buff2
        node.height = 1 + max(self.nodeHeight(node.branchLEFT), self.nodeHeight(node.branchRIGHT))
        buff.height = 1 + max(self.nodeHeight(buff.branchLEFT), self.nodeHeight(buff.branchRIGHT))
        return buff


    def leftRotation(self, node):
        buff = node.branchRIGHT
        buff2 = buff.branchLEFT
        buff.branchLEFT = node
        node.branchRIGHT = buff2
        node.height = 1 + max(self.nodeHeight(node.branchLEFT), self.nodeHeight(node.branchRIGHT))
        buff.height = 1 + max(self.nodeHeight(buff.branchLEFT), self.nodeHeight(buff.branchRIGHT))
        return buff

tree = AVL()
dict = {50:'A', 15:'B', 62:'C', 5:'D', 2:'E', 1:'F', 11:'G', 100:'H', 7:'I', 6:'J', 55:'K', 52:'L', 51:'M', 57:'N', 8:'O', 9:'P', 10:'R', 99:'S', 12:'T'}

def main():
    for keys,vals in dict.items():
        tree.insert(keys, vals)
    tree.print_tree()
    # print(tree.print_tree_list(tree.head))
    # print(tree.search(24))
    # tree.insert(20, "AA")
    # tree.insert(6, "M")
    # tree.delete(62)
    # tree.insert(59, "N")
    # tree.insert(100, "P")
    # tree.delete(8)
    # tree.delete(15)
    # tree.insert(55, "R")
    # tree.delete(50)
    # tree.delete(5)
    # tree.delete(24)
    # print(tree.height(tree.head))
    # print(tree.print_tree_list(tree.head))
    # tree.print_tree()

main()