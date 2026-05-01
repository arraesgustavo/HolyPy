# TOKENS

## Tipos de Dados

| Tipo           | Símbolo ‘C’  | Símbolo ‘HolyPy’ | Analisador Léxico | Token ‘C’ | Token ‘HolyPy’ |
| -------------- | ------------ | ---------------- | ----------------- | --------- | -------------- |
| Tipos de Dados | -            | let              | Palavra Reservada | -         | T_LET          |
| Tipos de Dados | int          | i8 à i64         | Palavra Reservada | T_INT     | T_INT          |
| Tipos de Dados | Unsigned Int | u8 à u64         | Palavra Reservada | T_UINT    | T_UINT         |
| Tipos de Dados | float        | f32              | Palavra Reservada | T_FLOAT   | T_FLOAT        |
| Tipos de Dados | double       | f64              | Palavra Reservada | T_DOUBLE  | T_DOUBLE       |
| Tipos de Dados | char         | char             | Palavra Reservada | T_CHAR    | T_CHAR         |
| Tipos de Dados | bool         | bool             | Palavra Reservada | T_BOOL    | T_BOOL         |


- **T_LET :** Identifica a palavra-chave `let`, que indica o início de uma de variável. Na linguagem HolyPy, a construção com `let` permite que a anotação do tipo seja opcional (ex: podendo ser `let x: i32 = 5` com tipo explícito, ou apenas `let x = 5` usando tipagem indefinida).
- **T_INT, T_UINT, T_FLOAT:** HolyPy adota a especificação específica de bits (ex: `i8` até `i64`, `u8` até `u64`, `f32`, `f64`). O Analisador Léxico vai agrupar essas variações em outros tokens (`T_INT`, `T_UINT`, `T_FLOAT`) para simplificar a criação das regras gramaticais, enquanto o lexema será salvo como atributo do token para o Analisador Semântico.
- **T_CHAR e T_BOOL:** Tratam de maneira normal as variáveis char e bool.

## Variáveis

| Tipo     | Símbolo ‘C’  | Símbolo ‘HolyPy’ | Analisador Léxico | Token ‘C’ | Token ‘HolyPy’ |
| -------- | ------------ | ---------------- | ----------------- | --------- | -------------- |
| Variável | letra        | letra            | Identificador     | T_ID      | T_ID           |
| Variável | letra+numero | letra+numero     | Identificador     | T_ID      | T_ID           |
| Literal  | número       | número           | Literal Numérico  | T_NUM     | T_NUM          |

- **T_ID:** Representa os identificadores (nomes de variáveis, rotinas e funções). No HolyPy, a regra é que o identificador pode mesclar letras e números sem problemas, mas não pode ser iniciado por um número.
- **T_NUM:** Representa literais numéricos puros agrupados em um único token genérico.

## Operadores Relacionais e de Atribuição

| Tipo       | Símbolo ‘C’ | Símbolo ‘HolyPy’ | Analisador Léxico | Token ‘C’ | Token ‘HolyPy’ |
| ---------- | ----------- | ---------------- | ----------------- | --------- | -------------- |
| Atribuição | =           | =                | Op. de Atribuição | T_ATR     | T_ATR          |
| Relacional | ==          | =                | Op. Relacional    | T_EQ      | T_EQ           |
| Relacional | !=          | !=               | Op. Relacional    | T_NEQ     | T_NEQ          |
| Relacional | >           | >                | Op. Relacional    | T_GT      | T_GT           |
| Relacional | <           | <                | Op. Relacional    | T_LT      | T_LT           |
| Relacional | >=          | >=               | Op. Relacional    | T_GEQ     | T_GEQ          |
| Relacional | <=          | <=               | Op. Relacional    | T_LEQ     | T_LEQ          |

- No HolyPy, os operadores determinam as interações booleanas. O símbolo `=` possui dois tipos de uso: atua como `T_ATR` e como `T_EQ`, sendo a diferença entre os dois ditada pelas regras implementadas no Código Sintático. Outros permanecem iguais ao C.

## Operadores Lógicos

| Tipo   | Símbolo ‘C’ | Símbolo ‘HolyPy’ | Analisador Léxico | Token ‘C’ | Token ‘HolyPy’ |
| ------ | ----------- | ---------------- | ----------------- | --------- | -------------- |
| Lógico | &&          | and              | Operador Lógico   | T_AND     | T_AND          |
| Lógico | \|\|        | or               | Operador Lógico   | T_OR      | T_OR           |
| Lógico | !           | not              | Operador Lógico   | T_NOT     | T_NOT          |

