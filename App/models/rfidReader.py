from models.rfidTag import RFIDTag

from monitors import log_function_name
class RFIDReader:

    def __init__(self, reader_id: int, zone_id: int):
        self.reader_id = reader_id
        self.location = zone_id
        self.connected = False
        self.rfid_tags = []

    @log_function_name("RFIDReader")
    def add_rfid_tag(self, tag: RFIDTag):
        self.rfid_tags.append(tag)

    @log_function_name("RFIDReader")
    def remove_rfid_tag(self, tag_id: int):
        self.rfid_tags = [tag for tag in self.rfid_tags if tag.tag_id != tag_id]

    def get_rfid_tags(self) -> list:
        return self.rfid_tags

    def connect(self):
        self.connected = True
        print(f"RFID reader {self.reader_id} connected at {self.location}")

    def disconnect(self):
        self.connected = False
        print(f"RFID reader {self.reader_id} disconnected")
        
    def get_reader_id(self):
        return self.reader_id

    def get_location(self):
        return self.location

    def is_connected(self):
        return self.connected
    
    # Iterator pattern
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.rfid_tags):
            tag = self.rfid_tags[self.index]
            self.index += 1
            return tag
        else:
            raise StopIteration
        
        