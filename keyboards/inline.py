from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def branch_keyboard(branches):
    buttons = [
        [InlineKeyboardButton(
            text=branch["name"],
            callback_data=f"branch_{branch['id']}"
        )]
        for branch in branches
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def vacancy_keyboard(vacancies, lang):
    buttons = [
        [InlineKeyboardButton(
            # Bazadan 'title_uz' emas, shunchaki 'title' kaliti kelyapti.
            # Tillarni saralash ishini SQL'ning o'zi (db/queries.py) bajarib bo'lgan!
            text=vacancy["title"], 
            callback_data=f"vac_{vacancy['id']}"
        )]
        for vacancy in vacancies
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)