- HolyPy não utiliza os operadores tradicionais de C como `&&` ou `||`. Eles são substituidos pelas palavras `and`, `or` e `not`, o que facilita  o escaneamento na construção do regex do projeto e dá fluidez de letura ao dev. O gerador do AST os processará em `T_AND`, `T_OR`, e `T_NOT`.

## Operadores Aritméticos

| Tipo       | Símbolo ‘C’ | Símbolo ‘HolyPy’ | Analisador Léxico | Token ‘C’ | Token ‘HolyPy’ |
| ---------- | ----------- | ---------------- | ----------------- | --------- | -------------- |
| Aritmético | +           | +                | Op. Aritmético    | T_PLUS    | T_PLUS         |
| Aritmético | -           | -                | Op. Aritmético    | T_MINUS   | T_MINUS        |
| Aritmético | *           | *                | Op. Aritmético    | T_MUL     | T_MUL          |
| Aritmético | /           | /                | Op. Aritmético    | T_DIV     | T_DIV          |
| Aritmético | %           | mod              | Op. Aritmético    | T_MOD     | T_MOD          |

- Os operadores seguem o padrão matemático tradicional. O operador de resto da divisão `%` comum em C é substituído pela palavra reservada `mod` no HolyPy, de maneira a alinhar a sintaxe a uma leitura mais descritiva.

## Símbolos Especiais e Delimitadores

| Tipo        | Símbolo ‘C’ | Símbolo ‘HolyPy’ | Analisador Léxico | Token ‘C’ | Token ‘HolyPy’ |
| ----------- | ----------- | ---------------- | ----------------- | --------- | -------------- |
| Delimitador | {           | {                | Delimitador       | T_LBRACE  | T_LBRACE       |
| Delimitador | }           | }                | Delimitador       | T_RBRACE  | T_RBRACE       |
| Delimitador | (           | (                | Delimitador       | T_LPAREN  | T_LPAREN       |
| Delimitador | )           | )                | Delimitador       | T_RPAREN  | T_RPAREN       |
| Delimitador | :           | :                | Símbolo Especial  | T_COLON   | T_COLON        |
| Delimitador | ,           | ,                | Símbolo Especial  | T_COMMA   | T_COMMA        |
| Delimitador | ->          | ->               | Símbolo Especial  | -         | T_ARROW        |
| Diretiva    | #           | !                | Símbolo Especial  | T_POUND   | T_BANG         |
| Comentário  | // ou /* */ | #                | Símbolo Especial  | T_COMMENT | T_COMMENT      |
| Delimitador | "           | "                | Símbolo Especial  | T_STR     | T_STR          |

- **Diretivas (`!`):** No HolyPy, o símbolo de exclamação `!` substitui o `#` do C para indicar funções de diretiva.
- **Comentários (`#`):** Os comentários são iniciados na linha com o caractere `#`, igual ao Python.
- **Parênteses e Chaves:** Os comandos de bloco, como `if`, não precisam do uso de parênteses para mostrar as condições, mas precisam que o bloco termine entre chaves `{ }`. Porém, `(` e `)` ainda cumprem sua função no mapeamento das chamadas e assinaturas de funções, além de uso matemático.
- **Anotações de tipo (`:` e `->`):** O símbolo de dois pontos `:` tem o papel de expressar a vinculação de um tipo a uma variável (`let x: i32`). Já a "seta" `->` mapeia o tipo de retorno na chamada de uma função.

## Palavras Reservadas

