# Roteiro de Execução do Trabalho

## 1. Visão Geral
O objetivo fundamental deste trabalho é projetar e especificar formalmente as bases da primeira fase de um compilador, contemplando a criação teórica de um analisador léxico e de um analisador sintático para uma linguagem de programação customizada ou natural. Você deverá definir a estrutura da linguagem desde as suas menores unidades lógicas (tokens, operadores, tipos e palavras reservadas) até as estruturas de comandos mais complexas (condicionais, repetições, atribuições e entrada/saída), comprovando o reconhecimento dessas estruturas através da modelagem matemática e lógica via Expressões Regulares, Autômatos Finitos (com aplicação do método de Thompson, se necessário) e Regras de Produção, culminando em uma documentação técnica completa.

## 2. Mapeamento Teoria -> Prática
*   **Conceito de Tokens, Padrões e Lexemas:** Este conceito será o seu ponto de partida funcional para separar a linguagem em elementos mínimos. Ele se aplica diretamente à restrição da especificação de mapear palavras reservadas, operadores silenciados (`+`, `<`, etc.) e símbolos especiales (`{}`, `;`).
*   **Definições Regulares e Classes de Caracteres:** Esta base teórica é aplicada no cumprimento da exigência de especificar expressões regulares para o reconhecimento de cada *token*. Você usará esse conceito para descrever matematicamente os identificadores de variáveis e os literais numéricos.
*   **Operadores de Expressões Regulares (União, Concatenação, Fechamento de Kleene):** Você precisará usar as regras de procedência e junção detalhadas na teoria (ex: o operador `*` e `|`) para construir as expressões regulares complexas que suportem as restrições de tipos numéricos flexíveis (inteiro, ponto flutuante) exigidos no documento principal de especificação.
*   **Autômatos Finitos (AFD / AFN) e Método de Thompson:** É a aplicação prática dos conceitos de transições computacionais exigidos na Seção 3 da especificação. Caso você não enxergue diretamente o AFD a partir da expressão regular complexa, deverá usar a definição dos conectivos regulares para criar micro-AFNs e uni-los via o Algoritmo de Thompson, apresentando todo o passo a passo da transição.
*   **Conceitos de Gramática e Regras de Produção:** Se aplicam diretamente à exigência da Seção 3 da especificação (construção do analisador sintático), exigindo que você defina a estrutura hierárquica e a ordem na qual os *tokens* (já convertidos) podem aparecer para formar blocos de comandos válidos.

## 3. Passo a Passo de Execução

### Fase 1: Especificação do Vocabulário (Análise Léxica Preliminar)
*   **Ação:** Defina exaustivamente todo o conjunto de caracteres e palavras da sua linguagem. Crie uma tabela mapeando as classes léxicas listadas na especificação (Tipos de dados, Operadores Relacionais, Operadores Lógicos, Operadores Aritméticos, Símbolos Especiais de Delimitação de escopo e Lista de Palavras Reservadas). 
*   **Referência Teórica:** Seção "Tokens, Padrões e Lexemas – Classes de Tokens" do documento *Análise Léxica*.
*   **Dica de Validação:** Consulte a tabela de "Tokens" do Exemplo de Referência. Verifique se todo item possui um Símbolo/Lexema claro, e qual será o nome formal do Token (ex: `T_INT`, `T_IF`) que será entregue ao Sintático.
- [ ] Tipos de Dados
- [ ] Variável
- [ ] Operadores Relacionais
- [ ] Operadores Lógicos
- [ ] Operadores Aritméticos
- [ ] Símbolos Especiais
- [ ] Palavras reservadas

