import sys
import json
import time
import trace
import threading

from models.item import Item
from models.zone import Zone
from models.rfidTag import RFIDTag
from models.rfidReader import RFIDReader
from models.employee import Employee, Role
from models.warehouse import Warehouse

def add_to_json(data, data_key, key, value, data_to_add):
    index, _ = next(((i, d) for i, d in enumerate(data[data_key]) if d.get(key) == value), (None, None))
    if index is None:
        data[data_key] += [data_to_add]
        return len(data[data_key]) - 1

    data[data_key][index] = data_to_add
    return index

def create_database():
    global warehouse, admin

    try:
        with open(db, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {
            "capacity": -1,
            "employees": [],
            "zones": [],
            "items": [],
            "tags": []
        }

    capacity = 230
    warehouse = Warehouse(capacity)
    data["capacity"] = capacity

    # create roles
    admin_role = Role(["add_item","remove_item",
                       "add_zone","remove_zone",
                       "add_employee","remove_employee"])

    employee_role = Role(["add_item","remove_item"])

    # create employees
    id = 12
    admin = Employee(id, "admin", admin_role)
    warehouse.add_employee(admin)
    warehouse.access_control.assign_role(admin, admin_role)
    add_to_json(data, "employees", "id", id, admin.serialize())

    id = 41
    employee = Employee(id, "employee1", employee_role)
    warehouse.add_employee(employee)
    warehouse.access_control.assign_role(employee, employee_role)
    add_to_json(data, "employees", "id", id, employee.serialize())

    # generate zones, items, and tags
    id = -1
    while( id != 10):

        id += 1
        zone = Zone(id, "")
        reader = RFIDReader(id, id)
        zone.add_rfid_reader(reader)

        warehouse.add_zone(admin,zone)
        index = add_to_json(data, "zones", "id", id, zone.serialize())

        item_id = id*10
        for _ in range(10):
            item_id += 1
            tag_id = item_id
            item = Item(item_id, f"item {item_id}", tag_id)
            tag = RFIDTag(tag_id)

            result = warehouse.add_item(admin, item, tag)
            if not result:
                print("Warehouse is at full capacity. Cannot add more items.")

            result = warehouse.add_tag_to_zone(id, tag)
            assert result, f"Zone {id} does not exist"

            add_to_json(data, "tags", "id", tag_id, tag.serialize())
            add_to_json(data, "items", "id", item_id, item.serialize())
            if item_id not in data["zones"][index]["items"]:
                data["zones"][index]["items"] += [item_id]
    
    with open(db, 'w') as file:
        json.dump(data, file, indent=4)

def client_function(thread_id):
    for i in range(5):
        time.sleep(1)
        print(f"Thread {thread_id}: {i}")

def main():
    global warehouse, admin
    create_database()
    
    nr_of_threads = 100
    threads = []
    for i in range(nr_of_threads):
        thread = threading.Thread(target=client_function, args=(i,))
        threads.append(thread)
        thread.start()

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

    # add observer - send message to observer when an item was add/remove from a zone
    warehouse.add_observer_to_all_readers(admin)

    # move item from one zone to another
    tag_id_to_search = 61
    tag = warehouse.get_tag_by_id(tag_id_to_search)
    assert tag, f"Tag {tag_id_to_search} does not exist"
    warehouse.move_item(tag, 6, 1)

    print()
    print(warehouse.get_tags_id_from_zone(1))
    print(warehouse.get_tags_id_from_zone(6))

    # find item in warehouse
    item = 100
    result = warehouse.find_item_location(item)
    assert result != -1, f"Item {item} does not exist"
    print(f"\nFind item {item}: zone {result}","\n\n")

    # # test access_control
    # role_employee = Role(["add_item","remove_item"])
    # employee1 = Employee(11,"Employee 11",role_employee)
    # add_to_json("employees", "id", 11, employee1.serialize())

    # zone = Zone(99,"Zone 99")
    # warehouse.add_zone(employee1,zone)
    # add_to_json("zones", "id", 99, zone.serialize())

    # print(employee1.role.permissions)

    # for zone in warehouse:
    #     print(f"Zone: {zone.get_zone_id()}")
    
    for thread in threads:
        thread.join()
    
    print("All threads have finished.")

if __name__ == "__main__":
    db = './database.json'

    with open("App/output.txt", 'w') as file:
        file.write("Fuctions messages.\n")

    tracer = trace.Trace(trace=False, ignoredirs=[sys.prefix, sys.exec_prefix])
    tracer.run('main()')

    r = tracer.results()
    r.write_results(show_missing=True, coverdir="./tema6")
