import sqlite3
from datetime import datetime


class Database:

    def __init__(self):

        self.conn = sqlite3.connect(
            "support_bot.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        # =========================
        # CORE TABLES
        # =========================

        self.create_messages_table()
        self.create_users_table()

        # Uploaded files table
        self.create_uploaded_files_table()

        # Safe migration
        self.add_stored_filename_column()


    # =========================
    # MESSAGES TABLE
    # =========================

    def create_messages_table(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                session_id TEXT NOT NULL,

                role TEXT NOT NULL,

                message TEXT NOT NULL,

                timestamp TEXT NOT NULL

            )
            """
        )

        self.conn.commit()



    # =========================
    # USERS TABLE
    # =========================

    def create_users_table(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE NOT NULL,

                password TEXT NOT NULL,

                role TEXT DEFAULT 'user'

            )
            """
        )

        self.conn.commit()



    # =========================
    # UPLOADED FILES TABLE
    # =========================

    def create_uploaded_files_table(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS uploaded_files (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                session_id TEXT NOT NULL,

                filename TEXT NOT NULL,

                stored_filename TEXT,

                file_type TEXT NOT NULL,

                content TEXT NOT NULL,

                created_at TEXT NOT NULL

            )
            """
        )

        self.conn.commit()



    # =========================
    # SAFE DATABASE MIGRATION
    # =========================

    def add_stored_filename_column(self):

        self.cursor.execute(
            """
            PRAGMA table_info(uploaded_files)
            """
        )

        columns = [
            row[1]
            for row in self.cursor.fetchall()
        ]


        if "stored_filename" not in columns:

            self.cursor.execute(
                """
                ALTER TABLE uploaded_files
                ADD COLUMN stored_filename TEXT
                """
            )

            self.conn.commit()



    # =========================
    # MESSAGE STORAGE
    # =========================

    def save_message(
        self,
        session_id,
        role,
        message
    ):

        self.cursor.execute(
            """
            INSERT INTO messages
            (
                session_id,
                role,
                message,
                timestamp
            )
            VALUES (?,?,?,?)
            """,
            (
                session_id,
                role,
                message,
                datetime.now().isoformat()
            )
        )

        self.conn.commit()



    # =========================
    # MESSAGE RETRIEVAL
    # =========================

    def get_messages(
        self,
        session_id
    ):

        self.cursor.execute(
            """
            SELECT role, message, timestamp
            FROM messages
            WHERE session_id=?
            ORDER BY id
            """,
            (session_id,)
        )

        rows = self.cursor.fetchall()


        return [

            {
                "role": row[0],
                "message": row[1],
                "timestamp": row[2]
            }

            for row in rows

        ]



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

        self.cursor.execute(
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


        self.conn.commit()



    # =========================
    # GET FILES
    # =========================

    def get_uploaded_files(
        self,
        session_id
    ):

        self.cursor.execute(
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


        rows = self.cursor.fetchall()


        return [

            {

                "filename": row[0],

                "stored_filename": row[1],

                "file_type": row[2],

                "content": row[3],

                "created_at": row[4]

            }

            for row in rows

        ]



    # =========================
    # USER FUNCTIONS
    # =========================

    def create_user(
        self,
        username,
        password,
        role="user"
    ):

        self.cursor.execute(
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
                password,
                role
            )
        )


        self.conn.commit()



    def get_user(
        self,
        username
    ):

        self.cursor.execute(
            """
            SELECT username, password, role

            FROM users

            WHERE username=?

            """,

            (username,)
        )


        return self.cursor.fetchone()