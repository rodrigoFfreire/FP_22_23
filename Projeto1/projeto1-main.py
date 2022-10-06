###################################
# PART 1 - Justificacao de texto
###################################

def limpa_texto(text: str) -> str:
    '''Esta função pega no argumento {text} e remove os caracteres (\\t, \\n, \\v, \\f, \\r) 
    Remove também espaços que aparecem mais do que duas vezes de seguida
    '''
    not_wanted_chars = {
        9: ' ',     # 9 -> \t
        10: ' ',    # 10 -> \n
        11: ' ',    # 11 -> \v
        12: ' ',    # 12 -> \f
        13: ' '     # 13 -> \r
    }
    
    return ' '.join(text.translate(not_wanted_chars).split())       # Nota 1 (Consultar no fim do ficheiro)


def corta_texto(text: str, size: int) -> tuple:
    '''Esta função corta {text} em duas partes: \n
    1 -> Contem todo o texto que tem largura {size} sem cortar palavras ao meio
    2 -> Contem o resto de {text} que sobrou'''
    size_left = size
    text_first = []
    text_rest = text.split()
    
    for word in text.split():               
        if len(word) > size_left:
            break                   # Parar de adicionar texto a {text_first} se {word} exceder o limite restante de largura
        else:
            text_first.append(word)
            text_rest.remove(word)
            size_left -= len(word) + 1
            
    return ' '.join(text_first), ' '.join(text_rest)


def insere_espacos(text: str, padding: int) -> str:
    '''Esta função insere espaços entre as palavras de forma homogénea de forma
    a que {text} atinga uma certa largura
    '''
    pad = padding - len(text)
    text_splitted = text.split()
    if len(text_splitted) < 2:      # Se uma sequencia for constituida por menos de 2 palavras
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
                
 
def justifica_texto(text: str, length: int) -> tuple:
    '''Função que pega em {text} e retorna o texto justificado
    ou seja, todas as linhas do texto têm a mesma largura {length}
    
    Entre as linhas sao inseridas espaços de modo que a linha atinga
    a desejada {largura}
    A ultima linha não tem espaços entre as palavras mas sim no final
    da linha
    '''
    if not isinstance(text, str) or not isinstance(length, int):        # Erro se os argumentos nao forem do tipo correto
       raise ValueError('justifica texto: argumentos invalidos') 
    
    max_word_size = 0
    for word in limpa_texto(text).split():
        if len(word) > max_word_size:
            max_word_size = len(word)
        
    if len(limpa_texto(text)) == 0 or length < max_word_size:           # Erro se o texto for vazio ou {length} for inferior à largura da maior palavra do texto
        raise ValueError('justifica texto: argumentos invalidos')
    
    text_clean = limpa_texto(text)
    text_final = []
    def splitter(text: str, length: int) -> None:
        '''Esta função utiliza recursão para ir cortando o texto em pedaços
        de largura {length} até a largura do último pedaço ser inferior a
        {length}. Juntando no final esses pedaços a uma lista para serem processados
        mais tarde
        '''
        nonlocal text_final      # nonlocal faz com que esta variavel se refira a {text_final} definida na funcao exterior a esta
        cut = corta_texto(text, length)
        text_final.append(cut[0])
        if len(cut[1]) > length:
            splitter(cut[1], length)
        else:
            text_final.append(cut[1])
            
    splitter(text_clean, length)       
    for i, word in enumerate(text_final):
        if len(word) != length and word != text_final[-1]:
            text_final[i] = insere_espacos(word, length)
        else:                                               # Executar isto quando chegar à linha final
            text_final[i] += ' ' * (length - len(word))
                
    return tuple(text_final)

###################################
# PART 2 - Metodo de Hondt
###################################

def calcula_quocientes(votes: dict, deputies: int) -> dict:
    '''Calcula os quocientes dos votos dependendo do valor de {deputies}
    para o método de hondt
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
        new_letter = [p for p, value in votes_copy.items() if value == max(votes_copy.values())]  # Nota 2 (Consultar no fim do ficheiro)
        if len(new_letter) > 1:                                                                   # No caso de haver partidos com o mesmo num de votos
            least_voted = min([votes[p] for p in new_letter])                                     # Nota 3 (Consultar no fim do ficheiro)
            new_letter = filter(lambda dep: votes[dep] == least_voted, new_letter)                # Nota 4 (Consultar no fim do ficheiro)
           
        new_letter = ''.join(new_letter) 
        votes_copy[new_letter] = quotients[new_letter][                                             
            quotients[new_letter].index(votes_copy[new_letter]) + 1                               # Nota 5 (Consultar no fim do ficheiro)
            ]   
        selected_deps.append(new_letter) 
                 
    return selected_deps


def obtem_partidos(votes: dict) -> list:
    '''Retorna a lista de todos os partidos'''
    parties = [j for i in votes.values() for j in i['votos']]
    
    return list(dict.fromkeys(parties))    # Ao fazer esta conversao eliminamos elementos duplicados 


def obtem_resultado_eleicoes(votes: dict) -> list:
    '''Retorna os resultados das eleições
    O numero de votos totais de cada partido
    O numero de deputados de cada partido'''
    if not isinstance(votes, dict) or not votes:
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')            # Erro se o argumento nao for dict
    
    for j, i in votes.items():                                
        if (not isinstance(j, str)
            or not isinstance(i, dict) 
            or not 'votos' in i.keys()                                              # Erro se nao existir a key 'votos'
            or not 'deputados' in i.keys()                                          # Erro se nao existir a key 'deputados'
            or not isinstance(i['votos'], dict)                                     # Erro se nao existir a key 'votos'
            or not isinstance(i['deputados'], int)                                  # Erro se nao existir a key 'votos'
            or not any(i['votos'].values())                                         # Erro se nao existir a key 'votos'
            or i['deputados'] < 1                                                   # Erro se nao existir a key 'votos'
            ):
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        
        for key, value in i['votos'].items():
            if not isinstance(key, str) or not isinstance(value, int) or value < 0:  # Erro se a keys (partidos, votos) sao do tipo (STR, INT) e se nao existe votos negativos
                raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        
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


def produto_interno(vet1: tuple, vet2: tuple) -> float:
    product = 0
    for i in range(len(vet1)):
        product += vet1[i] * vet2[i]

    return product

def verifica_convergencia(matrix: tuple, c: tuple, x: tuple, prec: float) -> bool:
    results = []
    for i in range(len(matrix)):
        if abs(produto_interno(matrix[i], x) - c[i]):
            results.append(True)
        else:
            results.append(False)
            
    return all(results)


def retira_zeros_diagonal(matrix: tuple, c: tuple) -> tuple:
    pass


def eh_diagonal_dominante(matrix: tuple) -> bool:
    pass


def resolve_sistema(matriz: tuple, c: tuple, precision: float) -> tuple:
    pass







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