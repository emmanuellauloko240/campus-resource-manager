resources = [
    {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
    {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
    {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3},
]
fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
borrow_records = []


def clean_id(text):
    return text.strip().upper()


def get_positive_number(prompt):
    while True:
        try:
            typed = int(input(prompt))
            if typed > 0:
                return typed
            print("Number must be greater than 0.")
        except ValueError:
            print("Please enter a whole number, for example 5.")


def find_resource(looking_for):
    looking_for = clean_id(looking_for)
    for resource in resources:
        if resource["id"] == looking_for:
            return resource
    return None


def add_resource(resource_id, name, category, total):
    resource_id = clean_id(resource_id)
    name = name.strip()
    category = category.strip()
    if resource_id == "":
        print("Rejected: resource ID cannot be empty.")
        return
    if find_resource(resource_id) is not None:
        print("Rejected: resource ID", resource_id, "already exists.")
        return
    if name == "" or category == "":
        print("Rejected: name and category cannot be empty.")
        return
    if not isinstance(total, int) or total <= 0:
        print("Rejected: total units must be a whole number greater than 0.")
        return
    resources.append({"id": resource_id, "name": name, "category": category,
                      "total": total, "available": total})
    print("Added resource", resource_id, "-", name)


def print_table(items):
    print(f"{'ID':<6} {'Name':<12} {'Category':<13} {'Total':>5} {'Available':>9}")
    for resource in items:
        print(f"{resource['id']:<6} {resource['name']:<12} {resource['category']:<13} "
              f"{resource['total']:>5} {resource['available']:>9}")


def list_resources():
    if len(resources) == 0:
        print("No resources in inventory.")
        return
    print_table(resources)


def get_loaned(fellow_id, resource_id):
    held = 0
    for record in borrow_records:
        if record["fellow"] == fellow_id and record["resource"] == resource_id:
            held = held + record["quantity"]
    return held


def borrow_resource(fellow_id, resource_id, quantity):
    fellow_id = clean_id(fellow_id)
    if fellow_id not in fellows:
        print("Rejected: fellow ID not found:", fellow_id)
        return
    resource = find_resource(resource_id)
    if resource is None:
        print("Rejected: resource ID not found:", resource_id)
        return
    if not isinstance(quantity, int) or quantity <= 0:
        print("Rejected: quantity must be a whole number greater than 0.")
        return
    if quantity > resource["available"]:
        print("Rejected: only", resource["available"], "unit(s) of", resource["name"], "available.")
        return
    resource["available"] = resource["available"] - quantity
    borrow_records.append({"fellow": fellow_id, "resource": resource["id"], "quantity": quantity})
    print("Success:", fellows[fellow_id], "borrowed", quantity, resource["name"])


def return_resource(fellow_id, resource_id, quantity):
    fellow_id = clean_id(fellow_id)
    if fellow_id not in fellows:
        print("Rejected: fellow ID not found:", fellow_id)
        return
    resource = find_resource(resource_id)
    if resource is None:
        print("Rejected: resource ID not found:", resource_id)
        return
    if not isinstance(quantity, int) or quantity <= 0:
        print("Rejected: quantity must be a whole number greater than 0.")
        return
    held = get_loaned(fellow_id, resource["id"])
    if quantity > held:
        print("Rejected:", fellows[fellow_id], "holds only", held, resource["name"], "- cannot return", quantity)
        return
    resource["available"] = resource["available"] + quantity
    borrow_records.append({"fellow": fellow_id, "resource": resource["id"], "quantity": -quantity})
    print("Success:", fellows[fellow_id], "returned", quantity, resource["name"])


def search_by_name(text):
    text = text.strip().lower()
    matches = [r for r in resources if text in r["name"].lower()]
    if len(matches) == 0:
        print("No resources found with name containing '" + text + "'.")
        return
    print_table(matches)


def filter_by_category(category):
    category = category.strip().lower()
    matches = [r for r in resources if r["category"].lower() == category]
    if len(matches) == 0:
        print("No resources found in category '" + category + "'.")
        return
    print_table(matches)


def generate_report():
    total_units = 0
    available_units = 0
    for resource in resources:
        total_units = total_units + resource["total"]
        available_units = available_units + resource["available"]
    borrowed_units = total_units - available_units

    print("===== INVENTORY REPORT =====")
    print("Total units:     ", total_units)
    print("Available units: ", available_units)
    print("Borrowed units:  ", borrowed_units)

    print("Low stock (fewer than 3 available):")
    found_low = False
    for resource in resources:
        if resource["available"] < 3:
            print("  -", resource["name"], "(" + str(resource["available"]) + ")")
            found_low = True
    if not found_low:
        print("  None")

    highest = 0
    for resource in resources:
        on_loan = resource["total"] - resource["available"]
        if on_loan > highest:
            highest = on_loan
    if highest == 0:
        print("Most borrowed: nothing is currently borrowed.")
    else:
        leaders = []
        for resource in resources:
            if resource["total"] - resource["available"] == highest:
                leaders.append(resource["name"])
        print("Most borrowed:", ", ".join(leaders), "(" + str(highest) + ")")


def show_available(resource_id):
    resource = find_resource(resource_id)
    print("   -> available", resource["name"], "units:", resource["available"])


def run_demo():
    print("\n--- Step 1: F001 borrows 2 laptops ---")
    borrow_resource("F001", "R001", 2)
    show_available("R001")
    print("\n--- Step 2: F002 borrows 3 keyboards ---")
    borrow_resource("F002", "R002", 3)
    show_available("R002")
    print("\n--- Step 3: F001 returns 1 laptop ---")
    return_resource("F001", "R001", 1)
    show_available("R001")
    print("\n--- Step 4: F003 requests 4 headsets ---")
    borrow_resource("F003", "R003", 4)
    show_available("R003")
    print("\n--- Step 5: F002 tries to return 4 keyboards ---")
    return_resource("F002", "R002", 4)
    show_available("R002")
    print("\n--- Step 6: Search for LAPtop ---")
    search_by_name("LAPtop")
    print("\n--- Step 7: Report ---")
    generate_report()
    print("\n--- Extra invalid-input test: F001 borrows -3 laptops ---")
    borrow_resource("F001", "R001", -3)
    show_available("R001")


def main():
    while True:
        print("\n===== Learn2Earn Resource Manager =====")
        print("1. Add resource")
        print("2. List resources")
        print("3. Borrow resource")
        print("4. Return resource")
        print("5. Search by name")
        print("6. Filter by category")
        print("7. Report")
        print("8. Run required demo (use on a fresh start)")
        print("9. Exit")
        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            rid = input("Resource ID: ")
            name = input("Name: ")
            category = input("Category: ")
            total = get_positive_number("Total units: ")
            add_resource(rid, name, category, total)
        elif choice == "2":
            list_resources()
        elif choice == "3":
            fid = input("Fellow ID: ")
            rid = input("Resource ID: ")
            qty = get_positive_number("Quantity: ")
            borrow_resource(fid, rid, qty)
        elif choice == "4":
            fid = input("Fellow ID: ")
            rid = input("Resource ID: ")
            qty = get_positive_number("Quantity: ")
            return_resource(fid, rid, qty)
        elif choice == "5":
            search_by_name(input("Name to search: "))
        elif choice == "6":
            filter_by_category(input("Category: "))
        elif choice == "7":
            generate_report()
        elif choice == "8":
            run_demo()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")


main()