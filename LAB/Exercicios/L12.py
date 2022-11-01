import math


def quadrado_a(n: int):
    if n <= 1:
        return 1
    return (n + n - 1) + quadrado_a(n - 1)

def quadrado_b(n: int):
    def aux(n, c):
        if n <= 1:
            return c + 1
        return aux(n - 1, c + n + n - 1)
    return aux(n, 0)

def quadrado_c(n: int):
    c = 0
    for i in range(1, n + 1):
        c += i + i - 1
    return c


def numero_digitos_a(n: int):
    if n // 10 == 0:
        return 1
    return 1 + numero_digitos_a(n // 10)

def numero_digitos_b(n: int):
    def aux(n, c):
        if n // 10 == 0:
            return c + 1
        return aux(n // 10, c + 1)
    return aux(n, 0)

def numero_digitos_c(n: int):
    c = 0
    while n > 0:
        if n // 10 != 0:
            c += 1
        n //= 10
    return c + 1

def numero_digitos_smart(n):
    return math.floor(math.log10(n) + 1)


def eh_capicua(n: int):
    def digito(n: int, i: int):
        return (n % (10 ** (i + 1))) // (10 ** i)
    def aux(n, i):
        if i >= numero_digitos_smart(n) // 2:
            return True
        if digito(n, i) == digito(n, numero_digitos_smart(n) - i - 1):
            return aux(n, i + 1)
        return False
    return aux(n, 0)


def espelho(n):
    def digito(n: int, i: int):
        return (n % (10 ** (i + 1))) // (10 ** i)
    def aux(n, c, k):
        if c >= numero_digitos_smart(n):
            return k
        return aux(n, c + 1, k * 10 + digito(n, c))
    return aux(n, 0, 0)


def g(n):
    if n == 0:
        return 0
    return n - g(g(n - 1))


def calc_soma(x, n):
    def fatorial(k):
        if k <= 1:
            return 1
        return k * fatorial(k - 1)
    def power(k, m):
        if m <= 1:
            return k
        return k * power(k, m - 1) 
    if n == 0:
        return 1
    return (power(x, n) / fatorial(n)) + calc_soma(x, n - 1)


def maior_inteiro(lim):
    def aux(lim, n, c):
        if c > lim:
            return n - 1
        return aux(lim, n + 1, c + n + 1)
    return aux(lim, 1, 1)


