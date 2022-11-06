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
    if s > 2**b - 1:
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
        seed = g['s']
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
    return xorshift(g, g['b'])


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
            (cria_copia_gerador(g2)['b'], obtem_estado(g2)):
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


##################
# TAD COORDENADA
##################
def cria_coordenada(col: str, lin: int):
    if (not isinstance(col, str) or not isinstance(lin, int) or
            len(col) != 1 or
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
# TAD CAMPO
#################
def cria_campo(c: str, l: int):
    if (not isinstance(c, str) or not isinstance(l, int) or
            len(c) != 1 or
            not 65 <= ord(c) <= 90 or
            not 1 <= l <= 99):
        raise ValueError('cria_campo: argumentos invalidos')
    
    field = {}
    for i in range(1, l + 1):
        for j in range(65, ord(c) + 1):
            field[f'{coordenada_para_str(cria_coordenada(chr(j), i))}'] = cria_parcela()
            
    return field

def cria_copia_campo(m):
    return {i: m[i].copy() for i in m}


def obtem_ultima_coluna(m):
    return tuple(m.keys())[-1][0]


def obtem_ultima_linha(m):
    return int(tuple(m.keys())[-1][1:])


def obtem_parcela(m, c):
    return m[f'{coordenada_para_str(c)}']


def obtem_coordenadas(m, s: str) -> tuple:
    def get_coords(m, fn):
        return tuple([cria_coordenada(i[0], int(i[1:])) for i in m if fn(m[i])])
    
    if s == 'tapadas':
        return get_coords(m, eh_parcela_tapada)
    elif s == 'marcadas':
        return get_coords(m, eh_parcela_marcada)
    elif s == 'limpas':
        return get_coords(m, eh_parcela_limpa)
    elif s == 'minadas':
        return get_coords(m, eh_parcela_minada)

    
def eh_coordenada_do_campo(m, c) -> bool:
    return coordenada_para_str(c) in m


def in_bounds_and_is_bomb(m, c):
    return eh_coordenada_do_campo(m, c) and eh_parcela_minada(m[coordenada_para_str(c)])


def obtem_numero_minas_vizinhas(m, c):
    neighbours = obtem_coordenadas_vizinhas(c)
    return len(tuple(filter(lambda c: in_bounds_and_is_bomb(m, c), neighbours)))


def eh_campo(m: any) -> bool:
    if not isinstance(m, dict) or len(m) < 1:
        return False
    for i in m:
        try:
            coord = cria_coordenada(i[0], int(i[1:]))
        except Exception:
            return False
        if not eh_parcela(m[i]):
            return False
    return True


def campos_iguais(m1, m2) -> bool:
    return eh_campo(m1) and eh_campo(m2) and m1.items() == m2.items()


def campo_para_str(m) -> str:
    columns = [chr(i) for i in range(65, ord(obtem_ultima_coluna(m)) + 1)]
    lines = [f'0{i}' if i < 10 else f'{i}' for i in range(1, obtem_ultima_linha(m) + 1)]  

    def populate_field(m, lin_list, col_list):
        field = ''
        for i in lin_list:
            field += f'{i}|'
            for j in col_list:
                parcela_str = parcela_para_str(m[f'{j}{i}'])
                if parcela_str == '?':
                    if obtem_numero_minas_vizinhas(m, cria_coordenada(j, int(i))) == 0:
                        field += ' '
                    else:
                        field += f'{obtem_numero_minas_vizinhas(m, cria_coordenada(j, int(i)))}'
                else:
                    field += parcela_para_str(m[f'{j}{i}'])
            field += '|\n'
        return field
       
    return (
        f"   {''.join(columns)}\n"
        f"  +{'-' * len(columns)}+\n"
        f"{populate_field(m, lines, columns)}  +{'-' * len(columns)}+"
    )  


def coloca_minas(m, c, g, n):
    not_allowed_coords = (c, ) + obtem_coordenadas_vizinhas(c)
    def generate_coord(g):
        return obtem_coordenada_aleatoria(cria_coordenada(obtem_ultima_coluna(m), obtem_ultima_linha(m)), g)
    
    new_coord = generate_coord(g)
    for i in range(n):
        while (new_coord in not_allowed_coords or eh_parcela_minada(obtem_parcela(m, new_coord)) == True):
            new_coord = generate_coord(g)
        esconde_mina(obtem_parcela(m, new_coord))
    return m
            

def empty_no_bombs_filter(m, c0, c0_last, c0_new, c):
    return eh_coordenada_do_campo(m, c) and obtem_numero_minas_vizinhas(m, c) == 0 and \
        c not in (*c0, *c0_last, *c0_new) and \
        eh_parcela_tapada(obtem_parcela(m, c))
        
def empty_near_bombs_filter(m, c1, c1_last, c1_new, c):
    return eh_coordenada_do_campo(m, c) and obtem_numero_minas_vizinhas(m, c) >= 1 and \
        c not in (*c1, *c1_last, *c1_new) and \
        eh_parcela_tapada(obtem_parcela(m, c)) 


def limpa_campo(m, c):
    if not eh_parcela_tapada(obtem_parcela(m, c)): return m
    if (eh_parcela_minada(obtem_parcela(m, c)) or obtem_numero_minas_vizinhas(m, c) >= 1):
        limpa_parcela(obtem_parcela(m, c))
        return m

    def get_clean_cells(m, c0, c1, c0_last, c1_last, p: int):
        if (*c0, *c1) == ():
            return c0_last + c1_last
        
        c0_new, c1_new = (), ()
        for i in c0:
            v = obtem_coordenadas_vizinhas(i)
            c0_new += tuple(filter(lambda c: empty_no_bombs_filter(m, c0, c0_last, c0_new, c), v))
            c1_new += tuple(filter(lambda c: empty_near_bombs_filter(m, c1, c1_last, c1_new, c), v))
        return get_clean_cells(m, c0_new, c1_new, c0 + c0_last, c1 + c1_last, p + 1)
    results = get_clean_cells(m, (c, ), (), (), (), 1)

    for i in results:
        limpa_parcela(obtem_parcela(m, i))
    
    return m


def jogo_ganho(m) -> bool:
    mined_cells = obtem_coordenadas(m, 'minadas')
    hidden_or_flagged = obtem_coordenadas(m, 'marcadas') + obtem_coordenadas(m, 'tapadas')
    return len(mined_cells) == len(hidden_or_flagged)


def until_valid_coordenate(m, c):
    while not eh_coordenada(c):
        c = input('Escolha uma coordenada:')
        try:
            if len(c) != 3: continue
            c = cria_coordenada(c[0], int(c[1:]))
            if not eh_coordenada_do_campo(m, c):
                c = ''
        except Exception:
            continue
    return c


def turno_jogador(m) -> bool:
    option, coord = '', ''
    while option != 'L' and option != 'M':
        option = input('Escolha uma ação, [L]impar ou [M]arcar:')
    coord = until_valid_coordenate(m, coord)

    if option == 'L':
        limpa_campo(m, coord)
        return not eh_parcela_minada(obtem_parcela(m, coord))
    alterna_bandeira(obtem_parcela(m, coord))
                
    return True


def main_loop(field, n):
    while True:
        flags = len(obtem_coordenadas(field, 'marcadas'))
        print(f'   [Bandeiras {flags}/{n}]')
        print(campo_para_str(field))
        
        if not turno_jogador(field):
            print(f'   [Bandeiras {flags}/{n}]')
            print(campo_para_str(field))
            print('BOOOOOOOM!!!')
            return False
        if jogo_ganho(field):
            print(f'   [Bandeiras {flags}/{n}]')
            print(campo_para_str(field))
            print('VITORIA!!!')
            return True

def minas(c: str, l: int, n: int, d: int, s: int) -> bool:
    if (not isinstance(c, str) or not isinstance(l, int) or
            not isinstance(n, int) or not isinstance(d, int) or
            not isinstance(s, int) or len(c) != 1 or
            not 65 <= ord(c) <= 90 or not 1 <= l <= 99 or
            not 1 <= n < (ord(c) - 64) * l or d != 32 and d != 64 or
            s < 1):
        raise ValueError('minas: argumentos invalidos')
    area = (ord(c) - 64 ) * l
    if area < 6:
        raise ValueError('minas: argumentos invalidos')
    
    field, generator, init_coord = cria_campo(c, l), cria_gerador(d, s), ''
    print(f'   [Bandeiras 0/{n}]')
    print(campo_para_str(field))
    init_coord = until_valid_coordenate(field, init_coord)
    
    field = coloca_minas(field, init_coord, generator, n)
    limpa_campo(field, init_coord)
    
    return main_loop(field, n)


minas('Z', 10, 16, 64, 2454)