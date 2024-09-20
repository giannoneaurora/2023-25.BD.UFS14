# json schema

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


# snapshot

def func(x):
    return x + 1

def test_function_output_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots'  
    pierino=func(5)
    pierino_stringa=str(pierino)
    snapshot.assert_match(pierino_stringa, 'foo_output.txt')


# ritorniamo un insieme di dati grande piuttosto che un numero

frutti = """
frutti,prezzo,colore,sapore
pera,100,rosso,buone
mela,10,giallo,squisita
ananas,23,verde,piccante
"""

def test_function_output_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots'  
    snapshot.assert_match(frutti, 'frutti.csv')

