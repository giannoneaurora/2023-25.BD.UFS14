import json
import os

path = "/workspaces/2023-25.BD.UFS14/MyProjFolder/note.json"  
# Funzione per caricare le note da un file JSON
def load_notes_from_json(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    return []

# Funzione per salvare le note in un file JSON
def save_notes_to_json(notes, path):
    with open(path, 'w') as file:
        json.dump(notes, file, indent=4)



def cerca_note(id_param=None, text_param=None, path="notes.json"):
    notes = load_notes_from_json(path)
    
    # Filtrare per ID
    if id_param:
        try:
            notes = [note for note in notes if note["ID"] == int(id_param)]
        except ValueError:
            return {"error": "Il parametro ID deve essere un numero."}
    
    # Filtrare per testo
    if text_param:
        notes = [note for note in notes if text_param.lower() in note["Nota"].lower()]
    
    if not notes:
        return {"error": "Nessuna nota trovata."}
    
    return notes



def aggiungi_note(note_text, path="notes.json"):
    notes = load_notes_from_json(path)
    
    # Calcolare il nuovo ID
    new_id = max([note["ID"] for note in notes], default=0) + 1
    new_note = {"ID": new_id, "Nota": note_text}
    
    notes.append(new_note)
    save_notes_to_json(notes, path)  # Salva la modifica
    
    return {"ID": new_id, "Nota": note_text}

def modifica_note(note_id, new_text, path="notes.json"):
    notes = load_notes_from_json(path)
    
    # Trovare la nota con l'ID specificato
    note_to_modify = next((note for note in notes if note["ID"] == note_id), None)
    if note_to_modify is None:
        return {"error": "Nota non trovata."}
    
    # Modificare il testo della nota
    note_to_modify["Nota"] = new_text
    save_notes_to_json(notes, path)  # Salva la modifica
    
    return {"ID": note_id, "Nota": new_text}

def cancella_note(note_id, path="notes.json"):
    notes = load_notes_from_json(path)
    
    # Verificare se la nota esiste
    if not any(note["ID"] == note_id for note in notes):
        return {"error": "Nota non trovata."}
    
    # Eliminare la nota con l'ID specificato
    notes = [note for note in notes if note["ID"] != note_id]
    save_notes_to_json(notes, path)  # Salva la modifica
    
    return {"message": f"Nota con ID {note_id} eliminata."}

