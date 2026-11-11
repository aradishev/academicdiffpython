import random
"""Шифр RSA"""



def is_prime(n: int) -> bool:
    """Простое или нет"""
    if n < 2:
        return False
    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i+= 1
    return True


def gcd(a: int, b: int) -> int:
    """Возвращает НОД"""
    while b:
        a, b = b, a % b
    return a


def multiplicative_inverse(e: int, phi: int) -> int:
    """Возвращает d, где e d% phi == 1"""
    r0, r1 = e, phi
    x0, x1 = 1, 0
    while r1:
        q = (r0// r1)
        r0, r1 = r1, r0- q*r1
        x0, x1 = x1, x0- q*x1
    if r0 != 1:
        raise ValueError("Обратного числа не существует")
    return x0 % phi

def generate_keypair(p: int, q: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """Генерирует пару ключей (e, n), (d, n) по простым числам p и q"""
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("p и q должны быть простыми")
    if p == q:
        raise ValueError("p и q не должны совпадать")
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)

def encrypt(public_key: tuple[int, int], text: str) -> list[int]:
    """Шифрует текст открытым ключом и возвращает список чисел"""
    e, n = public_key
    result = []
    for c in text:
        m = ord(c)
        result.append(pow(m, e, n))
    return result


def decrypt(private_key: tuple[int, int], cipher_list: list[int]) -> str:
    """Дешифрует список чисел закрытым ключом"""
    d, n = private_key
    result = ""
    for c in cipher_list:
        m = pow(c, d, n)
        result += chr(m)
    return result

