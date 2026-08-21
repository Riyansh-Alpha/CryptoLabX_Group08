from shift_cipher import ShiftCipher

# Standard English letter frequency distribution (A-Z)
ENGLISH_FREQ = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
]

def chi_square_attack(ciphertext: str) -> tuple[int, str, float]:
    """
    Performs Chi-Square frequency analysis to predict the decryption key[cite: 1].
    Returns (best_key, decrypted_text, min_chi_square_score).
    """
    best_key = 0
    min_chi_square = float('inf')
    best_decrypted = ""

    for key in range(26):
        decrypted = ShiftCipher.decrypt(ciphertext, key)
        letters_only = [c.upper() for c in decrypted if c.isalpha()]
        N = len(letters_only)

        if N == 0:
            continue

        observed = [0] * 26
        for char in letters_only:
            observed[ord(char) - 65] += 1

        chi_sq = 0.0
        for i in range(26):
            expected = N * ENGLISH_FREQ[i]
            if expected > 0:
                chi_sq += ((observed[i] - expected) ** 2) / expected

        if chi_sq < min_chi_square:
            min_chi_square = chi_sq
            best_key = key
            best_decrypted = decrypted

    return best_key, best_decrypted, min_chi_square