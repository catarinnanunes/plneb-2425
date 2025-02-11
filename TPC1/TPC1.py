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
        else:
            classes[sorted_word].append(w)
    return classes



# Testes
if __name__ == "__main__":
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
    