# TPC1 - Manipulação de strings

Este repositório contém um ficheiro Python (`TPC1.py`) que implementa várias funções para manipulação de strings. Abaixo está uma descrição das funcionalidades disponíveis.

## Funções Implementadas

1. **`reverse(string)`**:
   - **Descrição**: Inverte uma string.
   - **Exemplo**: `reverse("hello")` retorna `"olleh"`.

2. **`count_aA(string)`**:
   - **Descrição**: Conta o número de ocorrências das letras 'a' e 'A' na string.
   - **Exemplo**: `count_aA("Abracadabra")` retorna `5`.

3. **`count_vowels(string)`**:
   - **Descrição**: Conta o número de vogais na string (considerando maiúsculas e minúsculas).
   - **Exemplo**: `count_vowels("Hello World")` retorna `3`.

4. **`to_lower(string)`**:
   - **Descrição**: Converte a string para minúsculas.
   - **Exemplo**: `to_lower("Hello")` retorna `"hello"`.

5. **`to_upper(string)`**:
   - **Descrição**: Converte a string para maiúsculas.
   - **Exemplo**: `to_upper("Hello")` retorna `"HELLO"`.

6. **`is_capicua(string)`**:
   - **Descrição**: Verifica se a string é uma capicua (ou palíndromo), ou seja, se pode ser lida da mesma forma de trás para frente.
   - **Exemplo**: `is_capicua("Ana")` retorna `True`.

7. **`is_balanced(s1, s2)`**:
   - **Descrição**: Verifica se todos os caracteres da string `s1` estão presentes na string `s2`.
   - **Exemplo**: `is_balanced("abc", "cbadef")` retorna `True`.

8. **`count_ocorrences(s1, s2)`**:
   - **Descrição**: Conta o número de ocorrências da string `s1` na string `s2`.
   - **Exemplo**: `count_ocorrences("lo", "Hello World")` retorna `1`.

9. **`is_anagram(s1, s2)`**:
   - **Descrição**: Verifica se as strings `s1` e `s2` são anagramas uma da outra.
   - **Exemplo**: `is_anagram("listen", "silent")` retorna `True`.

10. **`anagram_classes(words)`**:
    - **Descrição**: Dada uma lista de palavras, retorna um dicionário onde as chaves são as palavras ordenadas alfabeticamente e os valores são listas de palavras que são anagramas entre si.
    - **Exemplo**: `anagram_classes(["listen", "silent", "enlist", "rat", "tar", "art"])` retorna `{'eilnst': ['listen', 'silent', 'enlist'], 'art': ['rat', 'tar', 'art']}`.

### Menu
Ao executar o ficheiro, será exibido um menu. As opções incluem:

- Testar funções individualmente (opções 1 a 10).

- **Executar testes pré-feitos** (opção 11), que mostram os resultados esperados para cada função sem necessidade de interação.

- Sair do programa (opção 0).