def cria_gerador(b: int, s: int):
    if (not isinstance(b, int) or not isinstance(s, int) or
            s < 0 or
            b != 32 and b != 64):
        raise ValueError('cria_gerador: argumentos invalidos')
    return [b, s]


def cria_copia_gerador(g):
    return g.copy()


def obtem_estado(g) -> int:
    return g[1]


def define_estado(g, s: int) -> int:
    g[1] = s
    return s


def atualiza_estado(g) -> int:
    def xorshift(g, b):
        seed = obtem_estado(g)
        if b == 32:
            seed ^= (seed << 13) & 0xFFFFFFFF
            seed ^= (seed >> 17) & 0xFFFFFFFF
            seed ^= (seed << 5) & 0xFFFFFFFF
            define_estado(g, seed)
            return seed
        else:
            seed ^= (seed << 13) & 0xFFFFFFFFFFFFFFFF
            seed ^= (seed >> 7) & 0xFFFFFFFFFFFFFFFF
            seed ^= (seed << 17) & 0xFFFFFFFFFFFFFFFF
            define_estado(g, seed)
            return seed
    return xorshift(g, cria_copia_gerador(g)[0])


def eh_gerador(g: any) -> bool:
    if not isinstance(g, list) or len(g) != 2:
        return False
    if (cria_copia_gerador(g)[0] != 32 and 
            cria_copia_gerador(g)[0] != 64 or
            obtem_estado(g) < 0):
        return False
    return True


def geradores_iguais(g1, g2) -> bool:
    if not eh_gerador(g1) or not eh_gerador(g2):
        return False
    if (cria_copia_gerador(g1)[0], cria_copia_gerador(g1)[1]) != \
            (cria_copia_gerador(g1)[0], cria_copia_gerador(g1)[1]):
        return False
    return True


def gerador_para_str(g):
    print(f'xorshift{cria_copia_gerador(g)[0]}(s={obtem_estado(g)})')


def gera_numero_aleatorio(g, n):
    atualiza_estado(g)
    return 1 + obtem_estado(g) % n


def gera_carater_aleatorio(g, c):
    atualiza_estado(g)
    return chr(65 + obtem_estado(g) % (ord(c) - ord('A') + 1))

