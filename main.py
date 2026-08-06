from utils.file_analysis import analyze_file
from utils.logger import log_menu

MENU = """
========== CryptoLabX ==========
1. Encrypt
2. Decrypt
3. Attack
4. Analyze Dataset
5. Exit
================================
"""

def main():

    while True:
        print(MENU)
        choice = input("Enter your choice: ")

        if choice == "1":
            log_menu("Encrypt")
            print("\nComing Soon...\n")

        elif choice == "2":
            log_menu("Decrypt")
            print("\nComing Soon...\n")

        elif choice == "3":
            log_menu("Attack")
            print("\nComing Soon...\n")

        elif choice == "4":
            log_menu("Analyze")
            filename = input("Enter dataset filename: ")
            analyze_file(filename)

        elif choice == "5":
            log_menu("Exit")
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()