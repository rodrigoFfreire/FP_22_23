# -*- coding: utf-8 -*-
# Rodrigo Freitas Freire
# N 106485
# rodrigofreitasfreire@tecnico.ulisboa.pt

###################################
# PART 1 - Justificacao de texto
###################################

def limpa_texto(text: str) -> str:
    '''Esta funcao limpa o texto removendo espacos duplicados em qualquer lugar
    da frase e remove caracteres brancos ASCII
    '''
    return ' '.join(text.split())


def corta_texto(text: str, size: int) -> str:
    '''Esta funcao corta {text} em duas partes:
    1 -> Contem todo o texto que tem largura {size} sem cortar palavras
    ao meio
    2 -> Contem o resto de {text} que sobrou
    '''
    text1 = ()
    text2 = text.split()
    for word in text.split():
        if len(word) > size:
            # Parar de adicionar texto a {text1} se {word} exceder a largura restante
            return ' '.join(text1), ' '.join(text2)
        else:
            text1 += (word, )
            text2.remove(word)
            size -= len(word) + 1

    return ' '.join(text1), ' '.join(text2)


def insere_espacos(text: str, padding: int) -> str:
    '''Esta funcao insere espaços entre as palavras de forma homogenea para que
    {text} atinga uma certa largura
    '''
    pad = padding - len(text)
    text_splitted = text.split()
    if len(text_splitted) < 2:
        return text + (' ' * pad)
    else:
        while pad > 0:
            for i, word in enumerate(text_splitted):
                if word != text_splitted[-1]:      # Nao inserir espacos na ultima palavra
                    text_splitted[i] = word + ' '
                    pad -= 1
                if pad == 0:
                    # Previne espacos extra enquanto o for loop nao termina a sua execucao
                    break

    return ' '.join(text_splitted)


def raise_errors_JT(text: str, length: int) -> None:
    '''Funcao que verificar erros para a funcao {justifica_texto}'''
    # Erro se {text} nao for STR ou {length} nao for INT ou o texto for vazio
    if (not text or
            not isinstance(text, str) or
            not isinstance(length, int)):
        raise ValueError('justifica_texto: argumentos invalidos')

    for word in limpa_texto(text).split():
        if len(word) > length:
            # Erro se houver uma palavra de largura maior que {length}
            raise ValueError('justifica_texto: argumentos invalidos')


def justifica_texto(text: str, length: int) -> tuple:
    '''Funcao que pega em {text} e retorna o texto justificado'''
    raise_errors_JT(text, length)
    text_clean = limpa_texto(text)
    text_final = []

    def splitter(text: str, length: int) -> None:
        '''Esta funcao utiliza recursao para ir cortando o texto em pedacos de largura {length}
        ate a largura do ultimo pedaco ser inferior a {length}.
        '''
        # nonlocal faz com que a variavel se refira a {text_final} definida na funcao exterior
        nonlocal text_final
        cut = corta_texto(text, length)
        text_final.append(cut[0])
        if len(cut[1]) > length:
            splitter(cut[1], length)
        else:
            if len(cut[1]) != 0:
                text_final.append(cut[1])

    splitter(text_clean, length)
    for i, line in enumerate(text_final):
        if len(line) != length and line != text_final[-1]:
            text_final[i] = insere_espacos(line, length)
        else:
            # Adiciona espacos no final da ultima frase
            text_final[i] += ' ' * (length - len(line))

    return tuple(text_final)


###################################
# PART 2 - Metodo de Hondt
###################################


def calcula_quocientes(votes: dict, deputies: int) -> dict:
    '''Calcula os quocientes dos votos dependendo do valor de
    {deputies} para o metodo de hondt
    '''
    vote_copy = votes.copy()
    for i in vote_copy:
        quot = []
        for j in range(1, deputies + 1):
            quot.append(vote_copy[i] / j)
        vote_copy.update({i: quot}) # .update() atualiza o valor de uma chave

    return vote_copy


def atribui_mandatos(votes: dict, deputies: int) -> list:
    '''Retorna a lista dos deputados elegidos
    identificados pela letra correspondente ao partido
    '''
    votes_copy = votes.copy()
    mandates = []

    for i in range(deputies):
        # adicionar os deputados que tenham o maior valor de votos no momento
        new_letter = [p for p, value in votes_copy.items() if value == max(votes_copy.values())]
        if len(new_letter) > 1:
            least_voted = min([votes[p] for p in new_letter])
            # remove todos os partidos exceto o {least_voted}
            new_letter = filter(lambda dep: votes[dep] == least_voted, new_letter)

        new_letter = ''.join(new_letter)
        # obtem o proximo quociente
        votes_copy[new_letter] = votes[new_letter] / (votes[new_letter] / votes_copy[new_letter] + 1)
        mandates.append(new_letter)

    return mandates


def obtem_partidos(votes: dict) -> list:
    '''Retorna a lista de todos os partidos'''
    parties = [j for i in votes.values() for j in i['votos']]
    parties.sort() # poem em ordem alfabetica

    return list(dict.fromkeys(parties))  # Ao fazer esta conversao eliminamos elementos duplicados


def raise_errors_MH(votes: dict) -> None:
    '''Funcao que verifica erros para a funcao
    {obtem_resultado_eleicoes}
    '''
    # Erro se o argumento nao for dict ou se o dicionario for vazio
    if not isinstance(votes, dict) or not votes:
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    # Erro se a estrutura e o tipo de variaveis do dicionario nao estiverem corretos
    for j, i in votes.items():
        if (not isinstance(j, str) or not isinstance(i, dict) or
                not len(i) == 2 or
                not j or not i or 'votos' not in i.keys() or 'deputados' not in i.keys() or
                not isinstance(i['votos'], dict) or not isinstance(i['deputados'], int) or
                not any(i['votos'].values()) or  # Caso de haver 0 votos totais num circulo
                i['deputados'] < 1):
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')

        for key, value in i['votos'].items():
            # Erro se as chaves e valores nao forem do tipo correto e se houver votos negativos
            if not isinstance(key, str) or not isinstance(value, int) or value < 0:
                raise ValueError('obtem_resultado_eleicoes: argumento invalido')


