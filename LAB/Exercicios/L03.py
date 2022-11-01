import math, timeit, os


# Ex1
def cinco(n):
    return n == 5

    
# Ex2
def horas_dias(h):
    return h / 24
    

# Ex3
def area_circulo(r):
    return 3.14 * r * r
    

# Ex4
def area_coroa(r1, r2):
    if r1 > r2:
        raise ValueError
    return area_circulo(r2) - area_circulo(r1)


# Ex5
def bissexto(year):
    return year % 4 == 0 or year % 400 == 0 and year % 100 != 0
    

# Ex6
def dia_mes(month, year):
    if month == 'jan' or 'mar' or 'mai' or 'jul' or 'ago' or 'out' or 'dez':
        return 31
    if month == 'apr' or 'jun' or 'set' or 'nov':
        return 30
    if month == 'fev':
        if bissexto(year):
            return 29
        return 28
    raise ValueError('Mes nao valido!')


# Ex7
def valor(q, j, n):
    if 0 < j < 1 and q > 0 and n > 0:
        return q * (1 + j)**n
    raise ValueError('valor: argumentos invalidos!')


def duplicar_fast(q, j):
    return math.ceil(math.log(2, 1 + j))


def duplicar_slow(q, j):
    years = 0
    while True:
        years += 1
        if valor(q, j, years) >= 2 * q:
            return years


# Ex8
def serie_geom(r, n):
    if n >= 0:
        return (1 - r**(n + 1)) / (1 - r)
    raise ValueError('serie_geom: argumentos invalidos!')


# Ex 9
def mes(m):
    if m == 1:
        return 13
    if m == 2:
        return 14
    return m

def dia(d):
    days = {
        0: 'sabado',
        1: 'domingo',
        2: 'segunda',
        3: 'terca',
        4: 'quarta',
        5: 'quinta',
        6: 'sexta'
    }
    return days[d]

def formula(d, m, y):
    return math.ceil(d + ((13 * mes(m) + 13) / 5) + y % 100 + ((y % 100) / 4) + ((y / 100) / 4) - 2 * (y / 100)) % 7

def erros(d, m, y):
    if (not isinstance(d, int) or not isinstance(m, int) or not isinstance(y, int)
        or not 1 <= d <= 31 or not 1 <= m <= 12):
        return True
    
def dia_da_semana(d, m, y):
    if not erros(d, m, y):
        return dia(formula(d, m, y))
    raise ValueError('dia_da_semana: argumento(s) nao valido(s)')


# Ex 10
def misterio(n):
    if len(n) != 3 or (n % 10) + (n // 100) < 3:
        return 'Condições não verificadas'
    