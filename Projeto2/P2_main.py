# -*- coding: utf-8 -*-
# Rodrigo Freitas Freire
# N 106485
# rodrigofreitasfreire@tecnico.ulisboa.pt

# Definicao explicita dos TAD para melhores documentacao das funcoes
Gerador = dict[str, int]
Coordenada = dict[str, int | str]
Parcela = dict[str, str | bool]
Campo = dict[str, Parcela]

#################
# TAD GERADOR
#################

# CONSTRUTORES
def cria_gerador(b: int, s: int) -> Gerador:
    '''Retorna um gerador que recebe o valor de bits `b` e o valor da seed `s`
    Representacao Interna:  {'b': `b`, 's': `s`}
    '''
    
    if not isinstance(b, int) or not isinstance(s, int) or s < 1 or b != 32 and b != 64:
        raise ValueError('cria_gerador: argumentos invalidos')
    if s > 2**b - 1: # seed nao pode ser o int maior que 32bit ou 64bit (tendo em conta o valor de `b`)
        raise ValueError('cria_gerador: argumentos invalidos')
    return {'b': b, 's': s}


def cria_copia_gerador(g: Gerador) -> Gerador:
    '''Recebe e retorna uma copia do gerador `g`'''
    
    return {i: g[i] for i in g}

# SELETORES
def obtem_estado(g: Gerador) -> int:
    '''Retorna o valor da seed do gerador `g` recebido'''
    
    return g['s']

# MODIFICADORES
def define_estado(g: Gerador, s: int) -> int:
    '''Modifica o valor da seed do gerador `g` com o valor `s`\n
    Retorna `s`'''
    
    g['s'] = s
    return s


def atualiza_estado(g: Gerador) -> int:
    '''Recebe um gerador `g` e atualiza o valor da sua seed utilizando a funcao `xorshift`'''
    
    def xorshift(g: Gerador, b: int) -> int:
        '''Funcao Auxiliar que recebe um gerador `g` e o valor de bits `b`
        e utiliza o algoritmo xorshift32/64 (depende do valor de `b`) para
        gerar uma nova seed\nRetorna o valor da nova seed'''
        
        seed = g['s']
        # O algoritmo utiliza operacoes bitwise
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

# RECONHECEDOR
def eh_gerador(arg) -> bool:
    '''Retorna `True` se `arg` for um TAD `Gerador` e `False` caso o contrario'''
    
    if not isinstance(arg, dict) or len(arg) != 2:
        return False
    if (('b', 's') != tuple(arg.keys()) or
            cria_copia_gerador(arg)['b'] != 32 and # unicas opcoes sao 32bits ou 64bits 
            cria_copia_gerador(arg)['b'] != 64 or
            obtem_estado(arg) < 1): # seed tem de ser um valor positivo
        return False
    return True

# TESTE
def geradores_iguais(g1: Gerador, g2: Gerador) -> bool:
    '''Recebe dois geradores `g1, g2` e retorna `True` se forem `Geradores` e se forem iguais'''
    
    if not eh_gerador(g1) or not eh_gerador(g2):
        return False
    return (cria_copia_gerador(g1)['b'], obtem_estado(g1)) == \
        (cria_copia_gerador(g2)['b'], obtem_estado(g2))

# TRANSFORMADOR
def gerador_para_str(g: Gerador) -> str:
    '''Recebe o gerador `g` e retorna a sua representacao externa'''
    
    return f'xorshift{cria_copia_gerador(g)["b"]}(s={obtem_estado(g)})'

# ALTO NIVEL
def gera_numero_aleatorio(g: Gerador, n: int) -> int:
    '''Recebe o gerador `g` atualizando o seu estado e retorna um numero pseudoaleatorio
    contido no intervalo [1, `n`]'''
    
    atualiza_estado(g)
    return 1 + obtem_estado(g) % n


