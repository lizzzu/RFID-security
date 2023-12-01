import sys
import trace

from models.item import Item
from models.zone import Zone
from models.rfidTag import RFIDTag
from models.rfidReader import RFIDReader
from models.employee import Employee, Role
from models.warehouse import Warehouse

def main():

    warehouse = Warehouse(145)

    # Create roles
    # admin_role = Role(["add_tag", "remove_tag"])
    basic_role = Role(["add_item"])

    # create employee
    employee = Employee(12,"employee1",basic_role)
    warehouse.add_employee(employee)
    warehouse.add_observer_to_all_readers(employee)

    warehouse.access_control.assign_role(employee, basic_role)

    # generate zones, items, and tags
    id = -1
    while( id != 10):

        id += 1
        zone = Zone(id,"")
        reader = RFIDReader(id, id)
        zone.add_rfid_reader(reader)

        warehouse.add_zone(zone)

        tag_id = id*10
        for _ in range(10):
            tag_id += 1
            item = Item(tag_id, f"item {id}", tag_id)
            tag = RFIDTag(tag_id)

            result = warehouse.add_item(employee, item, tag)
            if not result:
                print("Warehouse is at full capacity. Cannot add more items.")

            result = warehouse.add_tag_to_zone(id, tag)
            assert result, f"Zone {id} does not exist"

    # add tag in zone 2 - employee is notified
    zone = 2
    tag333 = RFIDTag(333)
    result = warehouse.add_tag_to_zone(zone, tag333)
    assert result, f"Zone {zone} does not exist"

    # find tag in warehouse
    target_tag_id = 333
    result = warehouse.find_tag_in_warehouse(target_tag_id)
    assert result, f"Tag {target_tag_id} does not exist"

    # print zone and their tags
    for zone in warehouse:
        print(f"Zone: {zone.get_zone_id()}")

        zone_tags = zone.get_items()
        print(f"  Tags in the zone: {[tag.tag_id for tag in zone_tags]}")

    # find item in warehouse
    tag_id_to_search = 22
    result = warehouse.find_item_location(tag_id_to_search)
    assert result != -1, f"Tag {tag_id_to_search} does not exist"
    print(f"\nTag location: {result}")

    # get item info
    item = 22
    result = warehouse.get_item_info_by_id(item)
    assert result, f"Item {item} does not exist"
    print(f"Item info: {result}")

    # get item location(zone id)
    result = warehouse.find_zone_location_of_item(item)
    assert result != -1, f"Item {item} does not exist"
    print(f"Tag location: {result}\n")

    # move item from one zone to another
    tag_id_to_search = 61
    tag = warehouse.get_tag_by_id(tag_id_to_search)
    assert tag, f"Tag {tag_id_to_search} does not exist"
    warehouse.move_item(tag, 6, 1)

    print(warehouse.get_tags_id_from_zone(1))
    print(warehouse.get_tags_id_from_zone(6))

    # find item in warehouse
    item = 100
    result = warehouse.find_item_location(item)
    assert result != -1, f"Item {item} does not exist"
    print(f"\nFind item {item}: zone {result}")

if __name__ == "__main__":
    tracer = trace.Trace(trace=False, ignoredirs=[sys.prefix, sys.exec_prefix])
    tracer.run('main()')
    
    r = tracer.results()
    r.write_results(show_missing=True, coverdir="./tema6")
