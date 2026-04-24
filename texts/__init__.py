from .uz import TEXTS as _UZ
from .ru import TEXTS as _RU


def t(key: str, lang: str = "uz") -> str:
    """
    Berilgan kalit va til bo'yicha matnni qaytaradi.
    Agar kalitni topilmasa, o'zbek tilidan oladi.
    """
    texts = _RU if lang == "ru" else _UZ
    return texts.get(key, _UZ.get(key, key))