def gera_carater_aleatorio(g: Gerador, c: str) -> str:
    '''Recebe o gerador `g` atualizando o seu estado e retorna um caracter pseudoaleatorio
    contido entre `"A"` e o caracter maiusculo `c`'''
    
    atualiza_estado(g)
    return chr(65 + obtem_estado(g) % (ord(c) - ord('A') + 1)) # 65 eh o offset, porque chr(65) = 'A'


##################
# TAD COORDENADA
##################

# CONSTRUTORES
def cria_coordenada(col: str, lin: int) -> Coordenada:
    '''Recebe os valores `col` e `lin` que correspondem ao valor da coluna e linha
    e retorna a coordenada apropriada\n
    Representacao interna: {'col': `col`, 'lin': `lin`}'''
    
    if (not isinstance(col, str) or not isinstance(lin, int) or
            len(col) != 1 or                # `col` so pode ser 1 letra
            not 65 <= ord(col) <= 90 or     # `col` tem de estar entre 'A' e 'Z'
            not 1 <= lin <= 99):
        raise ValueError('cria_coordenada: argumentos invalidos')
    return {'col': col, 'lin': lin}

# SELETORES
def obtem_coluna(c: Coordenada) -> str:
    '''Retorna o valor da coluna da coordenada `c` recebida'''
    
    return c['col']


def obtem_linha(c: Coordenada) -> int:
    '''Retorna o valor da linha da coordenada `c` recebida'''
    
    return c['lin']

# RECONHECEDOR
def eh_coordenada(arg) -> bool:
    '''Retorna `True` se `arg` for um TAD `Coordenada` e `False` caso o contrario'''
    
    if not isinstance(arg, dict) or len(arg) != 2:
        return False
    if (('col', 'lin') != tuple(arg.keys()) or
            not 65 <= ord(obtem_coluna(arg)) <= 90 or
            not 1 <= obtem_linha(arg) <= 99):
        return False
    return True

# TESTE
def coordenadas_iguais(c1: Coordenada, c2: Coordenada) -> bool:
    '''Recebe duas coordenadas `c1, c2` e retorna `True` se forem `Coordenadas` e se forem iguais'''
    
    if not eh_coordenada(c1) or not eh_coordenada(c2):
        return False
    return (obtem_coluna(c1), obtem_linha(c1)) == \
        (obtem_coluna(c2), obtem_linha(c2))

# TRANSFORMADOR
def coordenada_para_str(c: Coordenada) -> str:
    '''Recebe a coordenada `c` e retorna a sua representacao externa'''
    
    return f'{obtem_coluna(c)}0{obtem_linha(c)}' if obtem_linha(c) < 10 \
        else f'{obtem_coluna(c)}{obtem_linha(c)}' 


def str_para_coordenada(s: str) -> Coordenada:
    '''Recebe a representacao externa `s` e retorna a coordenada correspondente'''
    
    return cria_coordenada(s[0], int(s[1:]))

# ALTO NIVEL
def obtem_coordenadas_vizinhas(c: Coordenada) -> tuple:
    '''Retorna um tuplo com as coordenadas vizinhas a `c`'''
    
    neighbours = ()
    def loop_settings(i: int) -> list:
        '''Funcao auxiliar que gera uma lista com definicoes variaveis para ser utilizado na funcao `range`
        junto com um FOR loop de modo a tornar esse loop modular\n
        Esta funcao eh necessaria para que o mesmo FOR loop obtenha as coordenadas vizinhas em 4 etapas'''
        
        # Etapa 1: (i = 1) -> obtem coordenadas vizinhas acima da esquerda para a direita
        # Etapa 2: (i = 2) -> obtem coordenada vizinha ah direita
        # Etapa 3: (i = 3) -> obtem coordenadas vizinhas abaixo da direita para a esquerda
        # Etapa 4: (i = 4) -> obtem coordenada vizinha ah esquerda
        return [ord(obtem_coluna(c)) - 1, ord(obtem_coluna(c)) + 2] if i == 1 else \
            [ord(obtem_coluna(c)) + 1, ord(obtem_coluna(c)) + 2] if i == 2 else \
            [ord(obtem_coluna(c)) + 1, ord(obtem_coluna(c)) - 2, -1] if i == 3 else \
            [ord(obtem_coluna(c)) - 1, ord(obtem_coluna(c))]
                
    lines = (obtem_linha(c) - 1, obtem_linha(c), obtem_linha(c) + 1, obtem_linha(c)) # Cada das 4 etapas precisa da linha correspondente     
    for i, l in zip(range(1, 5), lines):
        for j in range(*loop_settings(i)):  # Operador * realiza o unpacking da lista retornada por `loop_settings`
            try:
                neighbours += (cria_coordenada(chr(j), l), )    # Usamos try/except para nao adicionar coordenadas invalidas e nao sair do programa
            except Exception:
                continue
    return neighbours


