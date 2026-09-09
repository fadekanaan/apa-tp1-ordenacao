"""
TEMPLATE PARA O ALUNO — TRABALHO PRÁTICO 1 (TP1)
Disciplina: Análise e Projetos de Algoritmos (APA)

Instruções:
1. Implemente seu método de ordenação autoral na função `my_authorial_sort`.
2. O retorno deve ser obrigatoriamente a tupla: (lista_ordenada, total_comparacoes, total_movimentacoes).
3. Execute este arquivo diretamente para rodar a suíte de testes de corretude e o benchmark rápido.
"""

from typing import Any, List, Tuple
import unittest


def my_authorial_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """
    Dual Selection Bubble Sort (DSB Sort).
    Combina a seleção simultânea de extremos (mínimo e máximo) com
    detecção de inversões locais e parada antecipada do Bubble Sort.

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
        min = left
        max = right
        is_sorted = True

        for j in range(left, right + 1):

            # Verifica a janela para detectar se a lista já não está ordenada
            if j < right:
                if a[j] > a[j + 1]:
                    is_sorted = False
                    comps += 1

            # Encontrar o valor máximo e mínimo da janela
            comps += 1
            if a[j] < a[min]:
                min = j
            elif a[j] > a[max]:
                max = j

        # Se já estava ordenada, encerra
        if is_sorted:
            break

         # Se o mínimo e o máximo forem iguais, significa que todos os elementos da janela são iguais
        if a[min] == a[max]:
            break

        # Trocar o mínimo com o elemento da esquerda
        if min != left:
            a[left], a[min] = a[min], a[left]
            moves += 2

            # Ajustar o índice do máximo se ele foi movido, caso o máximo estivesse na posição da esquerda, ele agora está na posição do mínimo
            if max == left:
                max = min

        # Trocar o máximo com o elemento da direita
        if max != right:
            a[right], a[max] = a[max], a[right]
            moves += 2

        left += 1
        right -= 1
        
        
    # =========================================================================

    return a, comps, moves


# =============================================================================
# SUÍTE DE TESTES AUTOMÁTICA DE VALIDAÇÃO
# =============================================================================
class TestStudentAuthorialSort(unittest.TestCase):
    def assert_sorted(self, original: List, result: List):
        self.assertEqual(len(result), len(original), "Tamanho divergente!")
        self.assertEqual(sorted(original), result, "A lista não foi ordenada corretamente!")

    def test_empty(self):
        res, _, _ = my_authorial_sort([])
        self.assert_sorted([], res)

    def test_single(self):
        res, _, _ = my_authorial_sort([99])
        self.assert_sorted([99], res)

    def test_sorted(self):
        data = list(range(100))
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_reverse(self):
        data = list(range(100, 0, -1))
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_identical(self):
        data = [5] * 50
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_random(self):
        import random
        random.seed(42)
        data = [random.randint(-1000, 1000) for _ in range(200)]
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)


if __name__ == "__main__":
    print("🧪 Executando testes unitários no seu algoritmo autoral...")
    unittest.main(verbosity=2)
