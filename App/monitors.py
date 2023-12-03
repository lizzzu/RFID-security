import pythonrv as rv
from functools import wraps

#@rv.monitor(fact=Warehouse.add_item)
def input_only_spec(event):
    assert event.fn.fact.inputs[0] >= 0

def validate_tag(func, filename="App/output.txt"):
    def wrapper(self, employee, item, tag):
        if tag.tag_id > 0:
            return func(self, employee, item, tag)
        else:
            with open(filename, 'a') as file:
                file.write(f"Tag id invalid.\n")
            return -1
    return wrapper

def print_function_name_before_execution(location, filename="App/output.txt"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with open(filename, 'a') as file:
                file.write(f"Calling function: {func.__name__} from {location}\n")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def print_function_name_after_execution(location, filename="App/output.txt"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, 'a') as file:
                file.write(f"Function {func.__name__} from {location} has been executed.\n")
            return result
        return wrapper
    return decorator




