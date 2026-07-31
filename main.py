import os
from utils.file_analysis import analyze_file
from utils.logger import write_log


def display_menu():
    print("\n===== CryptoLabX =====")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Attack")
    print("4. Analyze File")
    print("5. Exit")


while True:

    display_menu()

    choice = input("Select an option: ")

    if choice == "1":
        print("\nEncrypt Module Coming Soon")
        write_log("Encrypt")

    elif choice == "2":
        print("\nDecrypt Module Coming Soon")
        write_log("Decrypt")

    elif choice == "3":
        print("\nAttack Module Coming Soon")
        write_log("Attack")

    elif choice == "4":
        filename = input("Enter filename from datasets folder: ")

        path = os.path.join("datasets", filename)

        analyze_file(path)

        write_log("Analyze")

    elif choice == "5":
        write_log("Exit")
        print("Goodbye.")
        break

    else:
        print("Invalid choice")