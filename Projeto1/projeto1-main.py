###################################
# PART 1 - Justificacao de texto
###################################

def limpa_texto(text: str) -> str:
    '''Esta funcao pega no argumento {text} e remove os caracteres (\\t, \\n, \\v, \\f, \\r) 
    Remove tambem espacos que aparecem mais do que duas vezes de seguida
    '''
    return ' '.join(text.split())  # split() converte string em list (ignorando caracteres nao visiveis) | join() converte list em string e utiliza ' ' como separador


def corta_texto(text: str, size: int) -> str:
    '''Esta funcao corta {text} em duas partes: \n
    1 -> Contem todo o texto que tem largura {size} sem cortar palavras ao meio
    2 -> Contem o resto de {text} que sobrou'''
    text_first = []
    text_rest = text.split()
    
    for word in text.split():               
        if len(word) > size:
            break                # Parar de adicionar texto a {text_first} se {word} exceder o limite restante de largura
        else:
            text_first.append(word)
            text_rest.remove(word)
            size -= len(word) + 1
            
    return ' '.join(text_first), ' '.join(text_rest)


def insere_espacos(text: str, padding: int) -> str:
    '''Esta funcao insere espaços entre as palavras de forma homogenea de forma
    a que {text} atinga uma certa largura
    '''
    pad = padding - len(text)
    text_splitted = text.split()
    if len(text_splitted) < 2:  
        return text + (' ' * pad)
    else:
        while pad > 0:
            for i, word in enumerate(text_splitted):
                if pad == 0:                            # Como o while so para apos o for acabar isto serve para parar imediatamente o loop
                    break
                if word == text_splitted[-1]:           # Nao inserir espacos na ultima palavra
                    continue
                else:
                    text_splitted[i] = word + ' '
                    pad -= 1
                    
    return ' '.join(text_splitted)
                

def raise_errors_JT(text: str, length: int) -> None:
    '''Funcao auxiliar para levantar erros para a funcao {justifica_texto}'''
    if not isinstance(text, str) or not isinstance(length, int):        # Erro se os argumentos nao forem do tipo correto
       raise ValueError('justifica_texto: argumentos invalidos') 
    
    max_word_size = 0
    for word in limpa_texto(text).split():
        if len(word) > max_word_size:
            max_word_size = len(word)
        
    if len(limpa_texto(text)) == 0 or length < max_word_size:           # Erro se o texto for vazio ou {length} for inferior à largura da maior palavra do texto
        raise ValueError('justifica_texto: argumentos invalidos')

 
def justifica_texto(text: str, length: int) -> tuple:
    '''Funcao que pega em {text} e retorna o texto justificado
    ou seja, todas as linhas do texto teem a mesma largura {length}
    '''
    raise_errors_JT(text, length)
    
    text_clean = limpa_texto(text)
    text_final = []
    def splitter(text: str, length: int) -> None:
        '''Esta funcao utiliza recursão para ir cortando o texto em pedaços
        de largura {length} ate a largura do ultimo pedaco ser inferior a
        {length}. Juntando no final esses pedacos a uma lista para serem processados
        mais tarde
        '''
        nonlocal text_final                 # nonlocal faz com que esta variavel se refira a {text_final} definida na funcao exterior a esta
        cut = corta_texto(text, length)
        text_final.append(cut[0])
        if len(cut[1]) > length:
            splitter(cut[1], length)        # Corta a segunda string devolvida por {corta_texto}
        else:
            if len(cut[1]) != 0:            # nao adicionar o segundo resultado de {corta_texto} se for vazio
                text_final.append(cut[1])
            
    splitter(text_clean, length)
    print(text_final)       
    for i, word in enumerate(text_final):
        if len(word) != length and word != text_final[-1]:
            text_final[i] = insere_espacos(word, length)
        else:                                                  # Executar isto quando chegar à linha final
            text_final[i] += ' ' * (length - len(word))
                
    return tuple(text_final)


###################################
# PART 2 - Metodo de Hondt
###################################


