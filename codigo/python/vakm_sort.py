"""
Algoritmo Autoral 2 (Recursivo): Variance-Adaptive K-Way Merge Sort (VAKM Sort).

Raciocínio Projetual:
É um Merge Sort que, em vez de sempre dividir ao meio (k=2), decide em
quantas partes dividir (k entre 2 e 8) olhando a dispersão dos valores do
segmento: dados espalhados são cortados em mais pedaços; dados parecidos
entre si são cortados em poucos pedaços, quase como o Merge Sort comum.
Se todos os elementos do segmento forem iguais, ele já está ordenado e a
recursão para ali.

A união das partes já ordenadas é feita por um merge de k listas ao mesmo
tempo (não só duas), sempre escolhendo entre as cabeças das listas o menor
valor, com empate resolvido a favor da lista mais à esquerda (garante
estabilidade).

Propriedades Teóricas:
- Melhor Caso: Theta(N log N) - o fator k não depende da ordem dos dados,
  apenas da dispersão de valores; não há adaptação a pré-ordenação.
- Pior Caso: O(N log N) - como k é sempre limitado a [2, K_MAX] (constante),
  a recorrência T(N) = k*T(N/k) + Theta(N*k) permanece, pelo Teorema Mestre
  (caso 2, com a = b = k), em Theta(N log_k N) = Theta(N log N).
- Caso Médio: Theta(N log N).
- Espaço Auxiliar: O(N) - cada nível de recursão aloca novas sublistas
  (fatiamento) e o merge produz uma lista de saída nova, como no Merge Sort.
- Estabilidade: Estável - o desempate no k-way merge favorece sempre a
  sublista de menor índice (mais à esquerda na ordem original) em caso de
  empate de chaves.
"""

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

    def insertion_sort(lst: List[Any]) -> List[Any]:
        for i in range(1, len(lst)):
            key = lst[i]
            moves[0] += 1
            j = i - 1
            while j >= 0:
                comps[0] += 1
                if lst[j] > key:
                    lst[j + 1] = lst[j]
                    moves[0] += 1
                    j -= 1
                else:
                    break
            lst[j + 1] = key
            moves[0] += 1
        return lst

    def find_extremes(lst: List[Any]) -> Tuple[Any, Any]:
        # Acha o menor e o maior do segmento em uma única passada.
        lo = lst[0]
        hi = lst[0]
        for i in range(1, len(lst)):
            comps[0] += 1
            if lst[i] < lo:
                lo = lst[i]
            else:
                comps[0] += 1
                if lst[i] > hi:
                    hi = lst[i]
        return lo, hi

    def choose_k(lst: List[Any], lo: Any, hi: Any) -> int:
        # Calcula o quão espalhados estão os valores e usa isso para
        # escolher k. Essas contas não contam como comparações de ordenação.
        try:
            n = len(lst)
            rng = hi - lo
            mean = sum(lst) / n
            variance = sum((x - mean) ** 2 for x in lst) / n
            disp = variance / (rng ** 2) if rng != 0 else 0.0
            disp = min(disp, 0.25)  # dispersão máxima possível, normaliza para [0, 1]
            norm = disp / 0.25
            k = 2 + round(norm * (K_MAX - 2))
        except TypeError:
            # Elementos sem suporte a aritmética: usa um k fixo.
            k = 4
        return max(2, min(K_MAX, k))

    def k_way_merge(parts: List[List[Any]]) -> List[Any]:
        result = []
        cursors = [0] * len(parts)
        total = sum(len(p) for p in parts)

        for _ in range(total):
            best = -1
            for pi in range(len(parts)):
                if cursors[pi] < len(parts[pi]):
                    if best == -1:
                        best = pi
                    else:
                        comps[0] += 1
                        if parts[pi][cursors[pi]] < parts[best][cursors[best]]:
                            best = pi
            result.append(parts[best][cursors[best]])
            moves[0] += 1
            cursors[best] += 1

        return result

    def sort_recursive(lst: List[Any]) -> List[Any]:
        n = len(lst)
        if n <= 1:
            return lst

        if n <= INSERTION_THRESHOLD:
            return insertion_sort(lst)

        lo, hi = find_extremes(lst)

        # Todos os elementos são iguais: já está ordenado.
        comps[0] += 1
        if lo == hi:
            return lst

        k = choose_k(lst, lo, hi)
        k = min(k, n)

        block_size = -(-n // k)  # ceil(n / k)
        parts = [lst[i:i + block_size] for i in range(0, n, block_size)]
        sorted_parts = [sort_recursive(part) for part in parts]

        return k_way_merge(sorted_parts)

    result = sort_recursive(list(arr))
    return result, comps[0], moves[0]
