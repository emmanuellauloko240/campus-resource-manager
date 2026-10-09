# Learn2Earn Resource Manager

A command-line Python program for Learn2Earn that tracks equipment inventory, lends items to fellows, accepts returns, searches inventory and produces reports. It uses only the Python standard library.

## Requirements

- Python 3.8 or newer
- No third-party packages, frameworks, databases or external services

## How to run

```
python3 main.py
```

The program shows a menu and keeps looping until you choose option 9 (Exit).

## Menu options

| Option | What it does |
|---|---|
| 1 | Add a resource (rejects duplicate IDs and invalid input) |
| 2 | List all resources in a table |
| 3 | Borrow a resource (fellow ID, resource ID, quantity) |
| 4 | Return a resource (only what the fellow currently holds) |
| 5 | Search resources by name (case-insensitive, partial match) |
| 6 | Filter resources by category (case-insensitive) |
| 7 | Report: totals, low stock, most borrowed |
| 8 | Run the required demonstration (use on a fresh start) |
| 9 | Exit |

## Starting data

- Resources: R001 Laptop (10), R002 Keyboard (5), R003 Headset (3)
- Fellows: F001 Ada, F002 John, F003 Grace
- Loan log (`borrow_records`): starts empty

## How the data is represented

- **Inventory:** a list of dictionaries with the keys `id`, `name`, `category`, `total` and `available`.
- **Fellows:** a dictionary mapping fellow ID to name.
- **Loans:** a log list called `borrow_records`. Each entry holds `fellow`, `resource` and `quantity`. A borrow adds a positive quantity and a return adds a negative one, so the units a fellow currently holds for a resource is the sum of their entries.

## Key functions

- `find_resource` : cleans an ID (strips spaces, uppercases) and returns the matching resource or `None`
- `get_positive_number` : keeps asking until the user enters a whole number greater than 0
- `add_resource` : validates input and rejects duplicate IDs
- `borrow_resource` : validates everything first, then reduces availability and logs the loan
- `return_resource` : rejects any quantity above what the fellow holds, then restores stock and logs the return
- `get_loaned` : sums the log for one fellow and one resource
- `search_by_name` / `filter_by_category` : case-insensitive lookups
- `generate_report` : total, available and borrowed units, low stock (fewer than 3 available), and the most borrowed resource including ties
- `run_demo` : runs the required demonstration steps 1 to 7 plus one invalid-input test
- `main` : the menu loop

## Design rule

Every borrow and return validates all inputs before changing anything, so a rejected request never changes stock or the loan log.

## Required demonstration

Choose option 8 on a fresh start. Expected results:

1. F001 borrows 2 laptops: Laptop available 8
2. F002 borrows 3 keyboards: Keyboard available 2
3. F001 returns 1 laptop: Laptop available 9
4. F003 requests 4 headsets: rejected, stock stays 3
5. F002 tries to return 4 keyboards: rejected, stock stays 2
6. Search for `LAPtop`: finds Laptop
7. Report: total 18, available 14, borrowed 4, Keyboard low stock (2), Keyboard most borrowed (3)

Extra invalid-input test: F001 borrows -3 laptops, which is rejected with stock unchanged.

## Known limitations

- Data is held in memory and lost when the program closes. The optional JSON save and reload bonus is not implemented.
- Holdings are recalculated by scanning the whole loan log each time.
- The demo option does not reset data, so run it once per fresh start. Running it again gives different numbers.
- Fellows cannot be added from the menu.