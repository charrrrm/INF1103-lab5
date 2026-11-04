from abc import ABC, abstractmethod
import json
import os

class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)

    def get_product_id(self): return self.__product_id
    def get_name(self): return self.__name
    def get_price(self): return self.__price
    def get_stock(self): return self.__stock

    def update_stock(self, quantity):
        self.__stock += quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}", end="")

    @abstractmethod
    def get_fulfilment_info(self):
        pass


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)

    def get_weight(self): return self.__weight

    def display_information(self):
        super().display_information()
        shipping = self.calculate_shipping_cost()
        print(f" | Weight: {self.__weight}kg | Shipping Cost: ${shipping:.2f} | {self.get_fulfilment_info()}")

    def get_fulfilment_info(self):
        return "Requires physical shipping."

    def calculate_shipping_cost(self):
        return 5.00 + (self.__weight * 2.00)


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = float(download_size)

    def get_download_size(self): return self.__download_size

    def display_information(self):
        super().display_information()
        print(f" | Download Size: {self.__download_size}MB | {self.get_fulfilment_info()}")

    def get_fulfilment_info(self):
        return "Delivered digitally via download link."


class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def search_product(self, product_id):
        for p in self.products:
            if p.get_product_id() == product_id:
                return p
        return None

    def display_all(self):
        if not self.products:
            print("No products in inventory.")
        for p in self.products:
            p.display_information()

    def load_inventory(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                for item in data:
                    ptype = item.get("type")
                    if ptype == "physical":
                        product = PhysicalProduct(
                            item['product_id'], item['name'], item['price'], item['stock'], item['weight']
                        )
                    elif ptype == "digital":
                        product = DigitalProduct(
                            item['product_id'], item['name'], item['price'], item['stock'], item['download_size']
                        )
                    else:
                        continue
                    self.add_product(product)
        else:
            print("No existing inventory found. Starting fresh.")

    def save_inventory(self, filename):
        data = []
        for p in self.products:
            p_dict = {
                "product_id": p.get_product_id(),
                "name": p.get_name(),
                "price": p.get_price(),
                "stock": p.get_stock()
            }
            if isinstance(p, PhysicalProduct):
                p_dict["type"] = "physical"
                p_dict["weight"] = p.get_weight()
            elif isinstance(p, DigitalProduct):
                p_dict["type"] = "digital"
                p_dict["download_size"] = p.get_download_size()
            data.append(p_dict)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


def main():
    inventory = Inventory()
    inventory.load_inventory('inventory.json')

    while True:
        print("\n--- Inventory Menu ---")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            inventory.display_all()
        elif choice == '2':
            print("\nSelect Product Type:")
            print("1. Physical Product")
            print("2. Digital Product")
            ptype_choice = input("Enter type choice: ")

            pid = input("Enter product ID: ")
            name = input("Enter name: ")
            price = float(input("Enter price: "))
            stock = int(input("Enter stock: "))

            if ptype_choice == '1':
                weight = float(input("Enter weight (kg): "))
                new_product = PhysicalProduct(pid, name, price, stock, weight)
                inventory.add_product(new_product)
                print("Physical product added successfully.")
            elif ptype_choice == '2':
                dsize = float(input("Enter download size (MB): "))
                new_product = DigitalProduct(pid, name, price, stock, dsize)
                inventory.add_product(new_product)
                print("Digital product added successfully.")
            else:
                print("Invalid product type. Product creation cancelled.")
        elif choice == '3':
            pid = input("Enter product ID to update: ")
            product = inventory.search_product(pid)
            if product:
                qty = int(input("Enter quantity to add (use negative to remove): "))
                product.update_stock(qty)
                print("Stock updated successfully.")
            else:
                print("Product not found.")
        elif choice == '4':
            pid = input("Enter product ID to search: ")
            product = inventory.search_product(pid)
            if product:
                product.display_information()
            else:
                print("Product not found.")
        elif choice == '5':
            inventory.save_inventory('inventory.json')
            print("Inventory saved to file.")
        elif choice == '6':
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()