from functools import cache

MULTIPLICADORES_MODULO_11 = [9, 8, 7, 6, 5, 4, 3, 2]

@cache
def get_multiplicadores_modulo_11(len_numero):

    return (MULTIPLICADORES_MODULO_11*(len_numero//len(MULTIPLICADORES_MODULO_11)+1))[-len_numero:]


def calcular_modulo11(numero):
    multiplicadores = get_multiplicadores_modulo_11(len(numero))
    soma = sum(int(x) * y for x, y in zip(numero, multiplicadores))
    resto_divisao = soma % 11
    dac = 11 - resto_divisao if resto_divisao != 0 and resto_divisao != 1 else 0
    return str(dac)


MULTIPLICADORES_MODULO_10 = [1, 2]


@cache
def get_multiplicadores_modulo_10(len_numero):
    return (MULTIPLICADORES_MODULO_10*(len_numero//len(MULTIPLICADORES_MODULO_10)+1))[-len_numero:]


def calcular_modulo10(numero):
    numeros = [int(digito) for digito in str(numero)]

    # Inverte a lista
    #numeros.reverse()
    #print(numeros)
    multiplicadores = get_multiplicadores_modulo_10(len(numero))
    #print(multiplicadores)
    soma = sum(
        (x * y // 10 + x * y % 10) if x * y > 9 else x * y
        for x, y in zip(numeros, multiplicadores)
    )
    resto_divisao = soma % 10
    dv = 10 - resto_divisao if resto_divisao != 0 else 0
    return str(dv)

#print("######", calcular_modulo10("033990117"))

