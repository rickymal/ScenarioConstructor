# ScenarioConstructor
Simple Script in Python that allow best use of Scenarios in ML scripts



O pequeno trecho de código abaixo é uma implantanção para a criação de cenários utilizando apenas funções
Desenvolvi este pequeno código baseado em vários problemas que passei na universidade federal do Pará 
como desenvolvedor Python para Machine Learning..

Durante meu período na instituição, tive vários problemas para implementar um sistema em que eu pudesse avaliar
diferentes cenários com base nos resultados obtidos. Por exemplo: imagine que você deseje testar diferentes resultados
de uma função baseando-se em diferentes parâmetros. Não é algo complicado para quem já possui experiência, mas para 
mim que estava no começo foi responsável por uma necessidade de refatoração de quase quatro meses do meu projeto.

Este código busca trazer uma solução ergonômia para a criação destes cenários. apenas utilizando o objeto "Scenario"
e seu decorador "appender". Creio que com um exemplo fique bem mais simples:
    
supondo que tenhamos uma função que some dois números, mas queremos testar diferentes valores destes dois números
a = [10,20,30,],
b = [20,30,40,],

a função de soma receberá dois parâmetros 'a' e 'b', respectivamente, para o funcionamento a função deve ser
decorada com o método appender. os parâmetros deves ser encapsulados pelo método "set_parameters" ou por
alguma variáveis iterador como uma lista, contanto que seja setado para esta lista ser reconhecida como uma variável
para controle de cenário.

o valor resultante sempre é por definição uma tabela DataFrame contendo todas as combinações com os diferentes cenários

a função pode atualmente retornar um valor escalar (ou qualquer outro tipo) e um dicionário caso se tenha várias respostas

