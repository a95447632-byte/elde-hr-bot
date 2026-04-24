from aiogram.fsm.state import State, StatesGroup


class AppState(StatesGroup):
    language = State()   # til tanlash
    menu = State()       # asosiy menyu


class ResumeState(StatesGroup):
    branch    = State()
    vacancy   = State()
    fullname  = State()
    address   = State()
    phone     = State()
    birthdate = State()
    gender    = State()
    marital   = State()
    education = State()
    
    exp_org   = State()
    exp_pos   = State()
    exp_period = State()
    uzbek     = State()
    russian   = State()
    salary    = State()
    photo     = State()
    source    = State()
    privacy   = State()
    previous  = State()
    confirm   = State()


# 🔥 ADMIN UCHUN YANGI STATE
class AdminState(StatesGroup):
    branch = State()
    vacancy = State()

    add_vacancy = State()      # ➕ qo‘shish
    delete_vacancy = State()   # ❌ o‘chirish