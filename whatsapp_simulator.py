
def confirmation_flow():

    print("\n--- WhatsApp Confirmation ---")

    print("Business: Hi! Your order is ready.")
    print("Please confirm delivery by replying YES or NO.")

    reply = input("Customer: ").strip().lower()

    if reply in ["yes", "y"]:
        print("Business: Thank you! Your order is confirmed.")
        return "CONFIRMED"

    elif reply in ["no", "n"]:
        print("Business: Your order has been cancelled.")
        return "CANCELLED"

    else:
        print("Business: Please reply YES or NO.")
        return "WAITING"


def prepaid_flow():

    print("\n--- Prepaid Offer ---")

    print("Business: Get ₹20 off by paying online!")
    print("Your new total is ₹629.")

    reply = input("Customer: ").strip().lower()

    if reply in ["pay", "yes", "y"]:
        print("Business: Payment link generated.")
        print("Waiting for payment verification.")
        return "PAYMENT_PENDING"

    elif reply in ["no", "n", "cod"]:
        print("Business: Would you like to confirm your COD order?")
        return "COD_CONFIRMATION"

    else:
        print("Business: Please choose PAY or NO.")
        return "WAITING"


if __name__ == "__main__":

    print("1. Confirmation flow")
    print("2. Prepaid flow")

    choice = input("Select flow: ")

    if choice == "1":
        print("Final status:", confirmation_flow())

    elif choice == "2":
        print("Final status:", prepaid_flow())
