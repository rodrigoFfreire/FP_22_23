# -*- coding: utf-8 -*-
# Rodrigo Freitas Freire
# N 106485
# rodrigofreitasfreire@tecnico.ulisboa.pt


#################
# TAD GERADOR
#################

# CONSTRUTORES
def cria_gerador(b: int, s: int):
    """Retorna um gerador que recebe o valor de bits `b` e o valor da seed `s`
    Representacao Interna:  {'b': `b`, 's': `s`}
    """
    # seed tem de ser positiva e bits = [32 ou 64]
    if not isinstance(b, int) or not isinstance(s, int) or s < 1 or b != 32 and b != 64:
        raise ValueError('cria_gerador: argumentos invalidos')
    # seed nao pode ser o int maior que 32bit ou 64bit (tendo em conta o valor de `b`)
    if s > 2 ** b - 1:
        raise ValueError('cria_gerador: argumentos invalidos')
    return {'b': b, 's': s}


def cria_copia_gerador(g):
    """Recebe e retorna uma copia do gerador `g`"""

    return {i: g[i] for i in g}


# SELETORES
def obtem_estado(g) -> int:
    """Retorna o valor da seed do gerador `g` recebido"""

    return g['s']


# MODIFICADORES
def define_estado(g, s: int) -> int:
    """Modifica o valor da seed do gerador `g` com o valor `s`\n
    Retorna a nova seed `s`"""

    g['s'] = s
    return s


def atualiza_estado(g) -> int:
    """Recebe um gerador `g` e atualiza o valor da sua seed utilizando a funcao `xorshift`"""

    def xorshift(g, b: int) -> int:
        """Funcao Auxiliar que recebe um gerador `g` e o valor de bits `b`
        e utiliza o algoritmo xorshift32/64 (depende do valor de `b`) para
        gerar uma nova seed\n
        Retorna o valor da nova seed"""

        seed = g['s']
        if b == 32:
            seed ^= (seed << 13) & 0xFFFFFFFF   # 0xFFFFFFFF 32bit integer limit
            seed ^= (seed >> 17) & 0xFFFFFFFF
            seed ^= (seed << 5) & 0xFFFFFFFF
            define_estado(g, seed)
            return seed
        else:
            seed ^= (seed << 13) & 0xFFFFFFFFFFFFFFFF   # 0xFFFFFFFFFFFFFFFF 64bit integer limit
            seed ^= (seed >> 7) & 0xFFFFFFFFFFFFFFFF
            seed ^= (seed << 17) & 0xFFFFFFFFFFFFFFFF
            define_estado(g, seed)
            return seed

    return xorshift(g, g['b'])


# RECONHECEDOR
def eh_gerador(arg) -> bool:
    """Retorna `True` se `arg` for um TAD `Gerador` e `False` caso o contrario"""

    if not isinstance(arg, dict) or len(arg) != 2:
        return False
    if (('b', 's') != tuple(arg.keys()) or
            cria_copia_gerador(arg)['b'] != 32 and
            cria_copia_gerador(arg)['b'] != 64 or
            obtem_estado(arg) < 1):
        return False
    return True


# TESTE
def geradores_iguais(g1, g2) -> bool:
    """Recebe dois geradores `g1, g2` e retorna `True` se forem `Geradores` e se forem iguais"""

    if not eh_gerador(g1) or not eh_gerador(g2):
        return False
    return (cria_copia_gerador(g1)['b'], obtem_estado(g1)) == \
           (cria_copia_gerador(g2)['b'], obtem_estado(g2))


# TRANSFORMADOR
def gerador_para_str(g) -> str:
    """Recebe o gerador `g` e retorna a sua representacao externa"""

    return f'xorshift{cria_copia_gerador(g)["b"]}(s={obtem_estado(g)})' # Ex: xorshift64(s=1234)


# ALTO NIVEL
def gera_numero_aleatorio(g, n: int) -> int:
    """Recebe o gerador `g` atualizando o seu estado e retorna um numero pseudoaleatorio
    contido no intervalo [1, `n`]"""

    atualiza_estado(g)
    return 1 + obtem_estado(g) % n  # numero entre [1, n]


def gera_carater_aleatorio(g, c: str) -> str:
    """Recebe o gerador `g` atualizando o seu estado e retorna um caracter pseudoaleatorio
    contido entre `"A"` e o caracter maiusculo `c`"""

    atualiza_estado(g)
    return chr(65 + obtem_estado(g) % (ord(c) - ord('A') + 1))  # letra entre [chr(65), chr(c)]


