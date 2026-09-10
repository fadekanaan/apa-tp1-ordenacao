"""
Algoritmo Autoral 2 (Recursivo): Variance-Adaptive K-Way Merge Sort (VAKM Sort).

Raciocínio Projetual:
1. Sensor de Corridas Ordenadas (Natural Runs Sensor):
   Verifica em O(N) se o segmento já está monotonicamente ordenado e, em caso
   afirmativo, encerra a recursão ali. Garante melhor caso Theta(N) para entradas
   já ordenadas: exatamente N-1 comparações e zero movimentações.
   Este sensor subsome o teste de uniformidade: um segmento com todos os elementos
   iguais é monotonicamente não decrescente e já é interceptado aqui.

2. Fator de Ramificação Adaptativo (k in [2, K_MAX]):
   Mede a dispersão estatística (variância normalizada) do segmento. Dados com
   alta dispersão são divididos em mais fatias (k até 8), reduzindo a profundidade
   da árvore de recursão de log_2 N para log_k N. Essa redução diminui o número de
   passadas de alocação/escrita de memória (justificativa histórica do Merge Sort
   k-ário em ordenação externa, Knuth Vol. 3).

3. Fusão K-Ária por Min-Heap (Torneio / Loser Tree):
   A combinação das k fatias ordenadas utiliza um Min-Heap instrumentado.
   O custo de seleção da menor cabeça de lista cai de O(k-1) para O(log_2 k) por
   elemento. Acumulado na árvore de profundidade log_k N, o custo total de comparações
   torna-se log_k N * N * log_2 k = N log_2 N para qualquer k. Ou seja, o heap remove
   a dependência em k do TERMO DE FUSAO -- e e isso, e somente isso, que ele garante.
   O total medido permanece acima de N log_2 N (fator ~2,3 em N=10^4 aleatorio) porque
   o desempate estavel exige duas comparacoes de chave por invocacao de __lt__ e porque
   cada no paga duas varreduras lineares adicionais (sensor de corridas e extremos).
   Ver Secao 6.3 do relatorio para a decomposicao medida.

Propriedades Teóricas:
- Melhor Caso: Theta(N) - acionado pelo sensor de corridas ordenadas.
- Pior Caso: Theta(N log N) - como k varia por no, o Teorema Mestre nao se aplica na
  forma direta; a cota vem de ensanduichamento entre k=2 e k=K_MAX (relatorio, Secao 3.6).
  Particionamento posicional balanceado: sem risco de degradacao quadratica.
- Caso Médio: Theta(N log N).
- Espaço Auxiliar: O(N) - alocação de sublistas por nível de recursão e fusão.
- Estabilidade: Estável - desempate no Min-Heap favorece estritamente a sublista de
  menor índice (mais à esquerda na ordem original).
"""

import heapq
from typing import Any, List, Tuple


