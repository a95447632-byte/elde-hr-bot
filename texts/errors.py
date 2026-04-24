error_texts = {

    # ── TUGMA / INPUT ────────────────────────────────────────────────────────
    "err_button": {
        "uz": "❗ Iltimos, tugmalardan birini tanlang",
        "ru": "❗ Пожалуйста, выберите одну из кнопок"
    },
    "err_input": {
        "uz": "❌ Iltimos, maydonni to'g'ri to'ldiring",
        "ru": "❌ Пожалуйста, заполните поле корректно"
    },

    # ── FOYDALANUVCHI MA'LUMOTLARI ───────────────────────────────────────────
    "err_fullname": {
        "uz": "❌ Ism familiyangizni to'g'ri kiriting (kamida 2 so'z)",
        "ru": "❌ Введите имя и фамилию корректно (минимум 2 слова)"
    },
    "err_phone": {
        "uz": "❌ Telefon raqamni to'g'ri kiriting (+998XXXXXXXXX)",
        "ru": "❌ Введите номер телефона корректно (+998XXXXXXXXX)"
    },
    "err_birthdate": {
        "uz": "❌ Tug'ilgan sanani to'g'ri kiriting (DD.MM.YYYY)",
        "ru": "❌ Введите дату рождения корректно (ДД.ММ.ГГГГ)"
    },
    "err_photo": {
        "uz": "❌ Iltimos, rasm yuboring",
        "ru": "❌ Пожалуйста, отправьте фото"
    },

    # ── TOPILMADI ────────────────────────────────────────────────────────────
    "branch_not_found": {
        "uz": "❌ Filial topilmadi",
        "ru": "❌ Филиал не найден"
    },
    "vacancy_not_found": {
        "uz": "❌ Vakansiya topilmadi",
        "ru": "❌ Вакансия не найдена"
    },
    "no_vacancies": {
        "uz": "❌ Hozircha bo'sh ish o'rinlari yo'q",
        "ru": "❌ Пока нет доступных вакансий"
    },

    # ── UMUMIY XATO ──────────────────────────────────────────────────────────
    "error_general": {
        "uz": "❌ Xatolik yuz berdi, qaytadan urinib ko'ring",
        "ru": "❌ Произошла ошибка, попробуйте снова"
    },
}


def t_error(key, lang="uz"):
    data = error_texts.get(key)
    if not data:
        return "❌ Xatolik" if lang == "uz" else "❌ Ошибка"
    return data.get(lang) or data.get("uz") or "❌ Xatolik"