def obtem_resultado_eleicoes(votes: dict) -> list:
    '''Retorna os resultados das eleicoes
    O numero de votos totais de cada partido
    O numero de deputados de cada partido
    '''
    raise_errors_MH(votes)

    vote_sum = {}.fromkeys(obtem_partidos(votes), 0)
    deputies = []
    for i in votes.values():
        for j in obtem_partidos(votes):
            if j not in i['votos'].keys():
                continue
            vote_sum.update({j: vote_sum[j] + i['votos'][j]})

        deputies += atribui_mandatos(i['votos'], i['deputados'])

    results = []
    for i in obtem_partidos(votes):
        results.append((i, deputies.count(i), vote_sum[i]))
    # Ordernar pelo numero de mandatos primeiro e depois pela soma em caso de empate
    results.sort(key=lambda party: (party[1], party[2]), reverse=True)

    return results


#############################################
# PART 3 - Resolucao de sistemas de equacoes lineares
#############################################


def produto_interno(vet1: tuple, vet2: tuple) -> float:
    '''Retorna o produto interno entre dois vetores'''
    # map gera um iteravel de acordo com a funcao que eh passada no argumento
    product = map(lambda v1, v2: v1 * v2, vet1, vet2)

    return float(sum(tuple(product)))


def verifica_convergencia(matrix: tuple, c: tuple, x: tuple, error: float) -> bool:
    '''Verifica se o valor absoluto do erro de todas as equacoes eh
    inferior a {error} e retorna True ou False consoante
    '''
    for matrix_i, c_i in zip(matrix, c): # gera o par de tuplos composto pelos argumentos
        if abs(produto_interno(matrix_i, x) - c_i) >= error:
            return False
    return True


def swap(i: int, j: int, matrix: tuple) -> tuple:
    '''Troca os elementos das posicoes {i} e {j} de um tuplo {matrix}'''
    if i > j:
        return matrix[:j] + (matrix[i], ) + matrix[j + 1:i] + (matrix[j], ) + matrix[i + 1:]
    return matrix[:i] + (matrix[j], ) + matrix[i + 1:j] + (matrix[i], ) + matrix[j + 1:]


def retira_zeros_diagonal(matrix: tuple, c: tuple) -> tuple:
    '''Troca linhas da matriz de modo a nao haver zeros nas diagonais'''
    matrix_res = matrix
    c_res = c
    for i in range(len(matrix)):
        if matrix_res[i][i] == 0:
            for j in range(len(matrix)):
                if i != j and matrix_res[j][i] != 0 and matrix_res[i][j] != 0:
                    # Trocar duas linhas {i} e {j}
                    matrix_res = swap(i, j, matrix_res)
                    c_res = swap(i, j, c_res)
                    break

    return matrix_res, c_res


def eh_diagonal_dominante(matrix: tuple) -> bool:
    '''Verifica se o tuplo {matrix} eh diagonal dominante'''
    for i in range(len(matrix)):
        sum_non_diagonal = 0
        for j in range(len(matrix)):
            if i != j:
                sum_non_diagonal += abs(matrix[i][j])
        if abs(matrix[i][i]) < sum_non_diagonal:
            return False
    return True


def raise_errors_SSE(matrix: tuple, c: tuple, error: float) -> tuple:
    '''Funcao que verifica erros para a funcao
    {resolve_sistema}
    '''
    # Erro se os tipos nao forem corretos, larguras diferentes entre matriz e vetor
    # E precisao nao compreendida entre ]0,1[
    if (not matrix or not c or    
            not isinstance(matrix, tuple) or not isinstance(c, tuple) or
            not isinstance(error, float) or len(matrix) != len(c) or
            not 0 < error < 1):
        raise ValueError('resolve_sistema: argumentos invalidos')
    # Erro se os tipos nao forem corretos, matrizes nao quadradas
    for i in range(len(matrix)):
        if (not isinstance(matrix[i], tuple) or len(matrix[i]) != len(matrix) or
                not isinstance(c[i], float) and not isinstance(c[i], int)):
            raise ValueError('resolve_sistema: argumentos invalidos')
        # Erro se os tipos nao forem corretos
        for j in range(len(matrix[i])):
            if (not isinstance(matrix[i][j], float) and
                    not isinstance(matrix[i][j], int)):
                raise ValueError('resolve_sistema: argumentos invalidos')


def resolve_sistema(pre_matrix: tuple, pre_c: tuple, error: float) -> tuple:
    '''Resolve um sistema de eqs. lineares utilizando o metodo
    de jacobi
    '''
    raise_errors_SSE(pre_matrix, pre_c, error)
    matrix, c = retira_zeros_diagonal(pre_matrix, pre_c)
    if not eh_diagonal_dominante(matrix):
        raise ValueError('resolve_sistema: matriz nao diagonal dominante')
    # Criar a lista de valores iniciais da solucao
    x = [0] * len(c)
    while not verifica_convergencia(matrix, c, x, error):
        x_prev = x.copy()
        for i in range(len(c)):
            x[i] = x_prev[i] + (c[i] - produto_interno(matrix[i], tuple(x_prev))) / matrix[i][i]

    return tuple(x)
