def ex20():
    i = 1
    n = 0
    while i < 10:
        n = n * 10 + i
        print(n, "x 8 +", i, "=", n * 8 + i)
        i += 1
 
        
def ex19():
    money = eval(input('Introduz a quantidade de dinheiro: ')) * 100
    
    print('Moedas / Notas necessarias para perfazer a quantia: ')
    print('Nota de 50: ', money // 5000)
    money %= 5000
    print('Nota de 20: ', money // 2000)
    money %= 2000
    print('Nota de 10: ', money // 1000)
    money %= 1000
    print('Nota de 5: ', money // 500)
    money %= 500
    print('Moeda de 2: ', money // 200)
    money %= 200
    print('Moeda de 1: ', money // 100)
    money %= 100
    print('Moeda de 0.50: ', money // 50)
    money %= 50
    print('Moeda de 0.20: ', money // 20)
    money %= 20
    print('Moeda de 0.10: ', money // 10)
    money %= 10
    print('Moeda de 0.05: ', money // 5)
    money %= 5
    print('Moeda de 0.02: ', money // 2)
    money %= 2
    print('Moeda de 0.01: ', money)
    
    
def ex18():
    num = eval(input('Numero ? '))
    count = 0
    while num != 0:
        digito = num % 10
        num //= 10
        if digito == 0 and num % 10 == 0:
            count += 1
    
    print('O numero tem ', count, ' zeros seguidos')
 
    
def ex17():
    n_alunos = eval(input('QUANTOS DREDIS SAO: '))
    positivas = 0
    totais = n_alunos
    i = 0
    while i < n_alunos:
        nota = eval(input('Nota do aluno: '))
        if nota >= 10:
            positivas += 1
        i += 1
    
    print('Notas Positivas: ', positivas)
    print('Percentagem de positivas: ', (positivas / totais) * 100, '%')
 
        
def ex16():
    num = eval(input('Escreve um numero: '))

    capi = num
    while num >= 1:
        capi = (capi * 10) + num % 10
        num //= 10
        
    print(capi)
 
    
def ex15():
    num = 0
    x = 0
    while num != -1:
        num = eval(input('Insere um digito (-1 para terminar): '))
        if num != -1:
            x = (x * 10) + num
        else:
            print(x)
 
            
def ex14():
    num = eval(input('Insere um inteiro: '))
    soma = 0
    while num != 0:
        soma += num % 10
        num //= 10
        
    print(soma)

    
def ex13():
    num = eval(input('Insere um numero para escrever a tabuadrieds: '))
    i = 1
    while i < 11:
        print(num, ' x ', i, ' = ', num * i)
        i += 1        


def ex12():
    x = eval(input('Qual o valor de x? '))
    n = eval(input('Qual o valor de n? '))
    
    soma = 0
    i = 0
    while i <= n:
        j = 0
        fatorial = 1
        while j <= i:
            if j > 1:
                fatorial *= j
            j += 1
        soma += (x**i) / fatorial
        i += 1
        
    print('O valor da soma é ', soma)
    

def ex11():
    num = eval(input('Escreve um numero inteiro: '))
    
    result = 0
    while num != 0:
        result = (result * 10) + num % 10
        num //= 10
        
    print(result)
    

def ex10():
    num = eval(input('Escreve um numero inteiro: '))
    pre_result = 0
    result = 0
    while num != 0:
        if (num % 10) % 2 != 0:
            pre_result = pre_result * 10 + num % 10
        num //= 10
    while pre_result != 0:
        result = (result * 10) + pre_result % 10
        pre_result //= 10
        
    print(result)