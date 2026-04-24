from db.connection import get_connection


def get_branches(lang="uz"):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    name_field = "name_uz" if lang == "uz" else "name_ru"

    cursor.execute(f"""
        SELECT b.id, b.{name_field} AS name, b.lat, b.lon
        FROM branches b
    """)

    result = cursor.fetchall()
    conn.close()
    return result


def get_branch_by_id(branch_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name_uz, name_ru, lat, lon
        FROM branches
        WHERE id = %s
    """, (branch_id,))

    result = cursor.fetchone()
    conn.close()
    return result


def get_vacancies_by_branch(branch_id, lang="uz"):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    title_field = "title_uz" if lang == "uz" else "title_ru"

    cursor.execute(f"""
        SELECT 
            v.id,
            v.{title_field} AS title,
            MAX(COALESCE(bv.is_active, 0)) AS is_active
        FROM vacancies v
        LEFT JOIN branch_vacancies bv 
            ON v.id = bv.vacancy_id AND bv.branch_id = %s
        GROUP BY v.id, v.{title_field}
    """, (branch_id,))

    result = cursor.fetchall()
    conn.close()
    return result

def get_vacancy_by_id(vacancy_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, title_uz, title_ru
        FROM vacancies
        WHERE id = %s
    """, (vacancy_id,))

    result = cursor.fetchone()
    conn.close()
    return result



def get_all_branches():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name_uz AS name
        FROM branches
    """)

    result = cursor.fetchall()
    conn.close()
    return result


def get_all_vacancies_with_status(branch_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            v.id,
            v.title_uz,
            MAX(COALESCE(bv.is_active, 0)) AS is_active
        FROM vacancies v
        LEFT JOIN branch_vacancies bv
            ON v.id = bv.vacancy_id AND bv.branch_id = %s
        GROUP BY v.id, v.title_uz
    """, (branch_id,))

    result = cursor.fetchall()
    conn.close()
    return result