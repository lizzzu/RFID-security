from abc import ABC, abstractmethod
# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, tag_id, action):
        pass

class Role:
    def __init__(self, permissions=[]):
        self.permissions = permissions

    def add_permission(self, permission):
        self.permissions.append(permission)

    def check_permission(self, required_permission):
        return required_permission in self.permissions
    
class Employee:

    def __init__(self, employee_id: int, name: str, role: Role):
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

    # Observer pattern
    def update(self, tag_id, action):
        print(f"employee id={self.employee_id}: Tag '{tag_id}' was {action}.")

    