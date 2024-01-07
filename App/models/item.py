
class Item:

    def __init__(self, item_id: int, name: str, rfid_tag_id: int):
        self.item_id = item_id
        self.rfid_tag_id = rfid_tag_id
        #self.zone_id = 0
        self.name = name

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
    
    def get_name(self):
        return self.name
    
    def get_rfid_tag_id(self):
        return self.rfid_tag_id
    
    def __str__(self):
        """Return a string representation of the item."""
        return f"Item ID: {self.item_id}, Name: {self.name} RFID Tag ID: {self.rfid_tag_id}"

    def serialize(self):
        return {
            "id": self.item_id,
            "name": self.name,
            "tag_id": self.rfid_tag_id
        }
    
    @staticmethod
    def deserialize(item):
        return Item(
            item["id"],
            item["name"],
            item["tag_id"]
        )
