import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class AESCBCOracle:
    """
    Simulates a remote server holding a secret AES key.
    Provides encryption and a boolean padding oracle interface.
    """
    def __init__(self):
        # Secret key (never exposed to the attacker)
        self._key = os.urandom(16)
        self.query_count = 0

    def encrypt(self, plaintext: bytes) -> tuple[bytes, bytes]:
        iv = os.urandom(16)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        cipher = Cipher(algorithms.AES(self._key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv, ciphertext

    def query(self, iv: bytes, ciphertext: bytes) -> bool:
        """
        Padding Oracle: Returns True if decryption yields valid PKCS#7 padding,
        False otherwise.
        """
        self.query_count += 1
        cipher = Cipher(algorithms.AES(self._key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        try:
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            unpadder.update(padded_data) + unpadder.finalize()
            return True
        except ValueError:
            return False


def padding_oracle_attack(oracle: AESCBCOracle, iv: bytes, ciphertext: bytes) -> bytes:
    """
    Recovers the plaintext from an AES-CBC ciphertext using only the padding oracle.
    """
    block_size = 16
    # Chain IV and ciphertext blocks into a single indexed list
    blocks = [iv] + [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
    recovered_plaintext = bytearray()

    # Process target blocks C_1, C_2, ... C_N
    for b in range(1, len(blocks)):
        prev_block = bytearray(blocks[b - 1])
        target_block = blocks[b]

        intermediate = bytearray(block_size)    # Discovered D_K(C_b)
        block_plaintext = bytearray(block_size)  # Decrypted P_b

        # Decrypt block right-to-left (byte index 15 down to 0)
        for i in range(block_size - 1, -1, -1):
            pad_val = block_size - i  # Target padding byte value (0x01, 0x02, ...)
            c_prime = bytearray(block_size)

            # Fix lower-order bytes to produce target padding value
            for j in range(i + 1, block_size):
                c_prime[j] = intermediate[j] ^ pad_val

            # Brute-force byte at index i
            found = False
            for byte_guess in range(256):
                c_prime[i] = byte_guess

                if oracle.query(bytes(c_prime), target_block):
                    # Resolve multi-byte padding collisions when pad_val == 1
                    if pad_val == 1 and i > 0:
                        c_prime_check = bytearray(c_prime)
                        c_prime_check[i - 1] ^= 0xFF
                        if not oracle.query(bytes(c_prime_check), target_block):
                            continue

                    # Recover intermediate byte and original plaintext byte
                    inter_byte = byte_guess ^ pad_val
                    intermediate[i] = inter_byte
                    block_plaintext[i] = inter_byte ^ prev_block[i]
                    found = True
                    break

            if not found:
                raise RuntimeError(f"Failed to decrypt byte {i} in block {b}")

        recovered_plaintext.extend(block_plaintext)

    # Remove PKCS#7 padding from total recovered plaintext
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(bytes(recovered_plaintext)) + unpadder.finalize()


if __name__ == "__main__":
    server_oracle = AESCBCOracle()
    secret_message = b"Padding Oracle Attack on AES-CBC mode demonstration!"

    iv, ciphertext = server_oracle.encrypt(secret_message)

    print("=== Execution Details ===")
    print(f"Ciphertext length: {len(ciphertext)} bytes ({len(ciphertext) // 16} blocks)")

    # Execute attack
    recovered = padding_oracle_attack(server_oracle, iv, ciphertext)

    print("\n=== Attack Results ===")
    print(f"Recovered Plaintext : {recovered.decode('utf-8')}")
    print(f"Total Oracle Queries: {server_oracle.query_count}")