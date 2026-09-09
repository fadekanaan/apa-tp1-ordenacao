"""
Algoritmo Autoral 1 (Iterativo): Dual Selection Bubble Sort (DSB Sort).

Raciocínio Projetual:
Combina a Seleção Dupla de Extremos (Dual Selection) com a detecção de
inversões locais e mecanismo de parada antecipada do Bubble Sort.

Propriedades Teóricas:
- Melhor Caso: Omega(N) - Detecta vetor ordenado ou quase ordenado na primeira passada.
- Pior Caso: O(N^2) - Vetor estritamente decrescente ou aleatório.
- Caso Médio: Theta(N^2) - Redução de 50% no número de passadas em relação ao Selection Sort tradicional.
- Espaço Auxiliar: O(1) - Operação estritamente in-place.
- Estabilidade: Não estável (trocas distantes de extremos com extremidades podem inverter chaves idênticas).
"""

from typing import Any, List, Tuple


def dsb_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """
    Dual Selection Bubble Sort (DSB Sort).

    Parâmetros:
        arr (List[Any]): Lista de entrada a ser ordenada.

    Retorno:
        Tuple[List[Any], int, int]:
            - Lista ordenada
            - Total de comparações realizadas
            - Total de movimentações/trocas realizadas
    """
    a = list(arr)
    n = len(a)
    comps = 0
    moves = 0

    # Algoritmo autoral de ordenação, combinação de bubble sort com selection sort, 
    # basicamente é feita uma pinça, pegando o menor e o maior elemento da lista e 
    # colocando eles nas extremidades, depois repetindo o processo com a sublista restante.
    # Ele verifica se a janela já está ordenada ou possui elementos iguais,
    # em qualquer um dos casos, ele encerra a busca.
    left = 0
    right = n - 1

    while left < right:
        min_idx = left
        max_idx = left
        is_sorted = True

        for j in range(left, right + 1):

            # Verifica a janela para detectar se a lista já não está ordenada
            if j < right:
                comps += 1
                if a[j] > a[j + 1]:
                    is_sorted = False

            # Encontrar o valor máximo e mínimo da janela
            comps += 1
            if a[j] < a[min_idx]:
                min_idx = j
            else: 
                comps += 1
                if a[j] > a[max_idx]:
                    max_idx = j

        # Se já estava ordenada, encerra
        if is_sorted:
            break

        # Se o mínimo e o máximo forem iguais, significa que todos os elementos da janela são iguais
        comps += 1
        if a[min_idx] == a[max_idx]:
            break

        # Trocar o mínimo com o elemento da esquerda
        if min_idx != left:
            a[left], a[min_idx] = a[min_idx], a[left]
            moves += 2

            # Ajustar o índice do máximo se ele foi movido, caso o máximo estivesse na posição da esquerda, ele agora está na posição do mínimo
            if max_idx == left:
                max_idx = min_idx

        # Trocar o máximo com o elemento da direita
        if max_idx != right:
            a[right], a[max_idx] = a[max_idx], a[right]
            moves += 2

        left += 1
        right -= 1

    return a, comps, moves