def calcula_quocientes(votes: dict, deputies: int) -> dict:
    '''Calcula os quocientes dos votos dependendo do valor de {deputies}
    para o metodo de hondt
    '''
    vote_copy = votes.copy()
    for i in vote_copy:
        quocientes = []
        for j in range(1, deputies + 1):
            quocientes.append(vote_copy[i] / j)
        vote_copy.update({i : quocientes})            # Substitui a copia dos votos pelo o valor atualizado
        
    return vote_copy


def atribui_mandatos(votes: dict, deputies: int) -> list:
    '''Retorna a lista dos deputados elegidos identificados pela letra correspondente
    ao seu partido
    '''
    votes_copy = votes.copy()
    selected_deps = []
    quotients = calcula_quocientes(votes, deputies)
    
    for i in range(deputies):
        new_letter = [p for p, value in votes_copy.items() if value == max(votes_copy.values())]  # Nota 1 (Consultar no fim do ficheiro)
        if len(new_letter) > 1:                                                                   # No caso de haver partidos com o mesmo num de votos
            least_voted = min([votes[p] for p in new_letter])                                     # Nota 2 (Consultar no fim do ficheiro)
            new_letter = filter(lambda dep: votes[dep] == least_voted, new_letter)                # Nota 3 (Consultar no fim do ficheiro)
           
        new_letter = ''.join(new_letter) 
        votes_copy[new_letter] = quotients[new_letter][                                             
            quotients[new_letter].index(votes_copy[new_letter]) + 1                               # Nota 4 (Consultar no fim do ficheiro)
            ]   
        selected_deps.append(new_letter) 
                 
    return selected_deps


def obtem_partidos(votes: dict) -> list:
    '''Retorna a lista de todos os partidos'''
    parties = [j for i in votes.values() for j in i['votos']]
    
    return list(dict.fromkeys(parties))    # Ao fazer esta conversao eliminamos elementos duplicados 


def raise_errors_MH(votes):
    '''Funcao auxiliar para levantar erros para a funcao {obtem_resultado_eleicoes}'''
    if not isinstance(votes, dict) or not votes:
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')            # Erro se o argumento nao for dict
    
    for j, i in votes.items():                                
        if (not isinstance(j, str)                                                  # Erro se key 'circulo eleitoral' nao for STR
            or not isinstance(i, dict)                                              # Erro se valor da key 'ciruclo eleitoral' nao for DICT
            or not 'votos' in i.keys()                                              # Erro se nao existir a key 'votos'
            or not 'deputados' in i.keys()                                          # Erro se nao existir a key 'deputados'
            or not isinstance(i['votos'], dict)                                     # Erro se o valor da key 'votos' nao for DICT
            or not isinstance(i['deputados'], int)                                  # Erro se o valor da keu 'deputados' nao for INT
            or not any(i['votos'].values())                                         # Erro se houver um ciruclo eleitoral com 0 votos totais
            or i['deputados'] < 1                                                   # Erro se houver n de deputados negativos
            ):
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        
        for key, value in i['votos'].items():
            if not isinstance(key, str) or not isinstance(value, int) or value < 0:  # Erro se a key 'partido' e o seu valor nao for STR, INT respetivamente (sendo que nao existem votos negativos) 
                raise ValueError('obtem_resultado_eleicoes: argumento invalido')


def obtem_resultado_eleicoes(votes: dict) -> list:
    '''Retorna os resultados das eleicoes
    O numero de votos totais de cada partido
    O numero de deputados de cada partido
    '''
    raise_errors_MH(votes)    
        
    soma = dict.fromkeys(obtem_partidos(votes), 0)
    deputies = []
    for i in votes.values():
        value = 0
        for j in obtem_partidos(votes):
            if not j in i['votos'].keys():
                continue
            soma.update({j: soma[j] + i['votos'][j]})
            
        deputies += atribui_mandatos(i['votos'], i['deputados'])
    
    results = []
    for i in obtem_partidos(votes):
        results.append((i, deputies.count(i), soma[i]))
        
    results.sort(key=lambda party: party[2], reverse=True)
    
    return results


#############################################
# PART 3 - Resolucao de sistemas de equacoes lineares
#############################################


