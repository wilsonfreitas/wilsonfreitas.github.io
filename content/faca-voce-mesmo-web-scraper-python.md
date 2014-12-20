Title: Faça você mesmo um Web Scraper em Python
Category: programming
Author: Wilson Freitas
Tags: python, scraps
Date: 2014-12-18
Lang: pt

[1]: https://pypi.python.org/pypi?%3Aaction=search&term=scrap&submit=search "PyPI Scrap Search"
[2]: https://pypi.python.org/pypi?%3Aaction=search&term=crawler&submit=search "PyPI Crawler Search"
[scrapy]: http://scrapy.org/ "Scrapy"
[cetip]: http://www.cetip.com.br/ "CETIP"


Já não é de hoje que Python é tida como uma ótima linguagem para realizar tarefas de captura de dados na Internet.
Eu sempre gostei de utilizar Python para capturar dados na Internet, mas nunca me preocupei em fazer isso de forma estruturada.
No entanto, para um projeto pessoal, eu precisei recentemente realizar capturas de dados financeiros em diversos sites e senti a necessidade de alguma ferramenta que me permitisse fazer as capturas de forma mais estruturada.
Eu sei que há diversos projetos que atacam este problema de diversas formas.
Até investi algum tempo utilizando o [Scrapy][scrapy], mas logo vi que ele era demais para o que eu precisava.
Fora que eu não encontrei, num primeiro momento, uma forma de fazer nele exatamente o que eu precisava (já explico).
Foi assim que decidi fazer o meu próprio *web scraper* utilizando algumas coisas que eu já havia construído.

#### Por que você não usa o Scrapy?

Bem, não sei. Simplismente não gostei. Acho que tem dependências demais e não gosto de dependências demais.
Já basta o Pandas, numpy, scipy e matplotlib que eu tenho que usar e ter uma vida miserável toda vez que eu decido compilar uma nova versão.
Mas a verdade mesmo é que eu queria algo que pudesse executar no Google App Engine e com tamanha quantidade de dependências logo vi que não ia rolar.

Mas na verdade ainda, houveram alguns pontos que eu entendia relevantes e posto isso eu resolvi tentar uma solução caseira.
Estes pontos são:

- Não gostei da forma que a classe `Item` funciona. Na verdade gostei muito da classe `Item`, mas pra usar da maneira proposta eu me viro bem com um `dict`.
- Outra coisa é que o método de *parse* é implementado de uma forma que toda a inteligência do *scraper* fica num lugar só.Eu procurava algo com uma idéia mais transcedental, de transformação, onde eu tivesse o conteúdo extraído da página e fosse transformando ele até obter o que eu desejasse.
- A declaração das URLs no *spider* pra mim era limitada, uma vez que eu precisava de URLs dinâmicas (com datas), pois alguns dados do mercado financeiro são divulgados assim, infelizmente!

## Entra em cena: `scraps`

Bem, foi assim que eu começei, há alguns meses atrás, a escrever o `scraps` e desde então venho usando ele pra diversas capturas.

<script src="https://gist.github.com/wilsonfreitas/8bd1a0a5296c65948918.js"></script>

O `scraps` é um módulo Python muito simples onde eu tenho apenas 2 classes (`Scrap` e `Attribute`) e com elas eu resolvo a minha vida com capturas na Internet.
É óbvio que esta não é uma solução final, é um quebra galho mesmo, mas é um macaco gordo!

Coisas legais ao desenvolver `scraps`

- É muito bom desenvolver módulos para necessidades específicas. As vezes eu tenho a impressão que toda a programação (ou os programadores) querem tratar as soluções como grandes LEGOs e para isso ficam a busca de quais são os *frameworks* da moda para compor a obra. Obviamente para mim é fácil falar dado que não vivo de programação e não tenho a necessidade de mercado me pressionando para ficar na vanguarda. Na minha praia que é computação científica eu defendo menos bibliotecas e mais implementação.
- Eu pude finalmente utilizar **Python Descriptors** ou pelo mesmo usá-lo em algo útil que não um exemplo de descriptors. Fiquei muito feliz com o resultado final, apesar da implementação ainda parecer um *hack* malígno.


