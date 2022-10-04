# Ex1
def cinco(n):
    return n == 5

    
# Ex2
def horas_dias(h):
    return h / 24
    

# Ex3
def area_circulo(r):
    return 3.14 * r * r
    

# Ex4
def area_coroa(r1, r2):
    if r1 > r2:
        raise ValueError
    return area_circulo(r2) - area_circulo(r1)


# Ex5
def bissexto(year):
    if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
        return True
    return False
    

# Ex6
def dia_mes(month, year):
    m = {
        'jan': 31,
        'fev': [28, 29],
        'mar': 30,
        
    }
    