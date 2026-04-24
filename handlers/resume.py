import os
from datetime import datetime
from aiogram.types import FSInputFile
from db.queries import get_branch_by_id, get_vacancies_by_branch, get_vacancy_by_id
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from config import ADMIN_ID,chat_id
from state import ResumeState
from texts.errors import t_error as te   # faqat xato matnlari uchun
from texts import t                # UI matnlari uchun (savol, tugma, xulosa)
from keyboards.replay import (
    gender_keyboard, marital_keyboard, education_keyboard,
    uzbek_lang_keyboard, russian_lang_keyboard,
    source_keyboard, privacy_keyboard, yes_no_keyboard, confirm_keyboard, exp_keyboard, maosh_keyboard
)
from keyboards.inline import vacancy_keyboard
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
    


router = Router()


async def _lang(state: FSMContext) -> str:
    data = await state.get_data()
    return data.get("lang", "uz")


# ── Filial tanlash ────────────────────────────────────────────────────────────
@router.callback_query(ResumeState.branch)
async def branch_selected(call: CallbackQuery, state: FSMContext):
    lang = await _lang(state)

    if not call.data or not call.data.startswith("branch_"):
        await call.answer(te("err_button", lang))
        return

    try:
        branch_id = int(call.data.split("_")[1])
    except (IndexError, ValueError):
        await call.answer(te("err_input", lang))
        return

    branch = get_branch_by_id(branch_id)
    if not branch:
        await call.answer(te("branch_not_found", lang))
        return

    name = branch["name_uz"] if lang == "uz" else branch["name_ru"]
    await state.update_data(branch_id=branch_id, branch_name=name)

    try:
        await call.message.answer_location(latitude=branch["lat"], longitude=branch["lon"])
    except Exception:
        pass

    await call.message.answer(f"📍 {name}")

    vacancies = get_vacancies_by_branch(branch_id, lang)
    if not vacancies:
        await call.message.answer(te("no_vacancies", lang))
        await call.answer()
        return

    await state.set_state(ResumeState.vacancy)
    await call.message.answer(t("choose_vacancy", lang), reply_markup=vacancy_keyboard(vacancies))
    await call.answer()


# ── Vakansiya tanlash ─────────────────────────────────────────────────────────
@router.callback_query(ResumeState.vacancy)
async def vacancy_selected(call: CallbackQuery, state: FSMContext):
    lang = await _lang(state)

    if not call.data or not call.data.startswith("vac_"):
        await call.answer(te("error_general", lang))
        return

    try:
        vacancy_id = int(call.data.split("_")[1])
    except (IndexError, ValueError):
        await call.answer(te("err_input", lang))
        return

    vacancy = get_vacancy_by_id(vacancy_id)
    if not vacancy:
        await call.answer(te("vacancy_not_found", lang))
        return

    vacancy_name = vacancy["title_uz"] if lang == "uz" else vacancy["title_ru"]
    await state.update_data(vacancy_id=vacancy_id, vacancy_name=vacancy_name)
    await state.set_state(ResumeState.fullname)
    await call.message.answer(t("ask_fullname", lang))
    await call.answer()


# ── Shaxsiy ma'lumotlar ───────────────────────────────────────────────────────
@router.message(ResumeState.fullname)
async def get_fullname(msg: Message, state: FSMContext):
    lang = await _lang(state)
    fullname = (msg.text or "").strip()

    if not fullname or len(fullname.split()) < 2:
        await msg.answer(te("err_fullname", lang))
        return
    if any(len(p) < 2 for p in fullname.split()):
        await msg.answer(te("err_fullname", lang))
        return
    if not all(p.replace("'", "").isalpha() for p in fullname.split()):
        await msg.answer(te("err_fullname", lang))
        return

    await state.update_data(fullname=fullname)
    await state.set_state(ResumeState.address)
    await msg.answer(t("ask_address", lang))


@router.message(ResumeState.address)
async def get_address(msg: Message, state: FSMContext):
    lang = await _lang(state)
    address = (msg.text or "").strip()

    if not address:
        await msg.answer(te("err_input", lang))
        return

    await state.update_data(address=address)
    await state.set_state(ResumeState.phone)
    await msg.answer(t("ask_phone", lang))


@router.message(ResumeState.phone)
async def get_phone(msg: Message, state: FSMContext):
    lang = await _lang(state)
    phone = (msg.text or "").strip().replace(" ", "").replace("-", "")

    if not phone or not phone.startswith("+998") or len(phone) != 13 or not phone[1:].isdigit():
        await msg.answer(te("err_phone", lang))
        return

    await state.update_data(phone=phone)
    await state.set_state(ResumeState.birthdate)
    await msg.answer(t("ask_birthdate", lang))


