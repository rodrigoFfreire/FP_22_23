print("Introduza um número")
num = eval(input("? "))

counter = 0
while num != 0:
    digit = num % 10
    num //= 10  # num = num // 10
    if digit == 0 and num % 10 == 0:
        counter += 1

print("O numero tem", counter, "zeros seguidos")