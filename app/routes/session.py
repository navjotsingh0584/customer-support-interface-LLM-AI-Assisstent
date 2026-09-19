from fastapi import APIRouter, Depends, HTTPException

from app.services.database import Database
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/api"
)


db = Database()


import uuid
from fastapi import APIRouter

router = APIRouter(prefix="/api")

# =========================
# CREATE NEW SESSION (NEW ADDITION)
# =========================
@router.get("/session/new")
def create_session():

    return {
        "session_id": str(uuid.uuid4())
    }
# -----------------------------
# GET ALL CHAT SESSIONS
# -----------------------------

@router.get("/sessions")
def get_sessions(
    user=Depends(get_current_user)
):

    query = """

    SELECT
session_id,
MAX(timestamp),
(
SELECT message
FROM messages m2
WHERE m2.session_id=m1.session_id
AND role='user'
ORDER BY timestamp ASC
LIMIT 1
)

FROM messages m1

GROUP BY session_id

ORDER BY MAX(timestamp) DESC

    """


    rows = db.conn.execute(
        query
    ).fetchall()



    return [

        {
            "session_id": row[0],
            "last_time": row[1],
            "title":row[2][:25]
        }

        for row in rows

    ]




# -----------------------------
# GET SINGLE CHAT HISTORY
# -----------------------------

@router.get("/sessions/{session_id}")
def get_session(

    session_id: str,

    user=Depends(get_current_user)

):


    query = """

    SELECT 
        role,
        message,
        timestamp

    FROM messages

    WHERE session_id=?

    ORDER BY timestamp ASC

    """


    rows = db.conn.execute(

        query,

        (session_id,)

    ).fetchall()



    return [

        {

            "role": row[0],

            "message": row[1],

            "timestamp": row[2]

        }

        for row in rows

    ]





# -----------------------------
# DELETE CHAT SESSION
# -----------------------------

@router.delete("/sessions/{session_id}")
def delete_session(

    session_id: str,

    user=Depends(get_current_user)

):


    # check exists

    check = db.conn.execute(

        """
        SELECT session_id
        FROM messages
        WHERE session_id=?
        LIMIT 1
        """,

        (session_id,)

    ).fetchone()



    if check is None:

        raise HTTPException(

            status_code=404,

            detail="Chat session not found"

        )



    db.conn.execute(

        """
        DELETE FROM messages
        WHERE session_id=?
        """,

        (session_id,)

    )


    db.conn.commit()



    return {

        "status": "success",

        "deleted_session": session_id

    }