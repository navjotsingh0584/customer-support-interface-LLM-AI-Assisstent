from app.services.database import Database
from app.auth.password import hash_password, verify_password


class UserService:


    def __init__(self):

        self.db = Database()



    def create_user(
        self,
        username,
        password,
        role="user"
    ):


        hashed = hash_password(
            password
        )


        self.db.cursor.execute(

            """
            INSERT INTO users
            (
            username,
            password,
            role
            )

            VALUES (?,?,?)

            """,

            (
                username,
                hashed,
                role
            )

        )


        self.db.connection.commit()



        return True



    def authenticate(
        self,
        username,
        password
    ):


        self.db.cursor.execute(

            """
            SELECT username,password
            FROM users
            WHERE username=?

            """,

            (username,)

        )


        user = self.db.cursor.fetchone()



        if not user:
            return False



        return verify_password(
            password,
            user[1]
        )