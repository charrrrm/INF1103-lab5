import json
import os

class Product:
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
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")
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
                    product = Product(item['product_id'], item['name'], item['price'], item['stock'])
                    self.add_product(product)
        else:
            print("No existing inventory found. Starting fresh.")

    def save_inventory(self, filename):
        data = []
        for p in self.products:
            data.append({
                "product_id": p.get_product_id(),
                "name": p.get_name(),
                "price": p.get_price(),
                "stock": p.get_stock()
            })
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)