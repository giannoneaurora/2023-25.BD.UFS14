from jsonschema import validate
import os
import json
from main import aggiungi_note, modifica_note, cancella_note, cerca_note, save_notes_to_json, get_all_notes

note_schema = {
    "type": "object",
    "properties": {
        "ID": {"type": "integer"},
        "Nota": {"type": "string"}
    },
    "required": ["ID", "Nota"]
}

# Schema per la validazione dei messaggi di risposta
message_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
}

def validate_wrapper(instance, schema):
    try:
        validate(instance=instance, schema=schema)
        return True
    except Exception as e:
        print(f"Schema validation error: {e}")
        return False

def test_save_notes_to_file():
    notes = [
        {"ID": 1, "Nota": "Nota 1"},
        {"ID": 2, "Nota": "Nota 2"},
        {"ID": 3, "Nota": "Nota 3"}
    ]
    path = 'test_note.json'  
    save_notes_to_json(notes, path)
    assert os.path.exists(path), "Il file non è stato creato!"
    with open(path, 'r') as file:
        saved_notes = json.load(file)
    assert saved_notes == notes, "I dati nel file non corrispondono."

    if os.path.exists(path):
        os.remove(path)

def test_get_all_notes():
    test_file = 'test_note.json'
    sample_notes = [
        {"ID": 1, "Nota": "Questa è la prima nota"},
        {"ID": 2, "Nota": "Questa è la seconda nota"}
    ]
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(sample_notes, f, ensure_ascii=False, indent=4)
    notes = get_all_notes(test_file)
    
    assert notes == sample_notes, f"Expected {sample_notes}, but got {notes}"
    if os.path.exists(test_file):
        os.remove(test_file)


def test_aggiungi_note():
    result = aggiungi_note("Nuova nota di test", "test_note.json")
    assert validate_wrapper(result, note_schema) == True
    assert result["Nota"] == "Nuova nota di test"

def test_modifica_note_success():
    new_note = aggiungi_note("Nota da aggiornare", "test_note.json")
    result = modifica_note(new_note["ID"], "Nota aggiornata", "test_note.json")
    assert validate_wrapper(result, note_schema) == True
    assert result["Nota"] == "Nota aggiornata"

def test_modifica_note_fail():
    result = modifica_note(999, "Nota inesistente", "test_note.json")
    assert "error" in result
    assert result["error"] == "Nota non trovata."

def test_cancella_note_success():
    new_note = aggiungi_note("Nota da eliminare", "test_note.json")
    result = cancella_note(new_note["ID"], "test_note.json")
    assert validate_wrapper(result, message_schema) == True
    assert result["message"] == f"Nota con ID {new_note['ID']} eliminata."

def test_cancella_note_fail():
    result = cancella_note(999, "test_note.json")
    assert "error" in result
    assert result["error"] == "Nota non trovata."

def test_cerca_note_testo():
    aggiungi_note("Nota per test ricerca testo", "test_note.json")
    result = cerca_note(text_param="test ricerca", path="test_note.json")
    assert isinstance(result, list)
    assert len(result) > 0
    assert any("test ricerca" in note["Nota"] for note in result)

def test_cerca_note_testo_non_valido():
    result = cerca_note(text_param="test non esistente", path="test_note.json")
    assert isinstance(result, dict)
    assert "error" in result
    assert result["error"] == "Nessuna nota trovata."
