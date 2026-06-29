from models.note import Note

def save_note(db, transcript, notes, user_id):
    note = Note(
        user_id=user_id,
        transcript=transcript,
        summary=notes["summary"],
        key_points=notes["key_points"],
        action_items=notes["action_items"],
    )

    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def list_notes(db, user_id):
    return (db.query(Note).filter(Note.user_id == user_id).all()
    )
    
def get_note(db, note_id, user_id):
    return (
        db.query(Note)
        .filter(
            Note.note_id == note_id,
            Note.user_id == user_id,
        )
        .first()
    )

def delete_note(db, note_id, user_id):
    note = get_note(db, note_id, user_id)

    if note is None:
        return None

    db.delete(note)
    db.commit()

    return note
