def apenas_digitos_impares(n: int):
    if n == 0:
        return 0
    if (n % 10) % 2 == 0:
        return apenas_digitos_impares(n // 10)
    else:
        return apenas_digitos_impares(n // 10) * 10 + (n % 10)
    

def junta_ordenadas(l1: list, l2: list):
    if not l1 or not l2:
        return l1 + l2
    if l1[0] > l2[0]:
        return [l2[0]] + junta_ordenadas(l1, l2[1:])
    else:
        return [l1[0]] + junta_ordenadas(l1[1:], l2)


def sublistas(l: list):
    if len(l) == 0:
        return 0
    if isinstance(l[0], list):
        return 1 + sublistas(l[0]) + sublistas(l[1:])
    return sublistas(l[1:])


def soma_n_vezes(a: int, b: int, n: int):
    if n < 1:
        return b
    return soma_n_vezes(a, b, n - 1) + a


def soma_els_atomicos(t: tuple):
    if len(t) == 0:
        return 0
    if isinstance(t[0], tuple):
        return soma_els_atomicos(t[0] + t[1:])
    else:
        return soma_els_atomicos(t[1:]) + t[0]
    

def inverte(l: list):
    if len(l) == 0:
        return l
    return [l[-1]] + inverte(l[:-1])


def pertence(l: list, i: int):
    if len(l) == 0:
        return False
    if l[0] == i:
        return True
    return pertence(l[1:], i)


def subtrai(l1, l2):
    if len(l1) == 0:
        return []
    if pertence(l2, l1[0]):
        return subtrai(l1[1:], l2)
    return [l1[0]] + subtrai(l1[1:], l2)


def parte(l: list, i: int):
    def aux(l, i, m, n):
        if len(l) == 0:
            return [n, m]
        if l[0] < i:
            return aux(l[1:], i , m, n + [l[0]])
        return aux(l[1:], i, m + [l[0]], n)
    
    return aux(l, i, [], [])


def maior(l: list):
    def aux(l: list, m: int):
        if len(l) == 0:
            return m
        if l[0] > m:
            return aux(l[1:], l[0])
        return aux(l[1:], m)
    return aux(l, l[0])