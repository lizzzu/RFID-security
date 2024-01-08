import json
import time
import random
import threading

from models.item import Item
from models.zone import Zone
from models.rfidTag import RFIDTag
from models.rfidReader import RFIDReader
from models.employee import Employee, Role
from models.warehouse import Warehouse

def client_function(thread_id):    
    with open(db, 'r') as file:
        data = json.load(file)
    
    warehouse = Warehouse(data["capacity"])

    admin = Employee.deserialize(data["employees"][0])
    warehouse.add_employee(admin)
    warehouse.access_control.assign_role(admin, Role(data["employees"][0]["permissions"]))

    employee_index = random.randrange(1, len(data["employees"]))
    employee = Employee.deserialize(data["employees"][employee_index])
    warehouse.add_employee(employee)
    warehouse.access_control.assign_role(employee, Role(data["employees"][employee_index]["permissions"]))

    for zon in data["zones"]:
        zone = Zone.deserialize(zon)
        reader = RFIDReader(zone.get_zone_id(), zone.get_zone_id())
        zone.add_rfid_reader(reader)
        warehouse.add_zone(admin, zone)

        for itm in zon["items"]:
            index, _ = next(((i, d) for i, d in enumerate(data["items"]) if d.get("id") == itm), (None, None))
            item = Item.deserialize(data["items"][index])
            tag = RFIDTag(item.get_item_id())
            warehouse.add_item(admin, item, tag)
            warehouse.add_tag_to_zone(zone.get_zone_id(), tag)

    print(f"Thread {thread_id}: employee {employee.get_employee_id()}")

    for _ in range(10):
        # find tag in warehouse
        target_tag_id = random.randrange(0, 300)
        result = warehouse.find_tag_in_warehouse(target_tag_id)
        if not result:
            print(f"[{thread_id}] Tag {target_tag_id} does not exist")
        else:
            print(f"[{thread_id}] Tag {target_tag_id} found")
    
        # find item in warehouse
        id_to_search = random.randrange(0, 300)
        result = warehouse.find_item_location(id_to_search)
        if result == -1:
            print(f"[{thread_id}] Tag {id_to_search} does not exist")
        else:
            print(f"[{thread_id}] Tag location: {result}")

        # get item info
        id = random.randrange(0, 300)
        result = warehouse.get_item_info_by_id(id)
        if not result:
            print(f"[{thread_id}] Item {id} does not exist")
        else:
            print(f"[{thread_id}] Item info: {result}")
    
        # get item location(zone id)
        id = random.randrange(0, 300)
        result = warehouse.find_zone_location_of_item(id)
        if result == -1:
            print(f"[{thread_id}] Item {id} does not exist")
        else:
            print(f"[{thread_id}] Tag location: {result}")

if __name__ == '__main__':
    db = './database.json'
    time.sleep(1)

    nr_of_threads = 10
    threads = []
    for i in range(nr_of_threads):
        thread = threading.Thread(target=client_function, args=(i,))
        threads += [thread]
        thread.start()

    for thread in threads:
        thread.join()

    print("All client threads have finished.")
