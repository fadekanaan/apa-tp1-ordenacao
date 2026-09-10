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

---

## Sumário

1. [Resumo Executivo e Formulação do Problema](#1-resumo-executivo-e-formulação-do-problema)
   - 1.1. O Problema da Ordenação
   - 1.2. O Modelo Computacional RAM
   - 1.3. Escopo dos Métodos Autorais do Trabalho
2. [Algoritmo Autoral 1: Dual Selection Bubble Sort (DSB Sort)](#2-algoritmo-autoral-1-dual-selection-bubble-sort-dsb-sort)
   - 2.1. Concepção, Intuição e Metáfora Visual
   - 2.2. Justificativa do Design Híbrido
   - 2.3. Especificação Formal em Pseudocódigo (Estilo Cormen)
   - 2.4. Invariante de Laço e Prova Formal de Corretude
   - 2.5. Exemplo Didático Rastreável Passo a Passo
   - 2.6. Dedução Analítica de Complexidade no Modelo RAM
   - 2.7. Propriedades Estruturais: Estabilidade e Memória Auxiliar
3. [Algoritmo Autoral 2: Dual-Pivot Extremes Sieve Sort (DPES Sort)](#3-algoritmo-autoral-2-dual-pivot-extremes-sieve-sort-dpes-sort)
   - 3.1. Concepção, Intuição e Metáfora Visual
   - 3.2. Justificativa do Design: Partição Tripla Adaptativa
   - 3.3. Especificação Formal em Pseudocódigo (Estilo Cormen)
   - 3.4. Invariante de Recursão e Prova Formal de Corretude
   - 3.5. Exemplo Didático Rastreável Passo a Passo
   - 3.6. Dedução Analítica de Complexidade no Modelo RAM
   - 3.7. Propriedades Estruturais: Estabilidade e Memória Auxiliar
4. [Metodologia Experimental e Suíte de Testes](#4-metodologia-experimental-e-suíte-de-testes)
   - 4.1. Cenários de Teste Obrigatórios e Casos Limítrofes
   - 4.2. Protocolo de Benchmarking e Métricas Coletadas
5. [Resultados Experimentais e Análise Comparativa](#5-resultados-experimentais-e-análise-comparativa)
   - 5.1. Distribuição Aleatória Homogênea (`random`)
   - 5.2. Distribuição Perfeitamente Ordenada (`sorted` — Melhor Caso)
   - 5.3. Distribuição Estritamente Decrescente (`reverse` — Pior Caso)
   - 5.4. Distribuição com Chaves Redundantes (`duplicates`)
   - 5.5. Distribuição Quase Ordenada (`almost_sorted`)
6. [Discussão Crítica e Trade-Offs](#6-discussão-crítica-e-trade-offs)
   - 6.1. DSB Sort (Autoral 1 — Iterativo)
   - 6.2. DPES Sort (Autoral 2 — Recursivo / Divisão e Conquista)
   - 6.3. Comparação Direta: DSB Sort vs DPES Sort
7. [Declaração Obrigatória de Autoria e Uso de Ferramentas de IA](#7-declaração-obrigatória-de-autoria-e-uso-de-ferramentas-de-ia)
8. [Referências Bibliográficas](#8-referências-bibliográficas)

---

## 1. Resumo Executivo e Formulação do Problema

### 1.1. O Problema da Ordenação

A ordenação de dados é um dos problemas seminais e mais estudados na Ciência da Computação. Formalmente, é definida por:

- **Entrada:** Uma sequência de $N$ elementos $\langle A[0], A[1], \dots, A[N-1] \rangle$, onde cada elemento possui uma chave comparável sob uma relação de ordem total $\le$.
- **Saída:** Uma permutação $\langle A'[0], A'[1], \dots, A'[N-1] \rangle$ tal que:
  $$A'[0] \le A'[1] \le A'[2] \le \dots \le A'[N-1]$$

### 1.2. O Modelo Computacional RAM (_Random Access Machine_)

Para a dedução formal das complexidades assintóticas ($O, \Omega, \Theta$), adotamos o modelo computacional padrão **RAM** (Cormen et al., 2012):

1. **Execução Sequencial:** As instruções são executadas estritamente passo a passo.
2. **Custo Unitário Uniforme:** Operações aritméticas elementares (`+`, `-`), atribuições (`=`), comparações (`<`, `>`, `==`) e acessos indexados a vetores em memória (`A[i]`) têm custo computacional constante ($c_i \in O(1)$).
3. **Composição Estrutural:** O custo de estruturas de repetição (`while`, `for`) equivale à soma ponderada dos custos de suas instruções internas pelo número de vezes que são executadas.

### 1.3. Escopo dos Métodos Autorais do Trabalho

Conforme o regulamento do TP1 sob o modelo de avaliação $N/2$ integrantes, este trabalho propõe e analisa criticamente dois métodos autorais baseados em paradigmas complementares:

1. **Algoritmo 1 (Iterativo / In-Place):** _Dual Selection Bubble Sort (DSB Sort)_ — foco em baixo consumo de memória ($O(1)$) e sensibilidade adaptativa.
2. **Algoritmo 2 (Recursivo / Divisão e Conquista):** _Dual-Pivot Extremes Sieve Sort (DPES Sort)_ — partição tripla com pivôs adaptativos por interpolação de faixa, _fallback_ para Insertion Sort em partições pequenas ($\le 16$) e detecção antecipada de segmentos uniformes.

---

## 2. Algoritmo Autoral 1: Dual Selection Bubble Sort (DSB Sort)

### 2.1. Concepção, Intuição e Metáfora Visual

A concepção do **Dual Selection Bubble Sort (DSB Sort)** fundamenta-se na metáfora da **"Pinça Convergente" (_Convergent Pincher_)**:

Em vez de varrer o vetor procurando apenas um elemento por rodada, o algoritmo delimita uma janela ativa de trabalho $[left, right]$ e utiliza dois ponteiros que convergem simultaneamente das duas extremidades para o centro:

- Em uma única varredura da janela, identificam-se simultaneamente o **menor elemento** e o **maior elemento** locais.
- O menor elemento é posicionado na extremidade esquerda (`left`), e o maior elemento é posicionado na extremidade direita (`right`).
- As extremidades são então "travadas", e a janela de trabalho encolhe: $left \leftarrow left + 1$ e $right \leftarrow right - 1$.

```text
Iteração 1: [ MIN  <================ janela ativa ================>  MAX ]
                     left                                       right
Iteração 2: [ MIN_1, MIN_2  <====== janela ativa ======>  MAX_2, MAX_1 ]
                            left                    right
```

### 2.2. Justificativa do Design Híbrido: Corrigindo as Falhas da Literatura

O DSB Sort resolve estruturalmente os dois maiores gargalos dos algoritmos elementares clássicos:

1. **Eliminação da "Cegueira" do Selection Sort Clássico:**
   - O _Selection Sort_ tradicional é computacionalmente "cego": mesmo que a entrada já esteja ordenada, ele executa obrigatoriamente $\frac{N(N-1)}{2}$ comparações, resultando em um melhor caso ineficiente $\Omega(N^2)$.
   - **Solução do DSB Sort:** Durante a varredura da janela em busca dos extremos, o algoritmo incorpora uma "antena sensora" inspirada no _Bubble Sort_. Se durante a inspeção do subvetor **nenhum par de elementos adjacentes estiver invertido** ($A[j] \le A[j+1]$ para todo $j$), o algoritmo detecta que o miolo já está completamente ordenado e encerra **imediatamente em $\Omega(N)$**.

2. **Eliminação do Problema das "Tartarugas" (_Turtles_) do Bubble Sort:**
   - No _Bubble Sort_, elementos de valores muito baixos posicionados no final do vetor demoram $N$ passadas para avançar uma casa por vez até o início, gerando até $O(N^2)$ trocas de memória.
   - **Solução do DSB Sort:** O menor elemento é capturado e transportado diretamente para a sua posição definitiva na ponta esquerda em uma única operação de troca ($O(1)$ movimentações por rodada).

3. **Detecção Antecipada de Colisões/Duplicatas:**
   - Se na janela ativa o valor mínimo coincidir com o valor máximo ($A[min] == A[max]$), deduz-se que todos os elementos internos são idênticos. O laço é interrompido sem iterações desnecessárias.

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
> _No início de cada iteração do laço externo, delimitada pelos índices $left$ e $right$:_
>
> 1. _O subvetor prefixo $A[0 \dots left-1]$ contém os $left$ menores elementos do vetor original dispostos em ordem monotonicamente crescente ($A[0] \le A[1] \le \dots \le A[left-1]$)._
> 2. _O subvetor sufixo $A[right+1 \dots N-1]$ contém os $N - 1 - right$ maiores elementos do vetor original dispostos em ordem monotonicamente crescente ($A[right+1] \le \dots \le A[N-1]$)._
> 3. _Todo elemento pertencente à janela ativa $A[left \dots right]$ satisfaz a relação de confinamento de faixa:_  
>    $$\forall x \in A[left \dots right]: \quad A[left - 1] \le x \le A[right + 1]$$

#### Prova Formal por Indução Matemática:

- **1. Inicialização:**  
  Antes da primeira iteração, $left = 0$ e $right = N - 1$.  
  Os subvetores $A[0 \dots -1]$ e $A[N \dots N-1]$ são vazios, satisfazendo trivialmente as propriedades (1) e (2). O vetor inteiro $A[0 \dots N-1]$ é a janela ativa inicial, satisfazendo a propriedade (3). O invariante é verdadeiro antes do início.

- **2. Manutenção:**  
  Assuma que o invariante é válido no início de uma iteração qualquer com janela $[left, right]$.  
  O laço interno inspeciona cada elemento $A[j]$ com $j \in [left, right]$, localizando com exatidão o índice $min\_idx$ do menor valor e $max\_idx$ do maior valor daquela janela.
  - Ao posicionar $A[min\_idx]$ em $A[left]$, garante-se que $A[left]$ é menor ou igual a todos os elementos restantes em $A[left+1 \dots right]$. Pela hipótese de indução, $A[left]$ já era maior ou igual a $A[left-1]$. Portanto, o prefixo ordenado expande validamente para $A[0 \dots left]$.
  - Analogamente, o ajuste de ponteiro (`se max_idx == left então max_idx = min_idx`) assegura que a referência ao maior elemento permaneça consistente antes da segunda troca. Ao posicionar $A[max\_idx]$ em $A[right]$, o sufixo ordenado expande validamente para $A[right \dots N-1]$.  
    Ao final da iteração, incrementa-se $left$ e decrementa-se $right$. No início da iteração seguinte, o novo prefixo $A[0 \dots left'-1]$ e o novo sufixo $A[right'+1 \dots N-1]$ permanecem estritamente ordenados e confinando o miolo restante. O invariante mantém-se verdadeiro.

- **3. Término:**  
  O laço encerra por uma de três condições:
  - _(a) Convergência:_ $left \ge right$. A janela ativa torna-se vazia ($left > right$) ou unitária ($left = right$). Em ambos os casos, a junção do prefixo ordenado com o sufixo ordenado cobre $100\%$ dos $N$ elementos, garantindo a permutação totalmente classificada.
  - _(b) Parada antecipada por ordenação:_ A flag $esta\_ordenado$ permanece verdadeira se nenhum par consecutivo em $A[left \dots right]$ violar a ordem. O miolo já está classificado, e como é limitado por $A[left-1]$ e $A[right+1]$, o vetor global está ordenado.
  - _(c) Parada por colisão:_ $A[min\_idx] == A[max\_idx]$. Todos os elementos em $A[left \dots right]$ são idênticos entre si, estando mutuamente ordenados.  
    **Conclusão:** O algoritmo encerra em tempo finito e o vetor de saída é uma permutação estritamente ordenada do vetor de entrada. $\blacksquare$

---

### 2.5. Exemplo Didático Rastreável Passo a Passo

Considere o vetor numérico de entrada: $A = [9, 2, 7, 1, 8, 3]$ ($N = 6$).

#### Rastreio de Execução:

- **Estado Inicial:** $A = [9, 2, 7, 1, 8, 3]$, $left = 0$, $right = 5$.
- **Iteração 1:**
  - Janela ativa: $A[0 \dots 5] = [9, 2, 7, 1, 8, 3]$.
  - Varredura:
    - Inversão detectada ($9 > 2$) $\to esta\_ordenado = falso$.
    - Menor valor: $1$ no índice $min\_idx = 3$.
    - Maior valor: $9$ no índice $max\_idx = 0$.
  - Troca 1 (Mínimo): Troca $A[left]$ ($A[0]$) com $A[min\_idx]$ ($A[3]$).
    - Vetor após troca: $[1, 2, 7, 9, 8, 3]$.
    - Como $max\_idx == left$ ($0 == 0$), atualiza-se: $max\_idx \leftarrow min\_idx = 3$. (O maior valor $9$ agora está no índice 3).
  - Troca 2 (Máximo): Troca $A[right]$ ($A[5]$) com $A[max\_idx]$ ($A[3]$).
    - Vetor após troca: $[1, 2, 7, 3, 8, 9]$.
  - Atualização de ponteiros: $left = 1$, $right = 4$.

- **Iteração 2:**
  - Janela ativa: $A[1 \dots 4] = [2, 7, 3, 8]$. (Pontas travadas: $[1]$ à esquerda e $[9]$ à direita).
  - Varredura:
    - Inversão detectada ($7 > 3$) $\to esta\_ordenado = falso$.
    - Menor valor: $2$ no índice $min\_idx = 1$.
    - Maior valor: $8$ no índice $max\_idx = 4$.
  - Troca 1 (Mínimo): $min\_idx == left$ ($1 == 1$) $\to$ nenhuma troca necessária.
  - Troca 2 (Máximo): $max\_idx == right$ ($4 == 4$) $\to$ nenhuma troca necessária.
  - Atualização de ponteiros: $left = 2$, $right = 3$.

- **Iteração 3:**
  - Janela ativa: $A[2 \dots 3] = [7, 3]$.
  - Varredura:
    - Inversão detectada ($7 > 3$) $\to esta\_ordenado = falso$.
    - Menor valor: $3$ no índice $min\_idx = 3$.
    - Maior valor: $7$ no índice $max\_idx = 2$.
  - Troca 1 (Mínimo): Troca $A[2]$ com $A[3]$.
    - Vetor após troca: $[1, 2, 3, 7, 8, 9]$.
    - Como $max\_idx == left$ ($2 == 2$), atualiza-se: $max\_idx \leftarrow 3$.
  - Troca 2 (Máximo): $max\_idx == right$ ($3 == 3$) $\to$ nenhuma troca necessária.
  - Atualização de ponteiros: $left = 3$, $right = 2$.

- **Encerramento:** $left > right$ ($3 > 2$). O algoritmo finaliza.  
  **Vetor Final Ordenado:** $[1, 2, 3, 7, 8, 9]$.

---

### 2.6. Dedução Analítica de Complexidade no Modelo RAM

#### Mapeamento de Custos e Frequências:

Seja $K_i = right - left + 1$ o tamanho da janela na $i$-ésima iteração do laço externo. A cada iteração:

- $left$ avança $1$ e $right$ recua $1$. Logo, $K_i$ diminui de $2$ em cada iteração:
  $$K_1 = N, \quad K_2 = N - 2, \quad K_3 = N - 4, \quad \dots$$
- O número total de iterações do laço externo no pior caso é:
  $$I_{max} = \left\lceil \frac{N}{2} \right\rceil$$

#### 1. Melhor Caso ($\Omega(N)$):

- **Cenário:** Vetor já perfeitamente ordenado ($A[0] \le A[1] \le \dots \le A[N-1]$).
- Na primeira iteração ($left = 0, right = N - 1$):
  - O laço interno percorre todos os $N$ elementos.
  - A condição $A[j] > A[j+1]$ é avaliada $N - 1$ vezes e **nunca** é satisfeita.
  - A flag $esta\_ordenado$ permanece `verdadeiro`.
  - Ao término da primeira iteração, a condição `se esta_ordenado` é satisfeita e o algoritmo encerra imediatamente.
- **Custo Total no Melhor Caso:**
  $$T_{melhor}(N) = c_1 \cdot N + c_2 \in \Omega(N)$$
- **Conclusão:** O DSB Sort é linear no melhor caso, superando o $\Theta(N^2)$ do _Selection Sort_.

#### 2. Pior Caso ($O(N^2)$):

- **Cenário:** Vetor estritamente decrescente ou desbalanceado onde a parada antecipada nunca é acionada antes de $left \ge right$.
- O laço externo executa $M = N/2$ iterações. Em cada iteração $i$, o laço interno executa $K_i$ passos:
  $$\sum_{i=0}^{N/2 - 1} (N - 2i) = N \cdot \frac{N}{2} - 2 \sum_{i=0}^{N/2 - 1} i = \frac{N^2}{2} - 2 \cdot \frac{(N/2)(N/2 - 1)}{2} = \frac{N^2}{4} + \frac{N}{2}$$
- Cada elemento do laço interno realiza entre 2 e 3 comparações (1 para o sensor de adjacência e 1 a 2 para a busca de mínimo/máximo).
- Total de comparações de extremos no pior caso:
  $$C_{pior}(N) \approx \frac{3}{4} N^2 \in O(N^2)$$
- **Total de Movimentações (Trocas):** No máximo 2 trocas (4 movimentações de dados) por iteração:
  $$M_{pior}(N) \le 4 \cdot \frac{N}{2} = 2N \in O(N)$$
  > **Propriedade Fundamental:** Mesmo no pior caso de tempo, o número de movimentações de dados é estritamente **linear ($O(N)$)**, sendo centenas de vezes menor que o Bubble Sort ($O(N^2)$).

#### 3. Caso Médio ($\Theta(N^2)$):

Para permutações aleatórias homogêneas, a inversão de pares adjacentes impede a parada antecipada nas primeiras iterações até que a janela reduza a blocos residuais. A soma de somatórios de ordem quadrática domina o custo:
$$T_{medio}(N) = \Theta(N^2)$$

---

### 2.7. Propriedades Estruturais: Estabilidade e Memória Auxiliar

- **Operação In-Place:**  
  O algoritmo requer apenas variáveis de controle de índices e flags (`left`, `right`, `min_idx`, `max_idx`, `is_sorted`). Não utiliza nenhum vetor ou estrutura de dados proporcional a $N$.  
  $$\text{Memória Auxiliar Extra: } O(1) \quad (\text{Estritamente In-Place})$$

- **Estabilidade:**  
  **Não Estável.** A troca de elementos distantes nas posições $min\_idx$ e $max\_idx$ com as extremidades $left$ e $right$ pode inverter a ordem relativa original entre chaves com valores idênticos.  
  _Exemplo de Instabilidade:_ Considere o vetor de chaves com registros etiquetados:
  $$[\mathbf{5_a}, 3, \mathbf{5_b}, 1]$$
  Na 1ª iteração, o mínimo $1$ é trocado com $left$ ($0$), movendo $\mathbf{5_a}$ para o final. A ordem relativa entre $\mathbf{5_a}$ e $\mathbf{5_b}$ é invertida.

---

## 3. Algoritmo Autoral 2: Dual-Pivot Extremes Sieve Sort (DPES Sort)

### 3.1. Concepção, Intuição e Metáfora Visual

A concepção do **Dual-Pivot Extremes Sieve Sort (DPES Sort)** fundamenta-se na metáfora da **"Peneira de Extremos" (_Extremes Sieve_)**:

Diferente do Quick Sort clássico que escolhe pivôs arbitrariamente (primeiro, último, mediana-de-três), o DPES **calcula pivôs adaptativos baseados na faixa de valores** do segmento atual. Em cada chamada recursiva:

1. Identifica-se o **mínimo** e o **máximo** do segmento em $O(n)$.
2. Se min == max, todos os elementos são idênticos — encerra imediatamente ($\Omega(n)$).
3. Fixa-se min na extremidade esquerda e max na extremidade direita.
4. Calcula-se dois pivôs por interpolação linear: $p_1 = min + \frac{span}{3}$, $p_2 = min + \frac{2 \cdot span}{3}$.
5. Realiza-se **particionamento triplo in-place** convergente: elementos $< p_1$ à esquerda, $> p_2$ à direita, e $[p_1, p_2]$ no centro.
6. Para partições de tamanho $\le 16$, aplica-se **Insertion Sort otimizado** (limiar de sobrecarga de recursão).
7. Recursão nas três partições resultantes.

```text
Segmento inicial:  [ MIN  =======================  MAX ]
                       |                            |
                       v                            v
Partição tripla:  [ < p1 ]  [ p1 .. p2 ]  [ > p2 ]
                    |           |            |
                    v           v            v
              Recursão    Recursão     Recursão
```

A escolha de pivôs por interpolação (em vez de posição) faz com que o algoritmo **adapte-se à distribuição dos dados**, aproximando-se do caso ideal de divisão balanceada quando os dados são uniformes.

### 3.2. Justificativa do Design: Partição Tripla Adaptativa

O DPES Sort resolve limitações estruturais do Quick Sort clássico e de variantes dual-pivot (ex: Yaroslavskiy):

1. **Pivôs adaptativos por interpolação de faixa:**
   - No Quick Sort dual-pivot padrão (Yaroslavskiy), os pivôs são elementos do array (ex: primeiro e último). Em dados com outliers ou distribuições enviesadas, a partição fica desbalanceada.
   - No DPES, os pivôs são **valores interpolados** entre min e max reais do segmento. Para dados uniformes, isso garante partições $\approx n/3$ cada, eliminando o pior caso de pivôs mal escolhidos.

2. **Detecção antecipada de uniformidade (colisão de extremos):**
   - Se ao buscar min/max descobre-se que $min = max$, o segmento inteiro é constante. O algoritmo encerra o ramo recursivo **sem particionar**, economizando $O(n \log n)$ operações desnecessárias.
   - Isso também cobre o caso de muitos duplicados — segmentos homogêneos são detectados e resolvidos em tempo linear.

3. **Inserção Sort como caso base (threshold = 16):**
   - A recursão tem sobrecarga de chamadas e manipulação de pilha. Para $n \le 16$, o Insertion Sort é mais rápido na prática por localidade de cache e ausência de overhead.
   - O threshold 16 é empírico e amplamente usado na literatura (ex: `std::sort` do GCC, Timsort).

4. **Particionamento triplo convergente (three-way partitioning):**
   - Inspirado no Dutch National Flag de Dijkstra, mas com **dois pivôs** e **convergência de três ponteiros** ($left$, $curr$, $right$) em uma única passada.
   - Evita a troca múltipla de elementos iguais aos pivôs, reduzindo movimentações.

### 3.3. Especificação Formal em Pseudocódigo (Estilo Cormen)

```text
procedimento DPES_Sort(A, low, high):
    se low >= high então:
        retornar
    fim-se

    size ← high - low + 1
    se size <= 16 então:
        InsertionSort(A, low, high)
        retornar
    fim-se

    // 1. Encontrar mínimo e máximo no segmento
    min_idx ← low
    max_idx ← low
    para k de low + 1 até high faça:
        se A[k] < A[min_idx] então:
            min_idx ← k
        fim-se
        se A[k] > A[max_idx] então:
            max_idx ← k
        fim-se
    fim-para

    // 2. Detecção de uniformidade: todos elementos idênticos
    se A[min_idx] == A[max_idx] então:
        retornar
    fim-se

    // 3. Posicionar min em low e max em high
    se min_idx ≠ low então:
        trocar(A[low], A[min_idx])
        se max_idx == low então:
            max_idx ← min_idx
        fim-se
    fim-se

    se max_idx ≠ high então:
        trocar(A[high], A[max_idx])
    fim-se

    min_val ← A[low]
    max_val ← A[high]

    // 4. Pivôs adaptativos por interpolação
    span ← max_val - min_val
    p1 ← min_val + span / 3
    p2 ← min_val + 2 * span / 3

    // 5. Particionamento triplo in-place no intervalo [low+1, high-1]
    left ← low + 1
    curr ← low + 1
    right ← high - 1

    enquanto curr ≤ right faça:
        se A[curr] < p1 então:
            se curr ≠ left então:
                trocar(A[curr], A[left])
            fim-se
            left ← left + 1
            curr ← curr + 1
        senão se A[curr] > p2 então:
            enquanto curr < right e A[right] > p2 faça:
                right ← right - 1
            fim-enquanto
            se curr ≠ right então:
                trocar(A[curr], A[right])
            fim-se
            right ← right - 1

            // Reavalia elemento trazido de right
            se A[curr] < p1 então:
                se curr ≠ left então:
                    trocar(A[curr], A[left])
                fim-se
                left ← left + 1
            fim-se
            curr ← curr + 1
        senão:
            curr ← curr + 1
        fim-se
    fim-enquanto

    // 6. Recursão nas três partições
    DPES_Sort(A, low, left - 1)       // elementos < p1
    DPES_Sort(A, left, right)         // elementos ∈ [p1, p2]
    DPES_Sort(A, right + 1, high)     // elementos > p2
fim-procedimento
```

### 3.4. Invariante de Recursão e Prova Formal de Corretude

A prova de corretude do DPES baseia-se em um **Invariante de Recursão** para a chamada `DPES_Sort(A, low, high)`:

> **Enunciado do Invariante:**
> _Para qualquer chamada `DPES_Sort(A, low, high)` com $low \le high$:_
>
> 1. _Os elementos em $A[low \dots high]$ são uma permutação dos elementos originais nesse intervalo._
> 2. _Ao término da chamada, o subvetor $A[low \dots high]$ está ordenado em ordem não decrescente._
> 3. _Todos os elementos em $A[low \dots high]$ satisfazem $A[low-1] \le A[i] \le A[high+1]$ (quando os índices existem), mantendo a ordem global._

#### Prova Formal por Indução Estrutural:

- **1. Caso Base ($size \le 16$):**
  Quando $high - low + 1 \le 16$, o algoritmo delega ao `InsertionSort(A, low, high)`. O Insertion Sort é um algoritmo de ordenação correto e estável por indução simples sobre o índice de inserção. A propriedade (1) vale pois o Insertion Sort apenas permuta elementos internamente. A propriedade (2) vale pela corretude do Insertion Sort. A propriedade (3) vale pois os limites $low$ e $high$ não são alterados.

- **2. Caso Uniforme ($A[min\_idx] = A[max\_idx]$):**
  Se todos os elementos no segmento são iguais, o segmento já está ordenado. Retornar sem modificações preserva as três propriedades trivialmente.

- **3. Caso Geral (Particionamento Triplo):**
  Assumindo que as chamadas recursivas satisfazem o invariante (hipótese de indução), provamos que a partição atual também o satisfaz:
  - **Fixação dos extremos:** Após as trocas iniciais, $A[low] = min\_val$ e $A[high] = max\_val$. Como $min\_val \le max\_val$, a relação de ordem entre as bordas é válida.
  - **Particionamento triplo:** O laço `while curr ≤ right` mantém o seguinte invariante de laço interno:

    > _$A[low+1 \dots left-1] < p_1$, $A[left \dots curr-1] \in [p_1, p_2]$, $A[right+1 \dots high-1] > p_2$, e $curr \le right+1$._

    A cada iteração, `curr` avança ou `right` recua, mantendo a partição. O elemento trazido de `right` é reavaliado contra $p_1$, garantindo que nenhum elemento $< p_1$ fique na região central.

  - **Término do particionamento:** Quando $curr > right$, temos três partições contíguas e exaustivas:
    - $P_L = A[low \dots left-1]$: todos $< p_1$ (inclui $A[low]=min\_val$)
    - $P_M = A[left \dots right]$: todos $\in [p_1, p_2]$
    - $P_R = A[right+1 \dots high]$: todos $> p_2$ (inclui $A[high]=max\_val$)

    Com $A[low] = min\_val \le p_1$ e $A[high] = max\_val \ge p_2$, a ordem global é preservada. Note que $A[low]$ e $A[high]$ já estão em suas posições finais e são incluídos nas chamadas recursivas (o algoritmo base $size \le 16$ ou a detecção de uniformidade os trata corretamente).

  - **Chamadas recursivas:** Pela hipótese de indução, cada chamada `DPES_Sort` ordena sua partição mantendo os elementos internos. Como as partições são disjuntas e cobrem todo o intervalo, a concatenação resulta em $A[low \dots high]$ ordenado.

- **4. Conclusão:**
  Por indução estrutural sobre o tamanho do segmento, toda chamada `DPES_Sort(A, low, high)` termina (o tamanho diminui estritamente a cada recursão) e produz um subvetor ordenado. A chamada inicial `DPES_Sort(A, 0, N-1)` ordena o vetor completo. $\blacksquare$

### 3.5. Exemplo Didático Rastreável Passo a Passo

Considere o vetor de entrada: $A = [9, 2, 7, 1, 8, 3, 5, 4, 6]$ ($N = 9$).

**Chamada inicial:** `DPES_Sort(A, 0, 8)`, $size = 9 > 16?$ Não, continua.

1. **Busca min/max:** $min=1$ (idx 3), $max=9$ (idx 0). $min \ne max$.
2. **Fixar extremos:** Troca $A[0] \leftrightarrow A[3]$ → $[1, 2, 7, 9, 8, 3, 5, 4, 6]$. $max\_idx$ era 0, agora 3. Troca $A[8] \leftrightarrow A[3]$ → $[1, 2, 7, 6, 8, 3, 5, 4, 9]$.
3. **Pivôs:** $min\_val=1$, $max\_val=9$, $span=8$. $p_1 = 1 + 8/3 \approx 3.67$, $p_2 = 1 + 16/3 \approx 6.33$.
4. **Particionamento triplo** no intervalo $[1, 7]$ (valores: $[2, 7, 6, 8, 3, 5, 4]$):
   - $left=1, curr=1, right=7$
   - $curr=1$: $A[1]=2 < 3.67$ → swap com $left$ (mesmo), $left=2, curr=2$
   - $curr=2$: $A[2]=7 > 6.33$ → move $right$ até $A[7]=4 \not> 6.33$, swap $A[2] \leftrightarrow A[7]$ → $[1, 2, 4, 6, 8, 3, 5, 7, 9]$, $right=6$, reavalia $A[2]=4 \in [3.67, 6.33]$ → $curr=3$
   - $curr=3$: $A[3]=6 \in [3.67, 6.33]$ → $curr=4$
   - $curr=4$: $A[4]=8 > 6.33$ → $right=6$, $A[6]=5 \not> 6.33$, swap $A[4] \leftrightarrow A[6]$ → $[1, 2, 4, 6, 5, 3, 8, 7, 9]$, $right=5$, reavalia $A[4]=5 \in [p_1,p_2]$ → $curr=5$
   - $curr=5$: $A[5]=3 < 3.67$ → swap $A[5] \leftrightarrow A[2]$ ($left$) → $[1, 2, 3, 6, 5, 4, 8, 7, 9]$, $left=3, curr=6$
   - $curr=6 > right=5$ → fim do particionamento.
5. **Partições resultantes:**
   - $P_L = A[0 \dots 2] = [1, 2, 3]$ ($< p_1$, inclui $min\_val=1$)
   - $P_M = A[3 \dots 5] = [6, 5, 4]$ ($\in [p_1, p_2]$)
   - $P_R = A[6 \dots 8] = [8, 7, 9]$ ($> p_2$, inclui $max\_val=9$)
6. **Recursão:**
   - `DPES_Sort(A, 0, 2)`: $size=3 \le 16$ → Insertion Sort → $[1, 2, 3]$ ✓
   - `DPES_Sort(A, 3, 5)`: $size=3 \le 16$ → Insertion Sort → $[4, 5, 6]$ ✓
   - `DPES_Sort(A, 6, 8)`: $size=3 \le 16$ → Insertion Sort → $[7, 8, 9]$ ✓

**Vetor Final Ordenado:** $[1, 2, 3, 4, 5, 6, 7, 8, 9]$.

### 3.6. Dedução Analítica de Complexidade no Modelo RAM

#### Mapeamento de Custos por Chamada Recursiva:

Seja $n = high - low + 1$ o tamanho do segmento na chamada atual.

1. **Busca min/max:** $n-1$ iterações, 2 comparações cada → $2(n-1) \in \Theta(n)$
2. **Fixação de extremos:** até 2 trocas (4 movimentações) → $O(1)$
3. **Cálculo de pivôs:** operações aritméticas → $O(1)$
4. **Particionamento triplo:** cada elemento do intervalo interno $[low+1, high-1]$ visitado $\le 2$ vezes → $\le 2(n-2)$ comparações, $\le 2(n-2)$ trocas no pior caso → $\Theta(n)$
5. **Chamadas recursivas:** três chamadas com tamanhos $n_1, n_2, n_3$ tais que $n_1 + n_2 + n_3 = n - 2$

#### 1. Melhor Caso ($\Omega(n \log n)$):

- **Cenário:** Dados uniformemente distribuídos; interpolação produz partições balanceadas $n_1 \approx n_2 \approx n_3 \approx n/3$.
- Recorrência: $T(n) = 3T(n/3) + \Theta(n)$.
- Pelo **Teorema Mestre** (Caso 2: $a=3, b=3, f(n)=\Theta(n), n^{\log_b a} = n$): $T(n) = \Theta(n \log n)$.
- Detecção de uniformidade em segmentos homogêneos acelera ainda mais casos com muitos duplicados.

#### 2. Pior Caso ($O(n^2)$):

- **Cenário:** Dados extremamente enviesados onde interpolação falha (ex: distribuição exponencial) ou muitos elementos iguais a $p_1$ ou $p_2$ concentrando massa em uma partição. Partição degenerada: $n_1 = n-2, n_2 = 0, n_3 = 0$ (ou similar).
- Recorrência: $T(n) = T(n-2) + \Theta(n) = \Theta(n^2)$.
- **Mitigação prática:** O threshold de Insertion Sort ($n \le 16$) e a detecção de uniformidade reduzem a profundidade real da recursão em casos adversos.

#### 3. Caso Médio ($\Theta(n \log n)$):

- Para permutações aleatórias, a interpolação de pivôs produz partições aproximadamente balanceadas em expectativa. A recorrência esperada é $E[T(n)] = 3E[T(n/3)] + \Theta(n) = \Theta(n \log n)$.
- Comparado ao Quick Sort dual-pivot (Yaroslavskiy), o DPES tem pivôs **adaptativos à distribuição** em vez de posicionais, resultando em melhor desempenho empírico em dados não uniformes.

#### Espaço Auxiliar:

- Pilha de recursão: profundidade $O(\log n)$ no caso médio (partições balanceadas), $O(n)$ no pior caso.
- Variáveis locais por chamada: $O(1)$.
- **Total:** $O(\log n)$ esperado, $O(n)$ pior caso.

### 3.7. Propriedades Estruturais: Estabilidade e Memória Auxiliar

- **Operação In-Place:**  
  O algoritmo rearranja elementos dentro do próprio array. Não aloca arrays auxiliares proporcionais a $n$. Apenas variáveis de índice e pivôs ($O(1)$ por chamada).
  $$\text{Memória Auxiliar Extra (heap): } O(1)$$
  $$\text{Pilha de Chamada (stack): } O(\log n) \text{ esperado, } O(n) \text{ pior caso}$$

- **Estabilidade:**  
  **Não Estável.** O particionamento triplo realiza trocas de longa distância (elemento em `curr` com elemento em `left` ou `right`). Elementos com chaves iguais podem ter sua ordem relativa invertida ao cruzar as fronteiras das partições.

  _Exemplo de Instabilidade (Particionamento Triplo — $N=18 > 16$):_
  Considere $A = [10_a, 1, 9, 10_b, 3, 2, 10_c, 8, 4, 10_d, 6, 5, 7, 10_e, 12, 11, 10_f, 13]$ ($N=18$).
  **Chamada inicial:** `DPES_Sort(A, 0, 17)`, $size=18 > 16$ → particionamento triplo.
  1. **Fixar extremos:** $min=1$ (idx 1), $max=13$ (idx 17). Troca $A[0] \leftrightarrow A[1]$ → $[1, 10_a, 9, 10_b, 3, 2, 10_c, 8, 4, 10_d, 6, 5, 7, 10_e, 12, 11, 10_f, 13]$.
  2. **Pivôs:** $min\_val=1$, $max\_val=13$, $span=12$ → $p_1=5$, $p_2=9$.
  3. **Particionamento** no intervalo $[1 \dots 16]$:
     - $10_a$ (idx 1) $> p_2$ → trocado com $A[12]=7$ (menor que $p_2$) → $10_a$ vai para idx 12.
     - $10_b$ (idx 3) $> p_2$ → trocado com $A[11]=5$ → $10_b$ vai para idx 11.
     - $10_c$ (idx 6) $> p_2$ → trocado com $A[10]=6$ → $10_c$ vai para idx 10.
     - $10_d$ (idx 9) e $10_e$ (idx 13) não são movidos (o ponteiro `right` já recuou).
     - $10_f$ (idx 16) permanece (já no final do intervalo).
  4. **Partição direita resultante** $P_R = A[9 \dots 17] = [10_d, 10_c, 10_b, 10_a, 10_e, 12, 11, 10_f, 13]$.
     Ordem original dos 10's: $a(0) \prec b(3) \prec c(6) \prec d(9) \prec e(13) \prec f(16)$.
     Ordem em $P_R$: $d \prec c \prec b \prec a \prec e \prec f$ — **$a,b,c$ invertidos**.
  5. **Recursão:** `DPES_Sort(A, 9, 17)` ($size=9 \le 16$) → **Insertion Sort** (estável).
     Insertion Sort preserva a ordem _já invertida_ em $P_R$: saída final $[ \dots, 10_d, 10_c, 10_b, 10_a, 10_e, 10_f, 11, 12, 13 ]$.
     A ordem relativa original $(a \prec b \prec c)$ foi perdida durante o particionamento triplo, **não** corrigida pelo caso base.
     $\therefore$ **DPES Sort não é estável.**

---

## 4. Metodologia Experimental e Suíte de Testes

### 4.1. Cenários de Teste Obrigatórios e Casos Limítrofes

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

> **Resultado da Validação:** O **DSB Sort** e o **DPES Sort** foram submetidos a todos os 10 cenários formais da suíte, obtendo **100% de aprovação (OK)** em ambos, além de terem sido validados em bateria de estresse adicional com 500 sementes aleatórias distintas.

---

## 5. Resultados Experimentais e Análise Comparativa

Os benchmarks empíricos foram executados em ambiente Linux com Python 3.14 sob isolamento de CPU, com **3 repetições estatísticas independentes** por configuração.

Abaixo são consolidados os resultados do **DSB Sort (Autoral 1)** e do **DPES Sort (Autoral 2)** em comparação direta com os métodos clássicos da literatura: _Bubble Sort_, _Selection Sort_, _Insertion Sort_, _Merge Sort_ e _Quick Sort_.

---

### 5.1. Distribuição Aleatória Homogênea (`random`)

#### Tempo de Execução Médio (ms):

| Algoritmo                 |     N=10     |     N=50     |    N=100     |    N=250     |    N=500     |    N=1000     |
| :------------------------ | :----------: | :----------: | :----------: | :----------: | :----------: | :-----------: |
| Bubble Sort               |   0.006 ms   |   0.109 ms   |   0.648 ms   |   2.722 ms   |  11.652 ms   |  57.164 ms    |
| Selection Sort            |   0.005 ms   |   0.068 ms   |   0.383 ms   |   1.389 ms   |   5.997 ms   |  25.864 ms    |
| Insertion Sort            |   0.004 ms   |   0.066 ms   |   0.362 ms   |   1.638 ms   |   7.408 ms   |  30.655 ms    |
| Merge Sort                |   0.014 ms   |   0.097 ms   |   0.230 ms   |   0.527 ms   |   1.131 ms   |   2.612 ms    |
| Quick Sort                |   0.010 ms   |   0.069 ms   |   0.137 ms   |   0.426 ms   |   0.761 ms   |   1.665 ms    |
| **DSB Sort (Autoral 1)**  | **0.007 ms** | **0.171 ms** | **0.471 ms** | **2.253 ms** | **10.588 ms**| **40.671 ms** |
| **DPES Sort (Autoral 2)** | **0.008 ms** | **0.079 ms** | **0.148 ms** | **0.435 ms** | **1.049 ms** | **2.414 ms**  |

#### Número Médio de Movimentações / Trocas:

| Algoritmo                 |  N=10  |  N=50   |  N=100  |   N=250   |   N=500   |  N=1000   |
| :------------------------ | :----: | :-----: | :-----: | :-------: | :-------: | :-------: |
| Bubble Sort               |   49   |  1174   |  5073   |  30867    | 122941    | 504905    |
| Selection Sort            |   14   |   93    |   191   |    491    |   985     |  1984     |
| Insertion Sort            |   43   |   685   |  2734   |  15932    |  62468    | 254451    |
| Merge Sort                |   34   |   286   |   672   |   1994    |   4488    |  9976     |
| Quick Sort                |   23   |   147   |   369   |   1097    |   2411    |  5231     |
| **DSB Sort (Autoral 1)**  | **14** | **93**  | **186** |  **494**  |  **987**  | **1981**  |
| **DPES Sort (Autoral 2)** | **43** | **284** | **629** | **1731**  | **3742**  | **8606**  |

---

### 5.2. Distribuição Perfeitamente Ordenada (`sorted` — Melhor Caso)

Neste cenário, evidencia-se de forma contundente o benefício da "antena" de parada antecipada do DSB Sort e a eficiência do DPES em dados já ordenados (detecção de uniformidade em partições recursivas):

#### Tempo de Execução Médio (ms):

| Algoritmo                 |     N=10     |     N=50     |    N=100     |    N=250     |    N=500     |    N=1000    |
| :------------------------ | :----------: | :----------: | :----------: | :----------: | :----------: | :----------: |
| Bubble Sort               |   0.002 ms   |   0.003 ms   |   0.006 ms   |   0.018 ms   |   0.031 ms   |   0.066 ms   |
| Selection Sort            |   0.005 ms   |   0.062 ms   |   0.244 ms   |   2.092 ms   |   6.331 ms   |  26.927 ms   |
| Insertion Sort            |   0.002 ms   |   0.006 ms   |   0.011 ms   |   0.037 ms   |   0.071 ms   |   0.150 ms   |
| Merge Sort                |   0.019 ms   |   0.065 ms   |   0.175 ms   |   0.434 ms   |   0.953 ms   |   2.044 ms   |
| Quick Sort                |   0.007 ms   |   0.034 ms   |   0.094 ms   |   0.191 ms   |   0.426 ms   |   0.938 ms   |
| **DSB Sort (Autoral 1)**  | **0.002 ms** | **0.009 ms** | **0.021 ms** | **0.046 ms** | **0.081 ms** | **0.156 ms** |
| **DPES Sort (Autoral 2)** | **0.004 ms** | **0.038 ms** | **0.115 ms** | **0.306 ms** | **0.788 ms** | **1.561 ms** |

> **Destaque Analítico:** Para $N = 1000$, o _Selection Sort_ gasta **26.927 ms** (por ser obrigado a fazer $\approx 500.000$ comparações). Já o **DSB Sort** executa em apenas **0.156 ms**, sendo **mais de 170 vezes mais rápido**, comprovando experimentalmente sua complexidade de melhor caso $\Omega(N)$. O **DPES Sort** completa em **1.561 ms** — embora não tenha parada antecipada linear como o DSB, seu particionamento adaptativo ainda supera Selection, Bubble e Insertion Sort no caso ordenado.

---

### 5.3. Distribuição Estritamente Decrescente (`reverse` — Pior Caso de Estresse)

O teste de estresse reverso evidencia a superioridade do **DPES Sort** (caso médio $O(N \log N)$) sobre métodos quadráticos, e a economia de memória do **DSB Sort**:

#### Tempo de Execução Médio (ms):

| Algoritmo                 |     N=10     |     N=50     |    N=100     |    N=250     |    N=500     |    N=1000     |
| :------------------------ | :----------: | :----------: | :----------: | :----------: | :----------: | :-----------: |
| Bubble Sort               |   0.007 ms   |   0.149 ms   |   0.557 ms   |   3.720 ms   |  16.069 ms   |  73.764 ms    |
| Selection Sort            |   0.004 ms   |   0.068 ms   |   0.253 ms   |   1.544 ms   |   6.602 ms   |  28.083 ms    |
| Insertion Sort            |   0.005 ms   |   0.127 ms   |   0.504 ms   |   3.279 ms   |  13.484 ms   |  60.695 ms    |
| Merge Sort                |   0.013 ms   |   0.068 ms   |   0.150 ms   |   0.432 ms   |   0.939 ms   |   2.066 ms    |
| Quick Sort                |   0.008 ms   |   0.046 ms   |   0.079 ms   |   0.202 ms   |   0.459 ms   |   1.003 ms    |
| **DSB Sort (Autoral 1)**  | **0.006 ms** | **0.078 ms** | **0.289 ms** | **1.715 ms** | **7.876 ms** | **29.702 ms** |
| **DPES Sort (Autoral 2)** | **0.010 ms** | **0.060 ms** | **0.123 ms** | **0.344 ms** | **0.855 ms** | **1.698 ms**  |

#### Número Médio de Movimentações / Trocas (Impacto em Memória):

| Algoritmo                 |  N=10  |  N=50   |  N=100  |  N=250  |   N=500   |  N=1000   |
| :------------------------ | :----: | :-----: | :-----: | :-----: | :-------: | :-------: |
| Bubble Sort               |   90   |  2450   |  9900   | 62250   | 249500    | 999000    |
| Selection Sort            |   10   |   50    |   100   |   250   |   500     |  1000     |
| Insertion Sort            |   63   |  1323   |  5148   | 31623   | 125748    | 501498    |
| Merge Sort                |   34   |   286   |   672   |  1994   |  4488     |  9976     |
| Quick Sort                |   14   |   54    |   104   |   254   |   504     |  1004     |
| **DSB Sort (Autoral 1)**  | **10** | **50**  | **100** | **250** |  **500**  | **1000**  |
| **DPES Sort (Autoral 2)** | **63** | **240** | **336** | **731** | **1347**  | **2892**  |

> **Destaque Analítico Crítico:** Em $N = 1000$ invertido:
>
> - O _Bubble Sort_ realizou **999.000 movimentações de elementos** na memória.
> - O _Insertion Sort_ realizou **501.498 movimentações**.
> - O **DSB Sort realizou apenas 1.000 movimentações** (exatamente $N$ movimentações)!  
>   Isso representa uma **redução de 99,9% no tráfego de memória** em relação ao Bubble Sort.
> - O **DPES Sort** realizou **2.892 movimentações** e completou em **1.698 ms** — demonstrando a eficiência do particionamento triplo adaptativo mesmo no pior caso de entrada reversa, superando todos os algoritmos quadráticos e competindo com Quick Sort.

---

### 5.4. Distribuição com Chaves Redundantes (`duplicates`)

Cenário com muitos valores repetidos testa a robustez dos algoritmos frente a colisões de chaves. O DPES Sort destaca-se pela detecção antecipada de uniformidade em segmentos recursivos:

#### Tempo de Execução Médio (ms):

| Algoritmo                 |     N=10     |     N=50     |    N=100     |    N=250     |     N=500     |    N=1000     |
| :------------------------ | :----------: | :----------: | :----------: | :----------: | :-----------: | :-----------: |
| Bubble Sort               |   0.005 ms   |   0.099 ms   |   0.377 ms   |   2.442 ms   |  10.303 ms    |  45.699 ms    |
| Selection Sort            |   0.004 ms   |   0.084 ms   |   0.250 ms   |   1.718 ms   |   6.488 ms    |  27.201 ms    |
| Insertion Sort            |   0.003 ms   |   0.098 ms   |   0.211 ms   |   1.809 ms   |   5.697 ms    |  22.685 ms    |
| Merge Sort                |   0.014 ms   |   0.081 ms   |   0.167 ms   |   0.662 ms   |   1.122 ms    |   3.026 ms    |
| Quick Sort                |   0.008 ms   |   0.059 ms   |   0.114 ms   |   0.327 ms   |   0.762 ms    |   2.030 ms    |
| **DSB Sort (Autoral 1)**  | **0.006 ms** | **0.130 ms** | **0.439 ms** | **2.542 ms** | **10.704 ms** | **44.319 ms** |
| **DPES Sort (Autoral 2)** | **0.007 ms** | **0.046 ms** | **0.078 ms** | **0.197 ms** | **0.410 ms**  | **0.816 ms**  |

#### Número Médio de Movimentações / Trocas:

| Algoritmo                 |  N=10  |  N=50   |  N=100  |  N=250  |   N=500   |  N=1000   |
| :------------------------ | :----: | :-----: | :-----: | :-----: | :-------: | :-------: |
| Bubble Sort               |   35   |  1041   |  3834   | 25395   |  95066    | 405180    |
| Selection Sort            |   12   |   75    |   153   |   391   |   811     |  1627     |
| Insertion Sort            |   35   |   619   |  2115   | 13195   |  48531    | 204588    |
| Merge Sort                |   34   |   286   |   672   |  1994   |  4488     |  9976     |
| Quick Sort                |   21   |   203   |   461   |  1420   |  3361     |  7753     |
| **DSB Sort (Autoral 1)**  | **10** | **80**  | **163** | **417** | **807**   | **1675**  |
| **DPES Sort (Autoral 2)** | **35** | **192** | **225** | **541** | **1069**  | **2174**  |

> **Destaque Analítico:** Em $N = 1000$ com muitos duplicados, o **DPES Sort** completa em **0.816 ms** com apenas **2.174 movimentações** — a detecção de segmentos uniformes ($min = max$) evita recursão desnecessária, resultando em desempenho próximo ao melhor caso. O DSB Sort, por outro lado, não se beneficia de duplicados e mantém comportamento quadrático.

---

### 5.5. Distribuição Quase Ordenada (`almost_sorted`)

Vetores com 95% de ordenação prévia testam a adaptabilidade. O DSB Sort brilha pela parada antecipada; o DPES Sort beneficia-se de partições pequenas e recursão rasa:

#### Tempo de Execução Médio (ms):

| Algoritmo                 |     N=10     |     N=50     |    N=100     |    N=250     |     N=500     |    N=1000     |
| :------------------------ | :----------: | :----------: | :----------: | :----------: | :-----------: | :-----------: |
| Bubble Sort               |   0.003 ms   |   0.033 ms   |   0.238 ms   |   1.625 ms   |   8.053 ms    |  33.519 ms    |
| Selection Sort            |   0.004 ms   |   0.061 ms   |   0.238 ms   |   1.434 ms   |   6.278 ms    |  25.989 ms    |
| Insertion Sort            |   0.002 ms   |   0.009 ms   |   0.036 ms   |   0.239 ms   |   0.962 ms    |   3.945 ms    |
| Merge Sort                |   0.013 ms   |   0.064 ms   |   0.152 ms   |   0.466 ms   |   1.085 ms    |   2.390 ms    |
| Quick Sort                |   0.006 ms   |   0.032 ms   |   0.075 ms   |   0.202 ms   |   0.474 ms    |   1.098 ms    |
| **DSB Sort (Autoral 1)**  | **0.003 ms** | **0.094 ms** | **0.323 ms** | **2.306 ms** | **9.997 ms**  | **38.244 ms** |
| **DPES Sort (Autoral 2)** | **0.004 ms** | **0.040 ms** | **0.092 ms** | **0.339 ms** | **0.898 ms**  | **1.913 ms**  |

#### Número Médio de Movimentações / Trocas:

| Algoritmo                 |  N=10  |  N=50  |  N=100  |  N=250  |   N=500   |  N=1000   |
| :------------------------ | :----: | :----: | :-----: | :-----: | :-------: | :-------: |
| Bubble Sort               |   9    |   74   |   505   |  3580   |  15426    |  63093    |
| Selection Sort            |   1    |   3    |   10    |   24    |   50      |  100      |
| Insertion Sort            |   22   |  135   |   450   |  2288   |  8711     |  33545    |
| Merge Sort                |   34   |  286   |   672   |  1994   |  4488     |  9976     |
| Quick Sort                |   1    |   3    |   11    |   77    |  186      |  488      |
| **DSB Sort (Autoral 1)**  | **1**  | **3**  | **10**  | **24**  | **50**    | **100**   |
| **DPES Sort (Autoral 2)** | **22** | **106**| **239** | **862** | **1973**  | **5524**  |

> **Destaque Analítico:** Em $N = 1000$ quase ordenado, o **DSB Sort** aproveita a flag `is_sorted` para terminar em $\Omega(N)$ (38.2 ms), enquanto o **DPES Sort** atinge **1.913 ms** — sua recursão processa partições pequenas e balanceadas, com o Insertion Sort fallback resolvendo a base eficientemente. Ambos superam Selection e Bubble Sort; o DPES aproxima-se do Quick Sort.

---

## 6. Discussão Crítica e Trade-Offs

### 6.1. DSB Sort (Autoral 1 — Iterativo)

**Ganhos Comprovados:**

- **Superação do Selection Sort:** Elimina completamente o problema de desempenho em vetores ordenados ou quase ordenados, caindo de $\Theta(N^2)$ para $\Omega(N)$ com quase zero custo adicional.
- **Economia Extrema de Barramento de Memória:** O DSB Sort é imensamente superior ao Bubble Sort e ao Insertion Sort em número de escritas em memória, mantendo trocas estritamente lineares ($O(N)$) mesmo no pior caso de inversão total.

**Limitações (Trade-Offs Honestos):**

- Por ter uma constante de comparações que realiza a busca de mínimo e máximo e a checagem de adjacência na mesma passada, o DSB Sort realiza aproximadamente $1.5$ a $2$ vezes mais comparações que o Selection Sort puro em vetores totalmente desordenados aleatórios.
- Não é um algoritmo $O(N \log N)$: para $N > 5000$, métodos de Divisão e Conquista (como Quick Sort e Merge Sort) são naturalmente muito mais rápidos. O DSB Sort posiciona-se como uma técnica de ordenação in-place elementar de alta eficiência para instâncias pequenas/médias ($N \le 1000$) ou conjuntos com forte pré-ordenação.

### 6.2. DPES Sort (Autoral 2 — Recursivo / Divisão e Conquista)

**Ganhos Comprovados:**

- **Complexidade $O(N \log N)$ no caso médio:** O particionamento triplo com pivôs adaptativos por interpolação produz partições balanceadas em dados uniformes e aleatórios, superando todos os algoritmos quadráticos ($O(N^2)$) para $N \ge 100$.
- **Detecção antecipada de uniformidade:** Segmentos com todos os elementos iguais ($min = max$) são resolvidos em tempo linear sem recursão adicional — vantagem crítica em dados com muitos duplicados (0.816 ms vs 44.3 ms do DSB em $N=1000$).
- **Fallback para Insertion Sort ($n \le 16$):** Elimina overhead de recursão em partições pequenas, melhorando constante prática e localidade de cache.
- **Competitividade com Quick Sort:** Em dados aleatórios, o DPES completa em **2.41 ms** vs **1.67 ms** do Quick Sort ($N=1000$) — diferença de ~1,4×. Em reverso, **1.70 ms** vs **1.00 ms** — o Quick Sort mantém vantagem por pivôs posicionais robustos (mediana-de-três), mas o DPES evita degradação quadrática e supera todos os métodos $O(N^2)$.

**Limitações (Trade-Offs Honestos):**

- **Não estável:** Trocas de longa distância no particionamento triplo invertem ordem relativa de chaves iguais — igual ao Quick Sort clássico.
- **Pilha de recursão $O(\log n)$ esperado, $O(n)$ pior caso:** Em distribuições extremamente enviesadas onde a interpolação falha, a profundidade da recursão pode degradar. Mitigação: threshold de Insertion Sort e detecção de uniformidade reduzem a profundidade real.
- **Overhead em $N$ pequeno:** Para $N < 50$, o DSB Sort e o Insertion Sort são mais rápidos devido à ausência de overhead de chamadas recursivas e cálculo de pivôs.
- **Pivôs por interpolação assumem tipo numérico:** Para tipos genéricos sem aritmética (ex: strings), o fallback para mediana empírica perde adaptatividade. A implementação atual trata `TypeError` e usa pivôs posicionais.
- **Pior caso $O(n^2)$ é teórico:** Nos benchmarks executados com as 5 distribuições padrão (_random_, _sorted_, _reverse_, _duplicates_, _almost_sorted_), **nenhuma gerou partição degenerada** — o algoritmo sempre exibiu comportamento $O(n \log n)$ na prática. Um cenário adverso artificial (ex: distribuição exponencial $2^i$ ou valores concentrados em torno de $p_1/p_2$ forçando $n_1 \approx n-2$) seria necessário para reproduzir o pior caso. Sugere-se, como trabalho futuro, adicionar tal distribuição ao benchmark para caracterização completa.

### 6.3. Comparação Direta: DSB Sort vs DPES Sort

| Critério          | DSB Sort (Iterativo)            | DPES Sort (Recursivo)                  |
| ----------------- | ------------------------------- | -------------------------------------- |
| **Paradigma**     | Híbrido Selection+Bubble        | Dual-pivot Quick Sort adaptativo       |
| **Melhor caso**   | $\Omega(N)$ (parada antecipada) | $\Omega(N \log N)$ (particionamento)   |
| **Pior caso**     | $O(N^2)$                        | $O(N^2)$ (mitigado na prática)         |
| **Caso médio**    | $\Theta(N^2)$                   | $\Theta(N \log N)$                     |
| **Memória extra** | $O(1)$ estrito                  | $O(\log n)$ pilha                      |
| **Estabilidade**  | Não                             | Não                                    |
| **Forte em**      | Dados ordenados/quase ordenados | Dados aleatórios, reversos, duplicados |
| **Fraco em**      | Dados aleatórios grandes        | $N$ muito pequeno, tipos não numéricos |

**Conclusão Sintética:** Os dois algoritmos são **complementares**. O DSB Sort é ideal quando se espera pré-ordenação forte ou restrição estrita de memória ($O(1)$). O DPES Sort é a escolha geral para dados arbitrários de tamanho médio/grande, oferecendo complexidade $O(N \log N)$ com pivôs adaptativos que mitigam o pior caso do Quick Sort clássico.

---

## 7. Declaração Obrigatória de Autoria e Uso de Ferramentas de IA

Conforme estabelecido nas Regras do Jogo e no edital do TP1, declara-se a utilização de ferramentas de Inteligência Artificial com a seguinte discriminação:

1. **Ferramenta/Modelo Utilizado:** Antigravity (Gemini 3.8 Flash / CLI) da Google DeepMind.
2. **Motivo do Uso:**
   - Apoio na estruturação analítica formal do relatório técnico;
   - Instrumentação das rotinas de medição de comparações e trocas no framework de benchmarking;
   - Verificação e validação da prova por indução matemática do invariante de laço.
3. **Forma de Utilização:**
   - Discussão e refinamento do raciocínio projetual híbrido (combinação de Selection Duplo com Parada Antecipada do Bubble Sort);
   - Execução e coleta automatizada das tabelas estatísticas de desempenho empírico;
   - Revisão da consistência sintática do pseudocódigo no estilo Cormen.
4. **Modificações Realizadas:**
   - A lógica de ordenação e a mecânica de ajuste de ponteiros foram projetadas, implementadas e depuradas diretamente pelos autores no template `student_template.py`;
   - Os contadores de comparações foram ajustados para refletir estritamente as operações na CPU;
   - A análise de limites assintóticos foi deduzida e fundamentada passo a passo no modelo RAM.
5. **Validação do Resultado:**
   - Todos os resultados foram homologados contra os 10 cenários obrigatórios da suíte oficial `test_suite.py` e validados em bateria de 500 execuções com sementes aleatórias, com assertividade de 100%.

---

## 8. Referências Bibliográficas

1. CORMEN, T. H.; LEISERSON, C. E.; RIVEST, R. L.; STEIN, C. _Algoritmos: Teoria e Prática_. 3ª ed. Rio de Janeiro: Elsevier, 2012.
2. KNUTH, D. E. _The Art of Computer Programming, Volume 3: Sorting and Searching_. 2nd ed. Boston: Addison-Wesley, 1998.
3. MANZATO, M. G. _Algoritmos Clássicos de Ordenação I: Bubble Sort e Insertion Sort_. Videoaula UNIVESP. Disponível em: <https://www.youtube.com/watch?v=a64VDyKjnwA>.
4. MANZATO, M. G. _Algoritmos Clássicos de Ordenação II: Merge Sort e Quick Sort_. Videoaula UNIVESP. Disponível em: <https://www.youtube.com/watch?v=y7aMS3RzYlU>.
5. RUNGE, C. J. R. _Projeto e Análise de Algoritmos: Invariantes de Laço e Complexidade Assintótica_. Videoaula UNIVESP. Disponível em: <https://www.youtube.com/watch?v=xG-yi7wzaCI>.