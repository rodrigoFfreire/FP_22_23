def produto_interno(vet1: tuple, vet2: tuple) -> float:
    if len(vet1) != len(vet2):
        return False
    
    product = 0
    for i in range(len(vet1)):
        product += vet1[i] * vet2[i]

    return product

def verifica_convergencia(matrix: tuple, c: tuple, x: tuple, prec: float) -> bool:
    pass
    

def retira_zeros_diagonal(matrix: tuple, c: tuple) -> tuple:
    pass


def eh_diagonal_dominante(matrix: tuple) -> bool:
    pass


def resolve_sistema(matriz: tuple, c: tuple, precision: float) -> tuple:
    pass


print(produto_interno((1,2,3,4,5),(-4,5,-6,7,-8)))