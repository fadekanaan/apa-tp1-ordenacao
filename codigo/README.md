# Pacote de Códigos e Benchmarks — TP1 (APA)

Este diretório contém a implementação dos algoritmos de ordenação clássicos, o algoritmo autoral de referência (**DPES - Dual-Pivot Extremes Sieve Sort**), a suíte de testes de validação obrigatória e o framework de medição de desempenho e gráficos em **Python 3**.

---

## 📂 Estrutura de Arquivos

```text
codigo/
├── Makefile                          # Automação de testes e benchmarks
├── README.md                         # Este guia de execução e desenvolvimento
│
└── python/                           # Implementação em Python 3
    ├── classical.py                  # Algoritmos clássicos (Bubble, Selection, Insertion, Merge, Quick)
    ├── authorial.py                  # Algoritmo autoral de referência (DPES)
    ├── metrics.py                    # Instrumentação (contagem de comparações, trocas e tempos)
    ├── test_suite.py                 # Suíte com todos os cenários de teste obrigatórios (unittest)
    ├── benchmark.py                  # Framework de benchmark com geração de gráficos matplotlib
    └── student_template.py           # Template inicial para o aluno desenvolver seu algoritmo
```

---

## 🚀 Como Executar

### 1. Suíte de Testes Obrigatória

* **Executar testes em Python:**
  ```bash
  make test
  # ou: uv run python python/test_suite.py
  ```

---

### 2. Benchmarks e Comparação de Desempenho

* **Executar benchmarks em Python (Gera tabelas Markdown e o gráfico `benchmark_results.png`):**
  ```bash
  make benchmark
  # ou: uv run python python/benchmark.py --trials 3 --plot benchmark_results.png
  ```

---

## 🧑‍💻 Guia para o Aluno (Como usar o template)

1. Abra o arquivo [`python/student_template.py`](file:///home/thoma/workspace/apa-tp1-ordenacao/codigo/python/student_template.py).
2. Escreva a lógica do seu algoritmo na função `my_authorial_sort(arr)`.
3. Certifique-se de incrementar os contadores de comparações (`comps`) e movimentações (`moves`).
4. Execute o arquivo diretamente para validar seu algoritmo contra a suíte de testes:
   ```bash
   uv run python python/student_template.py
   ```
5. Para comparar seu algoritmo diretamente contra a literatura no benchmark gráfico:
   * Importe seu método no `python/benchmark.py` e adicione ao dicionário `algorithms`.
   * Execute `uv run python python/benchmark.py` para gerar as curvas de tempo e comparações para o seu relatório ou apresentação!