| Tipo               | Símbolo ‘C’ | Símbolo ‘HolyPy’ | Analisador Léxico | Token ‘C’   | Token ‘HolyPy’ |
| ------------------ | ----------- | ---------------- | ----------------- | ----------- | -------------- |
| Estrutura de Fluxo | if          | if               | Palavra Reservada | T_IF        | T_IF           |
| Estrutura de Fluxo | else        | else             | Palavra Reservada | T_ELSE      | T_ELSE         |
| Estrutura de Fluxo | for / while | cycle            | Palavra Reservada | T_FOR/WHILE | T_CYCLE        |
| Controle de Fluxo  | break       | free             | Palavra Reservada | T_BREAK     | T_BREAK        |
| Tipo Nulo/Void     | void        | u0               | Palavra Reservada | T_VOID      | T_U0           |
| Declaração Função  | -           | fn               | Palavra Reservada | -           | T_FN           |
| Retorno            | return      | return           | Palavra Reservada | T_RETURN    | T_RETURN       |
| Entrada/Saída      | printf      | speak            | Palavra Reservada | T_PRINTF    | T_SPEAK        |
| Entrada/Saída      | scanf       | receive          | Palavra Reservada | T_SCANF     | T_RECEIVE      |
| Importação         | include     | import           | Palavra Reservada | T_INCLUDE   | T_IMPORT       |
| Memória            | malloc      | chain            | Palavra Reservada | T_MALLOC    | T_CHAIN        |
| Memória            | free        | unchain          | Palavra Reservada | T_FREE      | T_UNCHAIN      |
| Baixo Nível        | asm         | asm              | Palavra Reservada | T_ASM       | T_ASM          |
| Booleano           | true        | true             | Palavra Reservada | T_TRUE      | T_TRUE         |
| Booleano           | false       | false            | Palavra Reservada | T_FALSE     | T_FALSE        |

**Explicação das Palavras Reservadas**

- **Código de Máquina Inline (`asm`):** Permite a inserção de instruções Assembly dentro do código, sendo útil para operações de baixíssimo nível em modos `!kernel` ou `!embedded`.
- **Gerenciamento de Memória (`chain` / `unchain`):** No HolyPy, a alocação dinâmica é tratada de forma semântica. `chain` (corrente) aloca um bloco de memória vinculando-o a um ponteiro, enquanto `unchain` libera essa corrente de dados (igual ao `malloc` e `free` do C).
- **Entrada e Saída (`speak` / `receive`):** Substituem as funções nativas de IO do C .
- **Valores Booleanos (`true` / `false`):** Adição dos literais lógicos explícitos para compor expressões com o tipo `bool`.
- **Repetição Universal (`cycle`):** Os laços tradicionais como `for` e `while` são encapsulados em uma única chamada de looping chamada `cycle`. O escopo é fechado normalmente e interrompido por condições internas com `free`.
- **Tipo de Retorno Nulo (`u0`):** O equivalente ao `void` das linguagens estruturadas. A nomenclatura adota as regras da tipagem baseada em bits do HolyPy (`i8`, `u32`), representando perfeitamente a "ausência de valor" como zero bits.
- **Importação de Módulos (`import`):** Uma evolução do `#include` do C, atuando como palavra nativa sem necessitar sintaxe de diretiva extra para trazer bibliotecas e arquivos ao escopo.
- **Assinatura de Funções (`fn`):** Delimita a declaração de novos blocos lógicos executáveis, seguindo o molde de *Rust*.

## Expressões Regulares 

Abaixo estão formalizadas as expressões regulares utilizadas pelo Analisador Léxico para o reconhecimento e validação de cada token da linguagem HolyPy:

