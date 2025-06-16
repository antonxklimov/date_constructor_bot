from aiogram.fsm.state import StatesGroup, State

class DateConstructorStates(StatesGroup):
    atmosphere = State()
    custom_atmosphere = State()
    activity = State()
    custom_activity = State()
    final_touch = State()
    custom_final_touch = State()
    date = State()
    comment = State()
