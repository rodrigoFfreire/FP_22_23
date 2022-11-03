def cria_gerador(b: int, s: int):
    if (not isinstance(b, int) or not isinstance(s, int) or
            s < 1 or
            b != 32 and b != 64):
        raise ValueError('cria_gerador: argumentos invalidos')
    return {'b': b, 's': s}


def cria_copia_gerador(g):
    return g.copy()


def obtem_estado(g) -> int:
    return g['s']


def define_estado(g, s: int) -> int:
    g['s'] = s
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
    return xorshift(g, cria_copia_gerador(g)['b'])


def eh_gerador(arg: any) -> bool:
    if not isinstance(arg, dict) or len(arg) != 2:
        return False
    if (cria_copia_gerador(arg)['b'] != 32 and 
            cria_copia_gerador(arg)['b'] != 64 or
            obtem_estado(arg) < 1):
        return False
    return True


def geradores_iguais(g1, g2) -> bool:
    if not eh_gerador(g1) or not eh_gerador(g2):
        return False
    if (cria_copia_gerador(g1)['b'], obtem_estado(g1)) != \
            (cria_copia_gerador(g1)['b'], obtem_estado(g1)):
        return False
    return True


def gerador_para_str(g):
    return f'xorshift{cria_copia_gerador(g)["b"]}(s={obtem_estado(g)})'


def gera_numero_aleatorio(g, n: int):
    atualiza_estado(g)
    return 1 + obtem_estado(g) % n


def gera_carater_aleatorio(g, c: str):
    atualiza_estado(g)
    return chr(65 + obtem_estado(g) % (ord(c) - ord('A') + 1))




def cria_coordenada(col: str, lin: int):
    if (not isinstance(col, str) or not isinstance(lin, int) or
            not 65 <= ord(col) <= 90 or
            not 1 <= lin <= 99):
        raise ValueError('cria_coordenada: argumento invalido')
    return {'col': col, 'lin': lin}

def obtem_coluna(c):
    return c['col']

def obtem_linha(c):
    return c['lin']

def eh_coordenada(arg: any):
    if not isinstance(arg, dict) or len(arg) != 2:
        return False
    if (not 65 <= ord(obtem_coluna(arg)) <= 90 or
            not 1 <= obtem_linha(arg) <= 99):
        return False
    return True

def coordenadas_iguais(c1, c2):
    if not eh_coordenada(c1) or not eh_coordenada(c2):
        return False
    if (obtem_coluna(c1), obtem_linha(c1)) != \
            (obtem_coluna(c2), obtem_linha(c2)):
        return False
    return True

def coordenada_para_str(c):
    return f'{obtem_coluna(c)}0{obtem_linha(c)}' if obtem_linha(c) < 10 \
        else f'{obtem_coluna(c)}{obtem_linha(c)}' 

def str_para_coordenada(s: str):
    s_clean = s.replace('0', '')
    return cria_coordenada(s_clean[0], int(s_clean[1:]))

def obtem_coordenadas_vizinhas(c) -> tuple:
    neighbours = ()
    def loop_settings(i):
        return [ord(obtem_coluna(c)) - 1, ord(obtem_coluna(c)) + 2] if i == 1 else \
            [ord(obtem_coluna(c)) + 1, ord(obtem_coluna(c)) + 2] if i == 2 else \
            [ord(obtem_coluna(c)) + 1, ord(obtem_coluna(c)) - 2, -1] if i == 3 else \
            [ord(obtem_coluna(c)) - 1, ord(obtem_coluna(c))]
                
    lines = (obtem_linha(c) - 1, obtem_linha(c), obtem_linha(c) + 1, obtem_linha(c))     
    for i, l in zip(range(1, 5), lines):
        for j in range(*loop_settings(i)):
            try:
                neighbours += (coordenada_para_str(cria_coordenada(chr(j), l)), )
            except Exception:
                continue
    return neighbours

def obtem_coordenada_aleatoria(c, g):
    pass



c1 = cria_coordenada('C', 5)
print(obtem_coordenadas_vizinhas(c1))