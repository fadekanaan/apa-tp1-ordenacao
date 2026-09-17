# Trabalho Prático 1 (TP1) — Métodos de Ordenação Autorais
**Disciplina:** Análise e Projeto de Algoritmos (APA)  
**Linguagem Principal:** Python 3  

---

## 🎯 Proposta e Modelo de Avaliação

Este trabalho prático tem como objetivo conceber, formalizar matematicamente, implementar e validar experimentalmente algoritmos de ordenação autorais, comparando-os rigorosamente contra métodos clássicos da literatura (*Bubble Sort*, *Selection Sort*, *Insertion Sort*, *Merge Sort* e *Quick Sort*).

* **Formato de Entrega:** **Opção A — Relatório Técnico Completo** (análise analítica aprofundada, deduções assintóticas no modelo RAM, invariantes de laço, gráficos e testes de estresse).
* **Modelo de Avaliação:** **$N/2$ Algoritmos Autorais**, totalizando **2 algoritmos autorais** a serem desenvolvidos e analisados pelo grupo.

---

## 💡 Escopo dos Algoritmos Autorais

Para garantir amplitude teórica e experimental, os dois métodos abordarão diferentes paradigmas e naturezas algorítmicas:

1. **Algoritmo Autoral 1 — Abordagem Iterativa:**
   * Foco em operação estritamente *in-place* ($O(1)$ de memória auxiliar).
   * Raciocínio baseado em invariantes de laço iterativos, varreduras direcionadas/convergentes e mecanismos adaptativos de parada antecipada sensíveis a dados quase ordenados.

2. **Algoritmo Autoral 2 — Abordagem Recursiva:**
   * Foco no paradigma de **Divisão e Conquista** ou decomposição estrutural.
   * Raciocínio analítico modelado por relações de recorrência (resolução via Teorema Mestre ou Árvore de Recorrência), buscando eficiência assintótica ($O(N \log N)$ em caso médio).

> *Nota: O refinamento do design exato de cada algoritmo, suas metáforas e pseudocódigos formais serão detalhados nas próximas etapas de desenvolvimento.*

---

## 📂 Estrutura do Repositório

```text
apa-tp1-ordenacao/
├── .gitignore                                  # Arquivos e diretórios ignorados pelo Git
├── README.md                                   # Este documento explicativo
├── pyproject.toml                              # Configuração e dependências do projeto Python
├── uv.lock                                     # Versões fixadas das dependências
├── codigo/                                     # Pacote de códigos, testes e benchmarks
│   ├── Makefile                                # Automação de testes e benchmarks
│   ├── README.md                               # Guia detalhado de execução do código
│   └── python/                                 # Implementações em Python 3
│       ├── authorial.py                        # Algoritmo autoral de referência (DPES)
│       ├── benchmark.py                        # Framework de medição e geração de gráficos
│       ├── classical.py                        # Algoritmos clássicos de ordenação
│       ├── dsb_sort.py                         # Algoritmo autoral iterativo DSB Sort
│       ├── metrics.py                          # Instrumentação de métricas
│       ├── student_template.py                 # Template base para algoritmos autorais
│       ├── test_authorial.py                   # Testes específicos do DSB e VAKM
│       ├── test_suite.py                       # Suíte de testes obrigatória
│       └── vakm_sort.py                        # Algoritmo autoral recursivo VAKM Sort
├── docs/                                       # Diretrizes e fundamentação
│   ├── enunciado_tp1.md                        # Enunciado completo do trabalho
│   └── sintese_teorica_ordenacao_apa.md        # Síntese teórica sobre ordenação
└── relatorio/                                  # Documentação analítica
    └── relatorio_tp1.md                        # Relatório técnico completo unificado (DSB Sort e VAKM Sort)
```

---

## 🚀 Como Executar

### 1. Testes de Corretude (Suíte Obrigatória)

Valida o comportamento dos algoritmos contra cenários de borda (vazio, elemento único, ordenado, estritamente reverso, duplicados e aleatórios):

```bash
# Executar suíte de testes via UV
uv run python codigo/python/test_suite.py

# Ou via Makefile
make -C codigo test
```

### 2. Benchmarks e Comparação de Desempenho

Executa a bateria de medições estatísticas com tamanhos crescentes de entrada e gera o gráfico comparativo:

```bash
# Executar benchmark estatístico
uv run python codigo/python/benchmark.py --trials 3 --plot benchmark_results.png

# Ou via Makefile
make -C codigo benchmark
```

---
