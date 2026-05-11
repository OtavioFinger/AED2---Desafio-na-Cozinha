class TrieNode:

    def __init__(self):

        self.children = {}
        self.final = False


class Trie:

    def __init__(self):

        self.root = TrieNode()

    def inserir(self, palavra):

        curr = self.root

        for letter in palavra:

            if letter not in curr.children:
                curr.children[letter] = TrieNode()

            curr = curr.children[letter]

        curr.final = True

    def buscar(self, prefixo):

        curr = self.root

        for letter in prefixo:

            if letter not in curr.children:
                return []

            curr = curr.children[letter]

        palavras = []
        self.autocomplete(curr, prefixo, palavras)
        return palavras

    
    def autocomplete(self, nodo, prefixo, palavras):
        if nodo.final:
            palavras.append(prefixo)
        
        for letter in nodo.children:
            self.autocomplete(nodo.children[letter], prefixo + letter, palavras)
        
        