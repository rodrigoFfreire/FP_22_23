# -*- coding: utf-8 -*-
# Rodrigo Freitas Freire
# N 106485
# rodrigofreitasfreire@tecnico.ulisboa.pt

#################
# TAD GERADOR
#################
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
    if (('b', 's') != tuple(arg.keys()) or
            cria_copia_gerador(arg)['b'] != 32 and 
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


def gerador_para_str(g) -> str:
    return f'xorshift{cria_copia_gerador(g)["b"]}(s={obtem_estado(g)})'


def gera_numero_aleatorio(g, n: int) -> int:
    atualiza_estado(g)
    return 1 + obtem_estado(g) % n


def gera_carater_aleatorio(g, c: str) -> str:
    atualiza_estado(g)
    return chr(65 + obtem_estado(g) % (ord(c) - ord('A') + 1))


#################
# TAD COORDENADA
#################
def cria_coordenada(col: str, lin: int):
    if (not isinstance(col, str) or not isinstance(lin, int) or
            not 65 <= ord(col) <= 90 or
            not 1 <= lin <= 99):
        raise ValueError('cria_coordenada: argumentos invalidos')
    return {'col': col, 'lin': lin}


def obtem_coluna(c) -> str:
    return c['col']


def obtem_linha(c) -> int:
    return c['lin']


def eh_coordenada(arg: any) -> bool:
    if not isinstance(arg, dict) or len(arg) != 2:
        return False
    if (('col', 'lin') != tuple(arg.keys()) or
            not 65 <= ord(obtem_coluna(arg)) <= 90 or
            not 1 <= obtem_linha(arg) <= 99):
        return False
    return True


def coordenadas_iguais(c1, c2) -> bool:
    if not eh_coordenada(c1) or not eh_coordenada(c2):
        return False
    if (obtem_coluna(c1), obtem_linha(c1)) != \
            (obtem_coluna(c2), obtem_linha(c2)):
        return False
    return True


def coordenada_para_str(c) -> str:
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
                neighbours += (cria_coordenada(chr(j), l), )
            except Exception:
                continue
    return neighbours


def obtem_coordenada_aleatoria(c, g):
    return cria_coordenada(
        gera_carater_aleatorio(g, obtem_coluna(c)), 
        gera_numero_aleatorio(g, obtem_linha(c))
    )


#################
# TAD PARCELA
#################
def cria_parcela():
    return {'state': 'hidden', 'mined': False}


def cria_copia_parcela(p):
    return p.copy()


def limpa_parcela(p):
    p['state'] = 'clean'
    return p


def marca_parcela(p):
    p['state'] = 'flagged'
    return p


def desmarca_parcela(p):
    p['state'] = 'hidden'
    return p


def esconde_mina(p):
    p['state'] = 'hidden'
    p['mined'] = True
    return p


def eh_parcela(arg: any) -> bool:
    if not isinstance(arg, dict) or len(arg) != 2:
        return False
    if (('state', 'mined') != tuple(arg.keys()) or
            arg['state'] not in ('clean', 'flagged', 'hidden') or
            arg['mined'] != True and arg['mined'] != False):
        return False
    return True


def eh_parcela_tapada(p) -> bool:
    return eh_parcela(p) and p['state'] == 'hidden'


def eh_parcela_marcada(p) -> bool:
    return eh_parcela(p) and p['state'] == 'flagged'


def eh_parcela_limpa(p) -> bool:
    return eh_parcela(p) and p['state'] == 'clean'


def eh_parcela_minada(p) -> bool:
    return eh_parcela(p) and p['mined'] == True


def parcelas_iguais(p1, p2) -> bool:
    if not eh_parcela(p1) or not eh_parcela(p2):
        return False
    if p1['state'] != p2['state'] or p1['mined'] != p2['mined']:
        return False
    return True


def parcela_para_str(p) -> str:
    state_chars = {
        'hidden': '#',
        'flagged': '@',
        'clean': '?',
        'clean_mined': 'X'
    }
    return state_chars[p['state']] if p['mined'] == False or p['mined'] == True and p['state'] != 'clean' else \
        state_chars['clean_mined']


def alterna_bandeira(p) -> bool:
    if eh_parcela_marcada(p) or eh_parcela_tapada(p):
        if eh_parcela_marcada(p):
            desmarca_parcela(p)
        else:
            marca_parcela(p)
        return True
    return False


#################
# TAD PARCELA
#################
def cria_campo(c: str, l: int):
    if (not isinstance(c, str) or not isinstance(l, int) or
            not 65 <= ord(c) <= 90 or
            not 1 <= l <= 99):
        raise ValueError('cria_campo: argumentos invalidos')
    
    field = {}
    for i in range(1, l + 1):
        for j in range(65, ord(c) + 1):
            field[f'{coordenada_para_str(cria_coordenada(chr(j), i))}'] = cria_parcela()
            
    return field

def cria_copia_campo(m):
    return m.copy()


def obtem_ultima_coluna(m):
    return obtem_coluna(m[tuple(m.keys())[-1]])


def obtem_ultima_linha(m):
    return obtem_linha(m[tuple(m.keys())[-1]])


def obtem_parcela(m, c):
    return m[f'{obtem_coluna(c)}_{obtem_linha(c)}']


def obtem_coordenadas(m, s: str) -> tuple:
    def get_coords(m, fn):
        return tuple([i for i in m if fn(m[i])])
    
    if s == 'tapadas':
        return get_coords(m, eh_parcela_tapada)
    elif s == 'marcadas':
        return get_coords(m, eh_parcela_marcada)
    elif s == 'limpas':
        return get_coords(m, eh_parcela_limpa)
    elif s == 'minadas':
        return get_coords(m, eh_parcela_minada)
    

def obtem_numero_minas_vizinhas(m, c) -> int:
    def if_exists(m, v):
        for i in m:
            return i in v 
    neighbours = obtem_coordenadas_vizinhas(c)
    return filter(if_exists(m, neighbours), neighbours) 


m1 = cria_campo('D', 5)
print
