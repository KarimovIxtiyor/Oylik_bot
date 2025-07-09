from config import DB_CONFIG
import psycopg2
from psycopg2 import OperationalError

def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except OperationalError as e:
        print("PostgreSQL ulanish xatosi:")
        print(e)
        raise


# Bazani yaratish va foydalanuvchilar jadvalini tayyorlash
def create_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            language TEXT,
            name TEXT,
            surname TEXT,
            phone TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Foydalanuvchini bazaga qo'shish
def add_user(user_id, language):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, language)
        VALUES (%s, %s)
        ON CONFLICT (user_id) DO NOTHING
    """, (user_id, language))
    conn.commit()
    cursor.close()
    conn.close()

# Foydalanuvchining ism, familiya va telefonini yangilash
def update_user(user_id, field, value):
    if field not in ['name', 'surname', 'phone']:
        raise ValueError("Noto‘g‘ri ustun nomi!")
    conn = get_connection()
    cursor = conn.cursor()
    query = f"UPDATE users SET {field} = %s WHERE user_id = %s"
    cursor.execute(query, (value, user_id))
    conn.commit()
    cursor.close()
    conn.close()

# Foydalanuvchi ro'yxatdan o'tganmi, tekshirish
def is_registered(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, surname, phone FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return bool(result and all(result))

# Foydalanuvchi haqida ma'lumot olish
def get_user_info(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, surname, phone FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# Foydalanuvchining tilini olish
def get_user_language(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else "uz"

# Foydalanuvchining ismini olish
def get_name_by_user_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

# Barcha foydalanuvchi ID larini olish
def get_all_user_ids():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in results]

# Muayyan til bo‘yicha foydalanuvchilarni olish
def get_users_by_language(language_code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE language = %s", (language_code,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in results]