### Fase 2: Modelagem das Expressões Regulares
*   **Ação:** Para os itens cujo formato é dinâmico (principalmente números literais, cadeias de caracteres e identificadores de variáveis), construa uma Expressão Regular que capture todas as instâncias válidas respeitando as regras da linguagem (ex: variáveis só podem começar de uma determinada forma, números podem ter fração ou sinal).
*   **Referência Teórica:** Seção "Expressões Regulares – Definiões Regulares" e tópicos práticos finais do documento *Análise Léxica* (Atividade 1 - Identificadores e Atividade 2 - Números sem Sinal).
*   **Dica de Validação:** Olhe para a tabela "Expressões Regulares" do Exemplo de Referência. Certifique-se de que nenhum padrão dinâmico ficou de fora, validando desde o reconhecimento de um simples digito até regras lógicas contendo operadores matemáticos básicos.

### Fase 3: Construção e Simulação dos Autômatos
*   **Ação:** Converta cada uma das expressões regulares concebidas na fase anterior para diagramas de Autômatos. Desenvolva os estados correspondentes às uniões, concatenações e fechamentos de forma gráfica. Se utilizar AFNs em construções não triviais, aplique estritamente os moldes do Método de Thompson para a conversão até o AFN-Estendido. Use alguma ferramenta base (como o JFLAP, citado indiretamente) se achar necessário, exportando depois as imagens.
*   **Referência Teórica:** Conforme apontado na "Seção 3 Documentação" do documento principal, você precisa aliar o conhecimento prévio da disciplina teórica de Linguagens Formais sobre "Construção de Thompson" para estruturar a engenharia reversa das expressões unidas. 
*   **Dica de Validação:** No Exemplo de Referência, existem apontamentos de até 19 autômatos desenhados distintos (um para cada grande Regra/Token léxica, como números, condicionais, comentários). Cada expressão deve gerar o desenho de suas sequências de estados.

### Fase 4: Engenharia do Analisador Sintático (Regras de Produção)
*   **Ação:** Escreva a estrutura gramatical que dita as "Leis" do seu compilador, através das Regras de Produção. Você deve documentar as derivações que validam: 1. Comandos de atribuição, 2. Comandos de entrada e saída, 3. Comandos condicionais e 4. Comandos de repetição, além da delimitação obrigatória de blocos (seja com `begin/end` ou `{}`). 
*   **Referência Teórica:** A teoria primária enviada engloba a porção léxica, sinalizando que os nomes de Tokens vão submeter a leitura agora. Você usará a lógica composicional para agrupar tokens (ex: `<cmd> -> <if> ( <id> <op> <num> ) { <bloco> }`). 
*   **Dica de Validação:** Consulte a seção "Regras de Produção" e "Explicação das Regras de Produção" no Exemplo de Referência. Verifique se os nomes criados na esquerda (Cabeça da produção, como `Enquanto`) geram corretamente o encadeamento de *Tokens* formais (ex: `T_WHILE T_ABPAR...`) construídos durante a fase 1. E faça o acompanhamento com pequenas explicações textuais da finalidade de cada regra.

## 4. Checklist Final de Entrega

- [ ] Arquivo digitalizando a documentação base pronto para entrega limite até **06/05/2025**.
- [ ] Especificações matemáticas detalhando as Expressões Regulares desenvolvidas para o reconhecimento de cada Token da linguagem.
- [ ] Diagramas/Imagens dos Autômatos Finitos Determinísticos (AFDs) das linguagens.
- [ ] (Condicional) Diagramas dos Autômatos Finitos Não Determinísticos (AFN) e os passos de expansão pelo Método de Thompson, caso esta abordagem tenha sido sua rota construtiva principal.
- [ ] Listagem completa com definição, declaração e uma explicação detalhada das Regras de Produção / Gramática.
- [ ] As regras sintáticas elaboradas devemobrigatoriamente comportar os cenários de Atribuição, Condicional, Repetições, Entrada/Saída, blocos com fechamento, contendo além disso Operadores numéricos e lógicos explícitos.
- [ ] Preparação dos membros da equipe para a Apresentação Oral presencial estruturada para o dia **07/05/2025** (Pitch máximo de 10 minutos, focando na documentação produzida e dificuldades técnicas das montagens dos analisadores).
