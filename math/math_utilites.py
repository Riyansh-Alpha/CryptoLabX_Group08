def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def menu():
    print("Math Utilities Module")
    print("Example: gcd(24, 18) =", gcd(24, 18))


if __name__ == "__main__":
    menu()