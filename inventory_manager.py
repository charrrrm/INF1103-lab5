
inventory = [
    {"id": "P001", "name": "Laptop", "price": 1200.0, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.5, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.0, "stock": 25}
]

def search_product(inventory, product_id):
    """Searches for a product by ID and returns it, or None if not found."""
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None

def add_product(inventory, product_id, name, price, stock):
    """Adds a new product after checking for duplicates."""
    if search_product(inventory, product_id) is not None:
        return False 
    
    new_product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }
    inventory.append(new_product)
    return True