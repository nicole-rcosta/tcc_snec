# utils/validators.py
import re

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', str(cpf))

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito_1 = resto if resto < 10 else 0

    if int(cpf[9]) != digito_1:
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    digito_2 = resto if resto < 10 else 0

    if int(cpf[10]) != digito_2:
        return False
    
    return True