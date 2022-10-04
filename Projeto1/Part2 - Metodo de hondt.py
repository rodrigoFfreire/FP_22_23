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
            or not isinstance(list(i.keys())[1], str)
            or not isinstance(i['votos'], dict) 
            or not isinstance(i['deputados'], int)
            or not any(i['votos'].values())
            or i['deputados'] < 1
            ):
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
    
    results = []
    for i in obtem_partidos(votes):
        results.append((i, deputies.count(i), soma[i]))
        
    results.sort(key=lambda party: party[2], reverse=True)
    
    return results