from models.item import Item

test = Item(123,"name",2443)

print(test.zone_id)
test.update_zone_id(78)
print(test.zone_id , "\n")

print("rfid_tag_id: ", test.rfid_tag_id)
print("name: ", test.name)
print("item_id: ", test.item_id, "\n")
print(test.get_item_details())