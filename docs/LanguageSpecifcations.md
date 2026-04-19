| **ESPECIFICAÇÕES GENÉRICAS**                                                                                                        |
| --------------------------------------------------------------------------------------------------------------------------------- |
| Linguagem híbrida High-level & Low-level                            |
| Sintaxe Python-like com referências estruturais e tipos de C.                                                                     |
| Sem necessidade de ponto e vírgula no final dos comandos (fim do comando pela quebra de linha).                                 |
| Delimitação de blocos e escopos é feita obrigatoriamente por chaves `{ }`, misturando o estilo de C com a limpeza do Python.      |
| Nome de variáveis e funções pode ser composto por letras e números, mas não pode iniciar com números.                             |
| Declaração de variáveis através da palavra reservada `let`, com tipagem explícita opcional (ex: `let x: i32`).          |
| Funções são declaradas com `fn` e devem possuir o tipo de retorno explicitado (ex: `-> i32`).                                     |
| Sistema de tipos detalhado na base de bits: Inteiros (`i8` a `i64`), Unsigned (`u8` a `u64`), Reais (`f32`, `f64`), `char`, `bool`|
| Estrutura de repetição universal sob a palavra reservada `cycle { ... }`.                |
| Operadores lógicos legíveis: `and`, `or`, `not`.                                                                 |
| Entrada e Saída pelas funções `print()` e `input()`.                                             |
| Tipagem híbrida (inferida e explícita).                                                                                           |
| Modos de execução especializados definidos por diretivas (`!kernel`, `!embedded`).                                                |
| Operações de memória explícitas similares ao C, porém padronizadas com funções `chain(n)`, `unchain(ptr)`.                        |
| Suporte atrelado a ponteiros para estruturas de baixo nível (ex: `let ptr: *u32 = 0x1000`).                                       |
| Capacidade de código de máquina inline via palavra-chave e bloco `asm { }`.                                                       |