def produto_interno(vet1: tuple, vet2: tuple) -> float:
    product = 0
    for i in range(len(vet1)):
        product += vet1[i] * vet2[i]

    return product


def verifica_convergencia(matrix: tuple, c: tuple, x: tuple, prec: float) -> bool:
    results = []
    for i in range(len(matrix)):
        if abs(produto_interno(matrix[i], x) - c[i]) < prec:
            results.append(True)
        else:
            results.append(False)
            
    return all(results)


def swap(i: int, j: int, matrix: tuple) -> tuple:
    if i > j:
        return matrix[:j] + (matrix[i], ) + matrix[j + 1:i] + (matrix[j], ) + matrix[i + 1:]
    return matrix[:i] + (matrix[j], ) + matrix[i + 1:j] + (matrix[i], ) + matrix[j + 1:]

def retira_zeros_diagonal(matrix: tuple, c: tuple) -> tuple:
    matrix_res = matrix
    vector_res = ()
    for i in range(len(matrix)):
        if matrix_res[i][i] == 0:
            for j in range(len(matrix)):
                if i != j and matrix_res[j][i] != 0 and matrix_res[i][j] != 0:
                    matrix_res = swap(i, j, matrix_res)
                    break
                
    for k in matrix_res:
        vector_res += (c[matrix.index(k)], )
        
    return matrix_res, vector_res


def eh_diagonal_dominante(matrix: tuple) -> bool: 
    for i in range(len(matrix)):
        sum_non_diagonal = 0
        for j in range(len(matrix)):
            if i != j : sum_non_diagonal += abs(matrix[i][j])
        if abs(matrix[i][i]) < sum_non_diagonal:
            return False
    return True


def raise_errors_SSE(matrix: tuple, c: tuple, prec: float) -> tuple:
    if (not isinstance(matrix, tuple) 
        or not isinstance(c, tuple)
        or not isinstance(prec, float)
        or len(matrix) == 0
        or len(c) == 0
        or len(matrix) != len(c)
    ):
        raise ValueError('resolve_sistema: argumentos invalidos')
    
    for i in range(len(matrix)):
        if (len(matrix[i]) != len(matrix)
            or not isinstance(c[i], int())
        ):
            raise ValueError('resolve_sistema: argumentos invalidos')
        for j in range(len(matrix[i])):
            if not isinstance(j, int):
                raise ValueError('resolve_sistema: argumentos invalidos')
        
    if not eh_diagonal_dominante(matrix):
        raise ValueError('resolve_sistema: matriz nao diagonal dominante')


def resolve_sistema(matrix: tuple, c: tuple, prec: float) -> tuple:
    raise_errors_SSE(matrix, c, prec)
    x, current_precision = [0] * len(c), [1] * len(c)

    while max(current_precision) >= prec:
        for i in range(len(c)):
            last_x = x[i]
            x[i] = x[i] + (c[i] - produto_interno(matrix[i], x)) / matrix[i][i]
            current_precision[i] = abs((x[i] - last_x) / x[i])
    
    return tuple(x)


########
# NOTAS (Comentarios muitos grandes para caber ao lado de uma linha)
########

# NOTA 1: translate() converte os caracteres desejados em ' ' utilizando o dicionario {not_wanted_chars}
#          .split() converte uma string em lista e adiciona apenas as sequencias de caracteres nao vazios
#           .join() converte uma lista em string utilizando ' ' como separador


# NOTA 2: É adicionado um novo elemento p à lista quando encontrar o valor maximo de votos atual
#           correspondente a um dado circulo eleitoral.


# NOTA 3: Esta linha serve para descobrir dos partidos com votos iguais o que inicialmente foi menos votado


# NOTA 4: Depois da linha acima ter sido executada, precisamos de filtrar a lista new_letter e retirar todas as
#           letras exceto a least_voted. Utiliza-se a funcao filter().


# NOTA 5: O valor apos dividir os votos de um determinado partido é igual ao valor da lista de quocientes
#           dada por calcula_quocientes() cujo indice é o indice do valor atual + 1 