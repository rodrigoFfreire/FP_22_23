# Ex2
def piatorio(lbound, ubound, exp, inc):
    prod = 1
    while lbound <= ubound:
        prod *= exp(lbound)
        lbound = inc(lbound)
    return prod

# n = 5
# print(piatorio(lbound=1, ubound=n, exp=lambda x: x, inc=lambda x: x + 1))

# Ex3
def soma_fn_for(n: int, fn):
    soma = 0
    for i in range(1, n + 1):
        soma += fn(i)
    return soma

def soma_fn_recur(n: int, fn):
    def aux(n, fn, _sum):
        if n == 1:
            return _sum + fn(n)
        return aux(n - 1, fn, _sum + fn(n))
    return aux(n, fn, 0)


# Ex4
def filtra(lst, tst):
    def aux(lst, tst, result):
        if len(lst) == 0:
            return result
        return aux(lst[1:], tst, result + [lst[0]]) if tst(lst[0]) else \
            aux(lst[1:], tst, result)
    return aux(lst, tst, [])
            
def transforma(lst, fn):
    def aux(lst, fn , result):
        if len(lst) == 0:
            return result
        return aux(lst[1:], fn, result + [fn(lst[0])])
    return aux(lst, fn, [])

def acumula(lst, fn):
    def aux(lst, fn, result):
        if len(lst) == 0:
            return result
        return aux(lst[1:], fn, fn(result, lst[0]))
    return aux(lst[1:], fn, lst[0])


# Ex5
def soma_quadrados_impares(lst):
    return acumula(
                transforma(
                    filtra(
                        lst,
                        lambda x: x % 2 != 0
                    ),
                    lambda x: x * x
                ),
                lambda x, y: x + y
            )


# Ex6
def eh_primo(n):
    if n == 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def nao_primos(n: int) -> list:
    return [i for i in range(1, n + 1) if not eh_primo(i)]


# Ex8
def lista_digitos(n):
    return [int(i) for i in str(n)]


# Ex9
def produto_digitos(n, fn):
    return acumula(filtra(lista_digitos(n), fn), lambda x, y: x * y)


# Ex10
def apenas_digitos_impares(n):
    return acumula(filtra(lista_digitos(n), lambda x: x % 2 != 0), lambda x, y: (x* 10) + y)