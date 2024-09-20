from jsonschema import validate

schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}


def test_success():
    assert validate_wrapper(instance={"name" : "Eggs", "price" : 34.99}, schema=schema) == True


def test_validate_fail():
    assert validate_wrapper(instance={"name" : "Eggs", "price" : "Ciao"}, schema=schema) == False


def validate_wrapper(instance, schema):
    try:
        validate(instance=instance, schema=schema)
        return True
    except:
        return False



