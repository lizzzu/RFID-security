from aspectlib import Aspect
from models.employee import Employee 
from functools import wraps

class AccessControl:
    def __init__(self):
        self.employee_roles = {}

    def assign_role(self, employee, role):
        self.employee_roles[employee.employee_id] = role

    def check_access(self, employee, required_permission):
        if employee.employee_id in self.employee_roles:
            employee_role = self.employee_roles[employee.employee_id]
            return employee_role.check_permission(required_permission)
        else:
            return False

# Aspect for checking access control
def check_access_control(permission, filename="App/output.txt"):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            employee = args[0]  # Assuming the first argument is an Employee instance
            if self.access_control.check_access(employee, permission):
                with open(filename, 'a') as file:
                    #file.write(f"Employee {employee.employee_id} has called {permission}.\n")
                    file.write(f"Access permitted: Employee {employee.employee_id} has the required permission.\n")
                return func(self, *args, **kwargs)
            else:
                with open(filename, 'a') as file:
                    #file.write(f"Employee {employee.employee_id} has called {func.__name__}.\n")
                    file.write(f"Access denied: Employee {employee.employee_id} does not have the required permission.\n")
                #print(f"Access denied: Employee {employee.employee_id} does not have the required permission.")
        return wrapper
    return decorator
