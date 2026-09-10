"""Testes específicos dos algoritmos autorais DSB Sort e VAKM Sort."""

import unittest
from unittest.mock import patch

from dsb_sort import dsb_sort
from vakm_sort import vakm_sort


class TestDSBSortSpecific(unittest.TestCase):
    """Valida decisões internas que são exclusivas do DSB Sort."""

    def test_reajusta_max_idx_quando_maximo_comeca_em_left(self):
        """O máximo movido pela troca do mínimo deve continuar rastreado."""
        result, _, moves = dsb_sort([9, 2, 1, 8])

        self.assertEqual([1, 2, 8, 9], result)
        self.assertEqual(4, moves)

    def test_lista_ordenada_para_sem_movimentacoes(self):
        """A parada antecipada não deve movimentar uma janela já ordenada."""
        data = list(range(20))

        result, _, moves = dsb_sort(data)

        self.assertEqual(data, result)
        self.assertEqual(0, moves)

    def test_dois_elementos_invertidos_exigem_uma_unica_troca(self):
        """A menor janela não trivial deve realizar só uma troca (dois moves)."""
        result, _, moves = dsb_sort([2, 1])

        self.assertEqual([1, 2], result)
        self.assertEqual(2, moves)

    def test_elementos_identicos_nao_geram_movimentacoes(self):
        """Elementos iguais devem acionar a parada sem trocas desnecessárias."""
        data = [7] * 20

        result, _, moves = dsb_sort(data)

        self.assertEqual(data, result)
        self.assertEqual(0, moves)


class _StableItem:
    """Item comparável apenas pela chave, com identidade observável no teste."""

    def __init__(self, key, label):
        self.key = key
        self.label = label

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key


class TestVAKMSortSpecific(unittest.TestCase):
    """Valida os caminhos adaptativo, recursivo e estável do VAKM Sort."""

    def test_limite_acima_do_threshold_exercita_merge_desbalanceado(self):
        """N=17 força recursão e uma última parte menor no k-way merge."""
        data = [0, 1000] * 8 + [0]

        result, _, _ = vakm_sort(data)

        self.assertEqual(sorted(data), result)

    def test_elementos_identicos_acima_do_threshold_param_sem_moves(self):
        """Acima do threshold, lo == hi deve encerrar antes de dividir e mesclar."""
        data = [7] * 17

        result, _, moves = vakm_sort(data)

        self.assertEqual(data, result)
        self.assertEqual(0, moves)

    def test_dispersao_adapta_k_entre_tres_e_oito_partes(self):
        """Distribuições concentrada e bimodal devem escolher k distintos."""
        builtin_round = round
        concentrated = [0] * 32 + [1000]
        bimodal = [0, 1000] * 16 + [0]

        with patch("builtins.round", wraps=builtin_round) as round_spy:
            concentrated_result, _, _ = vakm_sort(concentrated)
            concentrated_k = 2 + builtin_round(round_spy.call_args_list[0].args[0])

        with patch("builtins.round", wraps=builtin_round) as round_spy:
            bimodal_result, _, _ = vakm_sort(bimodal)
            bimodal_k = 2 + builtin_round(round_spy.call_args_list[0].args[0])

        self.assertEqual(sorted(concentrated), concentrated_result)
        self.assertEqual(sorted(bimodal), bimodal_result)
        self.assertEqual(3, concentrated_k)
        self.assertEqual(8, bimodal_k)

    def test_estabilidade_com_objetos_comparaveis_por_chave(self):
        """Empates devem preservar a ordem original entre rótulos da mesma chave."""
        data = [
            _StableItem(key=i % 3, label=i)
            for i in range(20)
        ]

        result, _, _ = vakm_sort(data)

        for key in range(3):
            expected_labels = [item.label for item in data if item.key == key]
            result_labels = [item.label for item in result if item.key == key]
            self.assertEqual(expected_labels, result_labels)


if __name__ == "__main__":
    unittest.main(verbosity=2)
