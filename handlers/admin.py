from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from state import AdminState, AppState
from db.queries import get_all_branches, get_all_vacancies_with_status
from db.connection import get_connection
from keyboards.inline import branch_keyboard
from keyboards.replay import main_menu

router = Router()


# ── ADMIN START ─────────────────────────────────────
@router.message(F.text == "📋 Ishlarni boshqarish")
async def admin_start(msg: Message, state: FSMContext):
    if msg.from_user.id != ADMIN_ID:
        return

    branches = get_all_branches()  # 🔥 MUHIM

    if not branches:
        await msg.answer("❌ Filiallar yo‘q")
        return

    await state.set_state(AdminState.branch)

    await msg.answer(
        "🏢 Filial tanlang:",
        reply_markup=branch_keyboard(branches)
    )


# ── BRANCH SELECT ───────────────────────────────────
@router.callback_query(AdminState.branch, F.data.startswith("branch_"))
async def admin_branch_selected(call: CallbackQuery, state: FSMContext):
    branch_id = int(call.data.split("_")[1])

    await state.update_data(branch_id=branch_id)
    await state.set_state(AdminState.vacancy)

    vacancies = get_all_vacancies_with_status(branch_id)

    buttons = []

    for vac in vacancies:
        status = "🟢" if vac["is_active"] == 1 else "🔴"

        buttons.append([
            InlineKeyboardButton(
                text=f"{status} {vac['title_uz']}",
                callback_data=f"admin_vac_{vac['id']}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_back")
    ])

    await call.message.answer(
        "🧑‍💼 Ish o‘rinlarini boshqaring:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

    await call.answer()


# ── TOGGLE ──────────────────────────────────────────
@router.callback_query(AdminState.vacancy, F.data.startswith("admin_vac_"))
async def admin_toggle(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    branch_id = data.get("branch_id")

    if not branch_id:
        await call.answer("❌ Xatolik")
        return

    vacancy_id = int(call.data.split("_")[2])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    cursor.execute("""
        SELECT is_active
        FROM branch_vacancies
        WHERE branch_id = %s AND vacancy_id = %s
    """, (branch_id, vacancy_id))

    row = cursor.fetchone()

    if not row:
        await call.answer("❌ DB da yo‘q")
        conn.close()
        return

    new_status = 0 if row["is_active"] == 1 else 1

    cursor.execute("""
        UPDATE branch_vacancies
        SET is_active = %s
        WHERE branch_id = %s AND vacancy_id = %s
    """, (new_status, branch_id, vacancy_id))

    conn.commit()
    conn.close()

    await call.message.answer(
        "🟢 Yoqildi" if new_status else "🔴 O‘chirildi"
    )

    await call.answer()


# ── BACK ────────────────────────────────────────────
@router.callback_query(F.data == "admin_back")
async def admin_back(call: CallbackQuery, state: FSMContext):
    await state.set_state(AppState.menu)

    await call.message.answer(
        "🏠 Asosiy menyu",
        reply_markup=main_menu("uz", is_admin=True)
    )

    await call.answer()