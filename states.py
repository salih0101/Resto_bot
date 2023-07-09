from aiogram.dispatcher.filters.state import State, StatesGroup


class Add_product(StatesGroup):
    get_name = State()
    get_id = State()
    get_price = State()
    get_info = State()
    get_photo = State()
    get_colour_one = State()
    get_colour_two = State()


class GetProduct(StatesGroup):
    getting_pr_name = State()
    getting_pr_count = State()
    getting_pr_colour = State()


class Cart(StatesGroup):
    waiting_for_product = State()
    waiting_new_count = State()


class Order(StatesGroup):
    waiting_location = State()
    waiting_pay_type = State()
    waiting_accept = State()


class Settings(StatesGroup):
    set_setting = State()
    set_name_setting = State()
    set_number_setting = State()
    set_name = State()
    set_number = State()


class Registration(StatesGroup):
    getting_name_state = State()
    getting_phone_number = State()


class Admin(StatesGroup):
    get_status = State()


class Search(StatesGroup):
    search_product = State()

class Broadcast(StatesGroup):
    broadcast_message = State()