# TOKENS

## Tipos de Dados

| Tipo           | Símbolo ‘C’   | Símbolo ‘HolyPy’ | Analisador Léxico | Token ‘C’ | Token ‘HolyPy’ |
|----------------|--------------|------------------|-------------------|----------|----------------|
| Tipos de Dados | -            | let              | Palavra Reservada | -        | T_LET          |
| Tipos de Dados | int          | i8 à i64         | Palavra Reservada | T_INT    | T_INT          |
| Tipos de Dados | Unsigned Int | u8 à u64         | Palavra Reservada | T_UINT   | T_UINT         |
| Tipos de Dados | float        | f32, f64         | Palavra Reservada | T_FLOAT  | T_FLOAT        |
| Tipos de Dados | char         | char             | Palavra Reservada | T_CHAR   | T_CHAR         |
| Tipos de Dados | bool         | bool             | Palavra Reservada | T_BOOL   | T_BOOL         |

**Explicação dos Tokens de Tipos de Dados**

A tabela acima mapeia as palavras reservadas responsáveis pelos tipos e declaração de variáveis no compilador HolyPy. 

- **T_LET :** Identifica a palavra-chave `let`, que indica o início de uma de variável. Na linguagem HolyPy, a construção com `let` permite que a anotação do tipo seja opcional (ex: podendo ser `let x: i32 = 5` com tipo explícito, ou apenas `let x = 5` usando tipagem indefinida).
- **T_INT, T_UINT, T_FLOAT:** HolyPy adota a especificação explícita de bits (ex: `i8` até `i64`, `u8` até `u64`, `f32`, `f64`). O Analisador Léxico agrupará essas variações em outros tokens (`T_INT`, `T_UINT`, `T_FLOAT`) para simplificar a criação das regras gramaticais, enquanto o lexema será salvo como atributo do token para o Analisador Semântico.
- **T_CHAR e T_BOOL:** Tratam de maneira normal as variáveis char e bool.

## Variáveis

| Tipo           | Símbolo ‘C’  | Símbolo ‘HolyPy’ | Analisador Léxico | Token ‘C’ | Token ‘HolyPy’ |
|----------------|--------------|------------------|-------------------|-----------|----------------|
| Variável       | letra        | letra            | Identificador     | T_ID      | T_ID           |
| Variável       | letra+numero | letra+numero     | Identificador     | T_ID      | T_ID           |
| Literal        | número       | número           | Literal Numérico  | T_NUM     | T_NUM          |

**Explicação dos Tokens de Variáveis**

- **T_ID:** Representa os identificadores (nomes de variáveis, rotinas e funções). No HolyPy, a regra é que o identificador pode mesclar letras e números sem problemas, mas não pode ser iniciado por um número.
- **T_NUM:** Representa literais numéricos puros agrupados em um único token genérico. Depois, a árvore gramatical validará se esse literal se adequa a contextos de `i32`, `f64`, etc.

## Operadores Relacionais e de Atribuição

| Tipo           | Símbolo ‘C’  | Símbolo ‘HolyPy’ | Analisador Léxico | Token ‘C’ | Token ‘HolyPy’ |
|----------------|--------------|------------------|-------------------|-----------|----------------|
| Atribuição     | =            | =                | Op. de Atribuição | T_ATR     | T_ATR          |
| Relacional     | ==           | =                | Op. Relacional    | T_EQ      | T_EQ           |
| Relacional     | !=           | !=               | Op. Relacional    | T_NEQ     | T_NEQ          |
| Relacional     | >            | >                | Op. Relacional    | T_GT      | T_GT           |
| Relacional     | <            | <                | Op. Relacional    | T_LT      | T_LT           |
| Relacional     | >=           | >=               | Op. Relacional    | T_GEQ     | T_GEQ          |
| Relacional     | <=           | <=               | Op. Relacional    | T_LEQ     | T_LEQ          |

**Explicação dos Operadores Relacionais**

- No HolyPy, os operadores determinam as interações booleanas. O símbolo `=` possui dois tipos de uso: atua como `T_ATR` e como `T_EQ`, sendo a diferença entre os dois ditada pelas regras implementadas no Código Sintático. Outros permanecem iguais ao C.

## Operadores Lógicos

| Tipo           | Símbolo ‘C’  | Símbolo ‘HolyPy’ | Analisador Léxico | Token ‘C’ | Token ‘HolyPy’ |
|----------------|--------------|------------------|-------------------|-----------|----------------|
| Lógico         | &&           | and              | Operador Lógico   | T_AND     | T_AND          |
| Lógico         | \|\|         | or               | Operador Lógico   | T_OR      | T_OR           |
| Lógico         | !            | not              | Operador Lógico   | T_NOT     | T_NOT          |

**Explicação dos Operadores Lógicos**

- HolyPy não utiliza os operadores tradicionais de C como `&&` ou `||`. Eles são substituidos pelas palavras `and`, `or` e `not`, o que facilita  o escaneamento na construção do regex do projeto e dá fluidez de letura ao dev. O gerador do AST os processará em `T_AND`, `T_OR`, e `T_NOT`.