@router.message(ResumeState.birthdate)
async def get_birthdate(msg: Message, state: FSMContext):
    lang = await _lang(state)
    date_text = (msg.text or "").strip()
    parts = date_text.split(".")

    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        await msg.answer(te("err_birthdate", lang))
        return

    day, month, year = int(parts[0]), int(parts[1]), int(parts[2])

    if year < 1960 or year > 2020:
        await msg.answer(te("err_birthdate", lang))
        return

    try:
        datetime(year, month, day)
    except ValueError:
        await msg.answer(te("err_birthdate", lang))
        return

    await state.update_data(birthdate=date_text)
    await state.set_state(ResumeState.gender)
    await msg.answer(t("ask_gender", lang), reply_markup=gender_keyboard(lang))


@router.message(ResumeState.gender)
async def get_gender(msg: Message, state: FSMContext):
    lang = await _lang(state)
    valid = [t("gender_male", lang), t("gender_female", lang)]

    if not msg.text or msg.text not in valid:
        await msg.answer(te("err_button", lang), reply_markup=gender_keyboard(lang))
        return

    await state.update_data(gender=msg.text)
    await state.set_state(ResumeState.marital)
    await msg.answer(t("ask_marital", lang), reply_markup=marital_keyboard(lang))


@router.message(ResumeState.marital)
async def get_marital(msg: Message, state: FSMContext):
    lang = await _lang(state)
    valid = [t("marital_married", lang), t("marital_single", lang)]

    if not msg.text or msg.text not in valid:
        await msg.answer(te("err_button", lang), reply_markup=marital_keyboard(lang))
        return

    await state.update_data(marital=msg.text)
    await state.set_state(ResumeState.education)
    await msg.answer(t("ask_education", lang), reply_markup=education_keyboard(lang))


# ── Ta'lim ────────────────────────────────────────────────────────────────────
@router.message(ResumeState.education)
async def get_education_all(msg: Message, state: FSMContext):
    lang = await _lang(state)
    valid = [t("edu_student", lang), t("edu_secondary", lang), t("edu_higher", lang)]

    if not msg.text or msg.text not in valid:
        await msg.answer(te("err_button", lang), reply_markup=education_keyboard(lang))
        return

    await state.update_data(education=msg.text)
    await state.set_state(ResumeState.exp_org)
    await msg.answer(t("ask_exp_org", lang), reply_markup=exp_keyboard(lang))


# ── Ish tajribasi ─────────────────────────────────────────────────────────────
@router.message(ResumeState.exp_org)
async def get_exp_org(msg: Message, state: FSMContext):
    lang = await _lang(state)
    text = (msg.text or "").strip()
    no_text = t("no", lang)

    if text == no_text:
        await state.update_data(exp_org=no_text, exp_pos=no_text, exp_period=no_text)
        await state.set_state(ResumeState.uzbek)
        await msg.answer(t("ask_uzbek", lang), reply_markup=uzbek_lang_keyboard(lang))
        return

    if not text:
        await msg.answer(te("err_input", lang), reply_markup=exp_keyboard(lang))
        return

    await state.update_data(exp_org=text)
    await state.set_state(ResumeState.exp_pos)
    await msg.answer(t("ask_exp_pos", lang))


@router.message(ResumeState.exp_pos)
async def get_exp_pos(msg: Message, state: FSMContext):
    lang = await _lang(state)
    text = (msg.text or "").strip()

    if not text:
        await msg.answer(te("err_input", lang))
        return

    await state.update_data(exp_pos=text)
    await state.set_state(ResumeState.exp_period)
    await msg.answer(t("ask_exp_period", lang))


@router.message(ResumeState.exp_period)
async def get_exp_period(msg: Message, state: FSMContext):
    lang = await _lang(state)
    text = (msg.text or "").strip()

    if not text:
        await msg.answer(te("err_input", lang))
        return

    await state.update_data(exp_period=text)
    await state.set_state(ResumeState.uzbek)
    await msg.answer(t("ask_uzbek", lang), reply_markup=uzbek_lang_keyboard(lang))


# ── Til bilimi ────────────────────────────────────────────────────────────────
@router.message(ResumeState.uzbek)
async def get_uzbek(msg: Message, state: FSMContext):
    lang = await _lang(state)
    valid = [t("lang_free", lang), t("lang_medium", lang)]

    if not msg.text or msg.text not in valid:
        await msg.answer(te("err_button", lang), reply_markup=uzbek_lang_keyboard(lang))
        return

    await state.update_data(uzbek=msg.text)
    await state.set_state(ResumeState.russian)
    await msg.answer(t("ask_russian", lang), reply_markup=russian_lang_keyboard(lang))


