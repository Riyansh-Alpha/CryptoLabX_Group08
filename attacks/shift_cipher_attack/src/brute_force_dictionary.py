import re
from shift_cipher import ShiftCipher

def dictionary_attack(ciphertext: str, dictionary_words: set) -> tuple[int, str, int]:
    """
    Performs brute force cryptanalysis by matching decrypted words against a dictionary.
    Returns (best_key, decrypted_text, word_count_score).
    """
    best_key = 0
    max_score = -1
    best_decrypted = ""

    for key in range(26):
        decrypted = ShiftCipher.decrypt(ciphertext, key)
        # Tokenize alphabetic words
        words = re.findall(r'\b[A-Z]+\b', decrypted.upper())
        score = sum(1 for word in words if word.lower() in dictionary_words)

        if score > max_score:
            max_score = score
            best_key = key
            best_decrypted = decrypted

    return best_key, best_decrypted, max_score