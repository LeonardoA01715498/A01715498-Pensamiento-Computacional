numero = input("Ingrese un número: ")

inverso = []

j = 0

while j < len(numero):
    inverso.append(numero[len(numero) - j - 1])
    j += 1

print("El número invertido es:", "".join(inverso))