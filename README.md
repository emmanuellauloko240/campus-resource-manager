<!-- resources = [
  {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
  {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
  {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3}
]
fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
borrow_records = []

def get_positive_number(prompt):
    while True:
        try:
            typed = int(input(prompt))
            if typed > 0:
                return typed
            print("Number must be greater than 0.")
        except ValueError:
            print("Please enter a whole number, for example 5.")

def borrow_resource(fellow_id, resource_id,quantity):
    if fellow_id not in fellows:
        print("error.....")
        return
    resource = find_resource(resource_id)
        
    if resource is None:
        
        print("error....")
        return
    if quantity > resource["available"]:
        print("error.")
        return
    resource["available"] = resource["available"] - quantity
    borrow_records.append({"fellow":fellow_id,"resource":resource_id,"quantity":quantity})
    print("success..")

def get_loaned(fellow_id, resource_id):
    held = 0
    for record in borrow_records:
        if record["fellow"] == fellow_id and record["resource"] == resource_id:
            held = held + record["quantity"]
    return held

def borrow_resource(fellow_id, resource_id, quantity):
    fellow_id = fellow_id.strip().upper()
    if fellow_id not in fellows:
        print("Fellow ID not found:", fellow_id)
        return
    resource = find_resource(resource_id)
    if resource is None:
        print("Resource ID not found:", resource_id)
        return
    if quantity > get_loaned(fellow_id, resource["id"]):
        print("Rejected: you can only return what you currently hold.")
        return
    resource["available"] = resource["available"] + quantity
    borrow_records.append({"fellow": fellow_id, "resource": resource["id"], "quantity": -quantity})
    print("Return successful.")
def list_resources():
    for resource in resources:
        print(resource["id"],resource["name"],resource["category"],resource["total"],resource["available"])
def find_resource(looking_for):
    looking_for = (looking_for.strip().upper())
    for resource in resources:
        if resource["id"] == looking_for:
            return resource
    return None
borrow_resource("F001", "R001", 2)
print("Step 1: F001 borrows 2 laptops")
borrow_resource("F001", "R001", 2)
print(find_resource("R001"))

print("Step 2: F002 borrows 3 keyboards")
borrow_resource("F002", "R002", 3)
print(find_resource("R002"))

print("Step 3: F001 returns 1 laptop")
return_resource("F001", "R001", 1)
print(find_resource("R001"))

print("Step 4: F003 requests 4 headsets")
borrow_resource("F003", "R003", 4)
print(find_resource("R003"))

print("Step 5: F002 tries to return 4 keyboards")
return_resource("F002", "R002", 4)
print(find_resource("R002")) -->