class MinHeap:
    def __init__(self):
        # A lista armazena tuplas(prioridade, item)
        self.heap = []

    def _pai(self, i):
        return (i - 1) // 2

    def _filho_esquerdo(self, i):
        return 2 * i + 1

    def _filho_direito(self, i):
        return 2 * i + 2

    def _subir(self, i):
        pai = self._pai(i)
        if i > 0 and self.heap[i][0] < self.heap[pai][0]:
            # Troca o item atual com o pai se a prioridade for menor
            self.heap[i], self.heap[pai] = self.heap[pai], self.heap[i]
            self._subir(pai)

    def _descer(self, i):
        menor = i
        esq = self._filho_esquerdo(i)
        dir = self._filho_direito(i)
        tamanho = len(self.heap)

        if esq < tamanho and self.heap[esq][0] < self.heap[menor][0]:
            menor = esq
        if dir < tamanho and self.heap[dir][0] < self.heap[menor][0]:
            menor = dir

        if menor != i:
            self.heap[i], self.heap[menor] = self.heap[menor], self.heap[i]
            self._descer(menor)

    def push(self, prioridade, item):
        """Insere um novo item no heap."""
        self.heap.append((prioridade, item))
        self._subir(len(self.heap) - 1)

    def pop(self):
        if self.is_empty():
            return None
        if len(self.heap) == 1:
            return self.heap.pop() 
        
        menor_par = self.heap[0]   
        self.heap[0] = self.heap.pop()
        self._descer(0)
        
        return menor_par

    def is_empty(self):
        return len(self.heap) == 0