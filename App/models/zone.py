
class Zone:

    def __init__(self, id, name, capacity):
        self.name = name
        self.id = id
        self.capacity = capacity
        self.itemList = []

    def add_item(self, item):
        if len(self.itemList) < self.capacity:
            self.itemList.append(item)
            print(f"Item id = {item.item_id} added to Zone {self.id}")
        else:
            print(f"Zone {self.id} is at full capacity. Cannot add more items.")

    def remove_item(self, item):
        if item in self.itemList:
            self.itemList.remove(item)
            print(f"Item id = {item.item_id} removed from Zone {self.id}")
        else:
            print(f"Item {item} not found in Zone {self.id}")
    
    def get_number_of_items(self):
        return len(self.itemList)

    def is_full(self):
        return len(self.itemList) == self.capacity
    
    def get_items(self):
        return self.itemList

    def get_capacity(self):
        return self.capacity
    
    def get_zone_id(self):
        return self.id

    def __str__(self):
        return f"name = {self.name}\nid = {self.id}\ncapacity = {self.capacity}"
