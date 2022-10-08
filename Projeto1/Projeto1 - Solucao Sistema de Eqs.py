def produto_interno(vet1: tuple, vet2: tuple) -> float:
    product = 0
    for i in range(len(vet1)):
        product += vet1[i] * vet2[i]

    return product


def verifica_convergencia(matrix: tuple, c: tuple, x: tuple, prec: float) -> bool:
    results = []
    for i in range(len(matrix)):
        if abs(produto_interno(matrix[i], x) - c[i]) < prec:
            results.append(True)
        else:
            results.append(False)
            
    return all(results)


def swap(i: int, j: int, matrix: tuple) -> tuple:
    if i > j:
        return matrix[:j] + (matrix[i], ) + matrix[j + 1:i] + (matrix[j], ) + matrix[i + 1:]
    return matrix[:i] + (matrix[j], ) + matrix[i + 1:j] + (matrix[i], ) + matrix[j + 1:]

def retira_zeros_diagonal(matrix: tuple, c: tuple) -> tuple:
    matrix_res = matrix
    vector_res = ()
    for i in range(len(matrix)):
        if matrix_res[i][i] == 0:
            for j in range(len(matrix)):
                if i != j and matrix_res[j][i] != 0 and matrix_res[i][j] != 0:
                    matrix_res = swap(i, j, matrix_res)
                    break
                
    for k in matrix_res:
        vector_res += (c[matrix.index(k)], )
        
    return matrix_res, vector_res


def eh_diagonal_dominante(matrix: tuple) -> bool: 
    for i in range(len(matrix)):
        sum_non_diagonal = 0
        for j in range(len(matrix)):
            if i != j : sum_non_diagonal += abs(matrix[i][j])
        if abs(matrix[i][i]) < sum_non_diagonal:
            return False
    return True


def resolve_sistema(matriz: tuple, c: tuple, prec: float) -> tuple:
    pass