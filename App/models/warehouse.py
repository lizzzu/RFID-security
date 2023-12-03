from models.item import Item
from models.zone import Zone
from models.rfidTag import RFIDTag
from models.employee import Employee
from security import AccessControl, check_access_control

from monitors import validate_tag, log_function_name
class Warehouse:

    _instance = None

    def __new__(cls, capacity: int):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.items = []
            cls._instance.rfid_tags = []
            cls._instance.zones = []
            cls._instance.employee = []
            cls._instance.capacity = capacity
            cls.access_control = AccessControl()
        return cls._instance

    def get_capacity(self):
        return self.capacity

    def get_zones(self):
        return self.zones

    def get_items(self):
        return self.items

    def get_rfid_tags(self):
        return self.rfid_tags

    @log_function_name("Warehouse")
    def get_tags_id_from_zone(self, zone_id: int):
        try:
            for zone in self.zones:
                if zone.id == zone_id:
                    elements = [tag.tag_id for tag in zone.rfid_reader.rfid_tags]
                    return elements
        except IndexError:
            return []

    @log_function_name("Warehouse")
    def get_tag_by_id(self, tag_id: int) -> RFIDTag:
        for tag in self.rfid_tags:
            if tag.tag_id == tag_id:
                return tag
        return None

    @log_function_name("Warehouse")
    def get_item_info_by_id(self, item_tag_id: int) -> Item:
        for item in self.items:
            if item.rfid_tag_id == item_tag_id:
                return item
        return None

    @check_access_control("add_item")
    @validate_tag
    def add_item(self, employee: Employee, item: Item, tag: RFIDTag) -> bool:
        if len(self.items) < self.capacity:
            self.items.append(item)
            self.rfid_tags.append(tag)
            return True
        return False

    @log_function_name("Warehouse")
    def remove_item(self, item_id: int) -> bool:
        for item in self.items:
            if item.item_id == item_id:
                tag_id = item.get_rfid_tag_id()
                self.items.remove(item)
                for tag in self.rfid_tags:
                    if tag.tag_id == tag_id:
                        self.items.remove(tag)
                return True
        return False

    @log_function_name("Warehouse")
    def add_zone(self, zone: Zone):
        self.zones.append(zone)

    @log_function_name("Warehouse")
    def remove_zone(self, zone_id: int) -> bool:
        for zone in self.zones:
            if zone.id == zone_id:
                self.zones.remove(zone)
                return True
        return False

    @log_function_name("Warehouse")
    def add_employee(self, employee: Employee):
        self.employee.append(employee)

    @log_function_name("Warehouse")
    def remove_employee(self, employee_id: int) -> bool:
        for employee in self.employee:
            if employee.employee_id == employee_id:
                self.employee.remove(employee)
                return True
        return False

    @log_function_name("Warehouse")
    def add_tag_to_zone(self, zone_id: int, tag: RFIDTag) -> bool:
        for zone in self.zones:
            if zone.id == zone_id:
                zone_index = self.zones.index(zone)
                self.zones[zone_index].add_rfid_tag(tag)
                return True
        return False

    @log_function_name("Warehouse")
    def remove_tag_from_zone(self, zone_id: int, tag_id: int) -> bool:
        for zone in self.zones:
            if zone.id == zone_id:
                zone_index = self.zones.index(zone)
                self.zones[zone_index].remove_rfid_tag(tag_id)
                return True
        return False

    @log_function_name("Warehouse")
    def move_item(self, tag: RFIDTag, zoneFrom_id: int, zoneTo_id: int):
        self.remove_tag_from_zone(zoneFrom_id, tag.tag_id)
        self.add_tag_to_zone(zoneTo_id, tag)

    @log_function_name("Warehouse")
    def find_tag_in_warehouse(self, target_tag_id: int ) -> bool:
        for zone in self.zones:
            if zone.is_tag_in_zone(target_tag_id):
                return True
        return False

    @log_function_name("Warehouse")
    def find_item_location(self, item_tag_id: int) -> int:
        for zone in self.zones:
            for tag in zone.rfid_reader.rfid_tags:
                if tag.tag_id == item_tag_id:
                    return zone.get_zone_id()
        return -1

    @log_function_name("Warehouse")
    def find_zone_location_of_item(self, item_tag_id: int) -> int:
        for _, zone in enumerate(self.zones):
            for tag in zone.rfid_reader.rfid_tags:
                if tag.tag_id == item_tag_id:
                    return zone.id
        return -1

    # Iterator pattern
    def __iter__(self):
        return iter(self.zones)

    # Observer design
    @log_function_name("Warehouse")
    def add_observer_to_all_readers(self, observer: Employee):
        for zone in self.zones:
            zone.add_observer(observer)

    @log_function_name("Warehouse")
    def remove_observer_from_zones(self, observer: Employee):
        for zone in self.zones:
            zone.remove_observer(observer)
