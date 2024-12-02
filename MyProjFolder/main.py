import json
import os
import logging 

path = "/workspaces/2023-25.BD.UFS14/MyProjFolder/note.json"  

def load_notes_from_json(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    return []

def save_notes_to_json(notes, path):
    with open(path, 'w') as file:
        json.dump(notes, file, indent=4)

def get_all_notes(path):
    if not os.path.exists(path):
        return {"error": "Il file delle note non esiste."}
    with open(path, 'r', encoding='utf-8') as file:
        notes = json.load(file)
    return notes



def cerca_note(id_param=None, text_param=None,path='note.json'):
    notes = load_notes_from_json(path)
    if id_param:
        try:
            notes = [note for note in notes if note["ID"] == int(id_param)]
        except ValueError:
            return {"error": "Il parametro ID deve essere un numero."}
    if text_param:
        notes = [note for note in notes if text_param.lower() in note["Nota"].lower()]
    if not notes:
        return {"error": "Nessuna nota trovata."}
    
    return notes



def aggiungi_note(note_text, path="notes.json"):
    notes = load_notes_from_json(path)
    logging.info(f"Note attuali: {notes}")

    new_id = max([note["ID"] for note in notes], default=0) + 1
    new_note = {"ID": new_id, "Nota": note_text}
    logging.info(f"Aggiunta nuova nota: {new_note}")

    notes.append(new_note)
    save_notes_to_json(notes, path)  

    logging.info(f"Note salvate: {notes}")
    return {"ID": new_id, "Nota": note_text}

    
    return {"ID": new_id, "Nota": note_text}

def modifica_note(note_id, new_text, path):
    notes = load_notes_from_json(path)
    note_to_modify = next((note for note in notes if note["ID"] == note_id), None)
    if note_to_modify is None:
        return {"error": "Nota non trovata."}
    note_to_modify["Nota"] = new_text
    save_notes_to_json(notes, path)  
    
    return {"ID": note_id, "Nota": new_text}

def cancella_note(note_id, path):
    notes = load_notes_from_json(path)
    if not any(note["ID"] == note_id for note in notes):
        return {"error": "Nota non trovata."}
    notes = [note for note in notes if note["ID"] != note_id]
    save_notes_to_json(notes, path) 
    return {"message": f"Nota con ID {note_id} eliminata."}

