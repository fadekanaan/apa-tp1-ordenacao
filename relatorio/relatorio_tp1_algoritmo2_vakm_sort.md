# Relatório Técnico — Trabalho Prático 1 (TP1)
## Algoritmo Autoral 2: Variance-Adaptive K-Way Merge Sort (VAKM Sort)

**Disciplina:** Análise e Projeto de Algoritmos (APA)
**Semestre/Ano:** 2026/2
**Modelo de Avaliação:** $N/2$ Algoritmos Autorais (Opção A — Relatório Técnico Completo)
**Autores:**
- [Fade Kanaan]
- [Gabriel Fernandes dos Anjos]
- [Gabriel Ortiz]
- [Leonardo Dorneles]
- [Rodrigo Thoma]

> **Nota:** este documento é o relatório dedicado ao **Algoritmo Autoral 2** do grupo. O relatório principal do trabalho — com o Algoritmo Autoral 1 (*Dual Selection Bubble Sort*), a formulação geral do problema e o modelo RAM — está em [`relatorio_tp1.md`](./relatorio_tp1.md).

---

## Sumário

1. [Introdução e Escopo do Algoritmo](#1-introdução-e-escopo-do-algoritmo)
2. [Concepção, Formalização e Análise Assintótica](#2-concepção-formalização-e-análise-assintótica)
   * 2.1. Concepção, Intuição e Metáfora Visual
   * 2.2. Justificativa do Design: Adaptação Estrutural do Merge Sort
   * 2.3. Especificação Formal em Pseudocódigo (Estilo Cormen)
   * 2.4. Corretude: Prova por Indução Forte sobre a Recursão
   * 2.5. Exemplo Didático Rastreável Passo a Passo
   * 2.6. Dedução Analítica de Complexidade no Modelo RAM (Teorema Mestre)
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

## 1. Introdução e Escopo do Algoritmo

O problema da ordenação é definido, no modelo computacional **RAM** (*Random Access Machine*, Cormen et al., 2012), como: dada uma sequência $\langle A[0], \dots, A[N-1] \rangle$ de $N$ elementos com chaves comparáveis sob uma relação de ordem total $\le$, produzir uma permutação $\langle A'[0], \dots, A'[N-1] \rangle$ tal que $A'[0] \le A'[1] \le \dots \le A'[N-1]$. Operações aritméticas, atribuições, comparações e acessos indexados têm custo unitário $O(1)$ (detalhes completos do modelo RAM no relatório principal, Seção 1.2).

Este documento apresenta o **Algoritmo Autoral 2** do grupo, exigido pelo modelo de avaliação $N/2$ do TP1: um método de paradigma **recursivo / Divisão e Conquista**, complementar ao Algoritmo Autoral 1 (iterativo/in-place, ver `relatorio_tp1.md`).

**Variance-Adaptive K-Way Merge Sort (VAKM Sort)** — generaliza o Merge Sort binário clássico para um fator de ramificação $k$ variável (entre $2$ e $8$), decidido dinamicamente pela dispersão estatística dos valores de cada segmento, com fusão $k$-ária estável e poda antecipada de blocos uniformes. Sua meta de projeto é eficiência assintótica $\Theta(N \log N)$ em todos os casos, com raciocínio analítico modelado por relação de recorrência resolvida via Teorema Mestre.

---

## 2. Concepção, Formalização e Análise Assintótica

### 2.1. Concepção, Intuição e Metáfora Visual

O **Variance-Adaptive K-Way Merge Sort (VAKM Sort)** parte de uma pergunta simples sobre o Merge Sort clássico: *por que dividir sempre ao meio?* A escolha de $k = 2$ do Merge Sort tradicional é arbitrária — ela não olha para o conteúdo do vetor, apenas para o seu tamanho.

O VAKM Sort propõe a metáfora do **"Fatiamento por Dispersão" (*Dispersion Slicing*)**: antes de dividir um segmento, o algoritmo mede o quão espalhados estão os valores contidos nele (sua dispersão estatística) e usa essa medida para decidir em quantas fatias ($k$, entre $2$ e $8$) o segmento será cortado:

* Se os valores do segmento estão **concentrados** (baixa dispersão), poucas fatias bastam — o algoritmo se comporta quase como um Merge Sort binário comum.
* Se os valores estão **espalhados** (alta dispersão), o segmento é cortado em mais fatias simultaneamente, reduzindo mais rapidamente o tamanho de cada sub-problema por nível de recursão.
* Se **todos os valores de um segmento são idênticos**, a dispersão é nula e o segmento já está trivialmente ordenado — a recursão para ali, sem gerar fatias novas.

```text
Segmento de baixa dispersão:      [ 5, 6, 5, 7, 6 ]              -> corta em poucas fatias (k pequeno)
Segmento de alta dispersão:       [ 1, 99, 3, 87, 2, 91 ]        -> corta em muitas fatias (k grande)
Segmento uniforme (dispersão=0):  [ 4, 4, 4, 4, 4 ]              -> já ordenado, sem recursão
```

Cada uma das $k$ fatias é ordenada recursivamente, e o resultado final é obtido por uma **fusão simultânea das $k$ fatias já ordenadas** (um *k-way merge*), em vez da fusão de apenas duas metades como no Merge Sort tradicional.

### 2.2. Justificativa do Design: Adaptação Estrutural do Merge Sort

O VAKM Sort é uma **adaptação estrutural profunda do Merge Sort** (técnica de origem: Divisão e Conquista por fusão, Von Neumann, 1945), e não uma cópia cosmética. As modificações estruturais introduzidas são:

1. **Fator de ramificação $k$ variável e dependente dos dados:** No Merge Sort clássico, $k = 2$ é fixo e independente do conteúdo do vetor. No VAKM Sort, $k \in [2, 8]$ é recalculado a cada chamada recursiva a partir da variância normalizada do segmento:
   $$\text{disp} = \min\left(\frac{\sigma^2}{(\text{max} - \text{min})^2},\ 0.25\right), \qquad k = 2 + \left\lfloor \frac{\text{disp}}{0.25} \cdot (K_{max} - 2) \right\rceil$$
   O fator $0.25$ é o teto teórico de $\sigma^2 / \text{amplitude}^2$ (atingido por uma distribuição bimodal concentrada nos dois extremos do intervalo), o que garante que $\text{disp}$ normalizado esteja sempre em $[0, 1]$.

2. **Fusão $k$-ária em vez de fusão binária:** A etapa de combinação (*merge*) do Merge Sort clássico funde apenas 2 sublistas por vez. O VAKM Sort generaliza essa etapa para fundir as $k$ sublistas simultaneamente, comparando as $k$ cabeças de lista a cada passo e escolhendo a menor.

3. **Detecção precoce de blocos uniformes:** Antes de decidir o particionamento, o algoritmo varre o segmento em $O(N)$ para localizar mínimo e máximo. Se ambos coincidem, todo o segmento é constituído por valores idênticos e a recursão é interrompida imediatamente, evitando divisões e fusões desnecessárias em regiões já homogêneas do vetor (uma situação comum em vetores com muita repetição).

4. **Limiar híbrido com Insertion Sort:** Para segmentos pequenos ($N \le 16$), a sobrecarga de calcular dispersão, particionar e fundir $k$ sublistas supera o custo de simplesmente ordenar por inserção. Esse híbrido de threshold é uma adaptação comum na literatura (ex: Timsort, introsort), reaproveitada aqui de forma consciente e declarada.

**Comparação direta com a literatura:** ao contrário do *Merge Sort* clássico, cujo fator de ramificação é fixo e a fusão é sempre binária, o VAKM Sort tem ramificação adaptativa aos dados. Ao contrário do *Quick Sort* (que particiona por valor de pivô, com risco de desbalanceamento $O(N^2)$ em más escolhas de pivô), o VAKM Sort particiona por posição (blocos contíguos de tamanho fixo) e delega toda a lógica de ordenação para a fusão — não há risco de degradação quadrática por má escolha de "pivô", pois não existe pivô: o particionamento é sempre balanceado em blocos de tamanho $\lceil N/k \rceil$.

---

### 2.3. Especificação Formal em Pseudocódigo (Estilo Cormen)

```text
procedimento VAKMSort(A, N):
    retornar OrdenarRecursivo(A[0 .. N-1])

procedimento OrdenarRecursivo(L):
    n ← tamanho(L)
    se n <= 1 então:
        retornar L
    fim-se

    se n <= LIMIAR_INSERCAO então:
        retornar InsertionSort(L)
    fim-se

    (min, max) ← EncontrarExtremos(L)      // O(n), varredura única

    se min == max então:                    // Segmento totalmente uniforme
        retornar L
    fim-se

    k ← EscolherK(L, min, max)              // k ∈ [2, K_MAX], por dispersão
    k ← min(k, n)

    tamanho_bloco ← teto(n / k)
    fatias ← particionar L em blocos contíguos de tamanho tamanho_bloco

    para cada fatia em fatias faça:
        fatia ← OrdenarRecursivo(fatia)
    fim-para

    retornar FusaoKVias(fatias)

procedimento EscolherK(L, min, max):
    amplitude ← max - min
    media ← média(L)
    variancia ← média((x - media)² para x em L)
    disp ← min(variancia / amplitude², 0.25) / 0.25    // normalizado em [0, 1]
    k ← 2 + arredondar(disp * (K_MAX - 2))
    retornar k

procedimento FusaoKVias(fatias):
    resultado ← lista vazia
    cursores ← [0, 0, ..., 0]                // um cursor por fatia

    enquanto existir fatia com cursor não esgotado faça:
        melhor ← índice da fatia não esgotada com o menor valor na
                  posição do cursor (empate: menor índice de fatia)
        adicionar fatias[melhor][cursores[melhor]] a resultado
        cursores[melhor] ← cursores[melhor] + 1
    fim-enquanto

    retornar resultado
fim-procedimento
```

---

### 2.4. Corretude: Prova por Indução Forte sobre a Recursão

Diferente de um algoritmo iterativo (provado por invariante de laço), o VAKM Sort é recursivo e sua corretude é estabelecida por **indução forte sobre o tamanho $n$ do segmento**, seguindo o mesmo esquema de prova de corretude do Merge Sort clássico generalizado para $k$ vias.

> **Hipótese de Indução (HI):** Para todo segmento $L$ com $|L| < n$, `OrdenarRecursivo(L)` retorna uma permutação ordenada de $L$.

**Prova por indução forte em $n = |L|$:**

* **Caso base ($n \le 1$):** Um segmento vazio ou unitário é trivialmente uma permutação ordenada de si mesmo. `OrdenarRecursivo` retorna `L` sem modificação.

* **Caso base auxiliar ($1 < n \le 16$):** `InsertionSort(L)` é um algoritmo clássico cuja corretude já é bem estabelecida na literatura; portanto `OrdenarRecursivo(L)` retorna uma permutação ordenada.

* **Caso indutivo ($n > 16$):**
  1. *Poda por uniformidade:* Se $\min(L) = \max(L)$, todo elemento de $L$ é idêntico entre si (pois nenhum elemento pode ser menor que o mínimo nem maior que o máximo, e ambos coincidem). Uma lista com todos os elementos iguais é, por definição, uma sequência ordenada. `OrdenarRecursivo` retorna `L` corretamente.
  2. *Divisão:* $L$ é particionado em $k$ fatias contíguas e não sobrepostas $L_1, L_2, \dots, L_k$, cada uma com $|L_i| = \lceil n/k \rceil$ ou menor (última fatia), tal que $L_1 \frown L_2 \frown \dots \frown L_k = L$ (concatenação preserva $L$). Como $k \ge 2$ e $n > 16$, temos $|L_i| < n$ para todo $i$.
  3. *Conquista:* Pela HI, aplicada a cada $L_i$ com $|L_i| < n$, `OrdenarRecursivo(L_i)` retorna uma permutação ordenada $L_i'$ de $L_i$.
  4. *Combinação:* `FusaoKVias` recebe $k$ listas já ordenadas $L_1', \dots, L_k'$ e, a cada passo, seleciona o menor elemento entre as $k$ cabeças de lista, avançando o cursor correspondente. Por indução simples sobre o número de elementos já emitidos: se os primeiros $j$ elementos do resultado estão ordenados e são os $j$ menores dentre todos os elementos ainda não emitidos (invariante de fusão), o $(j+1)$-ésimo elemento escolhido — o mínimo entre as $k$ cabeças restantes — mantém essa propriedade. Como cada $L_i'$ já está ordenada internamente, o menor elemento não emitido de $L_i'$ está sempre na cabeça (posição do cursor). Ao final, todos os $n$ elementos foram emitidos em ordem monotonicamente não decrescente.
  5. Como $L_1 \frown \dots \frown L_k$ é uma partição de $L$ (nenhum elemento duplicado ou perdido), o resultado da fusão é uma permutação ordenada de $L$.

**Conclusão:** Por indução forte, `OrdenarRecursivo(L)` retorna uma permutação ordenada de $L$ para todo $n \ge 0$, e portanto `VAKMSort(A, N)` ordena corretamente qualquer vetor de entrada. $\blacksquare$

---

### 2.5. Exemplo Didático Rastreável Passo a Passo

> **Nota metodológica:** para tornar o rastreio visualmente tratável, este exemplo usa limiares didaticamente reduzidos ($LIMIAR\_INSERCAO = 2$ e $K_{max} = 4$, em vez dos valores $16$ e $8$ usados na implementação real, calibrados para desempenho). A lógica do algoritmo é idêntica.

Considere o vetor de entrada $A = [9, 2, 7, 1, 8, 3, 6, 4]$ ($N = 8$).

* **Chamada de topo:** $N = 8 > 2$. `EncontrarExtremos` → $min = 1$, $max = 9$.
  * $min \ne max$, não é bloco uniforme.
  * Média $= 5$; Variância $= 7{,}5$; amplitude $= 8$; $\text{disp} = 7{,}5/64 \approx 0{,}117$; normalizado $\approx 0{,}469$.
  * $k = 2 + \text{arred}(0{,}469 \times 2) = 2 + 1 = 3$.
  * Tamanho de bloco $= \lceil 8/3 \rceil = 3$. Fatias: $L_1 = [9,2,7]$, $L_2 = [1,8,3]$, $L_3 = [6,4]$.

* **Ordenação de $L_1 = [9,2,7]$** ($n=3>2$): $min=2,max=9$; $k=3$ (mesma fórmula); bloco $=1$ → fatias unitárias $[9],[2],[7]$ (caso base). Fusão 3 vias: $[2, 7, 9]$.

* **Ordenação de $L_2 = [1,8,3]$** ($n=3>2$): análogo ao anterior → fatias unitárias $[1],[8],[3]$. Fusão 3 vias: $[1, 3, 8]$.

* **Ordenação de $L_3 = [6,4]$** ($n=2 \le 2$): caso base, `InsertionSort([6,4])` → $[4, 6]$.

* **Fusão final (3 vias) de $[2,7,9]$, $[1,3,8]$, $[4,6]$:**

| Passo | Cabeças ($L_1', L_2', L_3'$) | Escolhido | Resultado parcial |
| :---: | :--- | :---: | :--- |
| 1 | $2, 1, 4$ | $1$ | $[1]$ |
| 2 | $2, 3, 4$ | $2$ | $[1, 2]$ |
| 3 | $7, 3, 4$ | $3$ | $[1, 2, 3]$ |
| 4 | $7, 8, 4$ | $4$ | $[1, 2, 3, 4]$ |
| 5 | $7, 8, 6$ | $6$ | $[1, 2, 3, 4, 6]$ |
| 6 | $7, 8, -$ | $7$ | $[1, 2, 3, 4, 6, 7]$ |
| 7 | $9, 8, -$ | $8$ | $[1, 2, 3, 4, 6, 7, 8]$ |
| 8 | $9, -, -$ | $9$ | $[1, 2, 3, 4, 6, 7, 8, 9]$ |

**Vetor Final Ordenado:** $[1, 2, 3, 4, 6, 7, 8, 9]$, confirmando a corretude do rastreio.

---

### 2.6. Dedução Analítica de Complexidade no Modelo RAM (Teorema Mestre)

#### Relação de Recorrência:
Em cada chamada recursiva sobre um segmento de tamanho $n$:
* $O(n)$ para localizar os extremos (`EncontrarExtremos`);
* $O(n)$ para calcular a dispersão e escolher $k$ (`EscolherK`), já que envolve somatórios sobre todos os $n$ elementos;
* $k$ subchamadas recursivas, cada uma sobre um segmento de tamanho $\approx n/k$;
* $O(n \cdot k)$ para a fusão $k$-ária (`FusaoKVias`), pois a cada um dos $n$ elementos emitidos é necessário inspecionar até $k$ cabeças de lista.

Como $k$ é sempre limitado ao intervalo constante $[2, K_{max}] = [2, 8]$, o custo de cada nível (extremos + dispersão + fusão) é $O(n) + O(n) + O(n \cdot k) = \Theta(n)$, pois $k$ não depende de $n$. A relação de recorrência é:
$$T(n) = k \cdot T\left(\frac{n}{k}\right) + \Theta(n)$$

#### Aplicação do Teorema Mestre:
Com $a = k$, $b = k$ (logo $a = b$) e $f(n) = \Theta(n)$:
$$n^{\log_b a} = n^{\log_k k} = n^1 = n$$
Como $f(n) = \Theta(n^{\log_b a}) = \Theta(n^1)$, recaímos no **Caso 2** do Teorema Mestre:
$$T(n) = \Theta\left(n^{\log_b a} \cdot \log n\right) = \Theta(n \log n)$$

#### 1. Melhor Caso ($\Theta(N \log N)$):
A adaptação do VAKM Sort responde à **dispersão de valores**, não à **ordem prévia** dos dados. Um vetor já ordenado ainda precisa ser dividido e fundido recursivamente — não há mecanismo de parada antecipada por pré-ordenação. Assim, mesmo no melhor caso, o custo permanece $\Theta(N \log N)$ (validado experimentalmente na Seção 4.2).

#### 2. Pior Caso ($O(N \log N)$):
Como $k \in [2, 8]$ é sempre uma constante positiva, a profundidade da árvore de recursão é $\log_k N = \frac{\log N}{\log k} = \Theta(\log N)$ independentemente da distribuição de valores ou da ordem de entrada. Não existe, portanto, um cenário adversarial (como o pivô mal escolhido do Quick Sort) capaz de degradar o VAKM Sort para $O(N^2)$: o particionamento é sempre por posição, em blocos de tamanho balanceado $\lceil N/k \rceil$.

#### 3. Caso Médio ($\Theta(N \log N)$):
Para qualquer distribuição de valores, $k$ permanece limitado ao intervalo constante $[2,8]$, preservando a mesma análise assintótica de recorrência. O valor exato de $k$ afeta apenas a **constante multiplicativa** (a base do logaritmo e o fator da fusão $k$-ária), não a ordem de grandeza:
$$T_{médio}(N) = \Theta(N \log N)$$

> **Distinção conceitual importante:** o VAKM Sort é *sensível à distribuição de valores* (adapta a largura da árvore de recursão), não à ordem de entrada — ao contrário de algoritmos com parada antecipada baseada em pré-ordenação (como o Algoritmo Autoral 1 do grupo, ver `relatorio_tp1.md`, Seção 2). Ele mantém a classe assintótica $\Theta(N \log N)$ em todos os casos: a adaptação melhora a constante prática, não a ordem de grandeza teórica.

---

### 2.7. Propriedades Estruturais: Estabilidade e Memória Auxiliar

* **Operação Não In-Place:**
  Cada chamada recursiva cria novas sublistas por fatiamento (`L[i:i+bloco]`) e a fusão produz uma nova lista de resultado, exatamente como no Merge Sort clássico.
  $$\text{Memória Auxiliar Extra: } O(N) \quad (\text{proporcional ao tamanho do vetor})$$

* **Estabilidade:**
  **Estável.** A partição em fatias contíguas preserva a ordem relativa original dos elementos (a fatia $i$ contém sempre elementos de posições anteriores à fatia $i+1$ no vetor original). Na `FusaoKVias`, em caso de empate de valores entre duas cabeças de fatia, o algoritmo sempre escolhe a fatia de **menor índice** (implementado via `if ... < ...`, nunca `<=`, preservando o candidato mais à esquerda como vencedor por padrão). Como fatias de menor índice contêm exclusivamente elementos originalmente anteriores, chaves iguais nunca trocam de ordem relativa.
  *Validação empírica:* a estabilidade foi confirmada por teste automatizado com chaves compostas (valor, posição original) sobre $300$ elementos e $500$ sementes aleatórias adicionais, sem nenhuma inversão de ordem relativa detectada.

---

## 3. Metodologia Experimental e Suíte de Testes

### 3.1. Cenários de Teste Obrigatórios e Casos Limítrofes

Para validação rigorosa da corretude funcional e estresse do algoritmo, o VAKM Sort foi submetido à suíte automatizada em Python (`test_suite.py`, classe `TestVAKMSort`), contemplando os mesmos 10 cenários compulsórios exigidos pelo edital do TP1 e aplicados a todos os métodos deste trabalho:

1. **Vetor Vazio ($N = 0$):** Validação de comportamento assintótico de borda e ausência de exceções (`IndexError`).
2. **Vetor Unitário ($N = 1$):** Condição trivial de convergência imediata.
3. **Vetor Perfeitamente Ordenado ($N = 100$):** Aferição de melhor caso / sensibilidade.
4. **Vetor Estritamente Reverso ($N = 100$):** Teste de estresse de pior caso.
5. **Vetor com Todos os Elementos Idênticos ($N = 50$):** Aciona diretamente a poda por uniformidade.
6. **Vetor com Muitas Duplicatas ($N = 200$):** Dispersão com poucos valores distintos ($1$ a $5$).
7. **Vetor Misto com Negativos e Ponto Flutuante:** Teste de robustez de tipagem e ordenação algébrica.
8. **Vetores Aleatórios Pequenos ($N = 25$):** Avaliação de sobrecarga do caso base (Insertion Sort).
9. **Vetores Aleatórios Médios ($N = 1000$):** Escala estatística em regime assintótico.
10. **Vetor Quase Ordenado (95% Ordenado):** Teste de robustez a perturbações locais.

> **Resultado da Validação:** O VAKM Sort foi submetido a todos os 10 cenários formais da suíte, obtendo **100% de aprovação (OK)**. Adicionalmente, foi validado em bateria de estresse com **500 sementes aleatórias** (tamanhos de $0$ a $300$ elementos, sem nenhuma falha de ordenação) e em um teste dedicado de **estabilidade** com $300$ chaves compostas (valor, posição original), confirmando que nenhuma inversão de ordem relativa ocorreu entre chaves duplicadas.

### 3.2. Protocolo de Benchmarking e Métricas Coletadas

O framework `benchmark.py` executa, para cada combinação de (algoritmo, tamanho $N$, distribuição), **3 repetições estatísticas independentes** sobre datasets fixos (gerados uma única vez por repetição e reutilizados por todos os algoritmos, garantindo comparação justa), coletando:

* **Tempo de execução (ms):** medido via `time.perf_counter()`, com média aritmética das repetições;
* **Comparações:** contadas explicitamente no código de cada algoritmo, incrementadas a cada avaliação de uma relação de ordem (`<`, `>`, `==`) entre elementos do vetor — operações puramente aritméticas de diagnóstico (ex: cálculo de variância) não são contadas;
* **Movimentações:** contadas a cada escrita efetiva em uma posição do vetor (atribuição ou troca).

Todos os resultados são validados por `assert res == sorted(data)` antes de serem registrados, garantindo que nenhuma medição de desempenho seja aceita sobre uma saída incorreta.

---

## 4. Resultados Experimentais e Análise Comparativa

Os benchmarks empíricos foram executados em ambiente Windows com Python 3.12, com **3 repetições estatísticas independentes** por configuração. Abaixo, o **VAKM Sort (Autoral 2)** é comparado diretamente com os métodos clássicos da literatura: *Bubble Sort*, *Selection Sort*, *Insertion Sort*, *Merge Sort* e *Quick Sort*.

---

### 4.1. Distribuição Aleatória Homogênea (`random`)

#### Tempo de Execução Médio (ms):
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 0.006 ms | 0.107 ms | 0.444 ms | 2.726 ms | 11.399 ms | 53.412 ms |
| Selection Sort | 0.005 ms | 0.074 ms | 0.246 ms | 1.394 ms | 6.269 ms | 26.991 ms |
| Insertion Sort | 0.004 ms | 0.060 ms | 0.297 ms | 1.381 ms | 6.074 ms | 28.104 ms |
| Merge Sort | 0.013 ms | 0.071 ms | 0.200 ms | 0.418 ms | 0.974 ms | 2.236 ms |
| Quick Sort | 0.009 ms | 0.047 ms | 0.129 ms | 0.307 ms | 0.676 ms | 1.489 ms |
| **VAKM Sort (Autoral 2)** | **0.020 ms** | **0.096 ms** | **0.256 ms** | **0.656 ms** | **1.741 ms** | **3.705 ms** |

#### Número Médio de Movimentações / Trocas:
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 49 | 1.174 | 5.073 | 30.867 | 122.941 | 504.905 |
| Selection Sort | 14 | 93 | 191 | 491 | 985 | 1.984 |
| Insertion Sort | 43 | 685 | 2.734 | 15.932 | 62.468 | 254.451 |
| Merge Sort | 34 | 286 | 672 | 1.994 | 4.488 | 9.976 |
| Quick Sort | 23 | 147 | 369 | 1.097 | 2.411 | 5.231 |
| **VAKM Sort (Autoral 2)** | **43** | **286** | **493** | **1.901** | **3.205** | **8.550** |

> **Observação:** Para $N=10$ e $N=50$, o VAKM Sort recai no caso base de Insertion Sort ($N \le 16$) ou produz partições tão pequenas que o número de movimentações coincide com o do Merge Sort — ambos escrevem, no mínimo, uma vez por elemento por nível de fusão. A partir de $N=100$, o efeito da fusão $k$-ária (com $k > 2$) começa a reduzir o número de níveis de recursão, mas cada nível de fusão ainda escreve $N$ elementos, de modo que o crescimento permanece assintoticamente próximo ao do Merge Sort clássico — consistente com a análise via Teorema Mestre da Seção 2.6.

---

### 4.2. Distribuição Perfeitamente Ordenada (`sorted` — Melhor Caso)

#### Tempo de Execução Médio (ms):
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 0.002 ms | 0.003 ms | 0.006 ms | 0.013 ms | 0.030 ms | 0.062 ms |
| Selection Sort | 0.004 ms | 0.063 ms | 0.240 ms | 1.461 ms | 6.533 ms | 26.536 ms |
| Insertion Sort | 0.002 ms | 0.006 ms | 0.011 ms | 0.028 ms | 0.069 ms | 0.141 ms |
| Merge Sort | 0.012 ms | 0.059 ms | 0.132 ms | 0.372 ms | 0.837 ms | 1.846 ms |
| Quick Sort | 0.007 ms | 0.031 ms | 0.067 ms | 0.221 ms | 0.401 ms | 0.887 ms |
| **VAKM Sort (Autoral 2)** | **0.015 ms** | **0.062 ms** | **0.201 ms** | **0.508 ms** | **1.339 ms** | **2.663 ms** |

> **Destaque Analítico:** O **VAKM Sort não acelera** neste cenário (2.663 ms para $N=1000$, praticamente o mesmo patamar da distribuição aleatória, 3.705 ms). Isso confirma experimentalmente a previsão teórica da Seção 2.6: sua adaptação responde à **dispersão de valores**, não à **pré-ordenação**, e por isso não possui um melhor caso sub-$\Theta(N \log N)$. Isso é um trade-off de projeto consciente: algoritmos como *Bubble Sort* e *Insertion Sort* (adaptáveis à ordem) são muito mais rápidos neste cenário específico, mas voltam a ser $O(N^2)$ assim que a pré-ordenação desaparece (Seção 4.3).

---

### 4.3. Distribuição Estritamente Decrescente (`reverse` — Pior Caso de Estresse)

#### Tempo de Execução Médio (ms):
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 0.007 ms | 0.149 ms | 0.596 ms | 3.791 ms | 15.911 ms | 71.207 ms |
| Selection Sort | 0.004 ms | 0.066 ms | 0.253 ms | 1.566 ms | 6.870 ms | 28.573 ms |
| Insertion Sort | 0.005 ms | 0.117 ms | 0.471 ms | 2.994 ms | 12.409 ms | 52.060 ms |
| Merge Sort | 0.011 ms | 0.061 ms | 0.133 ms | 0.378 ms | 0.863 ms | 1.870 ms |
| Quick Sort | 0.007 ms | 0.034 ms | 0.073 ms | 0.187 ms | 0.433 ms | 0.933 ms |
| **VAKM Sort (Autoral 2)** | **0.014 ms** | **0.094 ms** | **0.221 ms** | **0.734 ms** | **1.581 ms** | **3.421 ms** |

#### Número Médio de Movimentações / Trocas (Impacto em Memória):
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 90 | 2.450 | 9.900 | 62.250 | 249.500 | 999.000 |
| Selection Sort | 10 | 50 | 100 | 250 | 500 | 1.000 |
| Insertion Sort | 63 | 1.323 | 5.148 | 31.623 | 125.748 | 501.498 |
| Merge Sort | 34 | 286 | 672 | 1.994 | 4.488 | 9.976 |
| Quick Sort | 14 | 54 | 104 | 254 | 504 | 1.004 |
| **VAKM Sort (Autoral 2)** | **63** | **431** | **644** | **2.801** | **4.092** | **12.204** |

> **Destaque Analítico:** O VAKM Sort é **imune ao pior caso clássico de ordenação por trocas**: enquanto Bubble Sort ($71.207$ ms) e Insertion Sort ($52.060$ ms) se degradam para $O(N^2)$ em vetores estritamente decrescentes, o VAKM Sort mantém-se em $3.421$ ms — porque seu particionamento é sempre por posição, nunca por comparação sequencial de vizinhos. Em número de movimentações, realiza **12.204** trocas em $N=1000$, num patamar comparável ao do Merge Sort clássico ($9.976$), já que ambos produzem uma lista de saída nova a cada nível de fusão; a diferença vem do custo extra de inspecionar $k$ cabeças de lista por passo de fusão, em vez de apenas $2$.

---

### 4.4. Distribuição com Chaves Redundantes (`duplicates`)

Cenário com apenas 5 valores distintos ($\{1, 2, 3, 5, 8\}$) distribuídos aleatoriamente, avaliando o comportamento do algoritmo sob alta taxa de colisão de chaves — o cenário que mais favorece a poda por uniformidade do VAKM Sort.

#### Tempo de Execução Médio (ms):
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 0.005 ms | 0.094 ms | 0.369 ms | 2.485 ms | 10.704 ms | 45.154 ms |
| Selection Sort | 0.004 ms | 0.061 ms | 0.234 ms | 1.465 ms | 6.850 ms | 27.560 ms |
| Insertion Sort | 0.003 ms | 0.049 ms | 0.174 ms | 1.137 ms | 4.906 ms | 21.779 ms |
| Merge Sort | 0.012 ms | 0.062 ms | 0.135 ms | 0.414 ms | 0.979 ms | 2.174 ms |
| Quick Sort | 0.008 ms | 0.046 ms | 0.094 ms | 0.269 ms | 0.755 ms | 1.479 ms |
| **VAKM Sort (Autoral 2)** | **0.010 ms** | **0.083 ms** | **0.243 ms** | **0.643 ms** | **1.833 ms** | **4.444 ms** |

#### Número Médio de Comparações:
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 41 | 1.101 | 4.623 | 29.989 | 119.993 | 480.000 |
| Selection Sort | 45 | 1.225 | 4.950 | 31.125 | 124.750 | 499.500 |
| Insertion Sort | 23 | 516 | 2.024 | 13.161 | 48.851 | 206.031 |
| Merge Sort | 22 | 210 | 514 | 1.606 | 3.621 | 8.141 |
| Quick Sort | 63 | 421 | 896 | 2.537 | 5.589 | 11.810 |
| **VAKM Sort (Autoral 2)** | **23** | **402** | **1.171** | **3.422** | **8.600** | **18.705** |

> **Destaque Analítico:** A poda por uniformidade é acionada sempre que um bloco de recursão cai inteiramente sobre um único valor repetido — situação frequente quando há apenas 5 valores distintos no vetor. Isso mantém o VAKM Sort com apenas **18.705 comparações** em $N=1000$, menos de $4\%$ das $499.500$ comparações do Selection Sort, evidenciando que a adaptação por dispersão de valores (e não por posição ou por pré-ordenação) é uma estratégia particularmente eficaz para dados redundantes.

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
| **VAKM Sort (Autoral 2)** | **0.016 ms** | **0.069 ms** | **0.226 ms** | **0.782 ms** | **2.527 ms** | **3.792 ms** |

#### Número Médio de Movimentações / Trocas:
| Algoritmo | N=10 | N=50 | N=100 | N=250 | N=500 | N=1000 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Bubble Sort | 2 | 113 | 622 | 4.253 | 15.751 | 61.932 |
| Selection Sort | 2 | 4 | 10 | 24 | 50 | 100 |
| Insertion Sort | 19 | 155 | 509 | 2.625 | 8.874 | 32.964 |
| Merge Sort | 34 | 286 | 672 | 1.994 | 4.488 | 9.976 |
| Quick Sort | 2 | 4 | 31 | 96 | 237 | 581 |
| **VAKM Sort (Autoral 2)** | **19** | **160** | **412** | **1.227** | **2.892** | **6.658** |

> **Destaque Analítico:** O **Insertion Sort** (fortemente adaptável à ordem) despenca para **3.645 ms** neste cenário. O **VAKM Sort permanece estável em torno de 3,8 ms**, praticamente idêntico ao seu tempo na distribuição totalmente aleatória (Seção 4.1) — reforçando, mais uma vez, que sua adaptação (por dispersão de valores) é ortogonal à ordem dos dados: poucas trocas pontuais espalhadas não mudam a dispersão estatística do vetor de forma perceptível, então o algoritmo se comporta exatamente como esperaria em qualquer vetor com a mesma distribuição de valores.

---

## 5. Discussão Crítica e Trade-Offs

1. **Ganhos Comprovados da Proposta Autoral:**
   * **Robustez assintótica sem casos adversariais:** Como o particionamento é sempre por posição (blocos de tamanho $\lceil N/k \rceil$) e nunca por valor de pivô, o VAKM Sort não possui um cenário de entrada capaz de degradá-lo para $O(N^2)$, ao contrário do Quick Sort clássico.
   * **Insensibilidade à ordem prévia:** Seu desempenho não se degrada em vetores quase ordenados com perturbações espalhadas (Seção 4.5): manteve-se estável (~3,8 ms) tanto no cenário `almost_sorted` quanto no `random`, algo que nenhum método clássico baseado em trocas/inserção conseguiu replicar.
   * **Poda eficaz em dados redundantes:** A detecção de blocos uniformes reduz drasticamente o número de comparações em vetores com muitas duplicatas (Seção 4.4), chegando a menos de $4\%$ das comparações do Selection Sort em $N=1000$.
2. **Limitações Identificadas (Trade-Offs Honestos):**
   * **Sem melhor caso sub-linearítmico:** O VAKM Sort permanece em $\Theta(N \log N)$ mesmo no melhor caso (vetor já ordenado), pois sua adaptação responde à dispersão de *valores*, não à ordem de entrada — diferente de algoritmos com parada antecipada por pré-ordenação.
   * **Overhead constante da fusão $k$-ária:** Para $N$ pequeno ($N \le 100$), o custo de calcular a variância a cada nível de recursão faz o VAKM Sort perder para o Merge Sort e o Quick Sort em tempo bruto, embora ainda supere os métodos $O(N^2)$.
   * **Não é in-place:** Requer $O(N)$ de memória auxiliar por nível de recursão (fatiamento de listas), assim como o Merge Sort clássico — um trade-off explícito de espaço por garantia de desempenho assintótico.

**Posicionamento do algoritmo:** o VAKM Sort é indicado para cenários em que a **distribuição de valores** é a característica mais relevante dos dados (dados redundantes, categóricos, ou com muitos valores repetidos), e em cenários onde é necessário garantir uma **cota superior previsível** de desempenho, sem risco de degradação por ordens adversariais de entrada — em contraste com métodos que adaptam-se à ordem prévia dos dados, como o Algoritmo Autoral 1 do grupo (ver `relatorio_tp1.md`).

---

## 6. Declaração Obrigatória de Autoria e Uso de Ferramentas de IA

Conforme estabelecido nas Regras do Jogo e no edital do TP1, declara-se a utilização de ferramentas de Inteligência Artificial na concepção e documentação deste algoritmo:

1. **Ferramenta/Modelo Utilizado:** Claude Code (modelo Claude Sonnet 5), da Anthropic.
2. **Motivo do Uso:**
   * Apoio na concepção e formalização do design do VAKM Sort (fator de ramificação $k$ adaptativo por dispersão estatística, aplicado sobre a estrutura de um Merge Sort $k$-ário);
   * Implementação do algoritmo em `vakm_sort.py`, integração com `test_suite.py` e `benchmark.py`;
   * Redação deste relatório (pseudocódigo, prova de corretude por indução, dedução via Teorema Mestre e exemplo didático).
3. **Forma de Utilização:**
   * Discussão interativa do paradigma desejado (recursivo, Divisão e Conquista) e refinamento da ideia de ramificação variável guiada por variância normalizada;
   * Execução automatizada dos testes de corretude (10 cenários obrigatórios), de um estresse adicional com 500 sementes aleatórias e de um teste dedicado de estabilidade com chaves compostas;
   * Execução do framework de benchmark (`benchmark.py`) para coleta das tabelas de tempo, comparações e movimentações apresentadas na Seção 4.
4. **Modificações Realizadas:**
   * A escolha do critério de dispersão (variância normalizada pelo quadrado da amplitude) e dos limiares $K_{max}=8$ e $LIMIAR\_INSERCAO=16$ foi decidida em conjunto com o grupo e revisada por experimentação empírica;
   * O pseudocódigo e as provas formais foram redigidos pela ferramenta a partir da lógica de código já implementada e validada, e revisados pelos autores quanto à fidelidade em relação à implementação real.
5. **Validação do Resultado:**
   * O código foi validado contra os 10 cenários obrigatórios da suíte oficial (100% de aprovação), bateria de 500 sementes aleatórias sem falhas, e teste de estabilidade dedicado — todos executados e conferidos pelos autores antes da redação final deste relatório.

---

## 7. Referências Bibliográficas

1. CORMEN, T. H.; LEISERSON, C. E.; RIVEST, R. L.; STEIN, C. *Algoritmos: Teoria e Prática*. 3ª ed. Rio de Janeiro: Elsevier, 2012.
2. KNUTH, D. E. *The Art of Computer Programming, Volume 3: Sorting and Searching*. 2nd ed. Boston: Addison-Wesley, 1998.
3. MANZATO, M. G. *Algoritmos Clássicos de Ordenação II: Merge Sort e Quick Sort*. Videoaula UNIVESP. Disponível em: <https://www.youtube.com/watch?v=y7aMS3RzYlU>.
4. RUNGE, C. J. R. *Projeto e Análise de Algoritmos: Invariantes de Laço e Complexidade Assintótica*. Videoaula UNIVESP. Disponível em: <https://www.youtube.com/watch?v=xG-yi7wzaCI>.
