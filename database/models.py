from database.db import get_connection

def save_lead(phone, interest):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO leads (phone, interest)
    VALUES (%s,%s)
    """

    cursor.execute(query,(phone,interest))
    conn.commit()

    cursor.close()
    conn.close()


def get_user(phone):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE phone=%s"

    cursor.execute(query,(phone,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user
