def limpa_texto(text: str) -> str:
    '''Esta funcao pega no argumento {text} e remove os caracteres (\\t, \\n, \\v, \\f, \\r) 
    Remove tambem espacos que aparecam mais do que duas vezes de seguida
    '''
    return ' '.join(text.split())  # split() converte string em list (ignorando caracteres nao visiveise e ' ') | join() converte list em string e utiliza ' ' como separador


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
                if pad == 0:                            # Como o while so para apos o for acabar isto serve para parar imediatamente o loop para prevenir espacos nao extra n desejados
                    break
                if word != text_splitted[-1]:           # Nao inserir espacos na ultima palavra
                    text_splitted[i] = word + ' '
                    pad -= 1
                    
    return ' '.join(text_splitted)
                

def raise_errors_JT(text: str, length: int) -> None:
    '''Funcao auxiliar para levantar erros para a funcao {justifica_texto}'''
    if (not isinstance(text, str) or not isinstance(length, int)    # Erro se {text} nao for STR ou {length} nao for INT
        or len(limpa_texto(text)) == 0                              # Erro se {text} for {vazio}
    ): 
       raise ValueError('justifica_texto: argumentos invalidos') 
    
    for word in limpa_texto(text).split():
        if len(word) > length:
            raise ValueError('justifica_texto: argumentos invalidos')   # Erro se houver uma palavra de largura maior que {length}      

 
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
    for i, word in enumerate(text_final):
        if len(word) != length and word != text_final[-1]:
            text_final[i] = insere_espacos(word, length)
        else:                                               
            text_final[i] += ' ' * (length - len(word))
                
    return tuple(text_final)


cad = ('Computers are incredibly  \n\tfast,     \n\t\taccurate'
               ' \n\t\t\tand  stupid.   \n    Human beings are incredibly  slow  '
               'inaccurate, and brilliant. \n     Together  they  are powerful   '
               'beyond imagination.')


print(justifica_texto(cad, 40))