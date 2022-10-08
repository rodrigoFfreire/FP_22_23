def produto_interno(vet1: tuple, vet2: tuple) -> float:
    product = 0
    for i in range(len(vet1)):
        product += vet1[i] * vet2[i]

    return product


def verifica_convergencia(matrix: tuple, c: tuple, x: tuple, prec: float) -> bool:
    results = []
    for i in range(len(matrix)):
        if abs(produto_interno(matrix[i], x) - c[i]):
            results.append(True)
        else:
            results.append(False)
            
    return all(results)


def is_last(matrix: tuple, j: int) -> tuple:
    if j == len(matrix) - 1:
        return ()
    return matrix[j + 1:]

def retira_zeros_diagonal(matrix: tuple, c: tuple) -> tuple:
    matrix_res = matrix
    matrix_temp = ()
    vector_res = ()
    for i in range(len(matrix_res)):
        if matrix_res[i][i] == 0:
            for j in range(i + 1, len(matrix_res)):
                if matrix_res[j][i] != 0:
                    matrix_temp = matrix_res[i:j] + (matrix_res[i], ) + is_last(matrix_res, j)
                    matrix_res = matrix_res[:i] + (matrix_res[j], ) + matrix_temp[1:]
                    break
    for k in matrix_res:
        vector_res += (c[matrix.index(k)], )
        
    return matrix_res, vector_res


def eh_diagonal_dominante(matrix: tuple) -> bool:
    for i in range(len(matrix)):
        if abs(matrix[i][i]) <= sum(matrix[i], -matrix[i][i]):
            print(i, matrix[i])
            return False
    return True


def resolve_sistema(matriz: tuple, c: tuple, precision: float) -> tuple:
    pass


#matrix = ((0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 0, 1), (1, 1, 1, 0))
matrix = ((1, 0, 0), (0, 1, 0), (0, 1, 2))
print(eh_diagonal_dominante(matrix))