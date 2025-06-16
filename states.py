from aiogram.fsm.state import StatesGroup, State

class DateConstructorStates(StatesGroup):
    atmosphere = State()
    activity = State()
    final_touch = State()
    date = State()
    final = State()
    custom_atmosphere = State()
    custom_activity = State()
    custom_final_touch = State()
    comment = State()
