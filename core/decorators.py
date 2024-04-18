import json

def serialize_data(func):
    def wrapper(*args, **kwargs):
        # Call the original function
        result = func(*args, **kwargs)
        # Serialize the result using JSON
        serialized_result = json.dumps(result)
        return serialized_result
    return wrapper