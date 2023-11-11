
class Employee:

    def __init__(self, employee_id, name, role):
        self.employee_id = employee_id
        self.name = name
        self.role = role

    def get_employee_id(self):
        return self.employee_id

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_role(self):
        return self.role

    def set_role(self, value):
        self.role = value