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


class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)

    def get_weight(self): return self.__weight

    def display_information(self):
        super().display_information()
        print(f" | Weight: {self.__weight}kg | Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self):
        return "Requires physical shipping."


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = float(download_size)

    def get_download_size(self): return self.__download_size

    def display_information(self):
        super().display_information()
        print(f" | Download Size: {self.__download_size}MB | Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self):
        return "Delivered digitally via download link."
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
        print(f" | Weight: {self.__weight}kg | Shipping Cost: ${shipping:.2f} | Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self):
        return "Requires physical shipping."

    def calculate_shipping_cost(self):
        # Example rule: Base $5.00 + $2.00 per kg
        return 5.00 + (self.__weight * 2.00)       