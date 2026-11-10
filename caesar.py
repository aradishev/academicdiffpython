"""Шифр Цезаря для ASCII символов"""


def encrypt(plaintext: str, shift: int) -> str:
    """Шифрование шифа Цезаря"""
    result = ""
    for c in plaintext:
        code = ord(c)
        if 32 <= code <= 126:
            code = (code - 32 + shift) % 95 + 32
        result += chr(code)
    return result


def decrypt(ciphertext: str, shift: int) -> str:
    """Дешифрование шифра Цезаря"""
    return encrypt(ciphertext, -shift)


if __name__ == "__main__":
    print(encrypt("Hello, World!", 3))
    print(decrypt("Khoor/#Zruog$", 3))