from models.supplier import Supplier
from models.item import Item

supplier1 = Supplier(supplier_id="S123", name="ABC Electronics")

# Adding products to the supplier
supplier1.add_product(Item(1,"name1",1))
supplier1.add_product(Item(12,"name12",12))
supplier1.add_product(Item(13,"name13",13))

# Displaying supplier details
supplier1.display_supplier_details()