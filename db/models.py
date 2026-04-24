from db.connection import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # 🏢 FILIALLAR
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS branches (
        id INT AUTO_INCREMENT PRIMARY KEY,
        `key` VARCHAR(50) UNIQUE,
        name_uz VARCHAR(255),
        name_ru VARCHAR(255),
        lat DOUBLE,
        lon DOUBLE
    );
    """)

    # 💼 VAKANSIYALAR
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacancies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        `key` VARCHAR(50) UNIQUE,
        title_uz VARCHAR(255),
        title_ru VARCHAR(255)
    );
    """)

    # 🔗 BOG‘LOVCHI TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS branch_vacancies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        branch_id INT,
        vacancy_id INT,
        is_active TINYINT(1) DEFAULT 0,

        FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE CASCADE,
        FOREIGN KEY (vacancy_id) REFERENCES vacancies(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()