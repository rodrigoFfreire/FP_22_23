def cria_gerador(b: int, s: int):
    if (not isinstance(b, int) or not isinstance(s, int) or
            b < 1 or s < 1):
        raise ValueError('cria_gerador: argumentos invalidos')
    return [b, s]


def cria_copia_gerador(g):
    return g.copy()


def obtem_estado(g) -> int:
    def rand(g):
        g[1] ^= (g[1] << 13) & 0xFFFFFFFF
        g[1] ^= (g[1] >> 17) & 0xFFFFFFFF
        g[1] ^= (g[1] << 5) & 0xFFFFFFFF
        return g[1]
    return rand(g)


