"""Взлом шифра Цезаря частотным анализом"""
import caesar


def score(text: str) -> int:
    """Оценивает схожесть текста с английским языком"""
    weights = {"e": 12, "t": 9, "a": 8, "o": 7, "i": 7, "n": 7,"s": 6, "h": 6, "r": 6, "d": 4, "l": 4, "u": 3,}
    total = 0
    for c in text.lower():
        total += weights.get(c, 0)
    return total


def hack(ciphertext: str) -> tuple[str, int]:
    """Подбирает ключ шифра Цезаря и возвращает: текст, ключ"""
    best_text = ""
    best_shift = 0
    best_score = -1
    for shift in range(1, 26):
        text = caesar.decrypt(ciphertext, shift)
        s = score(text)
        if s > best_score:
            best_score = s
            best_text = text
            best_shift = shift
    return best_text, best_shift
