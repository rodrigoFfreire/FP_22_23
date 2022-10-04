def limpa_texto(text: str) -> str:
    '''
    Esta função pega no argumento {text} e remove os caracteres (\\t, \\n, \\v, \\f, \\r) 
    Remove também espaços que aparecem mais do que duas vezes de seguida
    '''
    not_wanted_chars = {
        9: ' ',     # 9 -> \t
        10: ' ',    # 10 -> \n
        11: ' ',    # 11 -> \v
        12: ' ',    # 12 -> \f
        13: ' '     # 13 -> \r
    }
    return ' '.join(text.translate(not_wanted_chars).split())


def corta_texto(text: str, size: int) -> tuple:
    '''Esta função corta {text} em duas partes: \n
    1 -> Contem todo o texto que tem largura {size} sem cortar palavras ao meio
    2 -> Contem o resto de {text} que sobrou'''
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
    
    for i, word in enumerate(text_final):
        if len(word) != length and word != text_final[-1]:
            text_final[i] = insere_espacos(word, length)
        else:
            text_final[i] += ' ' * (length - len(word))
                
    return tuple(text_final)