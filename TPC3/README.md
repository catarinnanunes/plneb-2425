# TPC3 - Extração de conceitos médicos

Este trabalho teve como objetivo processar um dicionário médico extraído de um PDF, formatá-lo corretamente e gerar um HTML estruturado. O principal desafio foi lidar com as quebras de página (`\f`) que causavam separação incorreta dos conceitos e descrições.

## Funcionalidades Implementadas

1. Marcação de Conceitos com `@`:
Para identificar conceitos no texto, foram adicionadas marcações `@`, permitindo distinguir das definições.

2. Remoção e Tratamento de `\f`:
Em vez de remover o `\f` diretamente (`re.sub(r'\f', '', texto`), foi usada a seguinte substituição:

`texto = re.sub(r"[^\f]\n\f", r"\n", texto)`

Isto impede que existam palavras a ser coladas indevidamente e mantém a estrutura correta dos dados.

3. Extração dos conceitos:
Foi melhorada a regex para capturar os conceitos e as suas descrições.

`conceitos_raw = re.findall(r"@(.+)\n([^@]+)",texto)`

A utilização de `.+` em vez de `.*` garante que haja pelo menos um carater no nome do conceito. O `([^@]+)` força a descrição a ter pelo menos um carater e impede que capture conceitos seguintes.

