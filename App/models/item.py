
class Item:

    def __init__(self, item_id, name, rfid_tag_id):
        self.item_id = item_id
        self.rfid_tag_id = rfid_tag_id
        self.zone_id = 0
        self.name = name

    def update_zone_id(self, zone_id):
        self.zone_id = zone_id

    def get_item_details(self):
        details = {
            'Item ID': self.item_id,
            'Name': self.name,
            'RFID Tag': self.rfid_tag_id,
            'Zone ID': self.zone_id
        }
        return details
    
    def get_item_id(self):
        return self.item_id
    
    def get_zone_id(self):
        return self.zone_id
    
    def get_name(self):
        return self.name
    
    def get_rfid_tag_id(self):
        return self.rfid_tag_id
    
    def __str__(self):
        """Return a string representation of the item."""
        return f"Item ID: {self.item_id}, Name: {self.name}, Zone ID: {self.zone_id}, RFID Tag ID: {self.rfid_tag_id}"
