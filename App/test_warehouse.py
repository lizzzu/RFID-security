from models.zone import Zone
from models.item import Item
from models.warehouse import Warehouse

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

