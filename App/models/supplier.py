
class Supplier:

    def __init__(self, supplier_id, name):
        self.supplier_id = supplier_id
        self.name = name
        self.products = []  # Assuming suppliers provide products to the warehouse

    def add_product(self, product):
        self.products.append(product)

    def display_supplier_details(self):
        print(f"Supplier ID: {self.supplier_id}")
        print(f"Name: {self.name}")
        print("Products Provided:")
        for product in self.products:
            print(f"  - {product.name}")
    
    