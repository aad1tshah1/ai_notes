from models.note import Note

"""
Responsibility:
Save and retrieve notes from Postgres.
"""

def save_note(db, transcript, notes):
    note = Note (
        transcript=transcript,
        summary=notes["summary"],
        key_points=notes["key_points"],
        action_items=notes["action_items"],
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def list_notes(db):
    return (
        db.query(Note)
        .order_by(Note.created_at.desc())
        .all()
    )
    
def get_note(db, note_id):
    pass

def delete_note(db, note_id):
    pass
