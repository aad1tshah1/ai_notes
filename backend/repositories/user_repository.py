from models.user import User


def create_user(db, email, password_hash):
    user = User (
        email=email,
        password_hash=password_hash,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db, email):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

def get_user_by_id(db, user_id):
    return (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )