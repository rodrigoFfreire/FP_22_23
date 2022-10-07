import math

# Ex1
def ex1():
    soma = 0
    for i in range(0, 19, 2):
        soma += 1
    print('Soma =', soma)


# Ex2   
def explode(n: int) -> tuple:
    if not isinstance(n, int):
        raise ValueError('explode: argumento invalido')
    result = ()
    for i in range(1, math.ceil(math.log(n, 10)) + 1):
        result = (n % 10, ) + result 
        n //= 10
    
    return result


# Ex 3
def implode(t: tuple) -> int:
    if not isinstance(t, tuple):
        raise ValueError('implode: argumento invalido')
    result = 0
    for i in t:
        result = result * 10 + i
    
    return result


# Ex 4
def filtra_pares(t: tuple) -> tuple:
    result = ()
    for i in t:
        if i % 2 == 0:
            result += (i, )
        
    return result


# Ex 7
def amigas(c1: str, c2: str) -> bool:
    if not len(c1) == len(c2):
        raise ValueError('amigas: argumentos invalidos')
    
    count = 0
    for i in range(len(c1)):
        if c1[i] != c2[i]:
            count += 1
            
    return (count / len(c1)) < 0.1


# Ex 10
def codifica(text: str) -> str:
    even = ''
    odd = ''
    for i in range(0, len(text), 2):
        even += text[i]
    for j in range(1, len(text), 2):
        odd += text[j]
    
    return f'{even}{odd}'


def n_even(text: str) -> int:
    if len(text) % 2 == 0:
        return len(text) / 2
    return ((len(text) - 1) / 2) + 1

def descodifica(text: str) -> str:
    result = ''
    for i in range(0, int(n_even(text)), 2):
        result += text[i]
    
    return result + text[int(n_even(text)) - 1:]

print(codifica('abcdef'))
print(descodifica('acebdf'))