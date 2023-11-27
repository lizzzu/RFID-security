
from models.item import Item
from models.zone import Zone
from models.rfidTag import RFIDTag
from models.rfidReader import RFIDReader
from models.employee import Employee, Role
from models.warehouse import Warehouse

if __name__ == "__main__":
    
    warehouse = Warehouse(145)

    # Create roles
    #admin_role = Role(["add_tag", "remove_tag"])
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
                item = Item(tag_id,f"item {id}", tag_id)
                tag = RFIDTag(tag_id)

                warehouse.add_item(employee, item, tag)
                warehouse.add_tag_to_zone(id, tag)

    # add tag in zone 2 - employee is notified
    tag333 = RFIDTag(333)
    print(warehouse.add_tag_to_zone(2,tag333))

    # find tag in warehouse
    target_tag_id = 333
    result = warehouse.find_tag_in_warehouse(target_tag_id)
    print(result)
    
    # print zone and their tags
    for zone in warehouse:
        print(f"Zone: {zone.get_zone_id()}")
        #for tag in zone:
        #    print(f"  RFID Tag ID: {tag.tag_id}")

        zone_tags = zone.get_items()
        print(f"  Tags in the zone: {[tag.tag_id for tag in zone_tags]}")
    
    # find item in warehouse
    tag_id_to_search = 22
    result = warehouse.find_item_location(tag_id_to_search)
    print("\nTag location: ",result)

    # get item info
    print("Item info: ",warehouse.get_item_info_by_id(22))

    # get item location(zone id)
    print("Tag location: ",warehouse.find_zone_location_of_item(22),"\n\n")

    # move item from one zone to another
    tag = warehouse.get_tag_by_id(61)
    warehouse.move_item(tag,6,1)

    print(warehouse.get_tags_id_from_zone(1))
    print(warehouse.get_tags_id_from_zone(6))

    # find item in warehouse
    print("\nFind item:", warehouse.find_item_location(401))

    


        