@router.message(ResumeState.russian)
async def get_russian(msg: Message, state: FSMContext):
    lang = await _lang(state)
    valid = [t("lang_free", lang), t("lang_medium", lang), t("lang_no", lang)]

    if not msg.text or msg.text not in valid:
        await msg.answer(te("err_button", lang), reply_markup=russian_lang_keyboard(lang))
        return

    await state.update_data(russian=msg.text)
    await state.set_state(ResumeState.salary)
    await msg.answer(t("ask_salary", lang), reply_markup=maosh_keyboard(lang))


# ── Maosh ─────────────────────────────────────────────────────────────────────
SALARY_OPTIONS = {
    "uz": ["1,8mln - 2,5 mln", "2,5mln - 4 mln", "4mln va yuqori"],
    "ru": ["1,8млн - 2,5 млн", "2,5млн - 4 млн", "4млн и выше"]
}

@router.message(ResumeState.salary)
async def get_salary(msg: Message, state: FSMContext):
    lang = await _lang(state)
    text = (msg.text or "").strip()

    

    await state.update_data(salary=text)
    await state.set_state(ResumeState.photo)
    await msg.answer(t("ask_photo", lang))


# ── Rasm ──────────────────────────────────────────────────────────────────────
@router.message(ResumeState.photo, F.photo)
async def get_photo(msg: Message, state: FSMContext, bot: Bot):
    lang = await _lang(state)

    if not msg.photo:
        await msg.answer(te("err_photo", lang))
        return

    photo = msg.photo[-1]
    os.makedirs("photos", exist_ok=True)
    file = await bot.get_file(photo.file_id)
    path = f"photos/{msg.from_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    await bot.download_file(file.file_path, path)

    await state.update_data(photo_path=path)
    await state.set_state(ResumeState.source)
    await msg.answer(t("ask_source", lang), reply_markup=source_keyboard(lang))


# ── Manba ─────────────────────────────────────────────────────────────────────
@router.message(ResumeState.source)
async def get_source(msg: Message, state: FSMContext):
    lang = await _lang(state)
    valid = [t("source_telegram", lang), t("source_instagram", lang), t("source_friend", lang),t("source_other", lang)]

    if not msg.text or msg.text not in valid:
        await msg.answer(te("err_button", lang), reply_markup=source_keyboard(lang))
        return

    await state.update_data(source=msg.text)
    await state.set_state(ResumeState.privacy)
    await msg.answer(t("ask_privacy", lang), reply_markup=privacy_keyboard(lang))


# ── Maxfiylik ─────────────────────────────────────────────────────────────────
 
@router.message(ResumeState.privacy)
async def get_privacy(msg: Message, state: FSMContext):
    lang = await _lang(state)
    yes = t("privacy_yes", lang)
    no = t("privacy_no", lang)

    if not msg.text or msg.text not in [yes, no]:
        await msg.answer(t("err_button", lang), reply_markup=privacy_keyboard(lang))
        return

    if msg.text == no:
        await msg.answer(t("privacy_declined", lang))
        await state.clear()
        return

    await state.update_data(privacy=msg.text)
    data = await state.get_data()

    summary = t("resume_summary", lang).format(
        branch_name=data.get("branch_name", ""),
        vacancy_name=data.get("vacancy_name", ""),
        fullname=data.get("fullname", ""),
        address=data.get("address", ""),
        phone=data.get("phone", ""),
        birthdate=data.get("birthdate", ""),
        gender=data.get("gender", ""),
        marital=data.get("marital", ""),
        education=data.get("education", ""),
        exp_org=data.get("exp_org", ""),
        exp_pos=data.get("exp_pos", ""),
        exp_period=data.get("exp_period", ""),
        uzbek=data.get("uzbek", ""),
        russian=data.get("russian", ""),
        salary=data.get("salary", ""),
        source=data.get("source", ""),
        previous=data.get("previous", ""),
    )

    await state.set_state(ResumeState.confirm)
    await msg.answer(summary, reply_markup=confirm_keyboard(lang))


