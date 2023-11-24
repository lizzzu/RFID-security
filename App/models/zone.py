from models.rfidTag import RFIDTag
from models.rfidReader import RFIDReader
from models.employee import Observer

class Zone:

    def __init__(self, id: int, name: str):
        self.name = name
        self.id = id
        self.observers = []
        #self.capacity = capacity
        #self.rfid_reader = RFIDReader

    def add_rfid_reader(self, reader: RFIDReader):
        self.rfid_reader = reader

    def add_rfid_tag(self, tag: RFIDTag):
        self.rfid_reader.add_rfid_tag(tag)
        self.notify_observers(tag.tag_id, f"added in zone with id = {self.id}")

    def remove_rfid_tag(self, tag_id: int):
        self.rfid_reader.remove_rfid_tag(tag_id)
        self.notify_observers(tag_id, f"removed from zone with id = {self.id}")

    def get_rfid_tags(self):
        return self.rfid_reader.get_rfid_tags()

    def get_items(self):
        return list(self.rfid_reader)
    
    def is_tag_in_zone(self, target_tag_id: int):
        for tag in self.rfid_reader:
            if tag.tag_id == target_tag_id:
                return True
        return False
    
    def get_zone_id(self):
        return self.id

    def __str__(self):
        return f"name = {self.name}\nid = {self.id}"
    
    # Iterator pattern
    def __iter__(self):
        return iter(self.rfid_reader)

    # Observer design 
    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, tag_id, action):
        for observer in self.observers:
            observer.update(tag_id, action)