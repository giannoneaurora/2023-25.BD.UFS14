from jsonschema import validate
import pandas as pd
import os
from main import aggiungi_note, get_all_notes, modifica_note, cancella_note, cerca_note, save_notes_to_file

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


'''
def test_save_notes_to_file():
    # Crea un DataFrame di esempio per il test
    data = {'id': [1, 2, 3], 'text': ['Nota 1', 'Nota 2', 'Nota 3']}
    notes_df = pd.DataFrame(data)
    path = 'test_note.csv'  # Percorso del file di test

    save_notes_to_file(notes_df, path)

    assert os.path.exists(path), "Il file non è stato creato!"

    saved_df = pd.read_csv(path)

    pd.testing.assert_frame_equal(notes_df, saved_df), "I dati nel file non corrispondono."

    if os.path.exists(path):
        os.remove(path)'''


def test_get_all_notes():
    notes = get_all_notes()
    assert isinstance(notes, list)
    for note in notes:
        assert validate_wrapper(note, note_schema) == True


def test_add_note():
    result = aggiungi_note("Nuova nota di test")
    assert validate_wrapper(result, note_schema) == True
    assert result["Nota"] == "Nuova nota di test"

def test_update_note_success():
    new_note = aggiungi_note("Nota da aggiornare")
    result = modifica_note(new_note["ID"], "Nota aggiornata")
    assert validate_wrapper(result, note_schema) == True
    assert result["Nota"] == "Nota aggiornata"

def test_update_note_fail():
    result = modifica_note(999, "Nota inesistente")
    assert "error" in result
    assert result["error"] == "Nota non trovata."

def test_delete_note_success():
    new_note = aggiungi_note("Nota da eliminare")
    result = cancella_note(new_note["ID"])
    assert validate_wrapper(result, message_schema) == True
    assert result["message"] == f"Nota con ID {new_note['ID']} eliminata."

def test_delete_note_fail():
    result = cancella_note(999)
    assert "error" in result
    assert result["error"] == "Nota non trovata."

def test_search_notes_by_text():
    aggiungi_note("Nota per test ricerca testo")
    result = cerca_note(text_param="test ricerca")
    assert isinstance(result, list)
    assert len(result) > 0
    assert any("test ricerca" in note["Nota"] for note in result)

def test_search_notes_by_invalid_text():
    result = cerca_note(text_param="test non esistente")
    assert isinstance(result, dict)
    assert "error" in result
    assert result["error"] == "Nessuna nota trovata."