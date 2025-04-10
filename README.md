# IA-AlgoritmoGenetico
Este projeto foi criado como parte do trabalho sobre Algoritmos Genéticos (AGs) para a disciplina de Inteligência Artificial da Fatec-SP e tem como objetivo demonstrar o funcionamento dos AGs e sua aplicação. 

## Dependências

- Python versão +3.10.6
- Pytest versão 8.3.5

## Diagrama de Máquina de Estados

![Diagrama de Máquina de Estados de um Algoritmo Genético](/img/DIAGRAMA%20-%20AI-AGs-Stmv2.png)

## Exemplos

### Caixeiro-viajante

#### Problema

Um vendedor precisa passar por uma lista de cidades uma única vez e retornar a  cidade de origem, o problema é encontrar o menor o caminho possível conforme a quantidade de cidades vai aumentando.

#### Solução

Uma solução poder ser encontrada na pasta /exemplos/caixeiro_viajante.py, ela utiliza um Algoritmo Genético para tentar chegar a solução mais próxima ou ótima 
do problema.

#### Dependências

- Nenhuma de terceiros
- Python:
    - random;
    - string;
    - itertools;
    - fractions;
    - enum;

#### Detalhes de implementação

A função custo foi implementada para 5 cidades seguindo os pesos que constam
nas imagens [Rotas Via única](#via-única) e [Rotas Via dupla](#via-dupla). Já para a quantidade de cidades que passem de 5, uma vez que fazer o diagrama e dar pesos é muito laborioso, se adotou o seguinte:

Para via única (ir de A para B tem o mesmo custo de B para A):

Se um par de cidades qualquer está na ordem alfabética, como "AB","BC", "CD", etc., terá o peso 1 e para qualquer outra combinação peso 2.

Para via dupla (ir de A para B não tem o mesmo custo de B para A):

Se um par de cidades qualquer está na ordem alfabética, como "AB","BC", "CD", etc., terá o peso 1.
Se o par estiver em ordem inversa, como "DC", "CB", "BA", etc., terá o peso 2 e para qualquer outra combinação peso 3.

Assim, a solução ou o menor caminho será aquele que estiver em ordem alfabética.

O máximo é 52 cidades que é a soma de todas as letras do alfabeto em letras maiúsculas e minúsculas.

#### Rotas

##### Via única

![Diagrama de rotas do caixeiro-viajante - 5 cidades - via unica](/img/DIAGRAMA%20-%20IA-ROTAS-CAIXEIRO_VIAJANTE-5_CIDADES-VIA_UNICA.png)

##### Via dupla

![Diagrama de rotas do caixeiro-viajante - 5 cidades - via dupla](/img/DIAGRAMA%20-%20IA-ROTAS-CAIXEIRO_VIAJANTE.png)
