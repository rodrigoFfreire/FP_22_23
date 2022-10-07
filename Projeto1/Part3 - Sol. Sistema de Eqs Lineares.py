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


def RTD_helper(matrix: tuple, j: int) -> tuple:
    if j == len(matrix) - 1:
        return ()
    return matrix[j + 1:]

def retira_zeros_diagonal(matrix: tuple, c: tuple) -> tuple:
    matrix_res = matrix
    matrix_temp = ()
    vector_res = ()
    for l in range(len(matrix_res)):
        if matrix_res[l][l] == 0:
            for j in range(l + 1, len(matrix_res)):
                if matrix_res[j][l] != 0:
                    matrix_temp = matrix_res[l:j] + (matrix_res[l], ) + RTD_helper(matrix_res, j)
                    matrix_res = matrix_res[:l] + (matrix_res[j], ) + matrix_temp[1:]
                    break
    for k in matrix_res:
        vector_res += (c[matrix.index(k)], )
        
    return matrix_res, vector_res


def eh_diagonal_dominante(matrix: tuple) -> bool:
    pass


def resolve_sistema(matriz: tuple, c: tuple, precision: float) -> tuple:
    pass


matrix = ((0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 0, 1), (1, 1, 1, 0))
print(retira_zeros_diagonal(matrix, (1, 2, 3, 4)))