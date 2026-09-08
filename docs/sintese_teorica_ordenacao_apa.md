# Fundamentação Teórica de Algoritmos de Ordenação: Síntese das Aulas UNIVESP e Diretrizes para o TP1

Este documento reúne a síntese teórica das três aulas de referência da UNIVESP (disciplinas de *Algoritmos e Programação de Computadores II* e *Projeto e Análise de Algoritmos*), sistematizando os conceitos formais de ordenação, funcionamento detalhado dos algoritmos clássicos (Bubble Sort, Insertion Sort, Merge Sort e Quick Sort), suas análises de complexidade assintótica e invariantes de corretude, além de estruturar as diretrizes de projeto e avaliação para o **Trabalho Prático 1 (TP1) — Métodos de Ordenação Autorais**.

---

## 1. Conceitos Fundamentais em Análise de Ordenação

Antes de modelar ou analisar qualquer algoritmo, é necessário definir o vocabulário formal exigido para a avaliação teórica e experimental:

### 1.1. Problema da Ordenação
* **Entrada:** Uma sequência de $N$ chaves $\langle A[0], A[1], \dots, A[N-1] \rangle$.
* **Saída:** Uma permutação (reordenação) $\langle A'[0], A'[1], \dots, A'[N-1] \rangle$ tal que:
  $$A'[0] \le A'[1] \le A'[2] \le \dots \le A'[N-1]$$

### 1.2. Propriedades Estruturais
1. **Estabilidade (*Stability*):**
   * Um método é estável se elementos com chaves de ordenação idênticas mantêm a sua ordem relativa original após a execução.
   * *Exemplo:* Em registros com múltiplos campos (ex.: ordenar pessoas por idade após já terem sido ordenadas por nome alfabeticamente), a estabilidade preserva a ordenação alfabética entre indivíduos com a mesma idade.
2. **Operação In-Place:**
   * Um algoritmo opera *in-place* quando necessita de uma quantidade desprezível de memória auxiliar de trabalho, isto é, memória adicional $O(1)$ além do vetor de entrada (tolerando-se $O(\log N)$ para a pilha de execução recursiva).
   * Algoritmos que dependem de vetores auxiliares de tamanho proporcional à entrada exigem memória adicional $O(N)$.

### 1.3. Paradigma de Divisão e Conquista (*Divide and Conquer*)
Estruturado em três etapas:
1. **Dividir:** Quebrar o problema original em subproblemas menores da mesma natureza.
2. **Conquistar:** Resolver os subproblemas recursivamente (se forem pequenos o suficiente, resolve-se diretamente no caso base).
3. **Combinar:** Fundir as soluções dos subproblemas para construir a solução do problema global.

---

## 2. Análise Detalhada dos Métodos Clássicos de Referência

### 2.1. Bubble Sort (Ordenação por Flutuação)

#### Raciocínio Projetual
O Bubble Sort percorre o vetor sequencialmente, comparando pares de elementos adjacentes $(A[j], A[j+1])$ e trocando-os caso estejam fora de ordem. A cada passagem completa, o maior elemento da porção não ordenada "flutua" para o final do vetor.

#### Invariante de Laço
*Ao término da $i$-ésima iteração do laço externo, o subvetor $A[N-i \dots N-1]$ contém os $i$ maiores elementos do vetor original dispostos em suas posições finais ordenadas.*

#### Pseudocódigo com Otimização (Parada Antecipada)
```text
procedimento BubbleSort(A, N):
    para i de 0 até N - 2 faça:
        houve_troca ← falso
        para j de 0 até N - 2 - i faça:
            se A[j] > A[j + 1] então:
                trocar(A[j], A[j + 1])
                houve_troca ← verdadeiro
            fim-se
        fim-para
        se não houve_troca então:
            interromper  // Vetor já ordenado
        fim-se
    fim-para
fim-procedimento
```

#### Dedução de Complexidade
* **Pior Caso:** Vetor em ordem decrescente reversa. O laço interno executa $(N-1) + (N-2) + \dots + 1 = \frac{N(N-1)}{2}$ comparações e trocas. Complexidade de tempo: $O(N^2)$.
* **Melhor Caso:** Vetor já ordenado. Com a flag `houve_troca`, o algoritmo encerra na primeira iteração após $N-1$ comparações e 0 trocas: $\Omega(N)$.
* **Caso Médio:** $\Theta(N^2)$ comparações e movimentações.
* **Memória Auxiliar:** $O(1)$ (*in-place*).
* **Estabilidade:** Estável (não há troca se $A[j] == A[j+1]$).

---

### 2.2. Insertion Sort (Ordenação por Inserção)