def obtem_coordenada_aleatoria(c: Coordenada, g: Gerador) -> Coordenada:
    '''Recebe uma coordenada `c` e um gerador `g` e retorna uma coordenada aleatoria utilizando `c`
    para definir a maxima coluna e linha'''
    
    return cria_coordenada(
        gera_carater_aleatorio(g, obtem_coluna(c)), 
        gera_numero_aleatorio(g, obtem_linha(c))
    )


#################
# TAD PARCELA
#################

# CONSTRUTORES
def cria_parcela() -> Parcela:
    '''Retorna uma parcela tapada sem mina escondida
    Representacao interna: {'state': `str`, 'mined': `bool`}'''
    
    return {'state': 'hidden', 'mined': False}


def cria_copia_parcela(p: Parcela) -> Parcela:
    '''Recebe uma parcela `p` e retorna uma copia'''
    
    return {i: p[i] for i in p}

# MODIFICADORES
def limpa_parcela(p: Parcela) -> Parcela:
    '''Recebe uma parcela `p` e modifica destrutivamente o seu estado para `limpa`
    Retorna a parcela `p` alterada'''
    
    p['state'] = 'clean'
    return p


def marca_parcela(p: Parcela) -> Parcela:
    '''Recebe uma parcela `p` e modifica destrutivamente o seu estado para `marcada`
    Retorna a parcela `p` alterada'''
    
    p['state'] = 'flagged'
    return p


def desmarca_parcela(p: Parcela) -> Parcela:
    '''Recebe uma parcela `p` e modifica destrutivamente o seu estado para `tapada`
    Retorna a parcela `p` alterada'''
    
    p['state'] = 'hidden'
    return p


def esconde_mina(p: Parcela) -> Parcela:
    '''Recebe uma parcela `p` e modifica destrutivamente o valor de mined para `True`
    efetivamente escondendo uma mina\n
    Retorna a parcela `p` alterada'''
    
    p['mined'] = True
    return p

# RECONHECEDOR
def eh_parcela(arg) -> bool:
    '''Retorna `True` se `arg` for um TAD `Parcela` e `False` caso o contrario'''
    
    if not isinstance(arg, dict) or len(arg) != 2:
        return False
    if (('state', 'mined') != tuple(arg.keys()) or
            arg['state'] not in ('clean', 'flagged', 'hidden') or
            arg['mined'] != True and arg['mined'] != False):
        return False
    return True


def eh_parcela_tapada(p: Parcela) -> bool:
    '''Recebe uma parcela `p` e retorna `True` se for uma parcela tapada\n
    E `False` caso o contrario'''
    
    return p['state'] == 'hidden'


def eh_parcela_marcada(p: Parcela) -> bool:
    '''Recebe uma parcela `p` e retorna `True` se for uma parcela marcada\n
    E `False` caso o contrario'''
    
    return p['state'] == 'flagged'


def eh_parcela_limpa(p: Parcela) -> bool:
    '''Recebe uma parcela `p` e retorna `True` se for uma parcela limpa\n
    E `False` caso o contrario'''
    
    return p['state'] == 'clean'


