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
        new_letter = [p for p, value in votes_copy.items() if value == max(votes_copy.values())]  # adicionar os deputados que tenham o maior valor de votos no momento
        if len(new_letter) > 1:                                                                   # No caso de haver partidos com o mesmo n de votos
            least_voted = min([votes[p] for p in new_letter])                                     # Escolhe dos partidos selecionados o que foi o menos votado
            new_letter = filter(lambda dep: votes[dep] == least_voted, new_letter)                # filtrar a lista de modo a remover todos os partidos exceto o {least_voted}
           
        new_letter = ''.join(new_letter) 
        votes_copy[new_letter] = quotients[new_letter][                                             
            quotients[new_letter].index(votes_copy[new_letter]) + 1                 # Da lista dos quocientes obter o valor do proximo quociente de um determinado partido
            ]   
        selected_deps.append(new_letter) 
                 
    return selected_deps


def obtem_partidos(votes: dict) -> list:
    '''Retorna a lista de todos os partidos'''
    parties = [j for i in votes.values() for j in i['votos']]
    
    return list(dict.fromkeys(parties))    # Ao fazer esta conversao eliminamos elementos duplicados 


def raise_errors_MH(votes: dict) -> None:
    '''Funcao auxiliar para levantar erros para a funcao {obtem_resultado_eleicoes}'''
    if not isinstance(votes, dict) or not votes:
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')            # Erro se o argumento nao for dict or se o dicionario for vazio
    
    for j, i in votes.items():                                
        if (not isinstance(j, str)
            or not isinstance(i, dict)
            or not 'votos' in i.keys()
            or not 'deputados' in i.keys()
            or not isinstance(i['votos'], dict)
            or not isinstance(i['deputados'], int)
            or not any(i['votos'].values())                                         # Erro se houver um ciruclo eleitoral com 0 votos totais
            or i['deputados'] < 1                                                  
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
        
    results.sort(key=lambda party: party[2], reverse=True)      #  Basta sortear pela soma pois nao pode haver um partido com menos votos e mais deputados que outro
    
    return results