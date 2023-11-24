from models.zone import Zone
from models.item import Item
from models.warehouse import Warehouse

import unittest

class TestWarehouseSingleton(unittest.TestCase):

    def test_singleton_instance(self):
        warehouse1 = Warehouse(234)
        warehouse2 = Warehouse(234)

        self.assertIs(warehouse1, warehouse2, "Instances are not the same")

    def test_add_item(self):
        warehouse = Warehouse(234)
        warehouse.add_item(Item(1,"name1",1))

        inventory = warehouse.get_items()
        self.assertEqual(inventory[0].item_id, 1, "Item not added to inventory")

    def test_singleton_inventory(self):
        warehouse1 = Warehouse(234)
        warehouse2 = Warehouse(234)

        warehouse1.add_item(Item(1,"name1",1))

        inventory2 = warehouse2.get_items()
        self.assertEqual(inventory2[0].item_id, 1, "Inventory not shared between instances")


if __name__ == '__main__':
    unittest.main()

"""
warehouse = Warehouse(456)

zoneA = Zone(1,"name1",13)
zoneB = Zone(2,"name2",56)

warehouse.add_zone(zoneA)
warehouse.add_zone(zoneB)
print(warehouse.get_zones(),"\n")

warehouse.remove_zone(2)
warehouse.remove_zone(5)
print(warehouse.get_zones(),"\n")

warehouse.add_item(Item(1,"name1",1))
print(warehouse.get_items(),"\n")

warehouse.remove_item(1)
warehouse.remove_item(10)
print(warehouse.get_items())
"""
