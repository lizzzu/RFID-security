
class RFIDTag:

    def __init__(self, tag_id: int, status="Active"):
        self.tag_id = tag_id
        #self.location = location
        self.status = status

    def get_tag_id(self):
        return self.tag_id

    def get_status(self):
        return self.status

    def deactivate_tag(self):
        self.status = "Inactive"

    def activate_tag(self):
        self.status = "Active"

    def __str__(self):
        return f"RFIDTag(ID: {self.tag_id}, Status: {self.status})"
    
    def serialize(self):
        return {
            "id": self.tag_id,
            "status": self.status
        }
    
    @staticmethod
    def deserialize(tag):
        return RFIDTag(
            tag["id"],
            tag["status"]
        )
