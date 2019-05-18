import sqlite3


def init_db():
    """Initializes the notes database"""
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS notes (
                    title text,
                    note text,
                    time_stamp text
                    )""")
    conn.commit()
    conn.close()
