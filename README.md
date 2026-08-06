# CryptoLabX

## Project Overview

CryptoLabX is a modular cryptography toolkit developed for **Cryptography Laboratory (22CPP307)** at MNIT Jaipur.
Throughout the semester, this toolkit will grow into a complete cryptanalysis framework covering classical ciphers,
modern algorithms, and cryptanalytic attacks.

**Week 1 — Assignment 1** establishes the project foundation: folder structure, a menu-driven CLI, file analysis,
and an execution logging system.

---

## Team Members

| Student ID     | Name     | Role (Week 1)                                      |
|----------------|----------|----------------------------------------------------|
| 2024UCP1319    | Riyansh  | Project structure, CLI, file analysis, datasets    |
| 2024UCP1444    | —        | Logger module, package setup, README documentation |

---

## Project Structure

```
CryptoLabX_Group08/
│
├── classical/          # Classical cipher implementations (Caesar, Vigenere, Playfair, Hill)
├── attacks/            # Cryptanalytic attacks (Brute Force, Frequency, Dictionary)
├── math/               # Mathematical utilities (GCD, modular arithmetic, matrices)
├── modern/             # Modern algorithms (AES, DES, RSA)
├── analysis/           # Statistical and frequency analysis tools
├── datasets/           # Sample text files for cipher input/analysis
│   ├── sample1.txt
│   ├── sample2.txt
│   ├── sample3.txt
│   ├── sample4.txt
│   └── sample5.txt
├── outputs/            # Execution logs and program output
│   └── execution.log
├── docs/               # Documentation and references
├── tests/              # Unit tests
├── utils/              # Shared utility modules
│   ├── file_analysis.py
│   └── logger.py
├── main.py
├── README.md
└── requirements.txt
```

---

## Week 1 — Completed Tasks

| Task | Description                                          | Status | Contributor  |
|------|------------------------------------------------------|--------|--------------|
| 1    | Git repository created (`CryptoLabX_Group08`)        | ✅     | 2024UCP1319  |
| 2    | Folder structure created                             | ✅     | 2024UCP1319  |
| 3    | Menu-driven CLI (Encrypt, Decrypt, Attack, Analyze)  | ✅     | 2024UCP1319  |
| 4    | File analysis (chars, words, lines, frequency)       | ✅     | 2024UCP1319  |
| 5    | Execution logging (date, time, menu option)          | ✅     | 2024UCP1444  |
| 6    | Five sample datasets created                         | ✅     | 2024UCP1319  |
| 7    | README documentation                                 | ✅     | 2024UCP1444  |

---

## Features (Week 1)

### Menu-Driven CLI
Run the application and interact via numbered options:
- **1. Encrypt** — Placeholder (Coming Soon)
- **2. Decrypt** — Placeholder (Coming Soon)
- **3. Attack** — Placeholder (Coming Soon)
- **4. Analyze Dataset** — Reads a file from `datasets/` and displays analysis
- **5. Exit** — Exits the application

### File Analysis (`utils/file_analysis.py`)
For any text file in `datasets/`, the tool reports:
- Total character count
- Total word count
- Total line count
- Unique character count
- Letter frequency (A–Z, case-insensitive)

### Execution Logging (`utils/logger.py`)
Every menu interaction is automatically logged to `outputs/execution.log`:
```
[2026-08-07 00:15:30] Menu Option Selected: Encrypt
[2026-08-07 00:15:45] Menu Option Selected: Analyze
[2026-08-07 00:16:02] Menu Option Selected: Exit
```

---

## How to Run

```bash
python main.py
```

**Requirements:** Python 3.8+ (no external packages needed for Week 1)

### Example Session
```
========== CryptoLabX ==========
1. Encrypt
2. Decrypt
3. Attack
4. Analyze Dataset
5. Exit
================================
Enter your choice: 4
Enter dataset filename: sample1.txt

------ File Analysis ------
Characters : 59
Words      : 8
Lines      : 1
Unique Chars: 36

Letter Frequency
a : 3
c : 3
...
```

---

## Output Files

| File                    | Description                          |
|-------------------------|--------------------------------------|
| `outputs/execution.log` | Timestamped log of all menu actions  |

---

## Future Modules

### Classical Ciphers (`classical/`)
- Caesar Cipher
- Vigenère Cipher
- Playfair Cipher
- Hill Cipher

### Modern Cryptography (`modern/`)
- AES (Advanced Encryption Standard)
- DES (Data Encryption Standard)
- RSA (Rivest–Shamir–Adleman)

### Cryptanalysis (`attacks/`)
- Frequency Analysis
- Dictionary Attack
- Brute Force
- Statistical Analysis

### Mathematical Utilities (`math/`)
- Modular Arithmetic
- Matrix Operations
- Prime Number Utilities
- GCD / Extended Euclidean Algorithm

---

## Submission Checklist (Week 1)

- [x] GitHub repository with meaningful commits from all members
- [x] Complete source code
- [x] Menu-driven CLI working
- [x] File analysis output
- [x] Execution log file generated
- [x] Five sample datasets
- [x] README (this document)

---

## Repository

**GitHub:** https://github.com/Riyansh-Alpha/CryptoLabX_Group08  
**Course:** Cryptography Laboratory (22CPP307)  
**Institute:** MNIT Jaipur