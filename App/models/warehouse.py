
class Warehouse:

    def __init__(self, capacity):
        self.capacity = capacity
        self.zones = []  
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            print(f"Item {item.item_id} added to Warehouse")
        else:
            print(f"Warehouse is at full capacity. Cannot add more items.")

    def remove_item(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                self.items.remove(item)
                print(f"Item {item_id} removed from Warehouse")
                return
        print(f"Item {item_id} not found in Warehouse")

    def add_zone(self, zone):
        self.zones.append(zone)
        print(f"Zone {zone.id} added to Warehouse")

    def remove_zone(self, zone_id):
        for zone in self.zones:
            if zone.id == zone_id:
                self.zones.remove(zone)
                print(f"Zone {zone_id} removed from Warehouse")
                return
        print("No zone with id = ", zone_id, "found in warehouse")

    def get_capacity(self):
        return self.capacity

    def get_zones(self):
        return self.zones
    
    def get_items(self):
        return self.items
    
