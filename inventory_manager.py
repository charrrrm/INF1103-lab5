import json
import os

# Global Constant
INVENTORY_FILE = "inventory.json"


# Persistence Functions (No UI/Printing)


def load_inventory():
    """Loads inventory from the JSON file if it exists."""
    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, "r") as file:
                inventory = json.load(file)
            return inventory, True
        except Exception:
            return [], False
    return [], False

def save_inventory(inventory):
    """Saves the current inventory to the JSON file."""
    try:
        with open(INVENTORY_FILE, "w") as file:
            json.dump(inventory, file, indent=4)
        return True
    except Exception:
        return False


# Data Functions (No UI/Printing)


def search_product(inventory, product_id):
    """Searches for a product by ID and returns it, or None if not found."""
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None

def add_product(inventory, product_id, name, price, stock):
    """Adds a new product after checking for duplicates."""
    if search_product(inventory, product_id) is not None:
        return False # Product already exists
    
    new_product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }
    inventory.append(new_product)
    return True

def update_stock(inventory, product_id, new_stock):
    """Updates the stock of an existing product."""
    product = search_product(inventory, product_id)
    if product:
        product["stock"] = new_stock
        return True
    return False


# UI & Orchestration Functions


def display_all(inventory):
    """Prints all inventory items."""
    print("\nCurrent Inventory")
    print("-" * 48)
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)

def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")
    
    inventory, status = load_inventory()
    
    if status:
        print("\ninventory.json found.")
        print("Inventory loaded successfully.")
    else:
        # Load default 3 products if file doesn't exist
        print("\ninventory.json not found. Loading default products.")
        inventory = [
            {"id": "P001", "name": "Laptop", "price": 1200.0, "stock": 15},
            {"id": "P002", "name": "Mouse", "price": 25.5, "stock": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.0, "stock": 25}
        ]

    exit_program = False
    while not exit_program:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")
        
        choice = input("Enter option: ")
        
        if choice == '1':
            display_all(inventory)
            
        elif choice == '2':
            print("\nAdd New Product")
            pid = input("Product ID: ")
            name = input("Product Name: ")
            price = float(input("Price: "))
            stock = int(input("Stock Quantity: "))
            
            if add_product(inventory, pid, name, price, stock):
                print("Product added successfully!")
            else:
                print("Error: Product ID already exists.")
                
        elif choice == '3':
            print("\nUpdate Stock")
            pid = input("Enter Product ID: ")
            product = search_product(inventory, pid)
            
            if product:
                print("Product Found:")
                print(f"Name: {product['name']}")
                print(f"Current Stock: {product['stock']}")
                new_stock = int(input("New Stock Quantity: "))
                update_stock(inventory, pid, new_stock)
                print("Stock updated successfully!")
            else:
                print("Product not found.")
                
        elif choice == '4':
            print("\nSearch Product")
            pid = input("Enter Product ID: ")
            product = search_product(inventory, pid)
            
            if product:
                print("Product Found")
                print("-" * 48)
                print(f"ID: {product['id']}")
                print(f"Name: {product['name']}")
                print(f"Price: ${product['price']:.2f}")
                print(f"Stock: {product['stock']}")
                print("-" * 48)
            else:
                print("Product not found.")
                
        elif choice == '5':
            print("\nSaving inventory...")
            if save_inventory(inventory):
                print("Inventory saved successfully to inventory.json.")
            else:
                print("Error saving inventory.")
                
        elif choice == '6':
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            exit_program = True
            
        else:
            print("\nInvalid option. Please try again.")

if __name__ == "__main__":
    main()