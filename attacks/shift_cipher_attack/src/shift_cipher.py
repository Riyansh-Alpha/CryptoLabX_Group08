class ShiftCipher:
    @staticmethod
    def encrypt(plaintext: str, key: int) -> str:
        """Encrypts text using a Shift Cipher with key k."""
        result = []
        for char in plaintext.upper():
            if char.isalpha():
                result.append(chr((ord(char) - 65 + key) % 26 + 65))
            else:
                result.append(char)
        return "".join(result)

    @staticmethod
    def decrypt(ciphertext: str, key: int) -> str:
        """Decrypts text using a Shift Cipher with key k."""
        return ShiftCipher.encrypt(ciphertext, -key)