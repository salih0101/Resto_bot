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
    kb.add('🛒Корзина')
    kb.add('☎️Обратная связь')
    kb.add('О нас', '👤Профиль')

    return kb


def catalog_folder():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add('Салфетки')
    kb.add('Плейсматы', 'Фартуки')
    kb.add('🛒Корзина', 'Назад🔙')

    return kb


def salfetki_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add('Салфетка "180гр"')
    kb.add('Салфетка "240гр"', 'Салфетка "300гр"')
    kb.add('Назад')

    return kb

def cart_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = KeyboardButton('Очистить🆑')
    button1 = KeyboardButton('Оформить заказ✅')
    back = KeyboardButton('Назад◀️')
    kb.add(button1, button, back)

    return kb


def colour180_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Выберите цвет модели")
    kb.add('Чeрный', 'Бeлый')
    kb.add('Назад◀️')

    return kb

def colour240_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Выберите цвет модели")
    kb.add('Горчичный')
    kb.add('Серый', 'Хаки')
    kb.add('Назад◀️')

    return kb


def colour300_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Выберите цвет модели")
    kb.add('Белый')
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
    send = InlineKeyboardButton(text='Перейти в чат', url='https://t.me/Ferrafa')

    kb.add(send)
    return kb


def payme_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    send = InlineKeyboardButton(text='Перейти к оплате', url='https://payme.uz/61824a6475752e8a58496324')

    kb.add(send)
    return kb


def confirmation_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = KeyboardButton('Подтвердить')
    back = KeyboardButton('Назадд')
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
    buttons = [KeyboardButton(str(i)) for i in [50, 100, 200]]
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


def count_kb(category_id):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад◀️')
    all_products = database.get_name_product(category_id)

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb
