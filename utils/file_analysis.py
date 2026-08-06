import os
from collections import Counter


def analyze_file(filename):

    path = os.path.join("datasets", filename)

    if not os.path.exists(path):
        print("File not found.")
        return

    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    characters = len(text)
    words = len(text.split())
    lines = len(text.splitlines())
    unique_characters = len(set(text))

    letters = [c.lower() for c in text if c.isalpha()]
    frequency = Counter(letters)

    print("\n------ File Analysis ------")
    print("Characters :", characters)
    print("Words      :", words)
    print("Lines      :", lines)
    print("Unique Chars:", unique_characters)

    print("\nLetter Frequency")

    for letter in sorted(frequency):
        print(f"{letter} : {frequency[letter]}")
