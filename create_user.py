from app.services.database import Database
from app.auth.password import hash_password


db = Database()


username = "admin"

password = "admin123"


hashed = hash_password(
    password
)


try:

    db.create_user(
        username,
        hashed,
        "admin"
    )


    print("USER CREATED")

    print(
        "Username:",
        username
    )

    print(
        "Password:",
        password
    )


except Exception as e:

    print(
        "ERROR:",
        e
    )