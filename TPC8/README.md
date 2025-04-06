# TPC8 - Atlas da Saúde

## Descrição
Este trabalho consiste em desenvolver um programa para extrair informações sobre doenças do site Atlas da Saúde. O objetivo é extrair dados estruturados sobre cada doença, incluindo:

- Descrição
- Causas
- Sintomas
- Tratamento
- Notas adicionais
- Artigos relacionados

Os dados são extraídos de todas as páginas de doenças organizadas por letra (A-Z) e guardados num ficheiro JSON.

## Estrutura do JSON criado
Cada entrada no JSON tem o formato:
```json
{
  "Abcesso dentário": {
    "url": "https://www.atlasdasaude.pt/abcesso-dentario-causas-sintomas-tratamento",
    "descricao": "Um abcesso dentário é uma bolsa de pus provocada por uma infeção bacteriana...",
    "causas": "A formação dos abcessos pode ter duas causas principais: as cáries ou a agressão dos tecidos próximos dos dentes...",
    "sintomas": [
      "Dor de dentes intensa, persistente e latejante",
      "Sensibilidade a temperaturas quentes e frias",
      "Febre",
      "Inchaço no rosto ou na bochecha"
    ],
    "tratamento": "Atualmente, o tratamento dos abcessos faz-se à base de antibióticos e da drenagem do pus no local...",
    "nota": "As informações e conselhos disponibilizados no Atlas da Saúde não substituem o parecer/opinião do seu Médico e/ou Farmacêutico.",
    "artigos_relacionados": [
      {
        "titulo": "Cárie Dentária",
        "url": "https://www.atlasdasaude.pt/publico/content/carie-dentaria"
      },
      {
        "titulo": "Escovagem dos dentes",
        "url": "https://www.atlasdasaude.pt/publico/content/escovagem-dos-dentes"
      }
    ],
    "resumo": "Um abcesso dentário é nada mais nada menos que uma bolsa de pus provocada por uma infeção bacteriana..."
  }
}