"""Шифр Виженера для ASCII символов"""


def convert(text: str, keyword: str, sign: int) -> str:
    """Применяет сдвиги ключа к тексту (sign=1 шифровка, sign=-1 дешифровка)"""
    shifts = [ord(k)- 97 for k in keyword.lower() if "a" <= k <= "z"]
    if not shifts:
        return text
    result = ""
    for i, c in enumerate(text):
        code = ord(c)
        if 32 <= code <= 126:
            s = shifts[i% len(shifts)] * sign
            code = (code - 32 + s) % 95 + 32
        result+= chr(code)
    return result


def encrypt(plaintext: str, keyword: str) -> str:
    """Шифрование шифром Виженера"""
    return convert(plaintext, keyword, 1)


def decrypt(ciphertext: str, keyword: str) -> str:
    """Дешифрование шифра Виженера."""
    return convert(ciphertext, keyword, -1)


if __name__ == "__main__":
    print(encrypt("attack at dawn", "LEMON"))
    print(decrypt("lx!opv$m#-oe$|", "LEMON"))