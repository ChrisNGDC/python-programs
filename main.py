import pyautogui
import keyboard


def clear_console():
    pyautogui.hotkey('ctrl', 'l')


def invert(string):
    return string[::-1]


def control_signado(numero_in, signado, base_in):
    if signado == 's':
        valor_signado = True
    else:
        valor_signado = False
    return (valor_signado and len(numero_in) == 8 and base_in == 2) or (not valor_signado)


def binary_sum(numero_primero, numero_segundo, carry):
    resultado = int(numero_primero) + int(numero_segundo) + carry
    cases = {
        0: '0',
        1: '1',
        2: '0',
        3: '1',
    }
    return cases[resultado]


def calculate_carry(numero_primero, numero_segundo, carry):
    resultado = int(numero_primero) + int(numero_segundo) + carry
    cases = {
        0: 0,
        1: 0,
        2: 1,
        3: 1,
    }
    return cases[resultado]


def sumar_binario_8bits(numero_primero, numero_segundo):
    resultado = ""
    carry = 0
    pos = 7
    for number in invert(numero_primero):
        resultado += binary_sum(number, numero_segundo[pos], carry)
        carry = calculate_carry(number, numero_segundo[pos], carry)
        pos -= 1
    return invert(resultado)


def to_base_10():
    while True:
        clear_console()
        numero_in = input("Ingrese el numero a convertir: ")
        base_in = int(input("Ingrese la base del numero: "))
        signado = input("Es un numero binario con signo (s/n): ")
        if base_in > int(max(numero_in)) and control_signado(numero_in, signado, base_in):
            break
    resultado = to_base_10_sum(numero_in, base_in)
    if signado == 's' and numero_in[0] == 1:
        signo = '-'
    else:
        signo = '+'
    print("El numero en decimal es:", signo, resultado)
    input("Presione Enter para continuar...")


def to_ten_10_signed(numero_in_signado, signo):
    numero_out_signado = ""
    if signo == '-':
        for number in numero_in_signado:
            if number == '1':
                numero_out_signado += '0'
            else:
                numero_out_signado += '1'
        return sumar_binario_8bits(numero_out_signado, '00000001')
    else:
        return numero_in_signado


def to_base_10_sum(numero_in, base_in):
    numero_in_aux = numero_in.split(',')
    numero_out_entero = 0
    numero_out_fraccionario = 0

    if len(numero_in_aux) == 1 and len(numero_in_aux[0]) == 8:
        numero_in_entero = to_ten_10_signed(numero_in, signo_numero_binario(numero_in))
    else:
        numero_in_entero = numero_in_aux[0]
    indice_entero = 0
    for number in numero_in_entero:
        numero_out_entero += int(number) * base_in ** (len(numero_in_entero) - 1 - indice_entero)
        indice_entero += 1

    indice_fraccionario = 1
    if len(numero_in_aux) > 1:
        numero_in_fraccionario = numero_in_aux[1]
        for number in numero_in_fraccionario:
            numero_out_fraccionario += int(number) * base_in ** (- indice_fraccionario)
            indice_fraccionario += 1
    return numero_out_entero + numero_out_fraccionario


def to_base_2_sum(numero_primero, numero_segundo):
    numero_primero_binario = from_base_10_to_2(numero_primero)
    numero_segundo_binario = from_base_10_to_2(numero_segundo)
    numero_primero_signado = to_ten_10_signed(numero_primero_binario, signo_numero_decimal(numero_primero))
    numero_segundo_signado = to_ten_10_signed(numero_segundo_binario, signo_numero_decimal(numero_segundo))
    resultado = sumar_binario_8bits(numero_primero_signado, numero_segundo_signado)
    return to_ten_10_signed(resultado, signo_numero_binario(resultado))


def from_base_10_to_2(numero):
    if numero >= 0:
        cociente = numero
    else:
        cociente = - numero
    resultado = ""
    while cociente > 0:
        resultado += str(cociente % 2)
        cociente = cociente // 2
    while len(resultado) < 8:
        resultado += '0'
    return invert(resultado)


def signo_numero_binario(numero):
    if numero[0] == '1':
        return '-'
    else:
        return '+'


def signo_numero_decimal(numero):
    if numero < 0:
        return '-'
    else:
        return '+'


def signo_suma(numero_primero, numero_segundo):
    numero_primero_binario = from_base_10_to_2(numero_primero)
    numero_segundo_binario = from_base_10_to_2(numero_segundo)
    numero_primero_signado = to_ten_10_signed(numero_primero_binario, signo_numero_decimal(numero_primero))
    numero_segundo_signado = to_ten_10_signed(numero_segundo_binario, signo_numero_decimal(numero_segundo))
    resultado = sumar_binario_8bits(numero_primero_signado, numero_segundo_signado)
    return signo_numero_binario(resultado)


def suma_decimal_8bits():
    while True:
        clear_console()
        numero_in_primero = int(input("Ingrese el primer numero: "))
        numero_in_segundo = int(input("Ingrese el segundo numero: "))
        if numero_in_primero < 128 and numero_in_segundo < 128:
            break
    resultado_signado = to_base_2_sum(numero_in_primero, numero_in_segundo)
    signo = signo_suma(numero_in_primero, numero_in_segundo)
    resultado_decimal = to_base_10_sum(resultado_signado, 2)
    print("El resultado en binario es:", signo, resultado_signado)
    print("El resultado en decimal es:", signo, resultado_decimal)
    input("Presione Enter para continuar...")


def menu_options(opcion):
    if opcion == 1:
        to_base_10(),
    else:
        if opcion == 2:
            suma_decimal_8bits()


def opcion_validate(opcion):
    return 0 < opcion < 3


def main():
    while True:
        clear_console()
        print("1: Pasaje de cualquier base a decimal")
        print("2: Suma de numeros decimales (signado 8 bits)")
        print("0: Salir")
        opcion = int(input("Ingrese la opcion a realizar: "))
        if opcion == 0:
            break
        if opcion_validate(opcion):
            menu_options(opcion)


main()