def eh_parcela_minada(p: Parcela) -> bool:
    '''Recebe uma parcela `p` e retorna `True` se for uma parcela minada\n
    E `False` caso contrario'''
    
    return p['mined'] == True

# TESTE
def parcelas_iguais(p1: Parcela, p2: Parcela) -> bool:
    '''Recebe duas parcelas `p1, p2` e retorna `True` se forem ambas TAD `Parcela`\n
    e se forem iguais. `False` caso contrario'''
    
    if not eh_parcela(p1) or not eh_parcela(p2):
        return False
    return p1['state'] == p2['state'] and p1['mined'] == p2['mined']

# TRANSFORMADOR
def parcela_para_str(p: Parcela) -> str:
    '''Devolve a representacao externa da parcela `p` em funcao do seu estado\n
    `# -> tapada`\n
    `@ -> marcada`\n
    `? -> limpa s/mina`\n
    `X -> limpa c/mina`'''
    
    state_chars = {'hidden': '#', 'flagged': '@', 'clean': '?','clean_mined': 'X'}
    
    # Apenas existem 3 estados (limpo, marcado, tapado). Logo eh preciso verificar se a parcela eh minada e limpa
    # para aceder ao caracter `X`
    if not p['mined'] or (p['state'] != 'clean' and p['mined']):
        return state_chars[p['state']]
    return state_chars['clean_mined']

# ALTO NIVEL
def alterna_bandeira(p) -> bool:
    '''Recebe uma parcela `p` e modifica o seu estado destrutivamente de modo 
    a marcar ou desmarcar a parcela'''
    
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

# CONSTRUTORES
def cria_campo(c: str, l: int) -> Campo:
    '''Recebe o numero maximo de colunas e linhas (`c`, `l`) e retorna um novo campo 
    com essas dimensoes populado com novas parcelas tapadas sem minas\n
    Representacao interna: {'A01': `Parcela`, 'B01': `Parcela`, ...etc}'''
    
    if (not isinstance(c, str) or not isinstance(l, int) or
            len(c) != 1 or              # `c` tem de ser apenas 1 letra
            not 65 <= ord(c) <= 90 or
            not 1 <= l <= 99):
        raise ValueError('cria_campo: argumentos invalidos')
    # Dois FOR loops (linhas, colunas). cada chave eh a representacao externa de uma coordenada
    # E o valor eh uma nova parcela
    return {
            f'{coordenada_para_str(cria_coordenada(chr(j), i))}': cria_parcela()
            for i in range(1, l + 1) 
            for j in range(65, ord(c) + 1)
    }

def cria_copia_campo(m: Campo) -> Campo:
    '''Recebe um campo `m` e retorna uma copia'''
    
    return {i: m[i].copy() for i in m}

# SELETORES
def obtem_ultima_coluna(m):
    return tuple(m.keys())[-1][0]


def obtem_ultima_linha(m):
    return int(tuple(m.keys())[-1][1:])


def obtem_parcela(m, c):
    return m[f'{coordenada_para_str(c)}']


def obtem_coordenadas(m, s: str) -> tuple:
    def get_coords(m, fn):
        return tuple([str_para_coordenada(i) for i in m if fn(m[i])])
    
    return get_coords(m, eh_parcela_tapada) if s == 'tapadas' else \
        get_coords(m, eh_parcela_marcada) if s == 'marcadas' else \
        get_coords(m, eh_parcela_limpa) if s == 'limpas' else \
        get_coords(m, eh_parcela_minada)

    
def eh_coordenada_do_campo(m, c) -> bool:
    return coordenada_para_str(c) in m


def in_bounds_and_is_bomb(m, c):
    return eh_coordenada_do_campo(m, c) and eh_parcela_minada(m[coordenada_para_str(c)])


def obtem_numero_minas_vizinhas(m, c):
    neighbours = obtem_coordenadas_vizinhas(c)
    return len(tuple(filter(lambda c: in_bounds_and_is_bomb(m, c), neighbours)))

