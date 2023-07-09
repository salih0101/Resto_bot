# from aiogram import Dispatcher, executor, Bot
# from aiogram.dispatcher import FSMContext
#
# from states import Registration, GetProduct, Cart, Order
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# import buttons as btns
# import database
# import states
# import os
# from dotenv import load_dotenv, find_dotenv
# import logging
# from datetime import datetime
# import config
# from aiogram import types
#
#
#
# load_dotenv(find_dotenv())
#
# bot = Bot(config.BOT_TOKEN)
#
# logging.basicConfig(filename='spam.log', level=logging.INFO)
#
#
# dp = Dispatcher(bot, storage=MemoryStorage())
#
# about = ('Мы - узбекская компания, основанная в 2011 году в Ташкенте. '
#          'Сегодня мы поставляем одежду для поваров и ресторанов по всему миру. '
#          'Наш успех определяется любовью к поварскому искусству. '
#          'Повар объединяет людей и создает яркие моменты счастья. '
#          'Мы считаем, что повар - самая важная профессия на Земле.')
#
#
# @dp.message_handler(commands=['start'])
# async def start_message(message):
#     # ---Получить user_id пользователя
#     user_id = message.from_user.id
#     # ---Происходит проверка в базе
#     checker = database.check_user(user_id)
#     if checker:
#         await message.answer('Приветствуем вас в нашем Онлайн магазине \n\nВыберите раздел🔽',
#                              reply_markup=btns.main_menu())
#     else:
#         await message.answer(
#             'Приветствую, Пройдите простую регистрацию чтобы в дальнейшем не было проблем!\n\nОтправьте Имя для регистрации!',
#             reply_markup=btns.ReplyKeyboardMarkup())
#         await Registration.getting_name_state.set()
#
#
# @dp.message_handler(state=Registration.getting_name_state)
# async def get_name(message, state=Registration.getting_name_state):
#     user_answer = message.text
#
#     await state.update_data(name=user_answer)
#     await message.answer('Имя сохранил!\n\nОтправьте номер телефона!\n\n', reply_markup=btns.phone_number_kb())
#
#     await Registration.getting_phone_number.set()
#
#
# # @dp.message_handler(state=Registration.getting_phone_number, content_types=['contact'])
# # async def get_number(message, state=Registration.getting_phone_number):
# #     user_answer = message.contact.phone_number
# #
# #     await state.update_data(number=user_answer)
# #     await message.answer('Номер сохранил!\n\nВыберите пол👫', reply_markup=btns.gender_kb())
# #
# #     await Registration.getting_gender.set()
#
#
#
# @dp.message_handler(state=Registration.getting_phone_number, content_types=['text', 'contact'])
# async def get_number(message: types.Message, state: FSMContext):
#     global user_answer
#
#     if message.content_type == 'text':
#         user_answer = message.text
#
#         if not user_answer.replace('+', '').isdigit():
#             await message.answer('Отправьте номер телефона')
#             return
#
#     elif message.content_type == 'contact':
#         user_answer = message.contact.phone_number
#
#     await state.update_data(number=user_answer)
#
#     await message.answer('Успешно зарегистрирован📝!\n\nВыберите раздел🔽', reply_markup=btns.main_menu())
#
#     all_info = await state.get_data()
#     name = all_info.get('name')
#     phone_number = all_info.get('number')
#     latitude = all_info.get('latitude')
#     longitude = all_info.get('longitude')
#     gender = user_answer
#     user_id = message.from_user.id
#     database.add_user(user_id, name, phone_number, latitude, longitude, gender)
#
#     await state.finish()
#
#
#
# @dp.message_handler(state=GetProduct.getting_pr_name, content_types=['text'])
# async def choose_count(message):
#     user_answer = message.text
#     user_id = message.from_user.id
#
#     user_data = await dp.current_state(user=user_id).get_data()
#     category_id = user_data.get('category_id')
#
#     actual_products = [i[0] for i in database.get_name_product(category_id)]
#
#
#     if user_answer == 'Назад◀️':
#         await message.answer('Выберите категорию🔽', reply_markup=btns.catalog_folder())
#
#         await dp.current_state(user=user_id).finish()
#
#     elif user_answer in actual_products:
#
#         product_info = database.get_all_info_product(user_answer)
#         await bot.send_photo(user_id, photo=product_info[4],
#                              caption=f'{product_info[0]}\n\nЦена: {product_info[2]} $\n\nОписание: {product_info[3]}\n\n@testname_bot\n\nВыберите количество1️⃣2️⃣3️⃣',
#                              reply_markup=btns.product_count())
#
#         await dp.current_state(user=user_id).update_data(user_product=message.text, price=product_info[2])
#
#         await states.GetProduct.getting_pr_count.set()
#
#
# @dp.message_handler(state=GetProduct.getting_pr_count)
# async def text_message3(message, state=GetProduct.getting_pr_count):
#     product_count = message.text
#     user_data = await state.get_data()
#     user_product = user_data.get('user_product')
#     category_id = user_data.get('category_id')
#     pr_price = float(user_data.get('price'))
#
#
#     if product_count.isnumeric():
#         database.add_pr_to_cart(message.from_user.id, user_product, pr_price, int(product_count))
#         # database.add_pr_to_cart2(message.from_user.id, user_product, pr_price, int(product_count))
#
#         await message.answer('Товар добавлен в корзину✅\n\nВыберите продукт🔽', reply_markup=btns.catalog_folder())
#         await state.finish()
#
#     # elif message.text != 'Назад◀️':
#     #     await message.answer('Выберите количество используя кнопки🔽', reply_markup=btns.product_count())
#
#     else:
#         await message.answer('Выберите товар из списка🔽', reply_markup=btns.count_kb(category_id))
#         await states.GetProduct.getting_pr_name.set()
#
#
#
# @dp.message_handler(state=Cart.waiting_for_product)
# async def cart_function(message, state=Cart.waiting_for_product):
#     user_answer = message.text
#     user_id = message.from_user.id
#
#     if user_answer == 'Назад◀️':
#         await message.answer('❗️Вы вернулись в Главное меню❗️\n\nВыберите раздел🔽', reply_markup=btns.main_menu())
#         await dp.current_state(user=message.from_user.id).finish()
#
#
#     elif user_answer == 'Очистить🆑':
#         # ---Очищаем корзину из базы(для конкретного пользователя)
#         database.delete_from_cart(user_id)
#         await message.answer('Корзина очищена✅\n\n❗️❗️Нажмите кнопку Назад❗️❗️')
#
#
#     if user_answer == 'Оформить заказ✅':
#
#         user_cart = database.get_user_cart(message.from_user.id)
#
#         if user_cart:
#
#             result_answer = 'Ваш заказ✅🔽:\n\n'
#             admin_message = 'Новый заказ✅✅:\n\n'
#             total_price = 0
#
#             for i in user_cart:
#                 result_answer += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n'
#                 admin_message += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n'
#                 total_price += i[3]
#
#             result_answer += f' \nИтог: {total_price:.2f}$'
#         await message.answer('Раздел оформления заказа🔽', reply_markup=btns.confirmation_kb())
#
#     elif user_answer == 'Подтвердить':
#         order_id = datetime.now().microsecond
#         user_cart = database.get_user_cart(message.from_user.id)
#
#         if user_cart:
#
#             result_answer = f'Ваш заказ №{order_id} :\n\n'
#             admin_message = f'Новый заказ {order_id} ✅✅:\n\n'
#             total_price = 0
#
#             for i in user_cart:
#                 result_answer += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n'
#                 admin_message += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n\n'
#                 total_price += i[3]
#
#             result_answer += f' \nИтог: {total_price:.2f}$'
#             admin_message += f'Номер телефона: {i[2]}\n\nИтог: {total_price:.2f}$'
#             # ---Отправка пользователю
#             await message.answer(result_answer, reply_markup=btns.main_menu())
#             await message.answer('Успешно оформлен✅\n\n')
#             await state.finish()
#
#             await bot.send_message(5928000362, admin_message)
#
#             database.delete_from_cart(user_id)
#
#
#
# # ---Независимый обработчик текста для основного меню
# @dp.message_handler(content_types=['text'])
# async def main_menu(message):
#     user_answer = message.text
#     user_id = message.from_user.id
#
#
#     if user_answer == '🛒Корзина':
#
#         user_cart = database.get_user_cart(message.from_user.id)
#
#         if user_cart:
#
#             result_answer = 'Ваша корзина🛒:\n\n'
#             total_price = 0
#
#             for i in user_cart:
#                 result_answer += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n\n'
#                 total_price += i[3]
#
#             result_answer += f' \nИтог: {total_price:.2f}$'
#             await message.answer(result_answer, reply_markup=btns.cart_kb())
#             await Cart.waiting_for_product.set()
#
#         else:
#             await message.answer('Ваша корзина пустая🛒\n\n'
#                                  'Для выбора продукта нажмите кнопку ❗️Каталог❗️')
#
#
#     if user_answer == '📦Каталог':
#         await message.answer('Выберите категорию🔽', reply_markup=btns.catalog_folder())
#
#     elif user_answer == 'Назад🔙':
#         await message.answer('❗️Вы вернулись в Главное меню❗️\n\nВыберите раздел🔽', reply_markup=btns.main_menu())
#
#     elif user_answer == 'Кители мужские':
#         await dp.current_state(user=user_id).update_data(category_id=11)
#         await message.answer('Выберите продукт🔽', reply_markup=btns.spray_kb())
#         await states.GetProduct.getting_pr_name.set()
#
#     elif user_answer == 'Кители женские':
#         await dp.current_state(user=user_id).update_data(category_id=22)
#         await message.answer('Выберите продукт🔽', reply_markup=btns.tablets_kb())
#         await states.GetProduct.getting_pr_name.set()
#
#     elif user_answer == 'Салфетки':
#         await dp.current_state(user=user_id).update_data(category_id=33)
#         await message.answer('Выберите продукт🔽', reply_markup=btns.syrup_kb())
#         await states.GetProduct.getting_pr_name.set()
#
#     elif user_answer == 'Фартуки':
#         await dp.current_state(user=user_id).update_data(category_id=44)
#         await message.answer('Выберите продукт🔽', reply_markup=btns.pastes_kb())
#         await states.GetProduct.getting_pr_name.set()
#
#     # elif user_answer == 'Головные уборы':
#     #     await dp.current_state(user=user_id).update_data(category_id=55)
#     #     await message.answer('Выберите продукт🔽', reply_markup=btns.other_pr_kb())
#     #     await states.GetProduct.getting_pr_name.set()
#
#
#     # elif user_answer == 'Поло, футболки':
#     #     await dp.current_state(user=user_id).update_data(category_id=66)
#     #     await message.answer('Выберите продукт🔽', reply_markup=btns.polo_kb())
#     #     await states.GetProduct.getting_pr_name.set()
#
#
#     elif user_answer == 'Назад◀️':
#         await message.answer('Выберите категорию🔽', reply_markup=btns.catalog_folder())
#
#     elif user_answer == 'О нас':
#         await message.answer(about)
#
#     elif user_answer == '☎️Обратная связь':
#         await message.answer(f'📞 Контактный телефон:'
#                              f'+9989*******\n'
#                              f'+9989*******\n'
#                              f'📧 E-mail: test@gmail.com\n'
#                              f'🌐 Instagram: testgram\n'
#                              f'📍 Наш адрес: г. Ташкент, Тестовый район\n'
#                              f'✉️ НАМ ВАЖНО ЗНАТЬ\n'
#                              f'Хотим услышать твое мнение о нас!\n'
#                              f'Просто напиши нам!\n'
#                              f'Telegram: @usernametest')
#
#     elif user_answer == '📄Список заказов':
#
#         user_cart = database.get_user_cart(message.from_user.id)
#
#         if user_cart:
#
#             result_answer = 'Ваш заказ✅:\n\n'
#             admin_message = 'Новый заказ✅✅:\n\n'
#             total_price = 0
#
#             for i in user_cart:
#                 result_answer += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n\n'
#                 admin_message += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n'
#                 total_price += i[3]
#
#             result_answer += f' \nИтог: {total_price:.2f}$'
#             admin_message += f' Номер телефона: {i[2]}\n\nИтог: {total_price:.2f}$'
#
#             await message.answer(result_answer, reply_markup=btns.order_kb())
#
#             await Order.waiting_accept.set()
#
#         else:
#             await message.answer('Ваша корзина пустая🛒\n\n'
#                                  'Для выбора продукта нажмите кнопку ❗️Каталог❗️')
#
#     logging.info(message.text)
# @dp.message_handler(state=Order.waiting_accept)
# async def accept_order(message):
#     user_answer = message.text
#     user_id = message.from_user.id
#
#     if user_answer == 'Назад◀️':
#         await message.answer('❗️Вы вернулись в Главное меню ActiveBee❗️\n\nВыберите раздел🔽', reply_markup=btns.main_menu())
#         await dp.current_state(user=message.from_user.id).finish()
#
#     elif user_answer == 'Оформить заказ':
#
#         user_cart = database.get_user_cart(message.from_user.id)
#
#         if user_cart:
#
#             result_answer = 'Ваш заказ✅🔽:\n\n'
#             admin_message = 'Новый заказ✅✅:\n\n'
#             total_price = 0
#
#             for i in user_cart:
#                 result_answer += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\nИтог: {total_price:.2f}$'
#                 admin_message += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n'
#                 total_price += i[3]
#
#             result_answer += f' \nИтог: {total_price:.2f}$'
#             admin_message += f'Номер телефона: {i[2]}\n\nИтог: {total_price:.2f}$'
#
#             await message.answer(result_answer, reply_markup=btns.main_menu())
#             await message.answer('Успешно оформлен✅\n\n')
#             await bot.send_message(5928000362, admin_message)
#             await dp.current_state(user=message.from_user.id).finish()
#             database.delete_from_cart(user_id)
#
#
# executor.start_polling(dp, skip_updates=True)