#### Raciocínio Projetual
Inspirado no ato de organizar cartas de baralho na mão. O algoritmo particiona logicamente o vetor em uma porção já ordenada à esquerda e uma porção desordenada à direita. A cada passo, o primeiro elemento da porção desordenada (a "chave") é retirado e inserido na sua posição correta dentro do subvetor ordenado, deslocando os elementos maiores para a direita.

#### Invariante de Laço
*No início de cada iteração $i$ (com $i$ de $1$ a $N-1$), o subvetor $A[0 \dots i-1]$ consiste dos elementos originais que ocupavam essas posições, porém em ordem totalmente classificada.*

#### Pseudocódigo
```text
procedimento InsertionSort(A, N):
    para i de 1 até N - 1 faça:
        chave ← A[i]
        j ← i - 1
        enquanto j >= 0 e A[j] > chave faça:
            A[j + 1] ← A[j]  // Deslocamento à direita
            j ← j - 1
        fim-enquanto
        A[j + 1] ← chave
    fim-para
fim-procedimento
```

#### Dedução de Complexidade
* **Melhor Caso:** Vetor já ordenado. A condição $A[j] > \text{chave}$ falha imediatamente na primeira comparação para cada $i$. Total de comparações: $N-1$. Tempo: $\Omega(N)$.
* **Pior Caso:** Vetor em ordem decrescente. Para cada $i$, o elemento precisa ser deslocado por todo o subvetor à esquerda ($i$ comparações e deslocamentos).
  $$\sum_{i=1}^{N-1} i = \frac{N(N-1)}{2} \implies O(N^2)$$
* **Caso Médio:** $\Theta(N^2)$.
* **Memória Auxiliar:** $O(1)$ (*in-place*).
* **Estabilidade:** Estável (o laço interrompe se $A[j] \le \text{chave}$, mantendo chaves iguais na ordem relativa original).
* **Aplicação Real:** Altamente eficiente para pequenos conjuntos de dados ($N \le 30$) e vetores quase ordenados (*nearly sorted*).

---

### 2.3. Merge Sort (Ordenação por Intercalação)

#### Raciocínio Projetual
Aplica estritamente a estratégia de Divisão e Conquista:
1. **Dividir:** Calcula o ponto médio $M = \lfloor (E + D)/2 \rfloor$ e particiona o vetor em duas metades balanceadas.
2. **Conquistar:** Invoca recursivamente o Merge Sort para a metade esquerda e direita.
3. **Combinar:** Realiza a intercalação (*merge*) de dois subvetores contíguos já ordenados em um vetor auxiliar, copiando o resultado de volta.

#### Relação de Recorrência
$$T(N) = 2T\left(\frac{N}{2}\right) + \Theta(N)$$
Pelo Teorema Mestre (Caso 2, onde $a=2, b=2, d=1$ e $\log_b a = 1 = d$):
$$T(N) = \Theta(N \log N)$$

#### Pseudocódigo
```text
procedimento Merge(A, inicio, meio, fim):
    criar vetores temporários E = A[inicio ... meio] e D = A[meio+1 ... fim]
    i ← 0, j ← 0, k ← inicio
    enquanto i < tamanho(E) e j < tamanho(D) faça:
        se E[i] <= D[j] então:
            A[k] ← E[i]
            i ← i + 1
        senão:
            A[k] ← D[j]
            j ← j + 1
        fim-se
        k ← k + 1
    fim-enquanto
    copiar remanescentes de E (se houver) para A
    copiar remanescentes de D (se houver) para A
fim-procedimento

procedimento MergeSort(A, inicio, fim):
    se inicio < fim então:
        meio ← (inicio + fim) / 2
        MergeSort(A, inicio, meio)
        MergeSort(A, meio + 1, fim)
        Merge(A, inicio, meio, fim)
    fim-se
fim-procedimento
```

#### Dedução de Complexidade e Propriedades
* **Tempo:** Melhor, Médio e Pior caso são estritamente $\Theta(N \log N)$ (o particionamento é sempre balanceado e a intercalação sempre analisa todos os elementos).
* **Memória Auxiliar:** Exige $O(N)$ de memória extra para os subvetores temporários durante a intercalação.
* **Estabilidade:** Estável (assegurado pelo operador $<=$ na decisão de prioridade de `E[i]`).

---

### 2.4. Quick Sort (Ordenação Rápida)

#### Raciocínio Projetual
Também fundamentado em Divisão e Conquista, mas com a etapa de combinação vazia e o trabalho concentrado na divisão:
1. **Particionar:** Escolhe um elemento como **pivô** e rearranja o vetor de forma que todos os elementos menores ou iguais fiquem à esquerda e os maiores fiquem à direita. O pivô assume sua posição final definitiva.
2. **Conquistar:** Ordena recursivamente os subvetores à esquerda e à direita do pivô.

