from models.item import Item
from models.zone import Zone
from models.rfidTag import RFIDTag
from models.employee import Employee
from security import AccessControl, check_access_control

from monitors import validate_tag, print_function_name_before_execution, print_function_name_after_execution
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
    
    def get_employee(self):
        return self.employee

    def get_zones(self):
        return self.zones

    def get_items(self):
        return self.items

    def get_rfid_tags(self):
        return self.rfid_tags

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    def get_tags_id_from_zone(self, zone_id: int):
        try:
            for zone in self.zones:
                if zone.id == zone_id:
                    elements = [tag.tag_id for tag in zone.rfid_reader.rfid_tags]
                    return elements
            return []
        except:
            return []

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    def get_tag_by_id(self, tag_id: int) -> RFIDTag:
        for tag in self.rfid_tags:
            if tag.tag_id == tag_id:
                return tag
        return None

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    def get_item_info_by_id(self, item_tag_id: int) -> Item:
        for item in self.items:
            if item.rfid_tag_id == item_tag_id:
                return item
        return None

    @check_access_control("add_item")
    @validate_tag
    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    def add_item(self, employee: Employee, item: Item, tag: RFIDTag) -> bool:
        if len(self.items) < self.capacity:
            self.items.append(item)
            self.rfid_tags.append(tag)
            return True
        return False

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    @check_access_control("remove_item")
    def remove_item(self, employee: Employee, item_id: int) -> bool:
        for item in self.items:
            if item.item_id == item_id:
                tag_id = item.get_rfid_tag_id()
                self.items.remove(item)
                for tag in self.rfid_tags:
                    if tag.tag_id == tag_id:
                        self.rfid_tags.remove(tag)
                return True
        return False

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    @check_access_control("add_zone")
    def add_zone(self, employee: Employee, zone: Zone):
        self.zones.append(zone)

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    @check_access_control("remove_zone")
    def remove_zone(self, employee: Employee, zone_id: int) -> bool:
        for zone in self.zones:
            if zone.id == zone_id:
                self.zones.remove(zone)
                return True
        return False

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    #@check_access_control("add_employee")
    def add_employee(self, employee: Employee):
        self.employee.append(employee)

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    @check_access_control("remove_employee")
    def remove_employee(self, employee: Employee, employee_id: int) -> bool:
        for employee in self.employee:
            if employee.employee_id == employee_id:
                self.employee.remove(employee)
                return True
        return False

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    def add_tag_to_zone(self, zone_id: int, tag: RFIDTag) -> bool:
        for zone in self.zones:
            if zone.id == zone_id:
                zone_index = self.zones.index(zone)
                self.zones[zone_index].add_rfid_tag(tag)
                return True
        return False

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    def remove_tag_from_zone(self, zone_id: int, tag_id: int) -> bool:
        for zone in self.zones:
            if zone.id == zone_id:
                zone_index = self.zones.index(zone)
                self.zones[zone_index].remove_rfid_tag(tag_id)
                return True
        return False

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    def move_item(self, tag: RFIDTag, zoneFrom_id: int, zoneTo_id: int):
        self.remove_tag_from_zone(zoneFrom_id, tag.tag_id)
        self.add_tag_to_zone(zoneTo_id, tag)

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    def find_tag_in_warehouse(self, target_tag_id: int ) -> bool:
        for zone in self.zones:
            if zone.is_tag_in_zone(target_tag_id):
                return True
        return False

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    def find_item_location(self, item_tag_id: int) -> int:
        for zone in self.zones:
            for tag in zone.rfid_reader.rfid_tags:
                if tag.tag_id == item_tag_id:
                    return zone.get_zone_id()
        return -1

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
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
    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    def add_observer_to_all_readers(self, observer: Employee):
        for zone in self.zones:
            zone.add_observer(observer)

    @print_function_name_before_execution("Warehouse")
    @print_function_name_after_execution("Warehouse")
    def remove_observer_from_zones(self, observer: Employee):
        for zone in self.zones:
            zone.remove_observer(observer)
