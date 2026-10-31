
import re


def validate_address(name, address):

    name = str(name).strip()
    address = str(address).strip()

    result = {
        "name_status": "valid",
        "address_status": "valid",
        "reason": []
    }

    # 1. Validate customer name
    fake_names = [
        "asdf",
        "test",
        "unknown",
        "abc",
        "qwerty",
        "dummy"
    ]

    if not name or name.lower() in fake_names:
        result["name_status"] = "suspicious"
        result["reason"].append(
            "Customer name appears incomplete or suspicious."
        )

    elif len(name) < 2 or not re.search(r"[a-zA-Z]", name):
        result["name_status"] = "review"
        result["reason"].append(
            "Customer name needs manual verification."
        )

    # 2. Validate address
    if not address:
        result["address_status"] = "incomplete"
        result["reason"].append(
            "Delivery address is missing."
        )

    elif len(address) < 10:
        result["address_status"] = "incomplete"
        result["reason"].append(
            "Delivery address is too short."
        )

    else:

        # Check for obvious placeholder addresses
        placeholders = [
            "asdf",
            "test address",
            "dummy address",
            "qwerty"
        ]

        if address.lower() in placeholders:
            result["address_status"] = "suspicious"
            result["reason"].append(
                "Address appears to be placeholder text."
            )

        # Landmark-only address may need clarification
        elif any(
            phrase in address.lower()
            for phrase in [
                "near",
                "opposite",
                "behind",
                "ke paas",
                "ke andar",
                "gali no",
                "petrol pump",
                "mandir ke paas",
                "school ke paas"
            ]
        ):
            result["address_status"] = "review"
            result["reason"].append(
                "Address contains landmark-based directions. "
                "Additional location details may be required."
            )

            result["address_status"] = "review"
            result["reason"].append(
                "Address uses landmarks without a clear "
                "house or building number."
            )

    if not result["reason"]:
        result["reason"].append(
            "No obvious address or name issue detected."
        )

    return result


# Test examples
if __name__ == "__main__":

    test_cases = [
        ("Olivia Ann", "House 24, MG Road, Kochi, Kerala"),
        ("asdf", "test address"),
        ("Rahul", "Near temple, call when nearby"),
        ("Anjali", "gali no 22 ke andar, petrol pump ke paas")
    ]

    for name, address in test_cases:

        print("\nCustomer:", name)
        print("Address:", address)

        print(validate_address(name, address))
