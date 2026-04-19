# Especificação do Trabalho - Parte 01

**Ministério da Educação**
Universidade Federal de Itajubá
Criada pela Lei nº 10.435, 24/04/2002

**Engenharia de Computação**
ECOM06A – Compiladores
*Profª. Thatyana de Faria Piola Seraphim*

---

## 1 Objetivos do Trabalho

Este trabalho tem por objetivos: criar, desenvolver um analisador léxico e um analisador sintático para uma linguagem de programação ou qualquer outro tipo de linguagem.

O trabalho poderá ser feito individual ou em dupla.

---

## 2 Características da Linguagem

Caso a linguagem a ser desenvolvida seja natural, as regras da linguagem são criadas de acordo com as definições dos alunos.

Se a linguagem a ser desenvolvida for linguagem de programação, esta deverá apresentar as seguintes características:

1. Suporte dos tipos de dados: inteiro, real, caractere.
2. Os comandos a serem tratados são:
   - Comandos de atribuição.
   - Comandos de entrada e saída.
   - Comandos condicionais.
   - Comandos de repetição.
3. Operadores relacionais (`=`, `>=`, `<=`, `>`, `<`, `!=`).
4. Operadores lógicos (`and`, `or`, `not`).
5. Operadores aritméticos (`+`, `-`, `*`, `/`, `mod`).
6. Símbolos especiais (`. , : ; ( ) { }`).
7. Blocos de comandos delimitados por `begin`/`end` ou `{ }`.
8. Lista de palavras reservadas.

---

## 3 Documentação

Deverá ser entregue até o dia **06/05/2025** em formato digital. O documento texto a ser entregue deverá conter:

1. As expressões regulares definidas para reconhecimento de cada *token*.
2. Os autômatos finitos determinísticos (AFDs) obtidos a partir das expressões regulares. Caso tenha obtido um autômato finito não determinístico (AFN), este deverá ser apresentado, assim como o AFN-estendido correspondente, obtido a partir do emprego do método de Thompson.
3. Definição, declaração e explicação detalhada das produções (regras) utilizadas para o reconhecimento dos comandos e operadores definidos.

---

## 4 Apresentação

No dia **07/05/2025** cada grupo fará uma breve apresentação do trabalho, com duração de no máximo 10 minutos. Deverá ser brevemente exposta a documentação do trabalho, destacando as principais dificuldades encontradas no desenvolvimento dos analisadores léxico e sintático.

---

## 5 Avaliação

O trabalho terá um total de **10 pontos**, onde **05 pontos** serão referentes à documentação apresentada e os demais **05 pontos** serão atribuídos à apresentação a ser realizada. A nota da documentação será a mesma para todos os componentes do grupo e a nota da apresentação será individual para cada aluno.
