from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from state import AppState, ResumeState
from texts import t
from keyboards.replay import language_keyboard, main_menu
from keyboards.inline import branch_keyboard
from db.queries import get_branches
from config import ADMIN_ID

router = Router()


# ── /start ─────────────────────────────
@router.message(Command("start"))
async def cmd_start(msg: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AppState.language)

    await msg.answer(
        t("choose_language"),
        reply_markup=language_keyboard()
    )


# ── Til tanlash ────────────────────────
@router.message(AppState.language, F.text.in_(["🇺🇿 O'zbek", "🇷🇺 Русский"]))
async def choose_language(msg: Message, state: FSMContext):
    lang = "uz" if "O'zbek" in msg.text else "ru"

    await state.update_data(lang=lang)
    await state.set_state(AppState.menu)

    # 🔥 ADMIN CHECK
    if msg.from_user.id == ADMIN_ID:
        await msg.answer(
            "🔐 Admin panelga xush kelibsiz",
            reply_markup=main_menu(lang, is_admin=True)  # 🔥 MUHIM
        )
    else:
        await msg.answer(
            t("welcome", lang),
            reply_markup=main_menu(lang)
        )


# ── ABOUT ─────────────────────────────
from aiogram.filters import StateFilter
from aiogram.types import FSInputFile
@router.message(StateFilter("*"), F.text.func(lambda t: "Biz haqimizda" in t or "О нас" in t))
async def about_handler(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await state.clear()

    photo = FSInputFile("texts/assets/elde.png")

    # 🔥 1. RASM (qisqa caption bilan)
    await msg.answer_photo(
        photo=photo,
        caption="🏢 ELDE kompaniyasi"
    )

    # 🔥 2. UZUN TEXT ALohida
    await msg.answer(t("about", lang))
# ── VACANCIES ─────────────────────────
@router.message(StateFilter("*"), F.text.func(lambda t: "Vakansiya" in t or "Вакансии" in t))
async def vacancies_handler(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await state.clear()  # 🔥 MUHIM
    await state.set_state(ResumeState.branch)

    branches = get_branches(lang)

    if not branches:
        await msg.answer("❌ Filiallar topilmadi")
        return

    await msg.answer(
        t("choose_branch", lang),
        reply_markup=branch_keyboard(branches)
    )