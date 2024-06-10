def ussd_session():
    session_data = {}
    session_id = "unique_session_id"  # Simulated session ID
    phone_number = input("Enter your phone number: ")

    while True:
        if session_id not in session_data:
            session_data[session_id] = {}

        response = "Welcome to Money Transfer Service\n"
        response += "1. Send Money\n"
        print(response)

        text = input("Choose an option: ")

        if text == "1":
            amount = input("Enter amount to send: ")
            recipient_phone = input("Enter recipient phone number: ")
            confirmation = input(f"Confirm sending KES {amount} to {recipient_phone}:\n1. Confirm\n2. Cancel\n")
            
            if confirmation == "1":
                print(f"KES {amount} has been sent to {recipient_phone}.")
            elif confirmation == "2":
                print("Transaction cancelled.")
            else:
                print("Invalid choice.")
        else:
            print("Invalid choice.")

        continue_session = input("Do you want to perform another transaction? (yes/no): ")
        if continue_session.lower() != 'yes':
            break

if __name__ == "__main__":
    ussd_session()
