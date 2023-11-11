
class RFIDReader:

    def __init__(self, reader_id, location):
        self.reader_id = reader_id
        self.location = location
        self.connected = False

    def connect(self):
        self.connected = True
        print(f"RFID reader {self.reader_id} connected at {self.location}")

    def disconnect(self):
        self.connected = False
        print(f"RFID reader {self.reader_id} disconnected")

    def read_rfid_tag(self, tag):
        if self.connected:
            print(f"RFID tag {tag.get_tag_id()} read by reader {self.reader_id} is at the location: {tag.get_location()}")
            return tag
        else:
            print("Error: RFID reader not connected.")
            return None
        
    def get_reader_id(self):
        return self.reader_id

    def get_location(self):
        return self.location

    def is_connected(self):
        return self.connected
        