##################
# TAD COORDENADA
##################

# CONSTRUTORES
def cria_coordenada(col: str, lin: int):
    """Recebe os valores `col` e `lin` que correspondem ao valor da coluna e linha
    e retorna a coordenada apropriada\n
    Representacao interna: {'col': `col`, 'lin': `lin`}"""

    if (not isinstance(col, str) or not isinstance(lin, int) or
            len(col) != 1 or             # `col` so pode ser 1 letra
            not 65 <= ord(col) <= 90 or  # `col` tem de estar entre 'A' e 'Z'
            not 1 <= lin <= 99):         # `lin` tem de estar entre 1 e 99
        raise ValueError('cria_coordenada: argumentos invalidos')
    return {'col': col, 'lin': lin}


# SELETORES
def obtem_coluna(c) -> str:
    """Retorna o valor da coluna da coordenada `c` recebida"""

    return c['col']


def obtem_linha(c) -> int:
    """Retorna o valor da linha da coordenada `c` recebida"""

    return c['lin']


# RECONHECEDOR
def eh_coordenada(arg) -> bool:
    """Retorna `True` se `arg` for um TAD `Coordenada` e `False` caso o contrario"""

    if not isinstance(arg, dict) or len(arg) != 2:
        return False
    if (('col', 'lin') != tuple(arg.keys()) or
            not 65 <= ord(obtem_coluna(arg)) <= 90 or
            not 1 <= obtem_linha(arg) <= 99):
        return False
    return True


# TESTE
def coordenadas_iguais(c1, c2) -> bool:
    """Recebe duas coordenadas `c1, c2` e retorna `True` se forem `Coordenadas` e se forem iguais"""

    if not eh_coordenada(c1) or not eh_coordenada(c2):
        return False
    return (obtem_coluna(c1), obtem_linha(c1)) == \
           (obtem_coluna(c2), obtem_linha(c2))


# TRANSFORMADOR
def coordenada_para_str(c) -> str:
    """Recebe a coordenada `c` e retorna a sua representacao externa"""

    return f'{obtem_coluna(c)}0{obtem_linha(c)}' if obtem_linha(c) < 10 \
        else f'{obtem_coluna(c)}{obtem_linha(c)}'   # Ex: A05 ; Z87


def str_para_coordenada(s: str):
    """Recebe a representacao externa `s` e retorna a coordenada correspondente"""

    return cria_coordenada(s[0], int(s[1:]))


# ALTO NIVEL
def obtem_coordenadas_vizinhas(c) -> tuple:
    """Retorna um tuplo com as coordenadas vizinhas a `c`"""

    neighbours, x, y = (), ord(obtem_coluna(c)), obtem_linha(c)     # x, y -> coordenadas de `c`
    order = (
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),     # coordenadas acima de `c`
            (x + 1, y),                                     # coordenada ah direita de `c`
            (x + 1, y + 1), (x, y + 1), (x - 1, y + 1),     # coordenadas abiaxo de `c`
            (x - 1, y)                                      # coordenada ah esquerda de `c`
        )
    for i in order:
        try:
            # Usamos try/except para filtrar coordenadas invalidas e nao sair do programa
            neighbours += (cria_coordenada(chr(i[0]), i[1]),)
        except ValueError:
            continue
    return neighbours


def obtem_coordenada_aleatoria(c, g):
    """Recebe uma coordenada `c` e um gerador `g` e retorna uma coordenada aleatoria utilizando `c`
    para definir a maxima coluna e linha"""

    return cria_coordenada(
        gera_carater_aleatorio(g, obtem_coluna(c)),
        gera_numero_aleatorio(g, obtem_linha(c))
    )


#################
# TAD PARCELA
#################

# CONSTRUTORES
def cria_parcela():
    """Retorna uma parcela tapada sem mina escondida
    Representacao interna: {'state': `str`, 'mined': `bool`}"""

    return {'state': 'hidden', 'mined': False}


def cria_copia_parcela(p):
    """Recebe uma parcela `p` e retorna uma copia"""

    return {i: p[i] for i in p}


# MODIFICADORES
def limpa_parcela(p):
    """Recebe uma parcela `p` e modifica destrutivamente o seu estado para `limpa`
    Retorna a parcela `p` alterada"""

    p['state'] = 'clean'
    return p


