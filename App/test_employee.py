from models.employee import Employee

employee1 = Employee(employee_id="E001", name="John Doe", role="Warehouse Worker")

print(f"Employee ID: {employee1.employee_id}")
print(f"Name: {employee1.name}")
print(f"Role: {employee1.role}","\n")

employee1.employee_id = "E002"
employee1.name = "Jane Doe"
employee1.role = "Supervisor"

print(f"Employee ID: {employee1.employee_id}")
print(f"Name: {employee1.name}")
print(f"Role: {employee1.role}")
