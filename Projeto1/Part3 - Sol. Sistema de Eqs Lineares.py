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


def retira_zeros_diagonal(matrix: tuple, c: tuple) -> tuple:
    pass


def eh_diagonal_dominante(matrix: tuple) -> bool:
    pass


def resolve_sistema(matriz: tuple, c: tuple, precision: float) -> tuple:
    pass