def marca_parcela(p):
    """Recebe uma parcela `p` e modifica destrutivamente o seu estado para `marcada`
    Retorna a parcela `p` alterada"""

    p['state'] = 'flagged'
    return p


def desmarca_parcela(p):
    """Recebe uma parcela `p` e modifica destrutivamente o seu estado para `tapada`
    Retorna a parcela `p` alterada"""

    p['state'] = 'hidden'
    return p


def esconde_mina(p):
    """Recebe uma parcela `p` e modifica destrutivamente o valor de mined para `True`
    efetivamente escondendo uma mina\n
    Retorna a parcela `p` alterada"""

    p['mined'] = True
    return p


# RECONHECEDOR
def eh_parcela(arg) -> bool:
    """Retorna `True` se `arg` for um TAD `Parcela` e `False` caso o contrario"""

    if not isinstance(arg, dict) or len(arg) != 2:
        return False
    if (('state', 'mined') != tuple(arg.keys()) or
            arg['state'] not in ('clean', 'flagged', 'hidden') or
            not arg['mined'] and arg['mined']):     # Se arg['mined] nao for True ou False
        return False
    return True


def eh_parcela_tapada(p) -> bool:
    """Recebe uma parcela `p` e retorna `True` se for uma parcela tapada\n
    E `False` caso o contrario"""

    return p['state'] == 'hidden'


def eh_parcela_marcada(p) -> bool:
    """Recebe uma parcela `p` e retorna `True` se for uma parcela marcada\n
    E `False` caso o contrario"""

    return p['state'] == 'flagged'


def eh_parcela_limpa(p) -> bool:
    """Recebe uma parcela `p` e retorna `True` se for uma parcela limpa\n
    E `False` caso o contrario"""

    return p['state'] == 'clean'


def eh_parcela_minada(p) -> bool:
    """Recebe uma parcela `p` e retorna `True` se for uma parcela minada\n
    E `False` caso contrario"""

    return p['mined']


# TESTE
def parcelas_iguais(p1, p2) -> bool:
    """Recebe duas parcelas `p1, p2` e retorna `True` se forem ambas TAD `Parcela`\n
    e se forem iguais. `False` caso contrario"""

    if not eh_parcela(p1) or not eh_parcela(p2):
        return False
    return p1['state'] == p2['state'] and p1['mined'] == p2['mined']


# TRANSFORMADOR
def parcela_para_str(p) -> str:
    """Devolve a representacao externa da parcela `p` em funcao do seu estado\n
    `#` -> tapada\n
    `@` -> marcada\n
    `?` -> limpa s/mina\n
    `X` -> limpa c/mina
    """

    state_chars = {'hidden': '#', 'flagged': '@', 'clean': '?', 'clean_mined': 'X'}

    # Apenas existem 3 estados (limpo, marcado, tapado). Logo eh preciso verificar se
    # a parcela eh (minada e limpa) para aceder ao caracter `X`
    if not p['mined'] or (p['state'] != 'clean' and p['mined']):
        return state_chars[p['state']]
    return state_chars['clean_mined']


# ALTO NIVEL
def alterna_bandeira(p) -> bool:
    """Recebe uma parcela `p` e modifica o seu estado destrutivamente de modo
    a marcar ou desmarcar a parcela"""

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
def cria_campo(c: str, l: int):
    """Recebe o numero maximo de colunas e linhas (`c`, `l`) e retorna um novo campo
    com essas dimensoes populado com novas parcelas tapadas sem minas\n
    Representacao interna: {'A01': `Parcela`, 'B01': `Parcela`, ...etc}"""

    if (not isinstance(c, str) or not isinstance(l, int) or
            len(c) != 1 or              # `c` tem de ser apenas 1 letra
            not 65 <= ord(c) <= 90 or   # `c` tem de estar entre 'A' e 'Z'
            not 1 <= l <= 99):          # `l` tem de estar entre 1 e 99
        raise ValueError('cria_campo: argumentos invalidos')
    
    # Dois FOR loops (linhas, colunas). cada chave eh a representacao externa de uma coordenada
    # e o valor eh uma nova parcela
    return {
        f'{coordenada_para_str(cria_coordenada(chr(j), i))}': cria_parcela()    # Ex: 'A01': cria_parcela()
        for i in range(1, l + 1)
        for j in range(65, ord(c) + 1)
    }


def cria_copia_campo(m):
    """Recebe um campo `m` e retorna uma copia"""

    return {i: m[i].copy() for i in m}


