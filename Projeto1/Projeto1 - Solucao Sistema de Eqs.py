def produto_interno(vet1: tuple, vet2: tuple) -> float:
    '''Retorna o produto interno entre dois vetores'''
    product = 0
    for i in range(len(vet1)):
        product += vet1[i] * vet2[i]

    return product


def verifica_convergencia(matrix: tuple, c: tuple, x: tuple, prec: float) -> bool:
    '''Verifica se o valor absoluto do erro de todas as equacoes eh inferior a {prec}
    e retorna True ou False consoante'''
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


def raise_errors_SSE(matrix: tuple, c: tuple, prec: float) -> tuple:
    if (not isinstance(matrix, tuple) 
        or not isinstance(c, tuple)
        or not isinstance(prec, float)
        or len(matrix) == 0
        or len(c) == 0
        or len(matrix) != len(c)
        or not 0 < prec < 1
    ):
        raise ValueError('resolve_sistema: argumentos invalidos')
    
    for i in range(len(matrix)):
        if (not isinstance(matrix[i], tuple)
            or len(matrix[i]) != len(matrix)
            or (not isinstance(c[i], float) and not isinstance(c[i], int))
        ):
            raise ValueError('resolve_sistema: argumentos invalidos')
        for j in range(len(matrix[i])):
            if (not isinstance(matrix[i][j], float) and not isinstance(matrix[i][j], int)):
                raise ValueError('resolve_sistema: argumentos invalidos')
        
    if not eh_diagonal_dominante(matrix):
        raise ValueError('resolve_sistema: matriz nao diagonal dominante')


def resolve_sistema(matrix: tuple, c: tuple, prec: float) -> tuple:
    raise_errors_SSE(matrix, c, prec)
    
    x, current_precision = [0] * len(c), [1] * len(c)

    while max(current_precision) >= prec:
        for i in range(len(c)):
            last_x = x[i]
            x[i] = x[i] + (c[i] - produto_interno(matrix[i], x)) / matrix[i][i]
            current_precision[i] = abs((x[i] - last_x) / x[i])
    
    return tuple(x)