| Categoria | Token | Expressão Regular | Exemplo de Lexema |
| :--- | :--- | :--- | :--- |
| **Identificadores** | `T_ID` | `[A-Za-z_][A-Za-z0-9_]*` | `variavel1`, `_soma` |
| **Literais Numéricos** | `T_NUM` | `[+-]?(0[xX][0-9A-Fa-f]+\|((([0-9]+(\.[0-9]*)?)\|(\.[0-9]+))([eE][+-]?[0-9]+)?))` | `42`, `-3.14`, `+2E10`, `0x1000` |
| **Literal de Caractere** | `T_CHAR_LIT` | `'(\\.\|[^'\\])'` | `'a'`, `'\n'` |
| **Literais em String** | `T_STR` | `"(\\.\|[^"\\])*"` | `"Ola"`, `"linha\n"` |
| **Comentários** | `T_COMMENT` | `#.*` | `# Isto é um comentário` |
| **Atribuição / Igualdade** | `T_ATR` / `T_EQ` | `=` \| `==` | `=`, `==` |
| **Operadores Relacionais** | `T_NEQ` | `!=` | `!=` |
| **Operadores Relacionais** | `T_GT`, `T_GEQ` | `>` \| `>=` | `>`, `>=` |
| **Operadores Relacionais** | `T_LT`, `T_LEQ` | `<` \| `<=` | `<`, `<=` |
| **Operadores Aritméticos** | `T_PLUS`, `T_MINUS` | `\+` \| `-` | `+`, `-` |
| **Operadores Aritméticos** | `T_MUL`, `T_DIV` | `\*` \| `/` | `*`, `/` |
| **Operadores Aritméticos** | `T_MOD` | `mod` | `mod` |
| **Operadores Lógicos** | `T_AND`, `T_OR`, `T_NOT` | `and` \| `or` \| `not` | `and`, `or`, `not` |
| **Delimitadores** | `T_LPAREN`, `T_RPAREN` | `\(` \| `\)` | `(`, `)` |
| **Delimitadores** | `T_LBRACE`, `T_RBRACE` | `\{` \| `\}` | `{`, `}` |
| **Delimitadores** | `T_LBRACKET`, `T_RBRACKET` | `\[` \| `\]` | `[`, `]` |
| **Símbolos / Pontuação** | `T_COLON`, `T_COMMA` | `:` \| `,` | `:`, `,` |
| **Símbolos / Pontuação** | `T_SEMI`, `T_DOT` | `;` \| `\.` | `;`, `.` |
| **Símbolos / Pontuação** | `T_ARROW`, `T_BANG` | `->` \| `!` | `->`, `!` |
| **Tipos Estruturais** | `T_INT` | `i(8\|16\|32\|64)` | `i32`, `i8` |
| **Tipos Estruturais** | `T_UINT` | `u(8\|16\|32\|64)` | `u16`, `u64` |
| **Tipos Estruturais** | `T_FLOAT` | `f(32\|64)` | `f32`, `f64` |
| **Tipos Estruturais** | `T_CHAR`, `T_BOOL`, `T_U0` | `char` \| `bool` \| `u0` | `char`, `u0` |
| **Palavras Reservadas** | Fluxo e Funções | `let` \| `fn` \| `if` \| `else` \| `cycle` \| `free` \| `return` | `let`, `cycle`, `fn` |
| **Palavras Reservadas** | I/O e Memória | `speak` \| `receive` \| `chain` \| `unchain` \| `import` \| `asm` | `speak`, `chain` |
| **Palavras Reservadas** | Constantes Booleanas | `true` \| `false` | `true`, `false` |


Algumas elucidações sobre as expressões mais complexas:

#### T_NUM

- O [+-]? no início é o sinal opcional — aceita +, - ou nada.
- Depois, a expressão se divide em dois ramos (com |):
  - Ramo 1 0[xX][0-9A-Fa-f]+: Começa obrigatoriamente com 0x ou 0X, seguido de um ou mais digitos hexa.
  - Ramo 2 (([0-9]+(\.[0-9]*)?)|(\.[0-9]+))([eE][+-]?[0-9]+)?, também há subdvisões:
    - [0-9]+(\.[0-9]*)? → inteiro com parte decimal opcional: aceita 42, 3.14, e até 3. (ponto sem dígitos depois)
    - \.[0-9]+ → começa com ponto obrigatório: aceita .5, .001
  - Outro ramo é opcional (([eE][+-]?[0-9]+)?), sendo associado à expoente.
  
#### T_CHAR_LIT

Abre e fecha com aspas simples ' '. O conteúdo entre elas aceita um dos dois padrões:

