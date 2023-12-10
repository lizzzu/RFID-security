import unittest

from models.warehouse import Warehouse
from models.employee import Employee, Role
from models.zone import Zone
from models.rfidReader import RFIDReader
from models.rfidTag import RFIDTag
from models.item import Item

class TestWarehouse(unittest.TestCase):

    def setUp(self):
        # Initialize a Warehouse for testing
        self.warehouse = Warehouse(455)

        # Create roles
        self.admin_role = Role(["add_item","remove_item",
                        "add_zone","remove_zone",
                        "remove_employee","add_employee"])

        # Create admin
        self.admin = Employee(1,"Admin",self.admin_role)

        # Create employee
        self.employee = Employee(2,"Employee",Role())

        # Add admin in warehouse
        self.warehouse.add_employee(self.admin)
        self.warehouse.access_control.assign_role(self.admin, self.admin_role)

        # Create item
        self.item = Item(1, f"item 1", 1)

        # Create tag
        self.tag = RFIDTag(1)

        # Create zone
        self.zone = Zone(id=1, name="Zone")
        reader = RFIDReader(id, id)
        self.zone.add_rfid_reader(reader)


    def test_add_item(self):

        result = self.warehouse.add_item(self.admin, self.item, self.tag)

        self.assertTrue(result)
        self.assertIn(self.item, self.warehouse.get_items())
        self.assertIn(self.tag, self.warehouse.get_rfid_tags())
    
    def test_remove_item(self):

        self.item.item_id += 1
        self.item.rfid_tag_id += 1

        self.tag.tag_id += 1

        self.warehouse.add_item(self.admin, self.item, self.tag)
        result = self.warehouse.remove_item(self.admin, self.item.item_id)

        self.assertTrue(result)
        self.assertNotIn(self.item, self.warehouse.get_items())
        self.assertNotIn(self.tag, self.warehouse.get_rfid_tags())


    def test_add_zone(self):

        zone = Zone(1,"Test Zone")
        reader = RFIDReader(id, id)
        zone.add_rfid_reader(reader)

        self.warehouse.add_zone(self.admin, zone)

        self.assertIn(zone, self.warehouse.get_zones())

    def test_remove_existing_zone(self):
        zone_id = 2
        zone = Zone(zone_id, "Test Zone")
        self.warehouse.add_zone(self.admin, zone)

        result = self.warehouse.remove_zone(self.admin, zone_id)

        self.assertTrue(result)
        self.assertNotIn(zone, self.warehouse.get_zones())

    def test_remove_nonexistent_zone(self):
        # Attempt to remove a zone that does not exist
        initial_number_of_zones = len(self.warehouse.get_zones())
        result = self.warehouse.remove_zone(self.admin, zone_id=99)

        self.assertFalse(result)  # Removal should fail
        self.assertEqual(len(self.warehouse.get_zones()), initial_number_of_zones)  # No zones should be removed

    def test_remove_zone_with_wrong_employee(self):
        zone_id = 1
        zone = Zone(id=zone_id, name="Test Zone")
        self.warehouse.add_zone(self.admin, zone)

        # Attempt to remove a zone with a different employee
        result = self.warehouse.remove_zone(self.employee, zone_id)

        self.assertFalse(result)  # Removal should fail
        self.assertIn(zone, self.warehouse.get_zones())  # Zone should not be removed


    def test_add_employee(self):
        self.warehouse.add_employee(self.employee)
        self.assertIn(self.employee, self.warehouse.get_employee())

    def test_remove_existing_employee(self):

        initial_employee_count = len(self.warehouse.employee)
        result = self.warehouse.remove_employee(self.admin, self.employee.employee_id)

        self.assertTrue(result)
        self.assertNotIn(self.employee, self.warehouse.employee)
        self.assertEqual(len(self.warehouse.employee), initial_employee_count - 1)

    def test_remove_nonexistent_employee(self):
        new_employee = Employee(employee_id=2, name="Jane Doe", role=Role())
        initial_employee_count = len(self.warehouse.employee)

        result = self.warehouse.remove_employee(new_employee, new_employee.employee_id)

        self.assertFalse(result)
        self.assertEqual(len(self.warehouse.employee), initial_employee_count)


    def test_get_tags_id_from_zone_with_valid_zone(self):
        # Create a zone and add RFID tags to it
        zone = Zone(id=100, name="Zone100")
        reader = RFIDReader(id, id)
        zone.add_rfid_reader(reader)
        self.warehouse.add_zone(self.admin,zone)

        for i in range(1,6):
            tag = RFIDTag(i)
            self.warehouse.add_tag_to_zone(100,tag)
        
        self.warehouse.add_tag_to_zone

        # Call the method and check the result
        result = self.warehouse.get_tags_id_from_zone(zone_id=100)

        self.assertListEqual(result, [1, 2, 3, 4, 5])

    def test_get_tags_id_from_zone_with_invalid_zone(self):
        # Call the method with an invalid zone ID
        result = self.warehouse.get_tags_id_from_zone(zone_id=979)
        self.assertListEqual(result, [])

    def test_get_tags_id_from_zone_with_empty_zone(self):
        # Create an empty zone
        zone = Zone(id=10, name="Zone10")
        self.warehouse.zones.append(zone)

        # Call the method on an empty zone and check the result
        result = self.warehouse.get_tags_id_from_zone(zone_id=10)

        self.assertListEqual(result, [])


    def test_get_tag_by_id_successful(self):
        tag_id = 100
        tag = RFIDTag(tag_id=tag_id)
        self.warehouse.rfid_tags.append(tag)

        result = self.warehouse.get_tag_by_id(tag_id)

        self.assertEqual(result, tag)

    def test_get_tag_by_id_not_found(self):
        tag_id = 1
        non_existing_tag_id = 2
        tag = RFIDTag(tag_id=tag_id)
        self.warehouse.rfid_tags.append(tag)

        result = self.warehouse.get_tag_by_id(non_existing_tag_id)

        self.assertIsNone(result)

    
    def test_get_item_info_by_id_existing_item(self):
        item_id = 1
        item_description = "Test Item"
        item = Item(item_id=item_id, name="Item", rfid_tag_id=1)
        tag = RFIDTag(tag_id=1)

        self.warehouse.add_item(self.admin, item, tag)

        result = self.warehouse.get_item_info_by_id(item_id)

        self.assertIsNotNone(result)
        self.assertEqual(result.item_id, item_id)

    def test_get_item_info_by_id_non_existing_item(self):
        result = self.warehouse.get_item_info_by_id(999)  # Assuming item with ID 999 does not exist

        self.assertIsNone(result)

    
    def test_add_tag_to_zone_success(self):
        self.warehouse.add_zone(self.admin, self.zone)

        result = self.warehouse.add_tag_to_zone(self.zone.id, self.tag)

        self.assertTrue(result)
        #self.assertIn(self.tag, self.zone.rfid_reader.rfid_tags)

    def test_add_tag_to_nonexistent_zone(self):
        result = self.warehouse.add_tag_to_zone(919, self.tag)  # Assuming 919 is an invalid zone ID

        self.assertFalse(result)
        self.assertNotIn(self.tag, self.warehouse.get_tags_id_from_zone(919))


    def test_remove_tag_from_zone(self):
        employee = Employee(employee_id=1, name="John Doe", role=Role())
        zone = Zone(id=1, name="Test Zone")
        tag = RFIDTag(tag_id=1)

        self.warehouse.add_zone(employee, zone)
        self.warehouse.add_tag_to_zone(zone.id, tag)

        result = self.warehouse.remove_tag_from_zone(zone.id, tag.tag_id)

        self.assertTrue(result)
        self.assertNotIn(tag.tag_id, self.warehouse.get_tags_id_from_zone(zone.id))

    def test_remove_tag_from_zone_nonexistent_zone(self):
        employee = Employee(employee_id=1, name="John Doe", role=Role())
        tag = RFIDTag(tag_id=1)

        result = self.warehouse.remove_tag_from_zone(999, tag.tag_id)

        self.assertFalse(result)  # Expecting failure since the zone doesn't exist


    def test_move_item(self):
        tag = RFIDTag(23)
        item = Item(item_id=23, name="Test Item", rfid_tag_id=23)

        initial_zone = Zone(id=31, name="Initial Zone")
        reader = RFIDReader(1, 31)
        initial_zone.add_rfid_reader(reader)

        target_zone = Zone(id=32, name="Target Zone")
        reader = RFIDReader(2, 32)
        target_zone.add_rfid_reader(reader)

        # Add item to initial zone
        initial_zone.add_rfid_tag(tag)
        self.warehouse.add_item(self.admin, item, tag)
        self.warehouse.add_zone(self.admin, initial_zone)

        # Move item to target zone
        self.warehouse.add_zone(self.admin, target_zone)
        self.warehouse.move_item(tag, initial_zone.id, target_zone.id)

        # Check if item is in the target zone
        self.assertNotIn(tag, initial_zone.rfid_reader.rfid_tags)
        self.assertIn(tag, target_zone.rfid_reader.rfid_tags)


    def test_find_tag_in_warehouse_positive_case(self):
        tag_id_to_find = 1
        zone = Zone(id=41, name="Zone")
        reader = RFIDReader(1, 41)
        zone.add_rfid_reader(reader)

        rfid_tag = RFIDTag(tag_id=tag_id_to_find)
        zone.rfid_reader.rfid_tags.append(rfid_tag)
        self.warehouse.zones.append(zone)

        result = self.warehouse.find_tag_in_warehouse(tag_id_to_find)

        self.assertTrue(result)

    def test_find_tag_in_warehouse_negative_case(self):
        tag_id_to_find = 143
        zone = Zone(id=441, name="Zone")
        reader = RFIDReader(1, 441)
        zone.add_rfid_reader(reader)

        rfid_tag = RFIDTag(tag_id=2)  # Different tag id
        zone.rfid_reader.rfid_tags.append(rfid_tag)
        self.warehouse.zones.append(zone)

        result = self.warehouse.find_tag_in_warehouse(tag_id_to_find)

        self.assertFalse(result)

    def test_find_tag_in_warehouse_empty_warehouse(self):
        tag_id_to_find = 123

        result = self.warehouse.find_tag_in_warehouse(tag_id_to_find)

        self.assertFalse(result)


    def test_find_item_location(self):
        # Create sample data
        item = Item(341, f"item 341", 341)
        tag = RFIDTag(341)
        zone = Zone(id=13, name="Test Zone")
        reader = RFIDReader(1, 13)
        zone.add_rfid_reader(reader)
        zone.add_rfid_tag(tag)

        # Add the item and zone to the warehouse
        self.warehouse.add_item(self.admin, item, tag)
        self.warehouse.add_zone(self.admin, zone)

        # Find the location of the item
        location = self.warehouse.find_item_location(item.rfid_tag_id)

        # Assert the expected result
        self.assertEqual(location, zone.get_zone_id())


    def test_find_zone_location_of_item(self):
        # Create a zone, item, and RFIDTag
        zone = Zone(id=16,  name="Test Zone")
        item = Item(371, f"item 341", 371)
        tag = RFIDTag(371)

        # Add the item and tag to the warehouse in a specific zone
        self.warehouse.add_zone(self.admin, zone)
        self.warehouse.add_item(self.admin, item, tag)
        self.warehouse.add_tag_to_zone(zone_id=1, tag=tag)

        # Test the find_zone_location_of_item method
        result = self.warehouse.find_zone_location_of_item(item_tag_id=1)

        # Assert that the result matches the expected zone ID
        self.assertEqual(result, 1)


    def test_add_observer_to_all_readers(self):
        zone1 = Zone(id=1, name="Zone A")
        zone2 = Zone(id=2, name="Zone B")

        self.warehouse.add_zone(self.employee, zone1)
        self.warehouse.add_zone(self.employee, zone2)

        self.warehouse.add_observer_to_all_readers(self.employee)

        for zone in self.warehouse.get_zones():
            self.assertTrue(self.employee in zone.observers)




if __name__ == '__main__':
    unittest.main()