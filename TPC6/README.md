# TPC6 - Funcionalidade de Pesquisa - Dicionário Médico
## Como Funciona a Pesquisa
A funcionalidade de pesquisa foi desenvolvida para ser simples e eficiente. Esta permite:

**Pesquisar por Termos**:

O utilizador pode escrever um termo no campo de pesquisa.

O sistema procura o termo na designação e na descrição dos conceitos.

**Destaque de Resultados**:

- Se o termo pesquisado for encontrado, será destacado a negrito nos resultados.

- Apenas a palavra exata que corresponde ao termo pesquisado é destacada.

**Case-sensitive**:

A procura diferencia maiúsculas de minúsculas. Por exemplo, pesquisar por "abalo" ou "ABALO" retornará resultados diferentes.

**Ligação para página da designação**:

Cada designação encontrada na pesquisa é um link clicável que redireciona para a página de detalhes do conceito (/conceitos/<designacao>).
