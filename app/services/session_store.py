from datetime import datetime
from app.services.database import Database
import json


class SessionStore:

    def __init__(self):

        self.db = Database()


    # =========================
    # MESSAGES
    # =========================

    def add_message(
        self,
        session_id,
        role,
        message
    ):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages
            (
                session_id,
                role,
                message,
                timestamp
            )

            VALUES (?, ?, ?, ?)

            """,

            (
                session_id,
                role,
                message,
                datetime.now().isoformat()
            )
        )

        self.db.conn.commit()



    def get_history(
        self,
        session_id
    ):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT
                role,
                message,
                timestamp

            FROM messages

            WHERE session_id=?

            ORDER BY id

            """,

            (session_id,)
        )


        rows = cursor.fetchall()


        return [

            {
                "role": row[0],
                "message": row[1],
                "timestamp": row[2]
            }

            for row in rows

        ]



    def clear_session(
        self,
        session_id
    ):

        cursor = self.db.conn.cursor()


        cursor.execute(
            """
            DELETE FROM messages

            WHERE session_id=?

            """,

            (session_id,)
        )


        cursor.execute(
            """
            DELETE FROM uploaded_files

            WHERE session_id=?

            """,

            (session_id,)
        )


        self.db.conn.commit()



    # =========================
    # FILE STORAGE
    # =========================

    def save_uploaded_file(
        self,
        session_id,
        filename,
        file_type,
        content,
        stored_filename=None
    ):

        cursor = self.db.conn.cursor()


        cursor.execute(
            """
            INSERT INTO uploaded_files
            (
                session_id,
                filename,
                stored_filename,
                file_type,
                content,
                created_at
            )

            VALUES (?, ?, ?, ?, ?, ?)

            """,

            (
                session_id,
                filename,
                stored_filename,
                file_type,
                content,
                datetime.now().isoformat()
            )
        )


        self.db.conn.commit()



    def get_uploaded_files(
        self,
        session_id
    ):

        cursor = self.db.conn.cursor()


        cursor.execute(
            """
            SELECT

                filename,
                stored_filename,
                file_type,
                content,
                created_at

            FROM uploaded_files

            WHERE session_id=?

            ORDER BY id DESC

            """,

            (session_id,)
        )


        rows = cursor.fetchall()


        files = []


        for row in rows:

            files.append(

                {

                    "filename": row[0],

                    "stored_filename": row[1],

                    "file_type": row[2],

                    "content": row[3],

                    "created_at": row[4]

                }

            )


        return files



    # =========================
    # VISION FILES
    # =========================

    def get_vision_files(
        self,
        session_id
    ):


        files = self.get_uploaded_files(
            session_id
        )


        vision_files = []


        for f in files:


            if f["file_type"] != "image":

                continue


            try:

                f["content"] = json.loads(
                    f["content"]
                )


                vision_files.append(f)


            except Exception as e:

                print(
                    "VISION JSON ERROR:",
                    e
                )


        return vision_files



    def get_latest_uploaded_file(
        self,
        session_id
    ):


        files = self.get_uploaded_files(
            session_id
        )


        if not files:

            return None


        return files[0]