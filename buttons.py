from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import database


def admin_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add('Меню клиента')
    kb.add('Добавить товар')

    return kb


def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add('📦Каталог')
    kb.add('📄Список заказов', '🛒Корзина')
    kb.add('☎️Обратная связь')
    kb.add('О нас', '👤Профиль')

    return kb


def catalog_folder():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add('Фартуки')
    kb.add('Салфетки')
    kb.add('🛒Корзина', 'Назад🔙')

    return kb


def salfetki_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add('Категория 1', 'Категория 2')
    kb.add('Назад')

    return kb

def cart_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = KeyboardButton('Очистить🆑')
    button1 = KeyboardButton('Оформить заказ✅')
    back = KeyboardButton('Назад◀️')
    kb.add(button1, button, back)

    return kb


def colour_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Выберите цвет модели")
    kb.add('⚫️Черный', '⚪️Белый')
    kb.add('Назад◀️')

    return kb


def change_data_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    ch_name = KeyboardButton('Изменить имя')
    ch_number = KeyboardButton('Изменить номер')
    back = KeyboardButton('НАЗАД')
    kb.add(ch_name, ch_number, back)

    return kb


def send_admin_kb():
    kb = InlineKeyboardMarkup(row_width=3)
    send = InlineKeyboardButton(text='Отправить администратору', url='https://t.me/activebee_tashkent')

    kb.add(send)
    return kb


def confirmation_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = KeyboardButton('Подтвердить')
    back = KeyboardButton('Назад◀️')
    kb.add(button, back)

    return kb


def order_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Оформить заказ')
    back = KeyboardButton('Назад◀️')
    kb.add(button1, back)

    return kb


def phone_number_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Отправить номер телефона', request_contact=True)
    kb.add(button)

    return kb


def product_count():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [KeyboardButton(i) for i in range(1, 5)]
    back = KeyboardButton('Назад◀️')
    kb.add(*buttons)
    kb.add(back)

    return kb


def spray_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад◀️')
    all_products = database.spray_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def tablets_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад◀️')
    all_products = database.tablets_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def syrup_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад◀️')
    all_products = database.syrup_product()
    #print(all_products)


    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def pastes_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад◀️')
    all_products = database.pastes_product()
    #print(all_products)


    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def other_pr_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад◀️')
    all_products = database.other_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def polo_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад◀️')
    all_products = database.spray_product()
    #print(all_products)


    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def count_kb(category_id):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад◀️')
    all_products = database.get_name_product(category_id)

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb
