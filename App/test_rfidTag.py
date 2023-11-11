from models.rfidTag import RFIDTag

rfid_tag = RFIDTag(tag_id="12345", location=1, status="Active")
print(rfid_tag, "\n")

rfid_tag.update_location(2)
print(rfid_tag, "\n")

rfid_tag.deactivate_tag()
print(rfid_tag, "\n")

rfid_tag.activate_tag()
print(rfid_tag, "\n")

print("RFID Tag location: ",rfid_tag.get_location())
