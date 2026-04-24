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


def vacancy_keyboard(vacancies):
    buttons = [
        [InlineKeyboardButton(
            text=vacancy["title"],
            callback_data=f"vac_{vacancy['id']}"
        )]
        for vacancy in vacancies
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)