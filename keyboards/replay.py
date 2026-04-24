from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from texts import t


def _kb(buttons: list[str], row: int = 2) -> ReplyKeyboardMarkup:
    rows, current = [], []
    for i, text in enumerate(buttons):
        current.append(KeyboardButton(text=text))
        if (i + 1) % row == 0:
            rows.append(current)
            current = []
    if current:
        rows.append(current)
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


# --- Til tanlash ---
def language_keyboard() -> ReplyKeyboardMarkup:
    return _kb(["🇺🇿 O'zbek", "🇷🇺 Русский"])


# --- Asosiy menyu ---
def main_menu(lang: str, is_admin: bool = False) -> ReplyKeyboardMarkup:
    buttons = [
        t("menu_about", lang),
        t("menu_vacancies", lang)
    ]

    # 🔥 ADMIN tugma (nom bir xil!)
    if is_admin:
        buttons.append("📋 Ishlarni boshqarish")

    return _kb(buttons, row=1)


# --- ADMIN MENU (optional, lekin hozir ishlatmaymiz) ---
def admin_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Ish o‘rni qo‘shish")],
            [KeyboardButton(text="❌ Ish o‘rni o‘chirish")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )

# --- Anketa klaviaturalari ---
def gender_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return _kb([t("gender_male", lang), t("gender_female", lang)])


def marital_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return _kb([t("marital_married", lang), t("marital_single", lang)])


def education_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return _kb(
        [t("edu_student", lang), t("edu_secondary", lang), t("edu_higher", lang)],
        row=1
    )


def uzbek_lang_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return _kb([t("lang_free", lang), t("lang_medium", lang)])


def russian_lang_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return _kb([t("lang_free", lang), t("lang_medium", lang), t("lang_no", lang)])


def source_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return _kb(
        [t("source_telegram", lang), t("source_instagram", lang), t("source_friend", lang),t("source_other", lang)],
    )


def privacy_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return _kb([t("privacy_yes", lang), t("privacy_no", lang)])


def yes_no_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return _kb([t("yes", lang), t("no", lang)])


def confirm_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return _kb([t("confirm_prompt", lang), t("cancel_prompt", lang)])


def education_main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return _kb([t("kunduzgi", lang), t("kechgi", lang), t("sirtqi", lang)])


def exp_keyboard(lang: str):
    return _kb([t("no", lang)])


def maosh_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return _kb(
        [
            t("1,8mln - 2,5 mln", lang),
            t("2,5mln - 4 mln", lang),
            t("4mln va yuqori", lang)
        ]
    )
