from db.connection import get_connection
from config import BRANCHES, VACANCIES

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # 🔹 1. BRANCHES qo‘shish
    for key, branch in BRANCHES.items():
        cursor.execute("""
        INSERT IGNORE INTO branches (`key`, name_uz, name_ru, lat, lon)
        VALUES (%s, %s, %s, %s, %s)
        """, (
            key,
            branch["name_uz"],   # ✅ to‘g‘rilandi
            branch["name_ru"],   # ✅ to‘g‘rilandi
            branch["lat"],
            branch["lon"]
        ))

    # 🔹 2. VACANCIES qo‘shish
    for key, vac in VACANCIES.items():
        cursor.execute("""
        INSERT IGNORE INTO vacancies (`key`, title_uz, title_ru)
        VALUES (%s, %s, %s)
        """, (
            key,
            vac["title_uz"],   # ⚠️ sen ham buni o‘zgartirgansan
            vac["title_ru"]
        ))

    # 🔹 3. IDlarni olish
    cursor.execute("SELECT id FROM branches")
    branch_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM vacancies")
    vacancy_ids = [row[0] for row in cursor.fetchall()]

    # 🔹 4. bog‘lash
    for b_id in branch_ids:
        for v_id in vacancy_ids:
            cursor.execute("""
            INSERT IGNORE INTO branch_vacancies (branch_id, vacancy_id, is_active)
            VALUES (%s, %s, 0)
            """, (b_id, v_id))

    conn.commit()
    conn.close()