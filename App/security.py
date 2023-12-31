from aspectlib import Aspect
from models.employee import Employee 
from functools import wraps

class Admin:
    def __init__(self):
        self.permission_requests = {}

    def request_permission(self, employee, required_permission, access_control, filename="App/output.txt"):
        with open(filename, 'a') as file:
            file.write(f"Permission request from employee with id {employee.employee_id} for permission: {required_permission}\n")
        access_control.process_permission_request(employee, required_permission)

    def grant_permission(self, employee, permission, filename="App/output.txt"):
        employee.role.add_permission(permission)
        with open(filename, 'a') as file:
            file.write(f"Permission granted to employee with id {employee.employee_id} for permission: {permission}\n")

class AccessControl:
    def __init__(self):
        self.employee_roles = {}
        self.admin = Admin()

    def assign_role(self, employee, role):
        self.employee_roles[employee.employee_id] = role

    def check_access(self, employee, required_permission):
        employee_role = employee.role.permissions 
        if required_permission in employee_role:
            return True
        else:
            self.request_permission(employee, required_permission)
            return required_permission in employee_role
        
    def request_permission(self, employee, required_permission):
        self.admin.request_permission(employee, required_permission, self)

    def process_permission_request(self, employee, permission, filename="App/output.txt"):
        admin_approval = input(f"Admin, do you approve permission request from {employee.employee_id} for {permission}? (yes/no): ")
        if admin_approval.lower() == "yes":
            self.admin.grant_permission(employee, permission)
        else:
            with open(filename, 'a') as file:
                file.write(f"Permission denied by admin for employee with id {employee.employee_id} for permission: {permission}\n")

def check_access_control(permission, filename="App/output.txt"):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            employee = args[0]  # Assuming the first argument is an Employee instance
            if self.access_control.check_access(employee, permission):
                with open(filename, 'a') as file:
                    file.write(f"Access permitted: Employee {employee.employee_id} has the required permission.\n")
                return func(self, *args, **kwargs)
            else:
                with open(filename, 'a') as file:
                    file.write(f"Access denied: Employee {employee.employee_id} does not have the required permission.\n")
        return wrapper
    return decorator
