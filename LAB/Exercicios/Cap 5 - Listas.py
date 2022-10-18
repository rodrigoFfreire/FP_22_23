from random import *


# Ex1
def lista_codigos(cad):
    return [ord(i) for i in cad]

# Ex2
def remove_multiplos(l: list, m: int()):
    l_copy = l.copy()
    for i in l:
        if i % m == 0:
            l_copy.remove(i)
    return l_copy
            
# Ex3
def soma_cumulativa(l: list):
    l_res = l.copy()
    for i in range(len(l)):
        if not i == 0:
            l_res[i] = sum(l[:i + 1])
    return l_res

# Ex4
def elemento_matriz(matrix: list, i: int, j: int):
    if not 0 <= i < len(matrix):
       raise ValueError('elemento_matriz: indice invalido, linha', i) 
    if not 0 <= j < len(matrix):
       raise ValueError('elemento_matriz: indice invalido, coluna', j)
   
    return matrix[i][j]

# Ex5
def write_matrix(matrix: list):
    for i in range(len(matrix)):
        print(' '.join([str(matrix[i][j]) for j in range(len(matrix))]))
        
# Ex6
def soma_mat(m1: list, m2: list):
    return [list(map(lambda a, b: a + b, m1[i], m2[i])) for i in range(len(m1))]

# Ex7
def multiplica_mat(m1: list, m2: list):
    return sum(list(product = map(lambda a, b: a * b, m1, m2)))

# Ex8
def seq_racaman(n: int):
    result = [0]
    for i in range(1, n):
        if result[i - 1] > i and not result[i - 1] - i in result:
            result.append(result[i - 1] - i)
        else:
            result.append(result[i - 1] + i)
    return result         

# Ex9
def numero_occ_lista(l: list, n: int):
    occ = 0
    l_copy = l.copy()
    for i in l_copy:
        if i == n and isinstance(i, int):
            occ += 1
        if isinstance(i, list):
            for j in i:
                l_copy = [j]
    return occ

# Ex10
def rand_chave():
    def rand_num(m):
        return int(random() * m) + 1
    return [[rand_num(50), rand_num(50), rand_num(50), rand_num(50), rand_num(50)],
            [rand_num(12), rand_num(12)]
    ]   
    
    
for i in range(10):
    print(rand_chave())