## `scraps` em ação

A seguir vou mostrar um exemplo simples do meu uso para `scraps`, mas a idéia é bastante simples.
Eu tenho a classe `scpras.Scrap` que representa o que eu quero extrair do texto.
Nessa classe eu declaro atributros de classe que são instâncias da classe `scraps.Attribute`.
Nesta classe eu já declaro o xpath que eu quero capturar, que sempre retorna uma coleção com o conteúdo em texto dos elementos.
A classe `scraps.Attribute` tem o argumento `apply` onde eu passo uma coleção de funções que será aplicada a cada elemento da coleção com o conteúdo em texto dos elementos.
Dessa maneira eu posso estruturar a transformação dos dados sem ficar preso a um método.
Funciona mais ou menos como no diagrama abaixo.

![Diagrama da classe Attribute]({filename}figure/attribute-diag-1.png) 

Abaixo segue uma implementação que eu utilizo `scraps` para obter a taxa de juros diária divulgada no site da [CETIP][cetip].

<script src="https://gist.github.com/wilsonfreitas/4b8e7e215e3a8a27eb90.js"></script>

O primeiro ponto importante é a criação da classe `CetipScrap` onde eu crio 2 atributos `data` e `taxa`.
Segue abaixo um pedaço da tela com as informações a serem capturadas (site da [CETIP][cetip]):

![CETIP]({filename}figure/cetip.png) 

Para cada atributo eu passo o xpath correspondente e a sequencia de funções a serem aplicadas.
Na verdade a diversão aqui é a criação dessas funções pois o ideal é que cada função execute apenas 1 ação e que o conjunto delas, sim, seja determinante para a conclusão da tarefa.

Por exemplo, a função `replace`:

```{python}
def replace(_from, _to):
    def _replace(text):
        for f, t in zip(_from, _to):
            text = text.replace(f, t)
        return text
    return _replace
```

Esta função retorna uma *closure* que executa diversas substituições em um texto.
Mas note que ambos argumentos são empacotados em um `zip`, de forma que ao executar `replace('aA', 'bB')` eu obtenho uma função que substitui todo `a` por `b` e todo `A` por `B`.
Já no tratamento do atributo `data` eu me deparei com um problema, eu precisava remover os parenteses.
Essa abordagem, que num primeiro momento me pareceu legal me gera este problema que, apesar de eu poder executar `replace(')(', ['', ''])`.
No entanto eu resolvi criar o *generator* `nothing` de strings vazias:

```{python}
def _nothing():
    while True:
        yield ''
nothing = _nothing()
```

E assim eu poderia chamar `replace(')(', nothing)`, o que me parece mais elegante.

No atributo `taxa` eu precisei trocar a vírgula por ponto e remover o `%` e assim `replace(',%', ['.', ''])` resolve o problema.

O campo `data` eu queria com o tipo `datetime.datetime` e por isso eu criei um *wrapper* para `strptime`

```{python}
def strptime(format='%Y-%m-%d'):
    return lambda text: datetime.strptime(text, format)
```

E para encerrar, o atributo `taxa` eu apenas converti para `float` e dividi por 100.

É claro que todas estas transformações poderiam ser programadas em uma única função.
Mas a graça aqui é utilizar a composição de funções para chegar ao resultado final.
A ideia é ser criativo no desenvolvimento das pequenas transformações.

Abaixo segue o resultado da execução do script acima.

```
[datetime.datetime(2014, 12, 18, 0, 0)]
[0.1159]
```

## Conclusão

Escrever `scpras` foi divertido e usá-lo é mais legal ainda.
Exercito muito a minha criatividade pensando em transformações para os dados.
Mas há uma ideia subliminar aqui que é a estruturação do tratamento dos dados.
Uma vez que eu consiga mapear um conjunto de funções que atende a um número considerável de problemas eu posso estruturar essa solução e torná-la mais automática, o que me faz pensar na construção de capturas on-line.
De qualquer forma, `scraps` é um módulo que eu classificaria como *quick-and-dirty*, mas me ajuda a exercitar a minha criatividade e a dar vazão as coisas.
