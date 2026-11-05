import random
import string
import time


class MT19937StreamCipher:
    """Stream cipher using MT19937 PRNG to generate 8-bit keystream bytes."""

    def __init__(self, seed: int):
        # Python's random module uses MT19937 as its core generator
        self.rng = random.Random(seed)

    def get_keystream_byte(self) -> int:
        """Extract an 8-bit keystream value (0-255)."""
        return self.rng.randint(0, 255)

    def encrypt_decrypt(self, data: bytes) -> bytes:
        """Symmetric XOR encryption/decryption function."""
        result = bytearray()
        for b in data:
            keystream_byte = self.get_keystream_byte()
            result.append(b ^ keystream_byte)
        return bytes(result)


def run_part_a():
    print("==================================================")
    print(" PART A: MT19937 Stream Cipher & Seed Recovery ")
    print("==================================================")

    # 1 & 2: Test Message Verification
    test_seed = 12345
    test_msg = b"Hello Cryptography World!"
    cipher_enc = MT19937StreamCipher(test_seed)
    ciphertext_test = cipher_enc.encrypt_decrypt(test_msg)

    cipher_dec = MT19937StreamCipher(test_seed)
    plaintext_test = cipher_dec.encrypt_decrypt(ciphertext_test)

    print(f"[1-2] Test Message: {test_msg.decode()}")
    print(f"      Ciphertext (hex): {ciphertext_test.hex()}")
    print(
        f"      Decryption Successful: {test_msg == plaintext_test} (Match Verified)\n"
    )

    # 3: Plaintext Generation & Encryption with 16-bit Seed
    random.seed(42)  # Fixed generator seed for laboratory repeatability
    prefix_len = random.randint(5, 20)
    prefix = "".join(
        random.choices(string.ascii_letters + string.digits, k=prefix_len)
    )
    known_sequence = b"AAAAAAAAAAAAAA"  # 14 consecutive 'A's
    full_plaintext = (prefix + known_sequence.decode()).encode("utf-8")

    secret_16bit_seed = random.randint(0, 65535)  # Random 16-bit seed
    target_cipher = MT19937StreamCipher(secret_16bit_seed)
    ciphertext_a = target_cipher.encrypt_decrypt(full_plaintext)

    print(f"[3] Setup Target Ciphertext:")
    print(f"    - Generated Plaintext: {full_plaintext}")
    print(f"    - True Secret 16-bit Seed: {secret_16bit_seed} (0x{secret_16bit_seed:04X})")
    print(f"    - Ciphertext (hex): {ciphertext_a.hex()}\n")

    # 4 & 5: Brute-Force 16-bit Seed Search Space (65,536 keys)
    print("[4-5] Executing Brute-Force Attack across 65,536 seeds...")
    start_time = time.time()

    recovered_seed = None
    recovered_plaintext = None

    for candidate_seed in range(65536):
        c = MT19937StreamCipher(candidate_seed)
        candidate_pt = c.encrypt_decrypt(ciphertext_a)
        if known_sequence in candidate_pt:
            recovered_seed = candidate_seed
            recovered_plaintext = candidate_pt
            break

    elapsed_time = time.time() - start_time

    print(f"      Brute-force Completed in: {elapsed_time:.4f} seconds")
    print(f"      Recovered Seed: {recovered_seed} (0x{recovered_seed:04X})")
    print(
        f"      Seed Verification: {'SUCCESS (Matches Secret Seed)' if recovered_seed == secret_16bit_seed else 'FAILED'}"
    )
    print(f"      Recovered Plaintext: {recovered_plaintext}\n")


def run_part_b():
    print("==================================================")
    print(" PART B: Predictable Password Reset Tokens ")
    print("==================================================")

    # 6, 7, 8: Token Generation using Timestamp T
    T = int(time.time())
    token_cipher = MT19937StreamCipher(T)
    token_bytes = bytes([token_cipher.get_keystream_byte() for _ in range(16)])
    token_hex = token_bytes.hex()

    print(f"[6-8] Token Generation:")
    print(f"      - Generation Timestamp (T): {T} (Unix seconds)")
    print(f"      - Observed 16-byte Reset Token (hex): {token_hex}\n")

    # 9, 10, 11: Token Prediction & Timestamp Search Space Attack
    window_start = T - 300
    window_end = T + 300
    print(
        f"[9-11] Attacker Search Window: [{window_start} to {window_end}] (Total: {window_end - window_start + 1} candidates)"
    )

    candidates_tested = 0
    recovered_T = None

    for candidate_t in range(window_start, window_end + 1):
        candidates_tested += 1
        cand_cipher = MT19937StreamCipher(candidate_t)
        cand_token_bytes = bytes(
            [cand_cipher.get_keystream_byte() for _ in range(16)]
        )

        if cand_token_bytes == token_bytes:
            recovered_T = candidate_t
            break

    print(f"       Timestamps Tested: {candidates_tested}")
    print(f"       Recovered Timestamp: {recovered_T}")
    print(
        f"       Timestamp Verification: {'SUCCESS (Matches T)' if recovered_T == T else 'FAILED'}"
    )

    # Regenerate token with recovered timestamp for double verification
    verify_cipher = MT19937StreamCipher(recovered_T)
    regen_token_hex = bytes(
        [verify_cipher.get_keystream_byte() for _ in range(16)]
    ).hex()

    print(f"       Regenerated Token: {regen_token_hex}")
    print(
        f"       Token Match Verification: {'SUCCESS (Tokens Match Exactly)' if regen_token_hex == token_hex else 'FAILED'}\n"
    )


if __name__ == "__main__":
    run_part_a()
    run_part_b()