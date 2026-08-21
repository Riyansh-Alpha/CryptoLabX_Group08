import sqlite3
import time

# Simulated authenticated user session (Logged in as User ID: 101)
CURRENT_USER_ID = 101

# In-memory cart storing: {product_id: quantity}
cart = {}

def init_database():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Schema setup
    cursor.execute("CREATE TABLE products (id INT PRIMARY KEY, name TEXT, price REAL)")
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?)", [
        (1, 'Wireless Laptop', 899.99),
        (2, 'Mechanical Keyboard', 79.99),
        (3, 'Gaming Mouse', 49.99)
    ])

    cursor.execute("CREATE TABLE orders (id INT PRIMARY KEY, user_id INT, details TEXT, total REAL)")
    # Pre-existing order belonging to User 102
    cursor.execute("INSERT INTO orders VALUES (5001, 102, '1x Wireless Laptop', 899.99)")

    conn.commit()
    return conn

# --- CORE FUNCTION 1: PRODUCT BROWSING ---
# VULNERABILITY 1: SQL Injection (SQLi)
def search_products(conn):
    keyword = input("\nEnter product search term: ")
    cursor = conn.cursor()
    
    # VULNERABLE: Direct f-string concatenation of unsanitized input
    sql_query = f"SELECT * FROM products WHERE name LIKE '%{keyword}%'"

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        print("\n--- Available Products ---")
        for row in results:
            print(f"ID: {row[0]} | Item: {row[1]} | Price: ${row[2]:.2f}")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")

# --- CORE FUNCTION 2: SHOPPING CART ---
def add_to_cart():
    try:
        prod_id = int(input("\nEnter Product ID to add: "))
        qty = int(input("Enter Quantity: "))
        cart[prod_id] = cart.get(prod_id, 0) + qty
        print("Product added to cart!")
    except ValueError:
        print("Invalid numerical input.")

# --- CORE FUNCTION 3: CHECKOUT ---
# VULNERABILITY 2: Price Manipulation due to Poor Validation
def checkout_cart(conn):
    if not cart:
        print("\nYour cart is empty.")
        return

    print("\n--- Checkout ---")
    grand_total = 0.0

    for prod_id, qty in cart.items():
        # VULNERABLE: Asks the client console to input unit price during checkout
        # instead of querying the authoritative database catalog price.
        client_supplied_price = float(input(f"Enter payment amount per unit for Product ID {prod_id}: $"))
        grand_total += (client_supplied_price * qty)

    new_order_id = int(time.time()) % 10000
    order_details = str(cart)

    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO orders VALUES ({new_order_id}, {CURRENT_USER_ID}, '{order_details}', {grand_total})")
    conn.commit()

    print(f"Checkout Complete! Order #{new_order_id} created. Total Paid: ${grand_total:.2f}")
    cart.clear()

# --- CORE FUNCTION 4: ORDER HISTORY ---
# VULNERABILITY 3: Insecure Direct Object Reference (IDOR)
def view_order_history(conn):
    try:
        order_id = int(input("\nEnter Order ID to lookup: "))
        cursor = conn.cursor()

        # VULNERABLE: Directly fetches order record without checking
        # if 'user_id' in the record matches 'CURRENT_USER_ID'.
        cursor.execute(f"SELECT * FROM orders WHERE id = {order_id}")
        row = cursor.fetchone()

        if row:
            print("\n--- Order Summary ---")
            print(f"Order ID   : {row[0]}")
            print(f"Belongs To : User #{row[1]}")
            print(f"Items      : {row[2]}")
            print(f"Total Paid : ${row[3]:.2f}")
        else:
            print("Order ID not found.")
    except ValueError:
        print("Invalid Order ID.")

def main():
    conn = init_database()

    while True:
        print("\n=========================================")
        print("       CONSOLE E-COMMERCE STORE          ")
        print("=========================================")
        print(f"Logged in User ID: {CURRENT_USER_ID}")
        print("1. Browse Products (Search)")
        print("2. Add Item to Shopping Cart")
        print("3. View Shopping Cart & Checkout")
        print("4. View Order History")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            search_products(conn)
        elif choice == '2':
            add_to_cart()
        elif choice == '3':
            checkout_cart(conn)
        elif choice == '4':
            view_order_history(conn)
        elif choice == '5':
            print("Exiting application. Goodbye!")
            conn.close()
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()