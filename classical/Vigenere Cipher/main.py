from collections import Counter, defaultdict

ENGLISH_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

def clean_ciphertext(raw_text):
    return "".join(c.upper() for c in raw_text if c.isalpha())

def find_repeated_patterns(text, min_len=3, max_len=5):
    patterns = defaultdict(list)
    for l in range(min_len, max_len + 1):
        for i in range(len(text) - l + 1):
            pat = text[i:i+l]
            patterns[pat].append(i)
    return {k: v for k, v in patterns.items() if len(v) > 1}

def calculate_distances(patterns):
    distances = []
    for pat, indices in patterns.items():
        for i in range(len(indices) - 1):
            distances.append(indices[i+1] - indices[i])
    return distances

def find_factors(distances):
    factor_counts = Counter()
    for d in distances:
        for f in range(2, 21):
            if d % f == 0:
                factor_counts[f] += 1
    return factor_counts

def calculate_ic(text):
    N = len(text)
    if N <= 1:
        return 0.0
    counts = Counter(text)
    return sum(c * (c - 1) for c in counts.values()) / (N * (N - 1))

def kasiski_analysis(ciphertext):
    patterns = find_repeated_patterns(ciphertext)
    distances = calculate_distances(patterns)
    factors = find_factors(distances)
    
    ic_scores = {}
    for k in range(1, 17):
        groups = split_into_groups(ciphertext, k)
        avg_ic = sum(calculate_ic(g) for g in groups) / k
        ic_scores[k] = avg_ic
        
    best_key_length = max(ic_scores, key=ic_scores.get)
    return best_key_length, factors, ic_scores

def split_into_groups(ciphertext, key_length):
    groups = ['' for _ in range(key_length)]
    for i, char in enumerate(ciphertext):
        groups[i % key_length] += char
    return groups

def frequency_analysis(group):
    counts = Counter(group)
    return {chr(ord('A') + i): counts.get(chr(ord('A') + i), 0) for i in range(26)}

def find_shift(group):
    N = len(group)
    freq = frequency_analysis(group)
    best_shift = 0
    min_chi = float('inf')
    
    for s in range(26):
        chi_sq = 0.0
        for i in range(26):
            c_char = chr(ord('A') + i)
            p_char = chr(ord('A') + (i - s) % 26)
            observed = freq[c_char]
            expected = N * ENGLISH_FREQ[p_char]
            chi_sq += ((observed - expected) ** 2) / expected
        if chi_sq < min_chi:
            min_chi = chi_sq
            best_shift = s
    return best_shift

def find_key(ciphertext, key_length):
    groups = split_into_groups(ciphertext, key_length)
    key_chars = []
    for g in groups:
        shift = find_shift(g)
        key_chars.append(chr(ord('A') + shift))
    return "".join(key_chars)

def vigenere_decrypt(ciphertext, key):
    pt = []
    k_len = len(key)
    for i, c in enumerate(ciphertext):
        shift = ord(key[i % k_len]) - ord('A')
        p = chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
        pt.append(p)
    return "".join(pt)

def vigenere_encrypt(plaintext, key):
    ct = []
    k_len = len(key)
    for i, p in enumerate(plaintext):
        shift = ord(key[i % k_len]) - ord('A')
        c = chr((ord(p) - ord('A') + shift) % 26 + ord('A'))
        ct.append(c)
    return "".join(ct)

def verify(original_ct, recovered_pt, key):
    return vigenere_encrypt(recovered_pt, key) == original_ct


# Execution & Spaced Display Function
def display_results(ciphertext_raw):
    ct = clean_ciphertext(ciphertext_raw)
    est_key_len, _, _ = kasiski_analysis(ct)
    recovered_key = find_key(ct, est_key_len)
    recovered_pt = vigenere_decrypt(ct, recovered_key)
    is_valid = verify(ct, recovered_pt, recovered_key)


    print(" 1. ESTIMATED KEY LENGTH")

    print(f" Estimated Key Length : {est_key_len}\n\n")

    print(" 2. FREQUENCY TABLES FOR EACH GROUP")
    
    groups = split_into_groups(ct, est_key_len)
    for idx, grp in enumerate(groups):
        freq = frequency_analysis(grp)
        shift = find_shift(grp)
        key_char = chr(ord('A') + shift)
        
        freq_str = " ".join([f"{k}:{v:02d}" for k, v in freq.items() if v > 0])
        print(f" Group {idx+1:02d} (Key: {key_char}) -> {freq_str}\n")
    print("\n")


    print(" 3. RECOVERED KEY & VERIFICATION")
    print(f" Recovered Key        : {recovered_key}")
    print(f" Verification Status : {'MATCHED (True)' if is_valid else 'FAILED (False)'}\n\n")

   
    print(" 4. RECOVERED PLAINTEXT")
    print(f" {recovered_pt}\n")
    

if __name__ == "__main__":
    ciphertext_2_raw = """
    QRBAI UWYOK ILBRZ XTUWL EGXSN VDXWR XMHXY FCGMW WWSME LSXUZ
    MKMFS BNZIF YEIEG RFZRX WKUFA XQEDX DTTHY NTBRJ LHTAI KOCZX
    QHBND ZIGZG PXARJ EDYSJ NUMKI FLBTN HWISW NVLFM EGXAI AAWSL
    FMHXR SGRIG HEQTU MLGLV BRSIL AEZSG XCMHT OWHFM LWMRK HPRFB
    ELWGF RUGPB HNBEM KBNVW HHUEA KILBN BMLHK XUGML YQKHP RFBEL
    EJYNV WSIJB GAXGO TPMXR TXFKI WUALB RGWIE GHWHG AMEWW LTAEL
    NUMRE UWTBL SDPRL YVRET LEEDF ROBEQ UXTHX ZYOZB XLKAC KSOHN
    VWXKS MAEPH IYQMM FSECH RFYPB BSQTX TPIWH GPXQD FWTAI KNNBX
    SIYKE TXTLV BTMQA LAGHG OTPMX RTXTH XSFYG WMVKH LOIVU ALMLD
    LTSYV WYNVW MQVXP XRVYA BLXDL XSMLW SUIOI IMELI SOYEB HPHNR
    WTVUI AKEYG WIETG WWBVM VDUMA EPAUA KXWHK MAUPA MUKHQ PWKCX
    EFXGW WSDDE OMLWL NKMWD FWTAM FAFEA MFZBN WIHYA LXRWK MAMIK
    GNGHJ UAZHM HGUAL YSULA ELYHJ BZMSI LAILH WWYIK EWAHN PMLBN
    NBVPJ XLBEF WRWGX KWIRH XWWGQ HRRXW IOMFY CZHZL VXNVI OYZCM
    YDDEY IPWXT MMSHS VHHXZ YEWNV OAOEL SMLSW KXXFX STRVI HZLEF JXDAS FIE
    """
    display_results(ciphertext_2_raw)