# SELETORES
def obtem_ultima_coluna(m) -> str:
    """Retorna a string que corresponde ah ultima coluna do campo `m`"""
    return tuple(m.keys())[-1][0]


def obtem_ultima_linha(m) -> int:
    """Retorna o valor que corresponde ah ultima linha do campo `m`"""
    return int(tuple(m.keys())[-1][1:])


def obtem_parcela(m, c):
    """Retorna a parcela correspondente ah coordenada `c` do campo `m`"""
    return m[f'{coordenada_para_str(c)}']


def obtem_coordenadas(m, s: str) -> tuple:
    """Retorna o tuplo constituido pelas coordenadas do campo `m` que tem
    estado `s` (tapadas, minadas, marcadas, limpas)"""

    def get_coords(m, fn) -> tuple:
        """Funcao auxiliar recebe campo `m` e uma funcao `fn` que serve como predicado
        para filtrar as coordenadas"""

        return tuple([str_para_coordenada(i) for i in m if fn(m[i])])

    return get_coords(m, eh_parcela_tapada) if s == 'tapadas' else \
        get_coords(m, eh_parcela_marcada) if s == 'marcadas' else \
        get_coords(m, eh_parcela_limpa) if s == 'limpas' else \
        get_coords(m, eh_parcela_minada)


def eh_coordenada_do_campo(m, c) -> bool:
    """Retorna `True` se a coordenada `c` existir no campo `m`\n
    `False` caso contrario"""

    return coordenada_para_str(c) in m


def in_bounds_and_is_bomb(m, c):
    """Funcao auxiliar verifica se a coordenada `c` existe no campo `m` e
    se a parcela correspondente eh minada"""

    return eh_coordenada_do_campo(m, c) and eh_parcela_minada(m[coordenada_para_str(c)])


def obtem_numero_minas_vizinhas(m, c):
    """Retorna o numero de parcelas minadas do campo `m` e na vizinhanca da coordenada `c`"""

    neighbours = obtem_coordenadas_vizinhas(c)
    return len(tuple(filter(lambda c: in_bounds_and_is_bomb(m, c), neighbours)))


# RECONHECEDORES
def eh_campo(arg) -> bool:
    """Retorna `True` se `arg` eh um TAD `Campo`\n
    `False` caso contrario"""

    if not isinstance(arg, dict) or len(arg) < 1:
        return False
    for i in arg:
        try:
            # try/except para verificar se existe uma coordenada no campo invalida
            cria_coordenada(i[0], int(i[1:]))
        except ValueError:
            return False
        if not eh_parcela(arg[i]):
            return False
    return True


# TESTE
def campos_iguais(m1, m2) -> bool:
    """Retorna `True` se (`m1`, `m2`) forem ambos TAD `Campo` e se forem iguais"""

    return eh_campo(m1) and eh_campo(m2) and m1.items() == m2.items()


# TRANSFORMADOR
def campo_para_str(m) -> str:
    """Retorna a representacao externa do campo `m`"""

    # Lista das colunas ex: ['A', 'B', 'C', ...]
    columns = [chr(i) for i in range(65, ord(obtem_ultima_coluna(m)) + 1)]
    # Lista das linhas ex: ['01', '02', '03', ...]
    lines = [f'0{i}' if i < 10 else f'{i}' for i in range(1, obtem_ultima_linha(m) + 1)]

    def populate_field(m, lin_list: list, col_list: list) -> str:
        """Funcao auxiliar que retorna linhas do campo `m` utilizando as listas `lin_list` e `col_list`"""

        field = ''
        for i in lin_list:
            field += f'{i}|'  # Inicia a linha com o numero da linha. ex: 01|
            for j in col_list:
                parcela_str = parcela_para_str(m[f'{j}{i}'])
                if parcela_str == '?':
                    if obtem_numero_minas_vizinhas(m, cria_coordenada(j, int(i))) == 0:
                        field += ' '  # se a celula tiver 0 bombas na vizinhanca
                    else:
                        field += f'{obtem_numero_minas_vizinhas(m, cria_coordenada(j, int(i)))}'
                else:
                    field += parcela_para_str(m[f'{j}{i}'])
            field += '|\n'  # Acaba a linha e adiciona \n para estar pronta para a proxima linha
        return field

    return (
        f"   {''.join(columns)}\n"  # colunas ex: ABCDEFGH..
        f"  +{'-' * len(columns)}+\n"  # limites superiores do campo do campo  (+--...--+)
        f"{populate_field(m, lines, columns)}  +{'-' * len(columns)}+"  # As linhas do campo e os limites inferiores
    )


