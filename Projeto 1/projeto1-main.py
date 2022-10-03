def limpa_texto(text: str) -> str:
    not_wanted_chars = {
        9: ' ',     # 9 -> \t
        10: ' ',    # 10 -> \n
        11: ' ',    # 11 -> \v
        12: ' ',    # 12 -> \f
        13: ' '     # 13 -> \r
    }
    
    return ' '.join(text.translate(not_wanted_chars).split())


def corta_texto(text: str, size: int) -> tuple:
    size_left = size
    text_first = []
    text_rest = text.split()
    
    for word in text.split():
        if len(word) > size_left:
            break
        else:
            text_first.append(word)
            text_rest.remove(word)
            size_left -= len(word) + 1
            
    return (' '.join(text_first), ' '.join(text_rest))


def insere_espacos(text: str, padding: int) -> str:
    pad = padding - len(text)
    text_splitted = text.split()
    
    if len(text_splitted) < 2:
        return text + (' ' * pad)
    else:
        while pad > 0:
            for i, word in enumerate(text_splitted):
                if pad == 0:
                    break
                if word == text_splitted[-1]:
                    continue
                else:
                    text_splitted[i] = word + ' '
                    pad -= 1
                    
    return ' '.join(text_splitted)
                
 
def justifica_texto(text: str, length: int) -> tuple:
    if not isinstance(text, str) or not isinstance(length, int):
       raise ValueError('justifica texto: argumentos invalidos') 
    
    max_word_size = 0
    for word in limpa_texto(text).split():
        if len(word) > max_word_size:
            max_word_size = len(word)
        
    if len(limpa_texto(text)) == 0 or length < max_word_size:
        raise ValueError('justifica texto: argumentos invalidos')
    
    text_clean = limpa_texto(text)
    text_final = []
    
    def splitter(text: str, length: int) -> None:
        '''Esta funcao utiliza recursao para ir cortando o texto em pedacos
        de largura (length) ate a largura do ultimo pedaco ser inferior a
        (length). Juntando no final esses pedacos a uma lista para serem processados
        mais tarde
        '''
        nonlocal text_final
        cut = corta_texto(text, length)
        text_final.append(cut[0])
        if len(cut[1]) > length:
            splitter(cut[1], length)
        else:
            text_final.append(cut[1])
            
    splitter(text_clean, length)       
    
    print(text_final)
    for i, word in enumerate(text_final):
        if len(word) != length and word != text_final[-1]:
            text_final[i] = insere_espacos(word, length)
        else:
            text_final[i] += ' ' * (length - len(word))
                
    return tuple(text_final)


def calcula_quocientes(votes: dict, deputies: int) -> dict:
    vote_copy = votes.copy()
    for i in vote_copy:
        quocientes = []
        for j in range(1, deputies + 1):
            quocientes.append(vote_copy[i] / j)
        vote_copy.update({i : quocientes})
        
    return vote_copy


def atribui_mandatos(votes: dict, deputies: int) -> list:
    votes_copy = votes.copy()
    selected_deps = []
    
    for i in range(deputies):
        new_dep = [p for p, value in votes_copy.items() if value == max(votes_copy.values())]
        if len(new_dep) > 1:
            least_voted = min([votes[p] for p in new_dep])
            new_dep = filter(lambda dep: votes[dep] == least_voted, new_dep)
           
        new_dep = ''.join(new_dep) 
        votes_copy[new_dep] = votes[new_dep] / ((votes[new_dep] / votes_copy[new_dep]) + 1)
        selected_deps.append(new_dep) 
                 
    return selected_deps


def obtem_partidos(votes: dict) -> list:
    parties = [j for i in votes.values() for j in i['votos']]
    
    return list(dict.fromkeys(parties))


def obtem_resultado_eleicoes(votes: dict) -> list:
    if not isinstance(votes, dict) or not votes:
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    
    for i in votes.values():
        if not 'votos' in i.keys() or not 'deputados' in i.keys():
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        
        if (not isinstance(list(i.keys())[0], str)
            or not isinstance(list(i.keys())[1], str)):
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        
        if (not isinstance(i['votos'], dict) or not isinstance(i['deputados'], int)
            or i['deputados'] < 1):
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        
        if not any(i['votos'].values()):
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        
        for key, value in i['votos'].items():
            if not isinstance(key, str) or not isinstance(value, int) or value < 0:
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
    
    resultado = []
    for i in obtem_partidos(votes):
        resultado.append((i, deputies.count(i), soma[i]))
        
    resultado.sort(key=lambda party: party[2], reverse=True)
    
    return resultado