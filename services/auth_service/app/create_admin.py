from dependencies import engine, get_db
from hashing import hash_password
from models import Base, User


def create_admin():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Get DB session
    db = next(get_db())

    # Check if admin already exists
    admin_email = "admin@hobbyhosting.org"
    if db.query(User).filter(User.username == admin_email).first():
        print(f"Admin user {admin_email} already exists")
        return

    # Create admin user
    admin = User(
        username=admin_email,
        hashed_password=hash_password("supersecret123"),
        is_admin=True,
    )

    db.add(admin)
    db.commit()
    print(f"Created admin user: {admin_email}")


if __name__ == "__main__":
    create_admin()
