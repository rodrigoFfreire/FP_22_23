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
                

def raise_errors_JT(text: str, length: int, clean: str) -> None:
    '''Funcao auxiliar para levantar erros para a funcao {justifica_texto}'''
    if not isinstance(text, str) or not isinstance(length, int):        # Erro se os argumentos nao forem do tipo correto
       raise ValueError('justifica texto: argumentos invalidos') 
    
    max_word_size = 0
    for word in limpa_texto(text).split():
        if len(word) > max_word_size:
            max_word_size = len(word)
        
    if len(limpa_texto(text)) == 0 or length < max_word_size:           # Erro se o texto for vazio ou {length} for inferior à largura da maior palavra do texto
        raise ValueError('justifica texto: argumentos invalidos')

 
def justifica_texto(text: str, length: int) -> tuple:
    '''Funcao que pega em {text} e retorna o texto justificado
    ou seja, todas as linhas do texto teem a mesma largura {length}
    '''
    raise_errors_JT(text, length, limpa_texto(text).split())
    
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
            text_final.append(cut[1])
            
    splitter(text_clean, length)       
    for i, word in enumerate(text_final):
        if len(word) != length and word != text_final[-1]:
            text_final[i] = insere_espacos(word, length)
        else:                                                  # Executar isto quando chegar à linha final
            text_final[i] += ' ' * (length - len(word))
                
    return tuple(text_final)