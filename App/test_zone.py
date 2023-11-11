from models.zone import Zone
from models.item import Item

zone1 = Zone(1,"zone1",123)
item1 = Item(123,"name10",12)
item2 = Item(124,"name2",23)

zone1.add_item(item1)
zone1.add_item(item2)
print(zone1.get_items(), "\n")

print(zone1.get_number_of_items(),"\n")

zone1.remove_item("RFID-123")
zone1.remove_item(item2)
print(zone1.get_items(), "\n")

current_items = zone1.get_items()
print("First item's name: ",current_items[0].name)
print(f"Items in Zone {zone1.id}: {current_items}", "\n")

print(f"Is Zone {zone1.id} full? {zone1.is_full()}")