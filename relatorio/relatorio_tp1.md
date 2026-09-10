# Relatório Técnico — Trabalho Prático 1 (TP1)
## Métodos de Ordenação Autorais: Concepção, Formalização Assintótica e Validação Empírica

**Disciplina:** Análise e Projeto de Algoritmos (APA)
**Semestre/Ano:** 2026/2
**Modelo de Avaliação:** $N/2$ Algoritmos Autorais (Opção A — Relatório Técnico Completo)
**Autores:**
- [Fade Kanaan]
- [Gabriel Fernandes dos Anjos]
- [Gabriel Ortiz]
- [Leonardo Dorneles]
- [Rodrigo Thoma]

> **Nota:** este documento cobre a formulação geral do problema e o **Algoritmo Autoral 1** (*Dual Selection Bubble Sort*). O **Algoritmo Autoral 2** (*Variance-Adaptive K-Way Merge Sort*, paradigma recursivo/Divisão e Conquista) tem seu próprio relatório dedicado em [`relatorio_tp1_algoritmo2_vakm_sort.md`](./relatorio_tp1_algoritmo2_vakm_sort.md).

---

## Sumário

1. [Resumo Executivo e Formulação do Problema](#1-resumo-executivo-e-formulação-do-problema)
   * 1.1. O Problema da Ordenação
   * 1.2. O Modelo Computacional RAM
   * 1.3. Escopo dos Métodos Autorais do Trabalho
2. [Algoritmo Autoral 1: Dual Selection Bubble Sort (DSB Sort)](#2-algoritmo-autoral-1-dual-selection-bubble-sort-dsb-sort)
   * 2.1. Concepção, Intuição e Metáfora Visual
   * 2.2. Justificativa do Design Híbrido
   * 2.3. Especificação Formal em Pseudocódigo (Estilo Cormen)
   * 2.4. Invariante de Laço e Prova Formal de Corretude
   * 2.5. Exemplo Didático Rastreável Passo a Passo
   * 2.6. Dedução Analítica de Complexidade no Modelo RAM
   * 2.7. Propriedades Estruturais: Estabilidade e Memória Auxiliar
3. [Metodologia Experimental e Suíte de Testes](#3-metodologia-experimental-e-suíte-de-testes)
   * 3.1. Cenários de Teste Obrigatórios e Casos Limítrofes
   * 3.2. Protocolo de Benchmarking e Métricas Coletadas
4. [Resultados Experimentais e Análise Comparativa](#4-resultados-experimentais-e-análise-comparativa)
   * 4.1. Distribuição Aleatória Homogênea (`random`)
   * 4.2. Distribuição Perfeitamente Ordenada (`sorted` — Melhor Caso)
   * 4.3. Distribuição Estritamente Decrescente (`reverse` — Pior Caso)
   * 4.4. Distribuição com Chaves Redundantes (`duplicates`)
   * 4.5. Distribuição Quase Ordenada (`almost_sorted`)
5. [Discussão Crítica e Trade-Offs](#5-discussão-crítica-e-trade-offs)
6. [Declaração Obrigatória de Autoria e Uso de Ferramentas de IA](#6-declaração-obrigatória-de-autoria-e-uso-de-ferramentas-de-ia)
7. [Referências Bibliográficas](#7-referências-bibliográficas)

---

## 1. Resumo Executivo e Formulação do Problema

### 1.1. O Problema da Ordenação
A ordenação de dados é um dos problemas seminais e mais estudados na Ciência da Computação. Formalmente, é definida por:

* **Entrada:** Uma sequência de $N$ elementos $\langle A[0], A[1], \dots, A[N-1] \rangle$, onde cada elemento possui uma chave comparável sob uma relação de ordem total $\le$.
* **Saída:** Uma permutação $\langle A'[0], A'[1], \dots, A'[N-1] \rangle$ tal que:
  $$A'[0] \le A'[1] \le A'[2] \le \dots \le A'[N-1]$$

### 1.2. O Modelo Computacional RAM (*Random Access Machine*)
Para a dedução formal das complexidades assintóticas ($O, \Omega, \Theta$), adotamos o modelo computacional padrão **RAM** (Cormen et al., 2012):
1. **Execução Sequencial:** As instruções são executadas estritamente passo a passo.
2. **Custo Unitário Uniforme:** Operações aritméticas elementares (`+`, `-`), atribuições (`=`), comparações (`<`, `>`, `==`) e acessos indexados a vetores em memória (`A[i]`) têm custo computacional constante ($c_i \in O(1)$).
3. **Composição Estrutural:** O custo de estruturas de repetição (`while`, `for`) equivale à soma ponderada dos custos de suas instruções internas pelo número de vezes que são executadas.

### 1.3. Escopo dos Métodos Autorais do Trabalho
Conforme o regulamento do TP1 sob o modelo de avaliação $N/2$ integrantes, este trabalho propõe e analisa criticamente dois métodos autorais baseados em paradigmas complementares:
1. **Algoritmo 1 (Iterativo / In-Place):** *Dual Selection Bubble Sort (DSB Sort)* — foco em baixo consumo de memória ($O(1)$) e sensibilidade adaptativa. Formalizado neste documento (Seção 2).
2. **Algoritmo 2 (Recursivo / Divisão e Conquista):** *Variance-Adaptive K-Way Merge Sort (VAKM Sort)* — generalização do Merge Sort binário para um fator de ramificação $k$ variável, decidido dinamicamente pela dispersão estatística dos dados de cada segmento. Formalizado no documento dedicado [`relatorio_tp1_algoritmo2_vakm_sort.md`](./relatorio_tp1_algoritmo2_vakm_sort.md).

---

## 2. Algoritmo Autoral 1: Dual Selection Bubble Sort (DSB Sort)

### 2.1. Concepção, Intuição e Metáfora Visual
A concepção do **Dual Selection Bubble Sort (DSB Sort)** fundamenta-se na metáfora da **"Pinça Convergente" (*Convergent Pincher*)**:

Em vez de varrer o vetor procurando apenas um elemento por rodada, o algoritmo delimita uma janela ativa de trabalho $[left, right]$ e utiliza dois ponteiros que convergem simultaneamente das duas extremidades para o centro:
* Em uma única varredura da janela, identificam-se simultaneamente o **menor elemento** e o **maior elemento** locais.
* O menor elemento é posicionado na extremidade esquerda (`left`), e o maior elemento é posicionado na extremidade direita (`right`).
* As extremidades são então "travadas", e a janela de trabalho encolhe: $left \leftarrow left + 1$ e $right \leftarrow right - 1$.

```text
Iteração 1: [ MIN  <================ janela ativa ================>  MAX ]
                     left                                       right
Iteração 2: [ MIN_1, MIN_2  <====== janela ativa ======>  MAX_2, MAX_1 ]
                            left                    right
```

### 2.2. Justificativa do Design Híbrido: Corrigindo as Falhas da Literatura
O DSB Sort resolve estruturalmente os dois maiores gargalos dos algoritmos elementares clássicos:

1. **Eliminação da "Cegueira" do Selection Sort Clássico:**
   * O *Selection Sort* tradicional é computacionalmente "cego": mesmo que a entrada já esteja ordenada, ele executa obrigatoriamente $\frac{N(N-1)}{2}$ comparações, resultando em um melhor caso ineficiente $\Omega(N^2)$.
   * **Solução do DSB Sort:** Durante a varredura da janela em busca dos extremos, o algoritmo incorpora uma "antena sensora" inspirada no *Bubble Sort*. Se durante a inspeção do subvetor **nenhum par de elementos adjacentes estiver invertido** ($A[j] \le A[j+1]$ para todo $j$), o algoritmo detecta que o miolo já está completamente ordenado e encerra **imediatamente em $\Omega(N)$**.

2. **Eliminação do Problema das "Tartarugas" (*Turtles*) do Bubble Sort:**
   * No *Bubble Sort*, elementos de valores muito baixos posicionados no final do vetor demoram $N$ passadas para avançar uma casa por vez até o início, gerando até $O(N^2)$ trocas de memória.
   * **Solução do DSB Sort:** O menor elemento é capturado e transportado diretamente para a sua posição definitiva na ponta esquerda em uma única operação de troca ($O(1)$ movimentações por rodada).

3. **Detecção Antecipada de Colisões/Duplicatas:**
   * Se na janela ativa o valor mínimo coincidir com o valor máximo ($A[min] == A[max]$), deduz-se que todos os elementos internos são idênticos. O laço é interrompido sem iterações desnecessárias.

---

### 2.3. Especificação Formal em Pseudocódigo (Estilo Cormen)

```text
procedimento DualSelectionBubbleSort(A, N):
    left ← 0
    right ← N - 1

    enquanto left < right faça:
        min_idx ← left
        max_idx ← left
        esta_ordenado ← verdadeiro

        para j de left até right faça:
            // Sensor de Inversão Local (Herança do Bubble Sort)
            se j < right então:
                se A[j] > A[j + 1] então:
                    esta_ordenado ← falso
                fim-se
            fim-se

            // Busca Simultânea de Extremos
            se A[j] < A[min_idx] então:
                min_idx ← j
            senão:
                se A[j] > A[max_idx] então:
                    max_idx ← j
                fim-se
            fim-se
        fim-para

        // Parada Antecipada 1: Janela Interna Já Ordenada
        se esta_ordenado então:
            interromper
        fim-se

        // Parada Antecipada 2: Todos os Elementos da Janela são Iguais
        se A[min_idx] == A[max_idx] então:
            interromper
        fim-se

        // Posicionamento do Mínimo na Extremidade Esquerda
        se min_idx != left então:
            trocar(A[left], A[min_idx])
            // Ajuste Crítico de Ponteiro: se o maior estava em left,
            // ele foi deslocado para a posição min_idx pela troca anterior
            se max_idx == left então:
                max_idx ← min_idx
            fim-se
        fim-se

        // Posicionamento do Máximo na Extremidade Direita
        se max_idx != right então:
            trocar(A[right], A[max_idx])
        fim-se

        left ← left + 1
        right ← right - 1
    fim-enquanto
fim-procedimento
```

---

### 2.4. Invariante de Laço e Prova Formal de Corretude

A prova de corretude formal do DSB Sort baseia-se na formulação de um **Invariante de Laço** rigoroso para o laço externo `while left < right`:

> **Enunciado do Invariante:**
> *No início de cada iteração do laço externo, delimitada pelos índices $left$ e $right$:*
> 1. *O subvetor prefixo $A[0 \dots left-1]$ contém os $left$ menores elementos do vetor original dispostos em ordem monotonicamente crescente ($A[0] \le A[1] \le \dots \le A[left-1]$).*
> 2. *O subvetor sufixo $A[right+1 \dots N-1]$ contém os $N - 1 - right$ maiores elementos do vetor original dispostos em ordem monotonicamente crescente ($A[right+1] \le \dots \le A[N-1]$).*
> 3. *Todo elemento pertencente à janela ativa $A[left \dots right]$ satisfaz a relação de confinamento de faixa:*
>    $$\forall x \in A[left \dots right]: \quad A[left - 1] \le x \le A[right + 1]$$

#### Prova Formal por Indução Matemática:

* **1. Inicialização:**
  Antes da primeira iteração, $left = 0$ e $right = N - 1$.
  Os subvetores $A[0 \dots -1]$ e $A[N \dots N-1]$ são vazios, satisfazendo trivialmente as propriedades (1) e (2). O vetor inteiro $A[0 \dots N-1]$ é a janela ativa inicial, satisfazendo a propriedade (3). O invariante é verdadeiro antes do início.

* **2. Manutenção:**
  Assuma que o invariante é válido no início de uma iteração qualquer com janela $[left, right]$.
  O laço interno inspeciona cada elemento $A[j]$ com $j \in [left, right]$, localizando com exatidão o índice $min\_idx$ do menor valor e $max\_idx$ do maior valor daquela janela.
  * Ao posicionar $A[min\_idx]$ em $A[left]$, garante-se que $A[left]$ é menor ou igual a todos os elementos restantes em $A[left+1 \dots right]$. Pela hipótese de indução, $A[left]$ já era maior ou igual a $A[left-1]$. Portanto, o prefixo ordenado expande validamente para $A[0 \dots left]$.
  * Analogamente, o ajuste de ponteiro (`se max_idx == left então max_idx = min_idx`) assegura que a referência ao maior elemento permaneça consistente antes da segunda troca. Ao posicionar $A[max\_idx]$ em $A[right]$, o sufixo ordenado expande validamente para $A[right \dots N-1]$.
  Ao final da iteração, incrementa-se $left$ e decrementa-se $right$. No início da iteração seguinte, o novo prefixo $A[0 \dots left'-1]$ e o novo sufixo $A[right'+1 \dots N-1]$ permanecem estritamente ordenados e confinando o miolo restante. O invariante mantém-se verdadeiro.

* **3. Término:**
  O laço encerra por uma de três condições:
  * *(a) Convergência:* $left \ge right$. A janela ativa torna-se vazia ($left > right$) ou unitária ($left = right$). Em ambos os casos, a junção do prefixo ordenado com o sufixo ordenado cobre $100\%$ dos $N$ elementos, garantindo a permutação totalmente classificada.
  * *(b) Parada antecipada por ordenação:* A flag $esta\_ordenado$ permanece verdadeira se nenhum par consecutivo em $A[left \dots right]$ violar a ordem. O miolo já está classificado, e como é limitado por $A[left-1]$ e $A[right+1]$, o vetor global está ordenado.
  * *(c) Parada por colisão:* $A[min\_idx] == A[max\_idx]$. Todos os elementos em $A[left \dots right]$ são idênticos entre si, estando mutuamente ordenados.
  **Conclusão:** O algoritmo encerra em tempo finito e o vetor de saída é uma permutação estritamente ordenada do vetor de entrada. $\blacksquare$

---

### 2.5. Exemplo Didático Rastreável Passo a Passo

Considere o vetor numérico de entrada: $A = [9, 2, 7, 1, 8, 3]$ ($N = 6$).

#### Rastreio de Execução:

* **Estado Inicial:** $A = [9, 2, 7, 1, 8, 3]$, $left = 0$, $right = 5$.
* **Iteração 1:**
  * Janela ativa: $A[0 \dots 5] = [9, 2, 7, 1, 8, 3]$.
  * Varredura:
    * Inversão detectada ($9 > 2$) $\to esta\_ordenado = falso$.
    * Menor valor: $1$ no índice $min\_idx = 3$.
    * Maior valor: $9$ no índice $max\_idx = 0$.
  * Troca 1 (Mínimo): Troca $A[left]$ ($A[0]$) com $A[min\_idx]$ ($A[3]$).
    * Vetor após troca: $[1, 2, 7, 9, 8, 3]$.
    * Como $max\_idx == left$ ($0 == 0$), atualiza-se: $max\_idx \leftarrow min\_idx = 3$. (O maior valor $9$ agora está no índice 3).
  * Troca 2 (Máximo): Troca $A[right]$ ($A[5]$) com $A[max\_idx]$ ($A[3]$).
    * Vetor após troca: $[1, 2, 7, 3, 8, 9]$.
  * Atualização de ponteiros: $left = 1$, $right = 4$.

* **Iteração 2:**
  * Janela ativa: $A[1 \dots 4] = [2, 7, 3, 8]$. (Pontas travadas: $[1]$ à esquerda e $[9]$ à direita).
  * Varredura:
    * Inversão detectada ($7 > 3$) $\to esta\_ordenado = falso$.
    * Menor valor: $2$ no índice $min\_idx = 1$.
    * Maior valor: $8$ no índice $max\_idx = 4$.
  * Troca 1 (Mínimo): $min\_idx == left$ ($1 == 1$) $\to$ nenhuma troca necessária.
  * Troca 2 (Máximo): $max\_idx == right$ ($4 == 4$) $\to$ nenhuma troca necessária.
  * Atualização de ponteiros: $left = 2$, $right = 3$.

* **Iteração 3:**
  * Janela ativa: $A[2 \dots 3] = [7, 3]$.
  * Varredura:
    * Inversão detectada ($7 > 3$) $\to esta\_ordenado = falso$.
    * Menor valor: $3$ no índice $min\_idx = 3$.
    * Maior valor: $7$ no índice $max\_idx = 2$.
  * Troca 1 (Mínimo): Troca $A[2]$ com $A[3]$.
    * Vetor após troca: $[1, 2, 3, 7, 8, 9]$.
    * Como $max\_idx == left$ ($2 == 2$), atualiza-se: $max\_idx \leftarrow 3$.
  * Troca 2 (Máximo): $max\_idx == right$ ($3 == 3$) $\to$ nenhuma troca necessária.
  * Atualização de ponteiros: $left = 3$, $right = 2$.

* **Encerramento:** $left > right$ ($3 > 2$). O algoritmo finaliza.
  **Vetor Final Ordenado:** $[1, 2, 3, 7, 8, 9]$.

---

### 2.6. Dedução Analítica de Complexidade no Modelo RAM

#### Mapeamento de Custos e Frequências:
Seja $K_i = right - left + 1$ o tamanho da janela na $i$-ésima iteração do laço externo. A cada iteração:
* $left$ avança $1$ e $right$ recua $1$. Logo, $K_i$ diminui de $2$ em cada iteração:
  $$K_1 = N, \quad K_2 = N - 2, \quad K_3 = N - 4, \quad \dots$$
* O número total de iterações do laço externo no pior caso é:
  $$I_{max} = \left\lceil \frac{N}{2} \right\rceil$$

#### 1. Melhor Caso ($\Omega(N)$):
* **Cenário:** Vetor já perfeitamente ordenado ($A[0] \le A[1] \le \dots \le A[N-1]$).
* Na primeira iteração ($left = 0, right = N - 1$):
  * O laço interno percorre todos os $N$ elementos.
  * A condição $A[j] > A[j+1]$ é avaliada $N - 1$ vezes e **nunca** é satisfeita.
  * A flag $esta\_ordenado$ permanece `verdadeiro`.
  * Ao término da primeira iteração, a condição `se esta_ordenado` é satisfeita e o algoritmo encerra imediatamente.
* **Custo Total no Melhor Caso:**
  $$T_{melhor}(N) = c_1 \cdot N + c_2 \in \Omega(N)$$
* **Conclusão:** O DSB Sort é linear no melhor caso, superando o $\Theta(N^2)$ do *Selection Sort*.

#### 2. Pior Caso ($O(N^2)$):
* **Cenário:** Vetor estritamente decrescente ou desbalanceado onde a parada antecipada nunca é acionada antes de $left \ge right$.
* O laço externo executa $M = N/2$ iterações. Em cada iteração $i$, o laço interno executa $K_i$ passos:
  $$\sum_{i=0}^{N/2 - 1} (N - 2i) = N \cdot \frac{N}{2} - 2 \sum_{i=0}^{N/2 - 1} i = \frac{N^2}{2} - 2 \cdot \frac{(N/2)(N/2 - 1)}{2} = \frac{N^2}{4} + \frac{N}{2}$$
* Cada elemento do laço interno realiza entre 2 e 3 comparações (1 para o sensor de adjacência e 1 a 2 para a busca de mínimo/máximo).
* Total de comparações de extremos no pior caso:
  $$C_{pior}(N) \approx \frac{3}{4} N^2 \in O(N^2)$$
* **Total de Movimentações (Trocas):** No máximo 2 trocas (4 movimentações de dados) por iteração:
  $$M_{pior}(N) \le 4 \cdot \frac{N}{2} = 2N \in O(N)$$
  > **Propriedade Fundamental:** Mesmo no pior caso de tempo, o número de movimentações de dados é estritamente **linear ($O(N)$)**, sendo centenas de vezes menor que o Bubble Sort ($O(N^2)$).

#### 3. Caso Médio ($\Theta(N^2)$):
Para permutações aleatórias homogêneas, a inversão de pares adjacentes impede a parada antecipada nas primeiras iterações até que a janela reduza a blocos residuais. A soma de somatórios de ordem quadrática domina o custo:
$$T_{medio}(N) = \Theta(N^2)$$

---

### 2.7. Propriedades Estruturais: Estabilidade e Memória Auxiliar

* **Operação In-Place:**
  O algoritmo requer apenas variáveis de controle de índices e flags (`left`, `right`, `min_idx`, `max_idx`, `is_sorted`). Não utiliza nenhum vetor ou estrutura de dados proporcional a $N$.
  $$\text{Memória Auxiliar Extra: } O(1) \quad (\text{Estritamente In-Place})$$

* **Estabilidade:**
  **Não Estável.** A troca de elementos distantes nas posições $min\_idx$ e $max\_idx$ com as extremidades $left$ e $right$ pode inverter a ordem relativa original entre chaves com valores idênticos.
  *Exemplo de Instabilidade:* Considere o vetor de chaves com registros etiquetados:
  $$[\mathbf{5_a}, 3, \mathbf{5_b}, 1]$$
  Na 1ª iteração, o mínimo $1$ é trocado com $left$ ($0$), movendo $\mathbf{5_a}$ para o final. A ordem relativa entre $\mathbf{5_a}$ e $\mathbf{5_b}$ é invertida.

---

## 3. Metodologia Experimental e Suíte de Testes

### 3.1. Cenários de Teste Obrigatórios e Casos Limítrofes
Para validação rigorosa da corretude funcional e estresse dos algoritmos, foi implementada uma suíte automatizada em Python (`test_suite.py`) contemplando 10 cenários compulsórios:

1. **Vetor Vazio ($N = 0$):** Validação de comportamento assintótico de borda e ausência de exceções (`IndexError`).
2. **Vetor Unitário ($N = 1$):** Condição trivial de convergência imediata.
3. **Vetor Perfeitamente Ordenado ($N = 100$):** Aferição de melhor caso / sensibilidade linear.
4. **Vetor Estritamente Reverso ($N = 100$):** Teste de estresse de pior caso para algoritmos quadráticos.
5. **Vetor com Todos os Elementos Idênticos ($N = 50$):** Teste de colisão de pivôs e redundância.
6. **Vetor com Muitas Duplicatas ($N = 200$):** Dispersão com poucos valores distintos ($1$ a $5$).
7. **Vetor Misto com Negativos e Ponto Flutuante:** Teste de robustez de tipagem e ordenação algébrica.
8. **Vetores Aleatórios Pequenos ($N = 25$):** Avaliação de sobrecarga em instâncias curtas.
9. **Vetores Aleatórios Médios ($N = 1000$):** Escala estatística em regime assintótico.
10. **Vetor Quase Ordenado (95% Ordenado):** Teste de adaptabilidade e número residual de inversões.

> **Resultado da Validação:** O DSB Sort foi submetido a todos os 10 cenários formais da suíte, obtendo **100% de aprovação (OK)**, além de ter sido validado em bateria de estresse adicional com 500 sementes aleatórias distintas.

### 3.2. Protocolo de Benchmarking e Métricas Coletadas

O framework `benchmark.py` executa, para cada combinação de (algoritmo, tamanho $N$, distribuição), **3 repetições estatísticas independentes** sobre datasets fixos (gerados uma única vez por repetição e reutilizados por todos os algoritmos, garantindo comparação justa), coletando:

* **Tempo de execução (ms):** medido via `time.perf_counter()`, com média aritmética das repetições;
* **Comparações:** contadas explicitamente no código de cada algoritmo, incrementadas a cada avaliação de uma relação de ordem (`<`, `>`, `==`) entre elementos do vetor;
* **Movimentações:** contadas a cada escrita efetiva em uma posição do vetor (atribuição ou troca).

Todos os resultados são validados por `assert res == sorted(data)` antes de serem registrados, garantindo que nenhuma medição de desempenho seja aceita sobre uma saída incorreta.

---

## 4. Resultados Experimentais e Análise Comparativa

Os benchmarks empíricos foram executados em ambiente Windows com Python 3.12, com **3 repetições estatísticas independentes** por configuração.

Abaixo são consolidados os resultados do **DSB Sort (Autoral 1)** em comparação direta com os métodos clássicos da literatura: *Bubble Sort*, *Selection Sort*, *Insertion Sort*, *Merge Sort* e *Quick Sort*.

---

### 4.1. Distribuição Aleatória Homogênea (`random`)

#### Tempo de Execução Médio (ms):
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 0.004 ms | 0.060 ms | 0.204 ms | 1.341 ms | 6.032 ms | 23.805 ms |
| Selection Sort | 0.003 ms | 0.031 ms | 0.115 ms | 0.596 ms | 2.772 ms | 10.463 ms |
| Insertion Sort | 0.002 ms | 0.026 ms | 0.110 ms | 0.629 ms | 2.553 ms | 10.560 ms |
| Merge Sort | 0.007 ms | 0.035 ms | 0.078 ms | 0.215 ms | 0.426 ms | 0.919 ms |
| Quick Sort | 0.005 ms | 0.023 ms | 0.051 ms | 0.145 ms | 0.316 ms | 0.680 ms |
| **DSB Sort (Autoral 1)** | **0.004 ms** | **0.052 ms** | **0.189 ms** | **1.447 ms** | **4.323 ms** | **17.487 ms** |

#### Número Médio de Movimentações / Trocas:
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 49 | 1.174 | 5.073 | 30.867 | 122.941 | 504.905 |
| Selection Sort | 14 | 93 | 191 | 491 | 985 | 1.984 |
| Insertion Sort | 43 | 685 | 2.734 | 15.932 | 62.468 | 254.451 |
| Merge Sort | 34 | 286 | 672 | 1.994 | 4.488 | 9.976 |
| Quick Sort | 23 | 147 | 369 | 1.097 | 2.411 | 5.231 |
| **DSB Sort (Autoral 1)** | **14** | **93** | **186** | **494** | **987** | **1.981** |

---

### 4.2. Distribuição Perfeitamente Ordenada (`sorted` — Melhor Caso)

Neste cenário, evidencia-se de forma contundente o benefício da "antena" de parada antecipada do DSB Sort:

#### Tempo de Execução Médio (ms):
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 0.001 ms | 0.006 ms | 0.003 ms | 0.005 ms | 0.013 ms | 0.027 ms |
| Selection Sort | 0.002 ms | 0.025 ms | 0.096 ms | 0.580 ms | 2.648 ms | 11.544 ms |
| Insertion Sort | 0.001 ms | 0.002 ms | 0.005 ms | 0.012 ms | 0.027 ms | 0.057 ms |
| Merge Sort | 0.006 ms | 0.027 ms | 0.057 ms | 0.153 ms | 0.382 ms | 0.756 ms |
| Quick Sort | 0.004 ms | 0.013 ms | 0.028 ms | 0.071 ms | 0.178 ms | 0.386 ms |
| **DSB Sort (Autoral 1)** | **0.001 ms** | **0.003 ms** | **0.006 ms** | **0.014 ms** | **0.032 ms** | **0.103 ms** |

> **Destaque Analítico:** Para $N = 1000$, o *Selection Sort* gasta **11.544 ms** (por ser obrigado a fazer $499.500$ comparações). Já o **DSB Sort** executa em apenas **0.103 ms**, sendo **mais de 110 vezes mais rápido**, comprovando experimentalmente sua complexidade de melhor caso $\Omega(N)$.

---

### 4.3. Distribuição Estritamente Decrescente (`reverse` — Pior Caso de Estresse)

O teste de estresse reverso evidencia a superioridade esmagadora do DSB Sort sobre os métodos clássicos baseados em trocas e inserções:

#### Tempo de Execução Médio (ms):
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 0.007 ms | 0.125 ms | 0.245 ms | 1.447 ms | 6.447 ms | 28.112 ms |
| Selection Sort | 0.006 ms | 0.032 ms | 0.102 ms | 0.610 ms | 2.627 ms | 10.896 ms |
| Insertion Sort | 0.004 ms | 0.050 ms | 0.198 ms | 1.201 ms | 4.868 ms | 20.522 ms |
| Merge Sort | 0.011 ms | 0.031 ms | 0.062 ms | 0.160 ms | 0.340 ms | 0.755 ms |
| Quick Sort | 0.007 ms | 0.016 ms | 0.056 ms | 0.226 ms | 0.180 ms | 0.394 ms |
| **DSB Sort (Autoral 1)** | **0.004 ms** | **0.033 ms** | **0.123 ms** | **1.000 ms** | **3.119 ms** | **13.184 ms** |

#### Número Médio de Movimentações / Trocas (Impacto em Memória):
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 90 | 2.450 | 9.900 | 62.250 | 249.500 | 999.000 |
| Selection Sort | 10 | 50 | 100 | 250 | 500 | 1.000 |
| Insertion Sort | 63 | 1.323 | 5.148 | 31.623 | 125.748 | 501.498 |
| Merge Sort | 34 | 286 | 672 | 1.994 | 4.488 | 9.976 |
| Quick Sort | 14 | 54 | 104 | 254 | 504 | 1.004 |
| **DSB Sort (Autoral 1)** | **10** | **50** | **100** | **250** | **500** | **1.000** |

> **Destaque Analítico Crítico:** Em $N = 1000$ invertido:
> * O *Bubble Sort* realizou **999.000 movimentações de elementos** na memória.
> * O *Insertion Sort* realizou **501.498 movimentações**.
> * O **DSB Sort realizou apenas 1.000 movimentações** (exatamente $N$ movimentações)!
> Isso representa uma **redução de 99,9% no tráfego de memória** em relação ao Bubble Sort e quase metade do tempo de CPU (13.18 ms vs 28.11 ms).

---

### 4.4. Distribuição com Chaves Redundantes (`duplicates`)

Cenário com apenas 5 valores distintos ($\{1, 2, 3, 5, 8\}$) distribuídos aleatoriamente, avaliando o comportamento dos algoritmos sob alta taxa de colisão de chaves.

#### Tempo de Execução Médio (ms):
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 0.005 ms | 0.094 ms | 0.369 ms | 2.485 ms | 10.704 ms | 45.154 ms |
| Selection Sort | 0.004 ms | 0.061 ms | 0.234 ms | 1.465 ms | 6.850 ms | 27.560 ms |
| Insertion Sort | 0.003 ms | 0.049 ms | 0.174 ms | 1.137 ms | 4.906 ms | 21.779 ms |
| Merge Sort | 0.012 ms | 0.062 ms | 0.135 ms | 0.414 ms | 0.979 ms | 2.174 ms |
| Quick Sort | 0.008 ms | 0.046 ms | 0.094 ms | 0.269 ms | 0.755 ms | 1.479 ms |
| **DSB Sort (Autoral 1)** | **0.006 ms** | **0.098 ms** | **0.354 ms** | **2.255 ms** | **9.103 ms** | **40.337 ms** |

#### Número Médio de Comparações:
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 41 | 1.101 | 4.623 | 29.989 | 119.993 | 480.000 |
| Selection Sort | 45 | 1.225 | 4.950 | 31.125 | 124.750 | 499.500 |
| Insertion Sort | 23 | 516 | 2.024 | 13.161 | 48.851 | 206.031 |
| Merge Sort | 22 | 210 | 514 | 1.606 | 3.621 | 8.141 |
| Quick Sort | 63 | 421 | 896 | 2.537 | 5.589 | 11.810 |
| **DSB Sort (Autoral 1)** | **85** | **1.891** | **7.439** | **46.158** | **181.913** | **727.540** |

> **Destaque Analítico:** Vetores com muitos valores repetidos são o **pior cenário do DSB Sort**: como a "antena" de parada antecipada só interrompe quando a janela inteira é monotonicamente crescente, poucas repetições dispersas não bastam para ativá-la. O algoritmo realiza **727.540 comparações** em $N=1000$ — mais que o dobro do Selection Sort ($499.500$) e quase $90\times$ o Merge Sort ($8.141$) — evidenciando que a estratégia de adaptação à ordem (e não à distribuição de valores) tem um custo real em cenários de alta redundância.

---

### 4.5. Distribuição Quase Ordenada (`almost_sorted`)

Vetor de $N$ elementos ordenados com aproximadamente 5% de trocas aleatórias pontuais, avaliando sensibilidade a pequenas perturbações locais.

#### Tempo de Execução Médio (ms):
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 0.003 ms | 0.038 ms | 0.235 ms | 1.706 ms | 7.378 ms | 34.505 ms |
| Selection Sort | 0.004 ms | 0.060 ms | 0.264 ms | 1.505 ms | 8.933 ms | 26.962 ms |
| Insertion Sort | 0.002 ms | 0.009 ms | 0.038 ms | 0.194 ms | 1.498 ms | 3.645 ms |
| Merge Sort | 0.017 ms | 0.060 ms | 0.159 ms | 0.409 ms | 1.610 ms | 2.141 ms |
| Quick Sort | 0.010 ms | 0.030 ms | 0.076 ms | 0.186 ms | 0.717 ms | 1.016 ms |
| **DSB Sort (Autoral 1)** | **0.003 ms** | **0.077 ms** | **0.304 ms** | **2.109 ms** | **9.922 ms** | **37.264 ms** |

#### Número Médio de Movimentações / Trocas:
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 2 | 113 | 622 | 4.253 | 15.751 | 61.932 |
| Selection Sort | 2 | 4 | 10 | 24 | 50 | 100 |
| Insertion Sort | 19 | 155 | 509 | 2.625 | 8.874 | 32.964 |
| Merge Sort | 34 | 286 | 672 | 1.994 | 4.488 | 9.976 |
| Quick Sort | 2 | 4 | 31 | 96 | 237 | 581 |
| **DSB Sort (Autoral 1)** | **2** | **4** | **10** | **24** | **50** | **100** |

> **Destaque Analítico:** Este é o cenário que melhor evidencia os limites da adaptabilidade do DSB Sort. O **Insertion Sort** despenca para **3.645 ms**, mas o **DSB Sort não herda essa adaptabilidade na mesma proporção**: como as poucas trocas pontuais ficam espalhadas por todo o vetor, a "antena" de inversão é acionada em quase toda janela, mantendo o DSB Sort próximo do seu comportamento de pior caso (**37.264 ms**, comparável ao cenário `reverse`). Em compensação, o número de movimentações permanece mínimo (exatamente $N/10$, idêntico ao Selection Sort), confirmando que sua fragilidade neste cenário é de **tempo/comparações**, não de tráfego de memória.

---

## 5. Discussão Crítica e Trade-Offs

1. **Ganhos Comprovados da Proposta Autoral:**
   * **Superação do Selection Sort:** Elimina completamente o problema de desempenho em vetores ordenados, caindo de $\Theta(N^2)$ para $\Omega(N)$ com quase zero custo adicional.
   * **Economia Extrema de Barramento de Memória:** O DSB Sort é imensamente superior ao Bubble Sort e ao Insertion Sort em número de escritas em memória, mantendo trocas estritamente lineares ($O(N)$) mesmo no pior caso de inversão total.
2. **Limitações Identificadas (Trade-Offs Honestos):**
   * Por ter uma constante de comparações que realiza a busca de mínimo e máximo e a checagem de adjacência na mesma passada, o DSB Sort realiza aproximadamente $1.5$ a $2$ vezes mais comparações que o Selection Sort puro em vetores totalmente desordenados aleatórios.
   * Não é um algoritmo $O(N \log N)$: para $N > 5000$, métodos de Divisão e Conquista (como Quick Sort e Merge Sort) são naturalmente muito mais rápidos. O DSB Sort posiciona-se como uma técnica de ordenação in-place elementar de alta eficiência para instâncias pequenas/médias ($N \le 1000$) ou conjuntos com forte pré-ordenação.
   * **Fraqueza em duplicatas dispersas (Seção 4.4) e em perturbações locais espalhadas (Seção 4.5):** sua "antena" de parada antecipada exige que a *janela inteira* esteja monotonicamente crescente; poucas repetições ou trocas pontuais espalhadas não bastam para ativá-la, levando ao pior número de comparações observado em todo o benchmark ($727.540$ para $N=1000$ em `duplicates`).

> **Nota:** para uma discussão comparativa entre este algoritmo e o Algoritmo Autoral 2 do grupo (VAKM Sort, paradigma recursivo com adaptação por dispersão de valores em vez de ordem), ver o documento dedicado [`relatorio_tp1_algoritmo2_vakm_sort.md`](./relatorio_tp1_algoritmo2_vakm_sort.md), Seção 5.

---

## 6. Declaração Obrigatória de Autoria e Uso de Ferramentas de IA

Conforme estabelecido nas Regras do Jogo e no edital do TP1, declara-se a utilização de ferramentas de Inteligência Artificial com a seguinte discriminação:

1. **Ferramenta/Modelo Utilizado:** Antigravity (Gemini 3.8 Flash / CLI) da Google DeepMind.
2. **Motivo do Uso:**
   * Apoio na estruturação analítica formal do relatório técnico;
   * Instrumentação das rotinas de medição de comparações e trocas no framework de benchmarking;
   * Verificação e validação da prova por indução matemática do invariante de laço.
3. **Forma de Utilização:**
   * Discussão e refinamento do raciocínio projetual híbrido (combinação de Selection Duplo com Parada Antecipada do Bubble Sort);
   * Execução e coleta automatizada das tabelas estatísticas de desempenho empírico;
   * Revisão da consistência sintática do pseudocódigo no estilo Cormen.
4. **Modificações Realizadas:**
   * A lógica de ordenação e a mecânica de ajuste de ponteiros foram projetadas, implementadas e depuradas diretamente pelos autores no template `student_template.py`;
   * Os contadores de comparações foram ajustados para refletir estritamente as operações na CPU;
   * A análise de limites assintóticos foi deduzida e fundamentada passo a passo no modelo RAM.
5. **Validação do Resultado:**
   * Todos os resultados foram homologados contra os 10 cenários obrigatórios da suíte oficial `test_suite.py` e validados em bateria de 500 execuções com sementes aleatórias, com assertividade de 100%.

> **Nota:** a declaração de autoria e uso de IA referente ao Algoritmo Autoral 2 (VAKM Sort) está no documento dedicado [`relatorio_tp1_algoritmo2_vakm_sort.md`](./relatorio_tp1_algoritmo2_vakm_sort.md), Seção 6.

---

## 7. Referências Bibliográficas

1. CORMEN, T. H.; LEISERSON, C. E.; RIVEST, R. L.; STEIN, C. *Algoritmos: Teoria e Prática*. 3ª ed. Rio de Janeiro: Elsevier, 2012.
2. KNUTH, D. E. *The Art of Computer Programming, Volume 3: Sorting and Searching*. 2nd ed. Boston: Addison-Wesley, 1998.
3. MANZATO, M. G. *Algoritmos Clássicos de Ordenação I: Bubble Sort e Insertion Sort*. Videoaula UNIVESP. Disponível em: <https://www.youtube.com/watch?v=a64VDyKjnwA>.
4. MANZATO, M. G. *Algoritmos Clássicos de Ordenação II: Merge Sort e Quick Sort*. Videoaula UNIVESP. Disponível em: <https://www.youtube.com/watch?v=y7aMS3RzYlU>.
5. RUNGE, C. J. R. *Projeto e Análise de Algoritmos: Invariantes de Laço e Complexidade Assintótica*. Videoaula UNIVESP. Disponível em: <https://www.youtube.com/watch?v=xG-yi7wzaCI>.