# ─────────────────────────────────────────────────────────
#
# ─────────────────────────────────────────────────────────
# PDF GENERATOR (100% FIXED)
# ─────────────────────────────────────────────────────────
def generate_resume_pdf(data, filename):
    
    # papka
    os.makedirs("pdf", exist_ok=True)
    filepath = f"pdf/{filename}"

    # FONT
    font_path = "DejaVuSans.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont("DejaVu", font_path))
        font_name = "DejaVu"
    else:
        font_name = "Helvetica"

    doc = SimpleDocTemplate(filepath, pagesize=A4)
    styles = getSampleStyleSheet()

    # 🔥 STYLELAR
    normal = ParagraphStyle(
        name="NormalCustom",
        fontName=font_name,
        fontSize=10,
        leading=14
    )

    header_style = ParagraphStyle(
        name="Header",
        fontName=font_name,
        fontSize=14,
        leading=16,
        spaceAfter=10
    )

    section_title = ParagraphStyle(
        name="Section",
        fontName=font_name,
        fontSize=12,
        spaceBefore=10,
        spaceAfter=5,
        textColor=colors.darkgreen
    )

    elements = []

    # 🔥 HEADER (rasm + ism yonma-yon)
    photo_path = data.get("photo_path")

    if photo_path and os.path.exists(photo_path):
        img = Image(photo_path, width=4*cm, height=6*cm)
    else:
        img = Paragraph("", normal)

    header_text = Paragraph(f"""
    <b>{data.get("fullname","")}</b><br/>
    {data.get("vacancy_name","")}<br/>
    📞 {data.get("phone","")}
    """, header_style)

    header_table = Table([[img, header_text]], colWidths=[4*cm, 12*cm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 15))

    # 🔥 TABLE FUNKSIYA
    def make_table(data_list):
        t = Table(data_list, colWidths=[6*cm, 7*cm])
        t.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.3, colors.grey),
            ('FONTNAME', (0,0), (-1,-1), font_name),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        return t

    # 🔥 SHAXSIY MA'LUMOT
    elements.append(Paragraph("Shaxsiy ma'lumotlar", section_title))
    left_data = [
        ["Tug'ilgan sana", data.get("birthdate","")],
        ["Jins", data.get("gender","")],
        ["Oilaviy holat", data.get("marital","")],
        ["Ta'lim", data.get("education","")]
    ]
    elements.append(make_table(left_data))

    # 🔥 ASOSIY INFO
    elements.append(Paragraph("Asosiy ma'lumotlar", section_title))
    right_data = [
        ["Filial", data.get("branch_name","")],
        ["Vakansiya", data.get("vacancy_name","")],
        ["Manzil", data.get("address","")]
    ]
    elements.append(make_table(right_data))

    # 🔥 ISH TAJRIBASI
    elements.append(Paragraph("Ish tajribasi", section_title))
    exp_data = [
        ["Tashkilot", data.get("exp_org","")],
        ["Lavozim", data.get("exp_pos","")],
        ["Davr", data.get("exp_period","")]
    ]
    elements.append(make_table(exp_data))

    # 🔥 TILLAR + MAOSH
    elements.append(Paragraph("Qo‘shimcha", section_title))
    extra = [
        ["O'zbek tili", data.get("uzbek","")],
        ["Rus tili", data.get("russian","")],
        ["Maosh", data.get("salary","")]
    ]
    elements.append(make_table(extra))

    elements.append(Spacer(1, 10))

    doc.build(elements)
    return filepath

# ─────────────────────────────────────────────────────────
# CONFIRM + YUBORISH (FINAL)
# ─────────────────────────────────────────────────────────




from aiogram.types import FSInputFile, ReplyKeyboardRemove
import os

@router.message(ResumeState.confirm)
async def confirm_resume(msg: Message, state: FSMContext):
    lang = await _lang(state)
    data = await state.get_data()

    if msg.text != t("confirm_prompt", lang):
        await msg.answer(t("err_button", lang))
        return

    filename = f"resume_{msg.from_user.id}.pdf"

    # 🔥 PDF yaratamiz
    try:
        pdf_path = generate_resume_pdf(data, filename)
    except Exception as e:
        await msg.answer("PDF xatolik ❌")
        print("PDF ERROR:", e)
        return

    if not os.path.exists(pdf_path):
        await msg.answer("PDF topilmadi ❌")
        return

    file = FSInputFile(pdf_path)

    # 🔥 USER GA yuborish
    await msg.answer_document(
        file,
        caption="📄 Sizning rezyumengiz"
    )

    # 🔥 GROUP GA yuborish
    try:
        await msg.bot.send_document(
            chat_id=chat_id,
            document=FSInputFile(pdf_path),
            caption=(
                f"🆕 YANGI REZYUME\n\n"
                f"👤 {data.get('fullname','')}\n"
                f"📞 {data.get('phone','')}\n"
                f"🏢 {data.get('branch_name','')}\n"
                f"💼 {data.get('vacancy_name','')}"
            )
        )
    except Exception as e:
        print("GROUP ERROR:", e)

    # 🔥 FINAL MESSAGE + KEYBOARD REMOVE
    await msg.answer(
        "✅ Rezyumengiz muvaffaqiyatli yuborildi!\n\n"
        "🔄 Qaytadan boshlash uchun /start bosing",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()