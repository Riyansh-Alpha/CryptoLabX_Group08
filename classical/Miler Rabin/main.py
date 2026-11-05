import random
import time
import sympy


def miller_rabin(n: int, k: int = 40) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Decompose n - 1 into 2^s * d
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Conduct k testing round
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        composite = True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite = False
                break

        if composite:
            return False

    return True


def generate_candidate(bit_length: int = 512) -> int:
    """Generates a random candidate integer of exact bit len.

    Sets the Most Significant Bit (MSB) to 1 (ensuring bit length) and LSB to 1
    (ensuring odd parity).
    """
    candidate = random.getrandbits(bit_length)
    candidate |= (1 << (bit_length - 1)) | 1
    return candidate


def generate_512_bit_prime(bit_length: int = 512, k_rounds: int = 40):
    """Generates a probable prime of specified bit length using Miller-Rabin testing and

    small-prime pre-filtering.
    """
    # Pre-filtering primes to eliminate obvious composites fast
    small_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    candidates_tested = 0
    start_time = time.time()

    while True:
        candidates_tested += 1
        candidate = generate_candidate(bit_length)

        # Fast trial division with small primes
        if any(candidate % p == 0 for p in small_primes):
            continue

        # Miller-Rabin primality test
        if miller_rabin(candidate, k=k_rounds):
            elapsed_time = time.time() - start_time
            return candidate, candidates_tested, elapsed_time


if __name__ == "__main__":
    BIT_LENGTH = 512
    ROUNDS = 40

    prime, candidate_count, exec_time = generate_512_bit_prime(
        BIT_LENGTH, ROUNDS
    )

    print("=" * 50)
    print("      512-BIT PRIME GENERATION RESULTS")
    print("=" * 50)
    print(f"Assigned Bit Length   : {BIT_LENGTH}")
    print(f"Actual Bit Length     : {prime.bit_length()}")
    print(f"Candidates Tested     : {candidate_count}")
    print(f"Miller-Rabin Rounds   : {ROUNDS}")
    print(f"Execution Time        : {exec_time:.4f} seconds")
    print("\nGenerated Prime (Hex):")
    print(hex(prime))
    print("\nGenerated Prime (Decimal):")
    print(prime)

    # Independent Verification using SymPy
    is_valid = sympy.isprime(prime)
    print("\n" + "=" * 50)
    print(
        f"SymPy Independent Verification: {'PASSED' if is_valid else 'FAILED'}"
    )
    print("=" * 50)