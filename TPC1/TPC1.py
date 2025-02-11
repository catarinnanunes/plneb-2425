# 1. given a string "s", reverse it.

def reverse(string):
    return string[::-1]

# 2. given a string "s", returns how many "a" and "A" characters are present in it.

def count_aA(string):
    count = 0
    for letra in string:
        if letra=='a' or letra=='A':
        # if letra in 'aA':
            count+=1
    return count

# 3. given a string "s", returns the number of vowels there are present in it.
def count_vowels(string):
    count=0
    for letra in string:
        if letra in 'aeiouAEIOU':
            count+=1
    return count

# 4. given a string "s", convert it into lowercase.

def to_lower(string):
    return string.lower()

# 5. given a string "s", convert it into uppercase.

def to_upper(string):
    return string.upper()

# 6. Verifica se uma string é capicua

def is_capicua(string):
    string=string.lower()
    if string == string[::-1]:
        return True
    else:
        return False
    
# 7. Verifica se duas strings estão balanceadas (Duas strings, s1 e s2, estão balanceadas se todos os caracteres de s1 estão presentes em s2.)

def is_balanced(s1,s2):
    for c in s1:
        if c in s2:
            return True
        else:
            return False
            
# 8. Calcula o número de ocorrências de s1 em s2

def count_ocorrences(s1,s2):
    return s2.count(s1)
    
# 9. Verifica se s1 é anagrama de s2-
# "listen" e "silent": Deve imprimir True
# "hello", "world": Deve imprimir False

def is_anagram(s1,s2):
    if sorted(s1)==sorted(s2):
        return True
    else:
        return False 
    
# 10. Dado um dicionário, calcular a tabela das classes de anagramas.

def anagram_classes(words):
    classes={}
    for w in words:
        sorted_word = ''.join(sorted(w)) # o sorted cria uma lista. 
        if sorted_word not in classes:
            classes[sorted_word]=[]
        classes[sorted_word].append(w)
    return classes



# Testes
def run_testes():
    print("1- 'hello' reversed:", reverse("hello"))
    print("2- Contagem de 'a'/'A' em 'Abracadabra':", count_aA("Abracadabra"))
    print("3- Contagem de vogais em 'Hello World':", count_vowels("Hello World"))
    print("4- Minúsculas: 'Hello' ->", to_lower("Hello"))
    print("5- Maiúsculas: 'Hello' ->", to_upper("Hello"))
    print("6- Verifica se a palavra é capicua -> Ana: ", is_capicua("Ana"))
    print("7- Verifica se as strings estao balanceadas ('abc', 'cbadef')?", is_balanced("abc", "cbadef"))
    print("8- Ocorrências de 'lo' em 'Hello World':", count_ocorrences("lo", "Hello World"))
    print("9- Verifica anagramas:\n 'listen' e 'silent': ", is_anagram("listen", "silent"), "\n","'hello' e 'world': ", is_anagram("hello", "world"))
    words_list = ["listen", "silent", "enlist", "rat", "tar", "art"]
    print("10- Tabela de classes de anagramas:", anagram_classes(words_list))

def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Reverter uma string")
        print("2. Contar 'a' e 'A' numa string")
        print("3. Contar vogais numa string")
        print("4. Converter string para minúsculas")
        print("5. Converter string para maiúsculas")
        print("6. Verificar se uma string é capicua")
        print("7. Verificar se duas strings estão balanceadas")
        print("8. Contar ocorrencias de uma string noutra string")
        print("9. Verificar se duas strings são anagramas")
        print("10. Gerar tabela de classes de anagramas")
        print("11. Mostrar testes pré-feitos")
        print("0. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            s = input("Digite uma string: ")
            print(f"String revertida: {reverse(s)}")
        elif escolha == "2":
            s = input("Digite uma string: ")
            print(f"Número de 'a' e 'A': {count_aA(s)}")
        elif escolha == "3":
            s = input("Digite uma string: ")
            print(f"Número de vogais: {count_vowels(s)}")
        elif escolha == "4":
            s = input("Digite uma string: ")
            print(f"String em minúsculas: {to_lower(s)}")
        elif escolha == "5":
            s = input("Digite uma string: ")
            print(f"String em maiúsculas: {to_upper(s)}")
        elif escolha == "6":
            s = input("Digite uma string: ")
            print(f"É capicua? {is_capicua(s)}")
        elif escolha == "7":
            s1 = input("Digite a primeira string: ")
            s2 = input("Digite a segunda string: ")
            print(f"As strings estão balanceadas? {is_balanced(s1, s2)}")
        elif escolha == "8":
            s1 = input("Digite a substring: ")
            s2 = input("Digite a string principal: ")
            print(f"Número de ocorrências: {count_ocorrences(s1, s2)}")
        elif escolha == "9":
            s1 = input("Digite a primeira string: ")
            s2 = input("Digite a segunda string: ")
            print(f"São anagramas? {is_anagram(s1, s2)}")
        elif escolha == "10":
            words = input("Digite uma lista de palavras separadas por vírgula: ").split(',')
            words = [word.strip() for word in words]  # remover espacos em branco
            print(f"Tabela de classes de anagramas: {anagram_classes(words)}")
        elif escolha == "11":
            run_testes()
        elif escolha == "0":
            print("A Sair")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()