#### Esquema de Particionamento (Lomuto)
```text
procedimento ParticionarLomuto(A, inicio, fim):
    pivo ← A[fim]
    i ← inicio - 1
    para j de inicio até fim - 1 faça:
        se A[j] <= pivo então:
            i ← i + 1
            trocar(A[i], A[j])
        fim-se
    fim-para
    trocar(A[i + 1], A[fim])
    retornar i + 1
fim-procedimento

procedimento QuickSort(A, inicio, fim):
    se inicio < fim então:
        p ← ParticionarLomuto(A, inicio, fim)
        QuickSort(A, inicio, p - 1)
        QuickSort(A, p + 1, fim)
    fim-se
fim-procedimento
```

#### Dedução de Complexidade
* **Melhor Caso:** O pivô divide o vetor em duas metades aproximadamente iguais ($N/2$ cada) em todas as etapas:
  $$T(N) = 2T(N/2) + \Theta(N) \implies \Omega(N \log N)$$
* **Pior Caso:** Particionamento extremamente desbalanceado (ex.: escolher sempre o maior ou menor elemento, comum ao usar o último elemento como pivô em vetores já ordenados ou reversos):
  $$T(N) = T(N-1) + \Theta(N) \implies O(N^2)$$
* **Caso Médio:** $\Theta(N \log N)$ com constantes multiplicativas muito baixas devido à alta localidade de referência de cache.
* **Memória Auxiliar:** $O(\log N)$ no caso médio (pilha de chamadas de recursão) e $O(N)$ no pior caso.
* **Estabilidade:** Instável (as trocas não contíguas no particionamento podem inverter elementos idênticos).

---

## 3. Metodologia Formal de Análise Teórica (Modelo RAM & Cormen)

Para atender aos critérios de avaliação da disciplina e justificar as deduções de complexidade ($O, \Omega, \Theta$), a modelagem teórica dos algoritmos deve seguir o padrão clássico do livro do Cormen (Cap. 2).

### 3.1 O Modelo Computacional RAM (Random Access Machine)
* **Premissa:** Instruções executadas sequencialmente.
* **Custo Unitário:** Operações aritméticas básicas (`+`, `-`, `*`), atribuições (`=`), comparações condicionais (`if`) e acessos diretos à memória/vetor têm custo constante ($c_i \in O(1)$).
* **Estruturas Compostas:** Laços (`for`, `while`) e chamadas de função não são operações atômicas, mas sim a composição de $N$ passos de custo constante.

---

### 3.2 Dedução Analítica via Custos e Frequências (Exemplo: Insertion Sort)

A dedução matemática rigorosa deve mapear cada linha de código ao seu custo unitário ($c_i$) e à quantidade de vezes que é executada em função de $n$:

```c
void insertionSort(int arr[], int n) {
    int i, j, chave;                                 // c1 | 1
    for (i = 1; i < n; i++) {                        // c2 | n
        chave = arr[i];                              // c3 | n - 1
        j = i - 1;                                   // c4 | n - 1
        while (j >= 0 && arr[j] > chave) {           // c5 | sum(j=1 to n-1) t_j
            arr[j + 1] = arr[j];                     // c6 | sum(j=1 to n-1) (t_j - 1)
            j--;                                     // c7 | sum(j=1 to n-1) (t_j - 1)
        }
        arr[j + 1] = chave;                          // c8 | n - 1
    }
}
```

## 4. Matriz Comparativa Teórica

A tabela a seguir consolida o padrão de referência formal que deve ser contrastado com o método autoral:

| Algoritmo | Melhor Caso | Caso Médio | Pior Caso | Memória Auxiliar | Estável? | In-Place? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Bubble Sort** | $\Omega(N)$ | $\Theta(N^2)$ | $O(N^2)$ | $O(1)$ | Sim | Sim |
| **Insertion Sort** | $\Omega(N)$ | $\Theta(N^2)$ | $O(N^2)$ | $O(1)$ | Sim | Sim |
| **Selection Sort** | $\Omega(N^2)$ | $\Theta(N^2)$ | $O(N^2)$ | $O(1)$ | Não | Sim |
| **Merge Sort** | $\Omega(N \log N)$ | $\Theta(N \log N)$ | $O(N \log N)$ | $O(N)$ | Sim | Não |
| **Quick Sort** | $\Omega(N \log N)$ | $\Theta(N \log N)$ | $O(N^2)$ | $O(\log N)$ | Não | Sim |

---

## 5. Diretrizes para a Concepção e Modelagem do Método Autoral (TP1)

Para atender a todos os requisitos do TP1 de Análise e Projeto de Algoritmos, o desenvolvimento do método autoral deve seguir as seguintes orientações estruturais:

