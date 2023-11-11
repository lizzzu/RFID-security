from models.rfidReader import RFIDReader
from models.rfidTag import RFIDTag

reader1 = RFIDReader(reader_id="R1", location="Warehouse Entrance")
reader1.connect()

print("Reader ID:", reader1.get_reader_id())
print("Location:", reader1.get_location())
print("Connected:", reader1.is_connected(), "\n")

tag1 = RFIDTag(1,1)
reader1.read_rfid_tag(tag1)