def vakm_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """
    Variance-Adaptive K-Way Merge Sort (VAKM Sort).

    Parâmetros:
        arr (List[Any]): Lista de entrada a ser ordenada.

    Retorno:
        Tuple[List[Any], int, int]:
            - Lista ordenada
            - Total de comparações realizadas
            - Total de movimentações/trocas realizadas
    """
    comps = [0]
    moves = [0]

    INSERTION_THRESHOLD = 16
    K_MAX = 8

    class _HeapEntry:
        __slots__ = ("val", "part_idx", "elem_idx")

        def __init__(self, val: Any, part_idx: int, elem_idx: int):
            self.val = val
            self.part_idx = part_idx
            self.elem_idx = elem_idx

        def __lt__(self, other: "_HeapEntry") -> bool:
            comps[0] += 1
            if self.val < other.val:
                return True
            comps[0] += 1
            if not (other.val < self.val):
                # Estabilidade: quando as chaves são equivalentes (nem self < other nem other < self),
                # desempata a favor da sublista de menor índice (mais à esquerda na ordem original).
                return self.part_idx < other.part_idx
            return False

    def insertion_sort(lst: List[Any]) -> List[Any]:
        for i in range(1, len(lst)):
            key = lst[i]
            moves[0] += 1
            j = i - 1
            while j >= 0:
                comps[0] += 1
                if key < lst[j]:
                    lst[j + 1] = lst[j]
                    moves[0] += 1
                    j -= 1
                else:
                    break
            lst[j + 1] = key
            moves[0] += 1
        return lst

    def check_monotonic(lst: List[Any]) -> bool:
        """Sensor de corridas ordenadas: verifica se o segmento já está ordenado em O(N)."""
        for i in range(len(lst) - 1):
            comps[0] += 1
            if lst[i + 1] < lst[i]:
                return False
        return True

    def find_extremes(lst: List[Any]) -> Tuple[Any, Any]:
        """Acha o menor e o maior elemento do segmento em uma única passada."""
        lo = lst[0]
        hi = lst[0]
        for i in range(1, len(lst)):
            comps[0] += 1
            if lst[i] < lo:
                lo = lst[i]
            else:
                comps[0] += 1
                if hi < lst[i]:
                    hi = lst[i]
        return lo, hi

    def choose_k(lst: List[Any], lo: Any, hi: Any) -> int:
        """
        Calcula o fator de ramificação k adaptativo com base na dispersão de valores.
        Dados com maior variância são divididos em mais fatias (k até K_MAX), reduzindo
        a profundidade da árvore de recursão log_k N.
        """
        try:
            n = len(lst)
            rng = hi - lo
            mean = sum(lst) / n
            variance = sum((x - mean) ** 2 for x in lst) / n
            disp = variance / (rng ** 2) if rng != 0 else 0.0
            disp = min(disp, 0.25)  # Dispersão máxima teórica normalizada para [0, 1]
            norm = disp / 0.25
            k = 2 + round(norm * (K_MAX - 2))
        except TypeError:
            # Fallback para elementos não numéricos sem suporte a operações aritméticas
            k = 4
        return max(2, min(K_MAX, k))

    def k_way_merge(parts: List[List[Any]]) -> List[Any]:
        """
        Fusão K-Ária Estável utilizando Min-Heap (Torneio).
        Complexidade de comparações: O(N log_2 k) por nível de fusão.
        """
        valid_parts = [p for p in parts if p]
        if not valid_parts:
            return []
        if len(valid_parts) == 1:
            moves[0] += len(valid_parts[0])
            return list(valid_parts[0])

        heap = []
        for i, p in enumerate(valid_parts):
            heap.append(_HeapEntry(p[0], i, 0))
        heapq.heapify(heap)

        result = []
        while heap:
            entry = heap[0]
            result.append(entry.val)
            moves[0] += 1

            p_idx = entry.part_idx
            e_idx = entry.elem_idx + 1
            if e_idx < len(valid_parts[p_idx]):
                # heapreplace realiza UMA peneiracao (pop + push fariam duas),
                # reduzindo pela metade as comparacoes de reorganizacao do heap.
                heapq.heapreplace(heap, _HeapEntry(valid_parts[p_idx][e_idx], p_idx, e_idx))
            else:
                heapq.heappop(heap)

        return result

    def sort_recursive(lst: List[Any]) -> List[Any]:
        n = len(lst)
        if n <= 1:
            return lst

        # 1. Caso base por threshold
        if n <= INSERTION_THRESHOLD:
            return insertion_sort(lst)

        # 2. Sensor de Corridas Ordenadas (Melhor Caso Theta(N))
        if check_monotonic(lst):
            return lst

        # 3. Extremos do segmento, usados apenas para calibrar o fator k.
        #    Nao ha teste de uniformidade aqui: um segmento com todos os elementos
        #    iguais e monotonico e ja foi encerrado no passo 2.
        lo, hi = find_extremes(lst)

        # 4. Divisão adaptativa em k fatias
        k = choose_k(lst, lo, hi)
        k = min(k, n)

        block_size = -(-n // k)  # ceil(n / k)
        parts = [lst[i:i + block_size] for i in range(0, n, block_size)]
        sorted_parts = [sort_recursive(part) for part in parts]

        # 5. Fusão k-ária por Min-Heap
        return k_way_merge(sorted_parts)

    result = sort_recursive(list(arr))
    return result, comps[0], moves[0]