# AUXILARES P/ F.ALTO NIVEL
def no_bombs_filter(m, c0: tuple, c0_last: tuple, c0_new: tuple, c):
    """Funcao auxiliar a `limpa_campo` filtra o tuplo de coordenadas `c0` de modo a retirar coordenadas que:\n
    Ja foram limpas (`c0_last`) ou ja foram adicionadas a um tuplo para serem limpas (`c0_new`)\n
    Nao pertencam ao campo\n
    Nao Tenham minas na vizinhanca\n"""

    return eh_coordenada_do_campo(m, c) and obtem_numero_minas_vizinhas(m, c) == 0 and \
        c not in (*c0, *c0_last, *c0_new) and \
        eh_parcela_tapada(obtem_parcela(m, c))


def near_bombs_filter(m, c1: tuple, c1_last: tuple, c1_new: tuple, c):
    """Funcao auxiliar a `limpa_campo` filtra o tuplo de coordenadas `c1` de modo a retirar coordenadas que:\n
    Ja foram limpas (`c1_last`) ou ja foram adicionadas a um tuplo para serem limpas (`c1_new`)\n
    Nao pertencam ao campo\n
    Tenham 1 ou mais minas na vizinhanca\n"""

    return eh_coordenada_do_campo(m, c) and obtem_numero_minas_vizinhas(m, c) >= 1 and \
        c not in (*c1, *c1_last, *c1_new) and \
        eh_parcela_tapada(obtem_parcela(m, c))


# ALTO NIVEL
def coloca_minas(m, c, g, n: int):
    """Retorna o campo `m` destrutivamente modificado que esconde `n` minas geradas aleatoriamente
    pelo o gerador `g` mas que nao coincidam com a coordenada `c` e a sua vizinhanca ou que ja tenham
    minas"""

    not_allowed_coords = (c,) + obtem_coordenadas_vizinhas(c)

    def generate_coord(g):
        return obtem_coordenada_aleatoria(cria_coordenada(obtem_ultima_coluna(m), obtem_ultima_linha(m)), g)

    new_coord = generate_coord(g)
    for i in range(n):
        # Enquanto `new_coord` nao for uma coordenada adequada para ser 
        while new_coord in not_allowed_coords or eh_parcela_minada(obtem_parcela(m, new_coord)):
            new_coord = generate_coord(g)
        esconde_mina(obtem_parcela(m, new_coord))
    return m


def limpa_campo(m, c):
    """Retorna o campo `m` destrutivamente modificado limpando a parcela de coordenada `c`
    Se nao houver nenhuma mina escondida na vizinhanca vai limpando todas as parcelas vizinhas"""

    # Limpa somente essa parcela se tiver minas na vizinhanca
    if eh_parcela_minada(obtem_parcela(m, c)) or obtem_numero_minas_vizinhas(m, c) >= 1:
        limpa_parcela(obtem_parcela(m, c))
        return m
    # Nao modifica nada se nao for uma parcela tapada
    if not eh_parcela_tapada(obtem_parcela(m, c)):
        return m

    results = ()
    c0, c1 = (c, ), ()          # (`c0` e `c1`) -> coordenadas com (0, >=1) minas vizinhas para limpar
    c0_last, c1_last = (), ()   # (`c0_last`, `c1_last`) -> coordenadas (0, >=1) minas vizinhas que ja foram limpas
    while c0 or c1:
        c0_new, c1_new = (), ()     # coordenadas com (0, >=1) minas vizinhas que serao limpas na proxima iteracao
        for i in c0:
            v = obtem_coordenadas_vizinhas(i)
            # Filtrar os tuplos de modo a evitar coordenadas repetidas para melhor eficiencia
            c0_new += tuple(filter(lambda c: no_bombs_filter(m, c0, c0_last, c0_new, c), v))
            c1_new += tuple(filter(lambda c: near_bombs_filter(m, c1, c1_last, c1_new, c), v))
            
        # atualiza se o valor de `c0` e `c1` para as novas coordenadas a ser limpas
        c0, c1 = c0_new, c1_new
        # adiciona-se as que foram limpas para evitar coordenadas repetidas na proxima iteracao para melhor eficiencia
        c0_last, c1_last = c0 + c0_last, c1 + c1_last
        
    results = c0_last + c1_last
    for i in results:
        limpa_parcela(obtem_parcela(m, i))
    return m


