"""
================================================================================
EVALUATION OF OS RANDOM-NUMBER GENERATORS FOR CRYPTOGRAPHIC APPLICATIONS
================================================================================
"""

import os
import sys
import math
import subprocess
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

SAMPLE_SIZE = 1024 * 1024  # 1 MB = 1,048,576 bytes

# ==============================================================================
# TASK 1: DATA GENERATION MODULES
# ==============================================================================

def get_urandom_bytes(size: int = SAMPLE_SIZE) -> bytes:
    """Reads directly from /dev/urandom on Linux/POSIX, or falls back to os.urandom."""
    if os.path.exists("/dev/urandom"):
        try:
            with open("/dev/urandom", "rb") as f:
                return f.read(size)
        except Exception:
            pass
    return os.urandom(size)

def get_openssl_bytes(size: int = SAMPLE_SIZE) -> bytes:
    """Generates bytes using OpenSSL CLI if available, otherwise os.urandom fallback."""
    try:
        res = subprocess.run(
            ["openssl", "rand", str(size)], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            check=True
        )
        if len(res.stdout) == size:
            return res.stdout
    except Exception:
        pass
    return os.urandom(size)

def get_windows_cng_bytes(size: int = SAMPLE_SIZE) -> bytes:
    """Generates bytes using Windows PowerShell .NET RNG or os.urandom (BCryptGenRandom)."""
    if sys.platform == "win32":
        try:
            ps_cmd = (
                f"$b = New-Object byte[] {size}; "
                f"[System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($b); "
                f"[Console]::OpenStandardOutput().Write($b, 0, {size})"
            )
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                check=True
            )
            if len(res.stdout) == size:
                return res.stdout
        except Exception:
            pass
    return os.urandom(size)

def get_weak_lcg_bytes(size: int = SAMPLE_SIZE) -> bytes:
    """Generates 1 MB from a deterministic non-cryptographic Linear Congruential Generator."""
    stream = bytearray()
    state = 12345
    for _ in range(size):
        state = (1103515245 * state + 12345) & 0xFFFFFFFF
        stream.append((state >> 16) & 0xFF)
    return bytes(stream)


# ==============================================================================
# TASKS 2 & 3: STATISTICAL ANALYSIS ENGINE
# ==============================================================================

def analyze_random_stream(data: bytes, label: str) -> dict:
    """
    Computes statistical randomness metrics on a binary byte stream:
    - Byte Frequency Chi-Square Test & p-value
    - Shannon Entropy (bits/byte)
    - NIST SP 800-22 Frequency (Monobit) Test
    - NIST SP 800-22 Runs Test
    - Lag-1 Serial Correlation Coefficient
    """
    N = len(data)
    n_bits = N * 8
    arr = np.frombuffer(data, dtype=np.uint8)

    # 1. Byte Frequency Distribution & Chi-Square Test
    counts = np.bincount(arr, minlength=256)
    expected = N / 256.0
    chi2_stat = np.sum((counts - expected) ** 2 / expected)
    chi2_p = 1.0 - stats.chi2.cdf(chi2_stat, df=255)

    # 2. Shannon Entropy (bits per byte)
    probs = counts / N
    probs_nz = probs[probs > 0]
    entropy = -np.sum(probs_nz * np.log2(probs_nz))

    # 3. NIST SP 800-22 Monobit Frequency Test
    bits = np.unpackbits(arr).astype(np.int64)
    s_n = np.sum(bits * 2 - 1)
    s_obs = abs(s_n) / math.sqrt(n_bits)
    monobit_p = math.erfc(s_obs / math.sqrt(2.0))

    # 4. NIST SP 800-22 Runs Test
    pi = np.mean(bits)
    if abs(pi - 0.5) >= (2.0 / math.sqrt(n_bits)):
        runs_p = 0.0
    else:
        v_obs = np.sum(bits[:-1] != bits[1:]) + 1
        num = abs(v_obs - 2.0 * n_bits * pi * (1.0 - pi))
        den = 2.0 * math.sqrt(2.0 * n_bits) * pi * (1.0 - pi)
        runs_p = math.erfc(num / den) if den != 0 else 0.0

    # 5. Serial Correlation Coefficient (lag 1)
    arr_f = arr.astype(np.float64)
    mean_val = np.mean(arr_f)
    var_val = np.var(arr_f)
    serial_corr = (np.mean((arr_f[:-1] - mean_val) * (arr_f[1:] - mean_val)) / var_val) if var_val != 0 else 0.0

    passed = (chi2_p >= 0.01) and (monobit_p >= 0.01) and (runs_p >= 0.01)

    return {
        "Label": label,
        "Entropy": entropy,
        "Chi2_Stat": chi2_stat,
        "Chi2_p": chi2_p,
        "Monobit_p": monobit_p,
        "Runs_p": runs_p,
        "Serial_Corr": serial_corr,
        "Status": "PASS" if passed else "FAIL"
    }

