def cria_gerador(b: int, s: int) -> gerador:
    if (not isinstance(b, int) or not isinstance(s, int) or
            b < 1 or s < 1):
        raise ValueError('cria_gerador: argumentos invalidos')
    return {'b': b, 's': s}


def cria_copia_gerador(g: gerador) -> gerador:
    return g.copy()


def obtem_estado():
    pass