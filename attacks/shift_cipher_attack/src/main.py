import os
from shift_cipher import ShiftCipher
from brute_force_dictionary import dictionary_attack
from chi_square_attack import chi_square_attack

def load_dictionary(filepath: str) -> set:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return set(word.strip().lower() for word in f if word.strip())
    # Default fallback vocabulary if dictionary file is missing
    return {"the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog", "cryptanalysis", "shift", "cipher"}

def main():
    dict_path = os.path.join("..", "dictionary", "english_words.txt")
    dictionary_words = load_dictionary(dict_path)

    test_cases = [
        ("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG", 7),
        ("CRYPTANALYSIS OF SHIFT CIPHER USING BRUTE FORCE", 15),
        ("SHORT TEXT", 3)
    ]

    print(f"{'Test Case':<12} | {'Actual Key':<10} | {'Dict Key':<10} | {'ChiSq Key':<10} | {'Dictionary Correct?':<20} | {'Chi-Square Correct?':<20}")
    print("-" * 95)

    for idx, (plaintext, actual_key) in enumerate(test_cases, start=1):
        ciphertext = ShiftCipher.encrypt(plaintext, actual_key)

        dict_key, _, _ = dictionary_attack(ciphertext, dictionary_words)
        chisq_key, _, _ = chi_square_attack(ciphertext)

        dict_correct = "Yes" if dict_key == actual_key else "No"
        chisq_correct = "Yes" if chisq_key == actual_key else "No"

        print(f"{'Case ' + str(idx):<12} | {actual_key:<10} | {dict_key:<10} | {chisq_key:<10} | {dict_correct:<20} | {chisq_correct:<20}")

if __name__ == "__main__":
    main()