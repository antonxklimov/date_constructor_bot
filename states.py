from aiogram.fsm.state import StatesGroup, State

class DateConstructorStates(StatesGroup):
    atmosphere = State()
    activity = State()
    final_touch = State()
    date = State()
    comment = State()
