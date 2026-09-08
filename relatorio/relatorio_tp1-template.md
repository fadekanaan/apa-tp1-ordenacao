# Relatório Técnico — Trabalho Prático 1 (TP1)
## Métodos de Ordenação Autorais: Modelagem Assintótica, Implementação e Validação Empírica

**Disciplina:** Análise e Projeto de Algoritmos (APA)  
**Instituição:** UNIPAMPA / RS  
**Autores:**  
- [Fade Kanaan]  
- [Gabriel Fernandes dos Anjos]  
- [Gabriel Ortiz]  
- [Leonardo Dorneles] 
- [Rodrigo Thoma] 

---

## 1. Resumo Executivo e Formulação do Problema

### 1.1. O Problema da Ordenação
Formalização matemática da entrada e saída sob o modelo computacional RAM (*Random Access Machine*).

### 1.2. Escopo do Trabalho
Apresentação do objetivo de projetar, implementar e validar dois algoritmos autorais:
- **Método Autoral 1:** Abordagem Iterativa in-place com invariantes locais.
- **Método Autoral 2:** Abordagem Recursiva baseada em Divisão e Conquista.

---

## 2. Algoritmo Autoral 1 (Iterativo)

### 2.1. Concepção e Raciocínio Projetual
- Intuição central e metáfora visual.
- Justificativa do design e vantagens teóricas esperadas.

### 2.2. Invariantes de Laço e Prova de Corretude
- **Inicialização:**
- **Manutenção:**
- **Término:**

### 2.3. Especificação Formal (Pseudocódigo)
Pseudocódigo detalhado estilo Cormen.

### 2.4. Exemplo Numérico Passo a Passo (Rastreio)
Tabela de rastreio de variáveis para um vetor didático de exemplo.

### 2.5. Análise de Complexidade Teórica (Modelo RAM)
- **Melhor Caso ($\Omega$):**
- **Pior Caso ($O$):**
- **Caso Médio ($\Theta$):**
- **Espaço Auxiliar:**
- **Propriedades Estruturais:** Estabilidade e In-place.

---

## 3. Algoritmo Autoral 2 (Recursivo)

### 3.1. Concepção e Raciocínio Projetual
- Intuição central e divisão do espaço de busca.
- Justificativa do mecanismo de particionamento/fusão.

### 3.2. Prova de Corretude
- Invariantes estruturais e indução matemática.

### 3.3. Especificação Formal (Pseudocódigo)
Pseudocódigo formal com casos base e chamadas recursivas.

### 3.4. Exemplo Numérico Passo a Passo (Rastreio)
Árvore de recursão e transformações do vetor.

### 3.5. Análise de Complexidade Teórica (Relações de Recorrência)
- Formulação da relação $T(N)$.
- Dedução analítica (Teorema Mestre ou Árvore de Recorrência).
- Análise de espaço auxiliar (memória extra e pilha de chamadas).
- Propriedades estruturais: Estabilidade e In-place.

---

## 4. Matriz Comparativa Teórica contra a Literatura

Comparação detalhada dos dois algoritmos autorais contra os 5 métodos clássicos:
- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort
- Quick Sort

| Algoritmo | Paradigma | Melhor Caso | Caso Médio | Pior Caso | Memória Auxiliar | Estável? | In-Place? |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | Iterativo / Troca | $\Omega(N)$ | $\Theta(N^2)$ | $O(N^2)$ | $O(1)$ | Sim | Sim |
| Selection Sort | Iterativo / Seleção | $\Omega(N^2)$ | $\Theta(N^2)$ | $O(N^2)$ | $O(1)$ | Não | Sim |
| Insertion Sort | Iterativo / Inserção | $\Omega(N)$ | $\Theta(N^2)$ | $O(N^2)$ | $O(1)$ | Sim | Sim |
| Merge Sort | Divisão e Conquista | $\Omega(N \log N)$ | $\Theta(N \log N)$ | $O(N \log N)$ | $O(N)$ | Sim | Não |
| Quick Sort | Divisão e Conquista | $\Omega(N \log N)$ | $\Theta(N \log N)$ | $O(N^2)$ | $O(\log N)$ | Não | Sim |
| **Autoral 1 (Iterativo)** | *Iterativo* | *TBD* | *TBD* | *TBD* | *TBD* | *TBD* | *TBD* |
| **Autoral 2 (Recursivo)** | *Divisão e Conquista* | *TBD* | *TBD* | *TBD* | *TBD* | *TBD* | *TBD* |

---

## 5. Metodologia Experimental e Suíte de Testes

### 5.1. Cenários de Teste Obrigatórios
- Vetores aleatórios com distribuição uniforme ($N = 10, 50, 100, 250, 500, 1000, \dots$).
- Vetores perfeitamente ordenados (melhor caso / sensibilidade).
- Vetores em ordem estritamente reversa (pior caso / estresse).
- Vetores com chaves redundantes e repetidas (alta taxa de colisão).
- Casos limites: vetor vazio ($N=0$) e vetor unitário ($N=1$).

### 5.2. Métricas Coletadas
- Tempo de execução médio (com repetições estatísticas via `time.perf_counter`).
- Contagem exata de comparações entre chaves.
- Contagem exata de movimentações e trocas de elementos.

---

## 6. Resultados Experimentais e Benchmarking

### 6.1. Tabelas de Resultados por Distribuição
*(Inserir dados gerados pelo framework de benchmark)*

### 6.2. Gráficos Comparativos de Tempo e Operações
*(Inserir curvas geradas pelo matplotlib)*

---

## 7. Discussão Crítica e Trade-Offs

- Análise de aderência entre curvas teóricas ($O, \Theta$) e empíricas.
- Impacto de overhead de interpretador (Python) vs. complexidade assintótica.
- Limitações intrínsecas e cenários onde os algoritmos autorais se destacam ou perdem eficiência.

---

## 8. Declaração Obrigatória de Autoria e Uso de IA

1. **Ferramenta/Modelo Utilizado:** Antigravity (Gemini 3.8 Flash / CLI)
2. **Motivo do Uso:** Apoio na estruturação do relatório, instrumentação dos scripts de benchmark e formalização de equações.
3. **Forma de Utilização:** Geração da estrutura de documentação, templates de validação empírica e revisão matemática de somatórios.
4. **Modificações Realizadas:** Adaptações às diretrizes específicas do enunciado do TP1, parametrização dos cenários de teste e elaboração dos raciocínios projetuais autorais.
5. **Validação do Resultado:** Todos os códigos submetidos à suíte automatizada de testes unitários (`test_suite.py`) e revisão humana detalhada.

---

## 9. Referências Bibliográficas

1. CORMEN, T. H. et al. *Algoritmos: Teoria e Prática*. 3ª ed. Rio de Janeiro: Elsevier, 2012.
2. KNUTH, D. E. *The Art of Computer Programming, Volume 3: Sorting and Searching*. 2nd ed. Addison-Wesley, 1998.
3. MANZATO, M. G. *Algoritmos Clássicos de Ordenação I e II*. Videoaulas da Universidade Virtual do Estado de São Paulo (UNIVESP).
4. RUNGE, C. J. R. *Projeto e Análise de Algoritmos - Algoritmos de Ordenação*. Videoaula UNIVESP.