def plot_serial_correlations(datasets: list, output_filename: str = "rng_serial_correlation.png"):
    """Generates Lag-1 scatter plots for visual inspection of patterns."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    fig.suptitle("Lag-1 Serial Correlation Scatter Plots (First 10,000 Bytes)", fontsize=14, fontweight="bold")

    for ax, (label, data) in zip(axes.flatten(), datasets):
        arr = np.frombuffer(data[:10000], dtype=np.uint8)
        ax.scatter(arr[:-1], arr[1:], alpha=0.3, s=1, c="navy")
        ax.set_title(label, fontsize=11, fontweight="semibold")
        ax.set_xlabel("Byte x[t]")
        ax.set_ylabel("Byte x[t+1]")
        ax.set_xlim(0, 255)
        ax.set_ylim(0, 255)
        ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    print("[+] Correlation plot saved to " + output_filename)


# ==============================================================================
# MAIN EXECUTION & REPORTING
# ==============================================================================

def main():
    print("=" * 80)
    print(" OPERATING SYSTEM RANDOM-NUMBER GENERATION EVALUATION ")
    print("=" * 80)
    print("Generating 1 MB (1,048,576 bytes) per generator...\n")

    # 1. Fetch datasets
    d_urandom = get_urandom_bytes()
    d_openssl = get_openssl_bytes()
    d_cng = get_windows_cng_bytes()
    d_lcg = get_weak_lcg_bytes()

    datasets = [
        ("Linux /dev/urandom", d_urandom),
        ("OpenSSL rand CLI", d_openssl),
        ("Windows CNG / .NET", d_cng),
        ("Weak LCG (Control)", d_lcg)
    ]

    # 2. Run statistical evaluation
    results = [analyze_random_stream(data, name) for name, data in datasets]

    # 3. Print Formatted Results Table
    header = f"{'Generator':<22} | {'Entropy':<9} | {'Chi2 p-val':<10} | {'Monobit p':<10} | {'Runs p':<10} | {'Serial Corr':<11} | {'Verdict':<7}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    for r in results:
        print(
            f"{r['Label']:<22} | "
            f"{r['Entropy']:<9.6f} | "
            f"{r['Chi2_p']:<10.5f} | "
            f"{r['Monobit_p']:<10.5f} | "
            f"{r['Runs_p']:<10.5f} | "
            f"{r['Serial_Corr']:<11.6f} | "
            f"{r['Status']:<7}"
        )
    print("-" * len(header))

    # 4. Save Plots
    plot_serial_correlations(datasets)

    # 5. Technical Synthesis & Cryptographic Discussion
    print("\n" + "=" * 80)
    print(" ARCHITECTURAL COMPARISON & CRYPTOGRAPHIC SECURITY ")
    print("=" * 80)
    print("""
1. LINUX vs. WINDOWS RNG ARCHITECTURES:
   - Linux CRNG: Uses ChaCha20 seeded via BLAKE2s from kernel entropy pools.
     /dev/urandom and getrandom() are non-blocking once initialized at boot.
   - Windows CNG: Uses NIST SP 800-90A compliant AES-256 CTR DRBG in cng.sys.
     High-level APIs use user-space ProcessPrng cached state.

2. WHY PASSING STATISTICAL TESTS DOES NOT GUARANTEE CRYPTOGRAPHIC SECURITY:
   - Statistical Uniformity != Computational Unpredictability:
     Mersenne Twister (MT19937) passes all statistical tests easily, yet its
     state is fully recoverable after observing 624 outputs.
   - Next-Bit Unpredictability Requirement:
     CSPRNGs guarantee that predicting b_{k+1} given b_1..b_k is infeasible.
   - State Compromise Extension (Forward/Backward Secrecy):
     CSPRNGs implement key erasure and re-seeding to protect past and future output.
    """)

if __name__ == "__main__":
    main()