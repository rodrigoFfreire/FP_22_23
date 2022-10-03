info = {
'Endor':   {'deputados': 7,
             'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
'Hoth':    {'deputados': 6,
             'votos': {'B':11500, 87:9000, 'E':5000, 'D':1500}},
'Tatooine': {'deputados': 3,
             'votos': {'A':3000, 'B':1900}}}


# for i in info.values():
#     print(i['votos'])
        
        
# # parties = [j for i in info.values() for j in i['votos']]
# # print(list(dict.fromkeys(parties)))

# dict1 = {'A':12000, 'B':7500, 'C':5250, 'D':3000}
# dict2 = {'A':1000, 'B':1000, 'C':1000, 'D':1000}


# lista = [('A', 7, 24000), ('B', 6, 20900), ('C', 1, 5250), ('D', 1, 4500), ('E', 1, 5000)]

# lista.sort(key=lambda party: party[2], reverse=True)
# print(lista)
for i in info.values():
    for j, k in i['votos'].items():
        if not isinstance(j, str):
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')