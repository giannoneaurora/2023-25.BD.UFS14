from jsonschema import validate
from io import StringIO
from unittest.mock import patch
from main import aggiungi_note, visualizza_note, elimina_note, modifica_note, cerca_note

notes_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",  
    "items": {
        "type": "object",  
        "properties": {
            "id": {
                "type": "string",  
                "pattern": "^[a-f0-9-]{36}$"  
            },
            "content": {
                "type": "string",
                "minLength": 1  
            },
        },
        "required": ["id", "content"], 
        "additionalProperties": False  
    }
}

def validate_wrapper(notes):
    try:
        validate(instance=notes, schema=notes_schema)
        return True
    except Exception as e:
        print(f"Schema validation error: {e}")
        return False

def test_aggiungi_note():
    notes = []  
    nuova_nota = "New note"
    
    with patch('builtins.input', return_value=nuova_nota):
        aggiungi_note(notes)
    
    assert len(notes) == 1  
    assert notes[-1]['content'] == nuova_nota 

def test_visualizza_note(capsys):
    notes = ["Prima nota"]  

    with patch('builtins.input', return_value=""):
        visualizza_note(notes)
    
    captured = capsys.readouterr()
    assert 'Prima nota' in captured.out  

def test_modifica_note():
    notes = [{"id": "1", "content": "Nota 1"}]  
    nota_modificata = "Modified first note"
    
    with patch('builtins.input', side_effect=["1", nota_modificata]):
        modifica_note(notes)
    
    assert notes[0]['content'] == nota_modificata  

def test_cerca_note_found():
    notes = [{"id": "1", "content": "This is a special note"}, 
             {"id": "2", "content": "Another generic note"}]
    
    search_term = "special"
    with patch('builtins.input', return_value=search_term), patch('sys.stdout', new_callable=StringIO) as mocked_stdout:
        cerca_note(notes)

    output = mocked_stdout.getvalue().strip()
    assert "Risultati della ricerca:" in output
    assert "Nessuna nota trovata" not in output

def test_elimina_note():
    notes = ["nota1", "nota2"]
    
    with patch('builtins.input', side_effect=["1", "s"]):
        with patch('sys.stdout', new_callable=StringIO) as captured_output:
             elimina_note(notes)

    output = captured_output.getvalue().strip()
    assert len(notes) == 1  
