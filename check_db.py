import sqlite3


conn = sqlite3.connect("support_bot.db")

cursor = conn.cursor()


cursor.execute(
    """
    SELECT
        filename,
        stored_filename,
        file_type,
        created_at
    FROM uploaded_files
    ORDER BY id DESC
    LIMIT 5
    """
)


rows = cursor.fetchall()


print("TOTAL FILES:", len(rows))


for row in rows:

    print("----------------------")
    print("Original File :", row[0])
    print("Stored File   :", row[1])
    print("Type          :", row[2])
    print("Created       :", row[3])


conn.close()