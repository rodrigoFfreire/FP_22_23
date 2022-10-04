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
            break                   # Parar de adicionar texto a {text_first} se {word} exceder o limite restante de largura
        else:
            text_first.append(word)
            text_rest.remove(word)
            size_left -= len(word) + 1
            
    return (' '.join(text_first), ' '.join(text_rest))


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
        nonlocal text_final                 # nonlocal faz com que esta variavel se refira a {text_final} definida na funcao exterior a esta
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
        else:                                                  # Executar isto quando chegar à linha final
            text_final[i] += ' ' * (length - len(word))
                
    return tuple(text_final)