import pythonrv as rv

#@rv.monitor(fact=Warehouse.add_item)
def input_only_spec(event):
    assert event.fn.fact.inputs[0] >= 0

def validate_tag(func):
    def wrapper(self, employee, item, tag):
        if tag.tag_id > 0:
            return func(self, employee, item, tag)
        else:
            return -1
    return wrapper

def log_function_name(location):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Calling function: {func.__name__} from {location}")
            return func(*args, **kwargs)
        return wrapper
    return decorator




