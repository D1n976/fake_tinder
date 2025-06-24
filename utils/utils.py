from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import re
import yaml

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
    show_peoples = State()

def is_number(s):
    if re.match("^\d+?\.\d+?$", s) is None:
        return s.isdigit()
    return True

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


def get_profile_str(profile_info) :
        return f'Я {profile_info[-1][3]}, {profile_info[-1][8]}\n'\
               f'Живу в {profile_info[-1][-1]}\n'f'{profile_info[-1][6]}'

def is_user_valid(user) :
    return user[2] and user[3] and user[4] and user[5] and user[6] and user[7] and user[8]