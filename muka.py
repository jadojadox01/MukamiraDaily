import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Milk_store"
    )

def validate_phone(phone):
    return len(phone) == 10 and (phone.startswith("078") or phone.startswith("079"))

def register_customer():
    connection = connect_db()
    cursor = connection.cursor()
    
    print("Customer Registration")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    
    while not validate_phone(phone):
        print("We do not allow this kind of contact. Please enter a valid phone number.")
        phone = input("Enter your phone number: ")
    
    cursor.execute("SELECT * FROM Customers WHERE Email = %s", (email,))
    if cursor.fetchone():
        print("Email Exists. Please use a different email.")
        cursor.close()
        connection.close()
        return

    cursor.execute("SELECT * FROM Customers WHERE Phone = %s", (phone,))
    if cursor.fetchone():
        print("Phone Already Exists. Please use a different phone number.")
        cursor.close()
        connection.close()
        return
    
    road_nbr = input("Enter your road number: ")
    pin = input("Enter your pin: ")

    cursor.execute(
        "INSERT INTO Customers (Email, Phone, Road_nbr, Pin) VALUES (%s, %s, %s, %s)",
        (email, phone, road_nbr, pin)
    )
    connection.commit()
    print("Registration successful!")
    cursor.close()
    connection.close()

def login_customer():
    connection = connect_db()
    cursor = connection.cursor()

    print("Customer Login")
    pin = input("Enter your pin: ")

    cursor.execute("SELECT C_id FROM Customers WHERE Pin = %s", (pin,))
    result = cursor.fetchone()
    
    if result:
        customer_id = result[0]
        print("Login successful!")
        cursor.close()
        connection.close()
        return customer_id
    else:
        print("Invalid pin. Please try again or register.")
        cursor.close()
        connection.close()
        return None

def place_order(customer_id):
    connection = connect_db()
    cursor = connection.cursor()

    print("WELCOME TO MUKAMIRA DIARY LTD")
    print("1. Place Order")
    print("2. Exit")
    choice = input("Choose an option: ")

    if choice == '2':
        print("Exiting...")
        return

    # Step 2: Select a product
    print("SELECT A PRODUCT:\n")
    cursor.execute("SELECT P_name FROM products")
    products = cursor.fetchall()

    for idx, product in enumerate(products, start=1):
        print(f"{idx}. {product[0]}")

    product_choice = int(input("Choose a product: ")) - 1
    selected_product = products[product_choice][0]

    # Step 3: Select a size
    print("SELECT SIZE")
    sizes = ["250 ml", "1L", "3L","5L"]
    for idx, size in enumerate(sizes, start=1):
        print(f"{idx}. {size}")

    size_choice = int(input("Choose a size: ")) - 1
    selected_size = sizes[size_choice]

    # Step 4: Confirm order
    order_amount = int(input("Enter Order amount: "))
    cursor.execute("SELECT P_unitprice FROM products WHERE P_name = %s", (selected_product,))
    unit_price = cursor.fetchone()[0]
    total_price = order_amount * unit_price

    print("Confirm Order:")
    print(f"Product_Name: {selected_product}")
    print(f"Size: {selected_size}")
    print(f"Order_Amount: {order_amount}")
    print(f"Total_Price: {total_price}")
    print("1. Confirm")
    print("2. Cancel")

    final_choice = input("Choose an option: ")

    if final_choice == '1':
        cursor.execute(
            "INSERT INTO Orders (C_id, Order_amount, Order_totalprice) VALUES (%s, %s, %s)",
            (customer_id, order_amount, total_price)
        )
        connection.commit()
        print("Order placed successfully!")
    else:
        print("Order cancelled.")

    cursor.close()
    connection.close()

def main():
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            register_customer()
        elif choice == '2':
            customer_id = login_customer()
            if customer_id:
                place_order(customer_id)
                break 
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
