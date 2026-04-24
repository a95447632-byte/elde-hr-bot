from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("bot_token")
ADMIN_ID = os.getenv("admin_id")
chat_id = os.getenv("CHAT_ID")

BRANCHES = {
    "bosh_ofis": {
    "name_uz": "Bosh ofis (Andijon)",
    "name_ru": "Головной офис (Андижан)",
    "lat": 40.797476,
    "lon": 72.332978
}   ,
   
    "xojaobod": {
        "name_uz": "Xo'jaobod filiali",
        "name_ru": "Ходжаабадский филиал",
        "lat": 40.669524,
        "lon": 72.558374
    },
    "buloqboshi": {
        "name_uz": "Buloqboshi filiali",
        "name_ru": "Булокбашинский филиал",
        "lat": 40.626680,
        "lon": 72.500870
    },
    "baliqchi": {
        "name_uz": "Baliqchi filiali",
        "name_ru": "Балыкчинский филиал",
        "lat": 40.904254,
        "lon": 71.847822
    },
    "andijon_yangi": {
        "name_uz": "Andijon filiali",
        "name_ru": "Андижанский филиал",
        "lat": 40.797476,
        "lon": 72.332978
    },
    "qorgontepa": {
        "name_uz": "Qo'rg'ontepa filiali",
        "name_ru": "Кургантепинский филиал",
        "lat": 40.727286,
        "lon": 72.760329
    },
    "boston": {
        "name_uz": "Bo'ston filiali",
        "name_ru": "Бостанский филиал",
        "lat": 40.690127,
        "lon": 71.926154
    },
    "paxtobod": {
        "name_uz": "Paxtobod filiali",
        "name_ru": "Пахтаабадский филиал",
        "lat": 40.931627,
        "lon": 72.495867
    },
    "izboskan": {
        "name_uz": "Izboskan filiali",
        "name_ru": "Избасканский филиал",
        "lat": 40.895607,
        "lon": 72.252681
    },
    "qoshtepa": {
        "name_uz": "Oltinkol filiali",
        "name_ru": "Олтинкольский филиал",
        "lat": 40.827941,
        "lon": 72.028488
    }
}
VACANCIES = {
    "seller": {
        "title_uz": "Sotuvchi",
        "title_ru": "Продавец"
    },
    "marketer": {
        "title_uz": "Marketolog",
        "title_ru": "Маркетолог"
    },
    "delivery": {
        "title_uz": "Yetkazib beruvchi",
        "title_ru": "Доставщик"
    },
    "collector": {
        "title_uz": "Undiruv hodimi",
        "title_ru": "Сотрудник по взысканию"
    },
    "manager": {
        "title_uz": "Ish yurituvchi (manager)",
        "title_ru": "Менеджер (делопроизводитель)"
    },
    "warehouse_specialist": {
        "title_uz": "Ombor mutaxassisi",
        "title_ru": "Специалист склада"
    },
    "contract_specialist": {
        "title_uz": "Shartnoma hodimi",
        "title_ru": "Специалист по договорам"
    }
}