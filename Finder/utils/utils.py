from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()


class BotStates(StatesGroup) :
    none = State()
    change_nick_state = State()
    change_photo = State()
    change_description = State()
    change_genre = State()
    change_genre_like = State()
    change_country = State()
    change_age = State()
    like = State()
    reply_to_like = State()
    show_liked_people = State()