# FUNCOES ADICIONAIS
def jogo_ganho(m) -> bool:
    """Recebe um campo `m` e retorna `True` se todas as parcelas sem minas se encontram limpas\n
    `False` caso contrario"""

    mined_cells = obtem_coordenadas(m, 'minadas')
    hidden_or_flagged = obtem_coordenadas(m, 'marcadas') + obtem_coordenadas(m, 'tapadas')
    return len(mined_cells) == len(hidden_or_flagged)


def until_valid_coordenate(m, c: str):
    """Funcao auxiliar que faz um loop enquanto a representacao externa `c`
    de uma coordenada do campo `m` inserida pelo utilizador nao esteja correta"""

    while not eh_coordenada(c):
        c = input('Escolha uma coordenada:')
        try:
            if len(c) != 3:     # c tem de ter 3 caracteres pois a repr. externa da coordenada eh 'LXX'
                continue
            c = str_para_coordenada(c)
            if not eh_coordenada_do_campo(m, c):
                c = ''
        except ValueError:
            continue
    return c


def turno_jogador(m) -> bool:
    """Funcao que permite ao utilizador interagir com o jogo do campo `m`
    propondo duas opcoes `Limpar` e `Marcar` executando essas acoes\n
    Retorna `False` se caso o jogador tenha limpo uma parcela minada\n
    `True` caso contrario"""

    option, coord = '', ''
    while option != 'L' and option != 'M':
        option = input('Escolha uma ação, [L]impar ou [M]arcar:')
    coord = until_valid_coordenate(m, coord)

    if option == 'L':
        limpa_campo(m, coord)
        return not eh_parcela_minada(obtem_parcela(m, coord))
    # Se option == 'M'
    alterna_bandeira(obtem_parcela(m, coord))

    return True


def main_loop(field, n: int) -> bool:
    """Funcao auxiliar que gera o loop principal
    que permite ao utilizador jogar\n
    Retorna `True` se o jogador ganhar\n
    `False` caso contrario"""

    def field_info(field, n) -> None:
        """Funcao auxiliar que gera a GUI do campo `field`
        `n` eh o numero de minas que existem no campo"""

        flags = len(obtem_coordenadas(field, 'marcadas'))   # num de celulas marcadas no campo
        print(f'   [Bandeiras {flags}/{n}]')
        print(campo_para_str(field))

    while True:
        field_info(field, n)
        if not turno_jogador(field):
            field_info(field, n)
            print('BOOOOOOOM!!!')   # O jogador perdeu pois tentou limpar uma mina
            return False
        if jogo_ganho(field):
            field_info(field, n)
            print('VITORIA!!!')     # O jogador venceu pois limpou todas as celulas nao minadas
            return True


def minas(c: str, l: int, n: int, d: int, s: int) -> bool:
    """Funcao principal em conjunto com funcoes auxiliares permitem jogar
    o jogo das minas.\n
    `c` -> coluna maxima\n
    `l` -> linha maxima\n
    `n` -> num de minas\n
    `d` -> bits do gerador\n
    `s` -> seed incial do gerador"""

    if (not isinstance(c, str) or not isinstance(l, int) or
            not isinstance(n, int) or not isinstance(d, int) or
            not isinstance(s, int) or len(c) != 1 or
            not 65 <= ord(c) <= 90 or not 1 <= l <= 99 or   # coordenadas entre 'A01' e 'Z99' apenas
            # num de minas tem de ser > 1 e menor que num de parcelas do campo
            d != 32 and d != 64 or not 1 <= n < (ord(c) - 64) * l or
            s < 1):  # seed tem de ser positiva
        raise ValueError('minas: argumentos invalidos')
    area = (ord(c) - 64) * l
    if area < 6:  # Se area do campo for < 6 (campo menor que 2x3 ou 3x2) nao haveria espaco para gerar minas
        raise ValueError('minas: argumentos invalidos')

    field, generator, init_coord = cria_campo(c, l), cria_gerador(d, s), ''
    print(f'   [Bandeiras 0/{n}]')
    print(campo_para_str(field))
    init_coord = until_valid_coordenate(field, init_coord)

    field = coloca_minas(field, init_coord, generator, n)
    limpa_campo(field, init_coord)

    return main_loop(field, n)