\\. → uma barra invertida seguida de qualquer caractere: captura sequências de escape como '\n', '\t', '\\', '\''
[^'\\] → qualquer caractere que não seja ' nem \: captura 'a', 'Z', '@'

Como não há * ou +, a expressão aceita somente um caractere.

#### T_STR

Quase igual ao T_CHAR_LIT, porém:

- Usa aspas duplas " " em vez de simples
- O * no lugar do implícito "um único" permite zero ou mais caracteres — strings vazias "" são válidas

Com o [^"\\] garantimos que uma aspa dupla dentro da string não o feche e que uma barra invertida não quebre o parser.

### Explicações das expressões regulares

* **Identificadores**: Define nomes de variáveis e funções, exigindo início com letra ou underscore seguido de alfanuméricos.
* **Literais Numéricos**: Captura números inteiros, decimais e hexadecimais, suportando sinal opcional e notação científica.
* **Literal de Caractere**: Isola um único caractere entre aspas simples, permitindo sequências de escape.
* **Literais em String**: Captura cadeias de texto entre aspas duplas, aceitando caracteres de escape internos.
* **Comentários**: Ignora qualquer texto na linha a partir do símbolo (#).
* **Atribuição / Igualdade**: Diferencia a atribuição de valor em variáveis da comparação lógica de igualdade.
* **Operadores Relacionais (`!=`)**: Avalia a diferença lógica entre dois valores.
* **Operadores Relacionais (`>`, `>=`)**: Avalia se um valor é estritamente maior ou maior/igual a outro.
* **Operadores Relacionais (`<`, `<=`)**: Avalia se um valor é estritamente menor ou menor/igual a outro.
* **Operadores Aritméticos (`+`, `-`)**: Executa adições e subtrações matemáticas ou define a polaridade do número.
* **Operadores Aritméticos (`*`, `/`)**: Executa multiplicações e divisões matemáticas.
* **Operadores Aritméticos (`mod`)**: Obtém o resto de uma operação de divisão inteira.
* **Operadores Lógicos**: Mapeia as operações de conjunção, disjunção e negação booleana.
* **Delimitadores (`()`)**: Agrupa expressões matemáticas, condições ou isola argumentos de funções.
* **Delimitadores (`{}`)**: Define o escopo e agrupa blocos de código para funções, laços e condicionais.
* **Delimitadores (`[]`)**: Acessa índices de estruturas posicinais e arrays.
* **Símbolos / Pontuação (`:`, `,`)**: Especifica tipagem explícita e separa múltiplos argumentos ou elementos.
* **Símbolos / Pontuação (`;`, `.`)**: Encerra um comando explícito ou acessa membros de uma estrutura.
* **Símbolos / Pontuação (`->`, `!`)**: Indica o tipo de retorno da assinatura de uma função ou atua como modificador/macro.
* **Tipos Estruturais (`i8-64`)**: Define inteiros com sinal atrelados diretamente a uma dimensão de bits.
* **Tipos Estruturais (`u8-64`)**: Define inteiros sem sinal atrelados diretamente a uma dimensão de bits.
* **Tipos Estruturais (`f32-64`)**: Define variáveis de ponto flutuante com precisão simples ou dupla.
* **Tipos Estruturais (`char`, `bool`, `u0`)**: Define primitivos singulares para texto, estado lógico e tipo de retorno vazio.
* **Palavras Reservadas (Fluxo e Funções)**: Mapeia as palavras-chave para estruturas de controle, laços e definição de escopo base.
* **Palavras Reservadas (I/O e Memória)**: Mapeia as chamadas nativas de entrada/saída, alocação em heap e blocos de assembly embutido.
* **Palavras Reservadas (Constantes Booleanas)**: Reconhece os estados primitivos absolutos de verdadeiro e falso.

## Regras de Produção

| Nome | Regra |
| :--- | :--- |
| **Condicional** | `T_IF condicao T_LBRACE comandos+ T_RBRACE (T_ELSE T_LBRACE comandos+ T_RBRACE)?` |
| **Repetição** | `T_CYCLE T_LBRACE comandos+ T_RBRACE (T_BREAK)?` |
| **DecVariável** | `T_LET T_ID (T_COLON tipos)? (T_ATR (caracteres \| opAritmetica \| opLogica))?` |
| **Atribuição** | `T_ID T_ATR (caracteres \| opAritmetica \| opLogica) T_SEMI?` |
| **DecFunção** | `T_FN T_ID T_LPAREN parametros T_RPAREN T_ARROW tipos T_LBRACE comandos+ T_RETURN (caracteres \| T_U0) T_RBRACE` |
| **CallFunção** | `T_ID T_LPAREN parametros T_RPAREN` |
| **Speak** | `T_SPEAK T_LPAREN (caracteres \| T_COMMA \| T_STR \| T_ID)* T_RPAREN` |
| **Receive** | `T_RECEIVE T_LPAREN T_ID T_RPAREN` |
| **Comentário** | `T_COMMENT` |
| **Chain** | `T_CHAIN T_LPAREN (numero \| T_ID) T_RPAREN` |
| **Unchain** | `T_UNCHAIN T_LPAREN T_ID T_RPAREN` |
| **Bloco ASM** | `T_ASM T_LBRACE (T_STR)+ T_RBRACE` |
| **Indexação** | `T_ID T_LBRACKET (numero \| T_ID \| opAritmetica) T_RBRACKET` |
| **Acesso a Membro** | `T_ID T_DOT T_ID` |
| **DecPonteiro** | `T_LET T_ID T_COLON T_STAR tipos (T_ATR (numero \| T_ID))?` |
| **Literal Booleano** | `T_TRUE \| T_FALSE` |

## Explicação das regras de produção

| Nome | Finalidade | Exemplo de Uso |
|------|------------|----------------|
| **Programa** | Define a unidade sintática raiz: sequência de diretivas, declarações e funções. | !kernel<br>import stdio<br>fn main() -> i32 { return 0 } |
| **Diretiva de Modo (T_BANG)** | Ativa modo especial de compilação/executão por diretiva (!). | !embedded |
| **Importação (T_IMPORT)** | Importa módulos/arquivos para o escopo do programa. | import math |
| **Declaração de Função (T_FN)** | Declara função com nome, parâmetros, tipo de retorno e bloco. | fn soma(a: i32, b: i32) -> i32 { return a + b } |
| **Parâmetros de Função** | Define lista de parâmetros tipados (ou lista vazia) em assinatura/chamada. | fn inc(x: i32) -> i32 { return x + 1 } |
| **Tipo Estrutural (T_INT/T_UINT/T_FLOAT/T_CHAR/T_BOOL/T_U0)** | Restringe tipos válidos da linguagem como tokens próprios (não T_ID). | let x: i32 = 10<br>fn noop() -> u0 { return u0 } |
| **Bloco (T_LBRACE ... T_RBRACE)** | Delimita escopo de comandos. | if x > 0 { speak("ok") } |
| **Declaração de Variável (T_LET)** | Declara variável com tipagem opcional e inicialização opcional. | let a<br>let b: f64 = 3.14 |
| **Atribuição (T_ATR)** | Atribui valor a identificador já declarado. | total = total + 1 |
| **Chamada de Função** | Invoca rotina com argumentos posicionais. | soma(2, 3) |
| **Retorno (T_RETURN)** | Finaliza função retornando expressão compatível com tipo de retorno. | return resultado |
| **Condicional (T_IF / T_ELSE)** | Executa bloco condicionalmente, com ramo alternativo opcional. | if n >= 0 { speak("pos") } else { speak("neg") } |
| **Repetição (T_CYCLE)** | Executa bloco de repetição; parada por condição interna e/ou free. | cycle { if i >= 10 { free } i = i + 1 } |
| **Interrupção de Laço (T_BREAK via free)** | Interrompe laço cycle. | free |
| **Saída (T_SPEAK)** | Emite dados para saída padrão. | speak("Soma:", total) |
| **Entrada (T_RECEIVE)** | Lê valor de entrada para variável alvo. | receive(x) |
| **Expressão Relacional** | Compara operandos com =, ==, !=, >, <, >=, <=. | if a <= b { ... } |
| **Expressão Lógica** | Combina condições com and, or, not. | if not erro and ativo { ... } |
| **Expressão Aritmética** | Realiza operações +, -, *, /, mod. | media = soma / n |
| **Literal Numérico (T_NUM)** | Aceita inteiro/float com sinal opcional, hexadecimal e expoente. | -42<br>+2.5e3<br>0xFF |
| **Literal de Caractere (T_CHAR_LIT)** | Representa um caractere simples ou escape. | 'a'<br>'\\n' |
| **Literal de String (T_STR)** | Representa sequência textual com escapes válidos. | "linha\\n"<br>"aspas: \"ok\"" |
| **Identificador (T_ID)** | Nome de variável/função iniciado por letra ou _. | _tmp1 |
| **Palavra Reservada vs Identificador** | Garante prioridade de keywords/tipos sobre T_ID para evitar colisão. | if (keyword), não identificador |
| **Operadores Compostos (prioridade léxica)** | Garante casamento de ->, !=, >=, <=, == antes dos simples. | fn f() -> i32 { return 0 } |
| **Delimitador de Array ([ ])** | Permite indexação/acesso por posição. | v[0] |
| **Acesso a Membro (.)** | Permite seleção de membro/campo de estrutura/objeto. | obj.campo |
| **Separadores de Comando (; e quebra de linha)** | Permite separação explícita (quando necessário) | let x: i32 = 1; let y: i32 = 2 |
| **Comentário de Linha (T_COMMENT)** | Ignora texto após # até fim da linha. | # comentário |