# RECONHECEDORES
def eh_campo(m) -> bool:
    if not isinstance(m, dict) or len(m) < 1:
        return False
    for i in m:
        try:
            cria_coordenada(i[0], int(i[1:]))
        except Exception:
            return False
        if not eh_parcela(m[i]):
            return False
    return True

# TESTE
def campos_iguais(m1, m2) -> bool:
    return eh_campo(m1) and eh_campo(m2) and m1.items() == m2.items()

# TRANSFORMADOR
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

# AUXILARES P/ F.ALTO NIVEL
def empty_no_bombs_filter(m, c0, c0_last, c0_new, c):
    return eh_coordenada_do_campo(m, c) and obtem_numero_minas_vizinhas(m, c) == 0 and \
        c not in (*c0, *c0_last, *c0_new) and \
        eh_parcela_tapada(obtem_parcela(m, c))
        
def empty_near_bombs_filter(m, c1, c1_last, c1_new, c):
    return eh_coordenada_do_campo(m, c) and obtem_numero_minas_vizinhas(m, c) >= 1 and \
        c not in (*c1, *c1_last, *c1_new) and \
        eh_parcela_tapada(obtem_parcela(m, c))
        
# ALTO NIVEL
def coloca_minas(m, c, g, n):
    not_allowed_coords = (c, ) + obtem_coordenadas_vizinhas(c)
    def generate_coord(g):
            return obtem_coordenada_aleatoria(cria_coordenada(obtem_ultima_coluna(m), obtem_ultima_linha(m)), g)
    
    new_coord = generate_coord(g)
    for i in range(n):
        while (new_coord in not_allowed_coords or eh_parcela_minada(obtem_parcela(m, new_coord))):
            new_coord = generate_coord(g)
        esconde_mina(obtem_parcela(m, new_coord))
    return m 


def limpa_campo(m, c):
    if (eh_parcela_minada(obtem_parcela(m, c)) or obtem_numero_minas_vizinhas(m, c) >= 1):
        limpa_parcela(obtem_parcela(m, c))
        return m
    if not eh_parcela_tapada(obtem_parcela(m, c)): return m

    def get_clean_cells(m, c0, c1, c0_last, c1_last):
        if (*c0, *c1) == ():
            return c0_last + c1_last
        c0_new, c1_new = (), ()
        for i in c0:
            v = obtem_coordenadas_vizinhas(i)
            c0_new += tuple(filter(lambda c: empty_no_bombs_filter(m, c0, c0_last, c0_new, c), v))
            c1_new += tuple(filter(lambda c: empty_near_bombs_filter(m, c1, c1_last, c1_new, c), v))
        return get_clean_cells(m, c0_new, c1_new, c0 + c0_last, c1 + c1_last)
    
    results = get_clean_cells(m, (c, ), (), (), ())
    for i in results:
        limpa_parcela(obtem_parcela(m, i))
    return m


def jogo_ganho(m) -> bool:
    mined_cells = obtem_coordenadas(m, 'minadas')
    hidden_or_flagged = obtem_coordenadas(m, 'marcadas') + obtem_coordenadas(m, 'tapadas')
    return len(mined_cells) == len(hidden_or_flagged)

# FUNCOES ADICIONAIS
def until_valid_coordenate(m, c):
    while not eh_coordenada(c):
        c = input('Escolha uma coordenada:')
        try:
            if len(c) != 3: continue
            c = str_para_coordenada(c)
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
    def field_info(field, n):
        flags = len(obtem_coordenadas(field, 'marcadas'))
        print(f'   [Bandeiras {flags}/{n}]')
        print(campo_para_str(field))

    while True:
        field_info(field, n)
        if not turno_jogador(field):
            field_info(field, n)
            print('BOOOOOOOM!!!')
            return False
        if jogo_ganho(field):
            field_info(field, n)
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