### 5.1. O Que Torna o Algoritmo Válido e Autoral
* **Não é autoral:** Renomear variáveis de um Bubble Sort, inverter o sentido do laço de um Insertion Sort, ou alternar a varredura da esquerda para a direita de um Selection Sort.
* **É aceito e valorizado:**
  1. *Estratégias Híbridas não triviais:* Ex.: Particionamento adaptativo que comuta para ordenação por janelas deslizantes ou inserção balanceada com base na entropia/inversões detectadas.
  2. *Decomposições em Múltiplos Ponteiros / Baldes Locais:* Algoritmos com varreduras bidirecionais combinadas a inserção seletiva ou particionamento multinível.
  3. *Mecanismos com Invariantes Claros:* O algoritmo pode até ser $O(N^2)$, desde que sua mecânica possua motivação teórica fundamentada e prova analítica formal.

### 5.2. Roteiro Metodológico para o Relatório/Apresentação

```
[1. Intuição e Metáfora]
         │
         ▼
[2. Invariantes de Laço e Corretude] (Inicialização, Manutenção, Término)
         │
         ▼
[3. Dedução Matemática Formal] (Melhor, Médio e Pior Caso; Somatórios e Recorrências)
         │
         ▼
[4. Implementação e Validação] (Sanidade: ordenado, invertido, duplicados, bordas)
         │
         ▼
[5. Benchmarking Rigoroso] (Comparações e Movimentações vs. Tempo Real)
         │
         ▼
[6. Declaração Obrigatória de Autoria e IA]
```

### 5.3. Modelo da Seção Obrigatória de Declaração de IA
Toda entrega que empregar ferramentas de IA deve incluir o preenchimento desta declaração:

```markdown
### Declaração de Uso de Ferramentas de IA
1. **Ferramenta/Modelo Utilizado:** (Ex: Gemini 3 Flash / Claude 3.5 Sonnet / ChatGPT)
2. **Motivo do Uso:** (Ex: Auxílio na instrumentação do benchmark, formulação dos casos de teste de estresse ou síntese dos invariantes matemáticos)
3. **Forma de Utilização:** (Ex: Foi solicitado ao modelo scripts em Python para plotagem de curvas assintóticas e revisão sintática de fórmulas LaTeX)
4. **Modificações Realizadas:** (Ex: O código gerado foi adaptado para respeitar as interfaces do student_template.py e o cálculo analítico do somatório foi recalculado manualmente)
5. **Validação do Resultado:** (Ex: Todos os casos de teste foram executados via test_suite.py e a prova de convergência foi verificada pelo autor)
```

---

## 6. Referências e Videoaulas de Apoio (UNIVESP)

1. **Aula 1: Algoritmos Clássicos de Ordenação I (UNIVESP - Prof. Marcelo G. Manzato)**
   * **Vídeo:** [https://www.youtube.com/watch?v=a64VDyKjnwA](https://www.youtube.com/watch?v=a64VDyKjnwA)
   * **Foco:** Apresentação do problema de ordenação, conceitos fundamentais e métodos elementares/iterativos ($O(N^2)$), com ênfase no **Bubble Sort** e no **Insertion Sort** (e comparação intuitiva com o Selection Sort).
   * **Abordagem:** Raciocínio baseado em varreduras sequenciais, trocas de elementos adjacentes versus inserção ordenada e análise de melhor/pior caso com paradas antecipadas.

2. **Aula 2: Algoritmos Clássicos de Ordenação II (UNIVESP - Prof. Marcelo G. Manzato)**
   * **Vídeo:** [https://www.youtube.com/watch?v=y7aMS3RzYlU](https://www.youtube.com/watch?v=y7aMS3RzYlU)
   * **Foco:** Algoritmos eficientes baseados no paradigma de **Divisão e Conquista** ($O(N \log N)$), detalhando o **Merge Sort** e o **Quick Sort**.
   * **Abordagem:** Divisão recursiva do vetor, processo de intercalação/fusão ordenada (*merge*), particionamento in-place em torno de um pivô (procedimento *partition*) e o impacto da escolha do pivô no desempenho.

3. **Aula 3: Projeto e Análise de Algoritmos - Algoritmos de Ordenação (UNIVESP - Prof. Cristhof Johann Roosen Runge)**
   * **Vídeo:** [https://www.youtube.com/watch?v=xG-yi7wzaCI](https://www.youtube.com/watch?v=xG-yi7wzaCI)
   * **Foco:** Tratamento analítico rigoroso, dedução formal de complexidade assintótica ($O$, $\Omega$, $\Theta$), formulação de **Invariantes de Laço** (*Loop Invariants*) para prova de corretude e análise de relações de recorrência via Árvore de Recorrência e Teorema Mestre.