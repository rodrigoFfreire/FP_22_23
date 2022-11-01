# Ex1
def cria_racional(n, d):
    if not isinstance(n, int) or not isinstance(n, int) or d <= 0:
        raise ValueError('cria_racional: argumentos invalidos')
    return {'n': n, 'd': d}


def num(r):
    return r['n']

def den(r):
    return r['d']


def eh_racional(r):
    if not isinstance(r, dict) or len(r) != 2 or 'n' not in r or 'd' not in r:
        return False
    return isinstance(r['n'], int) and isinstance(r['d'], int) and r['d'] > 0

def eh_rac_zero(r):
    return eh_racional(r) and r['n'] == 0


def rac_iguais(r1, r2):
    if not eh_racional(r1) and not eh_racional(r2):
        raise ValueError('rac_iguais: argumentos invalidos')
    return num(r1) * den(r2) == den(r1) * num(r2)


def escreve_rac(r):
    if not eh_racional(r):
        raise ValueError('rac_iguais: argumentos invalidos')
    print(num(r), '/', den(r))
    
    
def produto_rac(r1, r2):
    return cria_racional(num(r1) * num(r2), den(r1) * den(r2))



# Ex2
def in_bounds(n, low, high):
    return low <= n <= high


def cria_rel(h, m, s):
    if (not isinstance(h, int) or not isinstance(m, int) or not isinstance(s, int) or
            not 0 <= h <= 23 or not 0 <= m <= 59 or not 0 <= s <= 59):
        raise ValueError('cria_rel: argumentos invalidos')
    return [h, m, s]


def horas(r):
    return r[0]

def minutos(r):
    return r[1]

def segundos(r):
    return r[2]


def eh_relogio(r):
    if (not isinstance(horas(r), int) or 
            not isinstance(minutos(r), int) or 
            not isinstance(segundos(r), int)):
        return False
    return in_bounds(horas(r), 0, 23) and in_bounds(minutos(r), 0, 59) and in_bounds(segundos(r), 0, 59)

def eh_meia_noite(r):
    if not eh_relogio(r):
        raise ValueError('eh_meia_noite: argumento invalido')
    return horas(r) == 0 and minutos(r) == 0 and segundos(r) == 0

def eh_meio_dia(r):
    if not eh_relogio(r):
        raise ValueError('eh_meia_noite: argumento invalido')
    return horas(r) == 12 and minutos(r) == 0 and segundos(r) == 0


def mesmas_horas(r1, r2):
    if not eh_relogio(r1) or not eh_relogio(r2):
        raise ValueError('eh_meia_noite: argumento invalido')
    return horas(r1) == horas(r2) and minutos(r1) == minutos(r2) and segundos(r1) == segundos(r2)


def escreve_relogio(r):
    pass