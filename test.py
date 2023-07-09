from settings import *
from about_company import about, contacts
import csv
from aiogram import types


load_dotenv(find_dotenv())
bot = Bot(config.BOT_TOKEN)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'], state='*')
async def start_message(message):

    start_txt = f'Добро пожаловать {message.from_user.first_name} \n' \
                f'Мы рады предложить вам широкий ассортимент высококачественных и стильных текстильных изделий , ' \
                f'которые сделают ваше заведение еще более привлекательным и профессиональным.'

    start_reg = f'Введите ваше имя: '

    user_id = message.from_user.id
    checker = database.check_user(user_id)

    if user_id == 5928000362:
        await message.answer('Приветствую Администратор',
                             reply_markup=btns.admin_kb())
        await states.Admin.get_status.set()

    elif checker:
        await message.answer(start_txt, reply_markup=btns.main_menu())

    else:
        await message.answer(start_txt)
        await message.answer(start_reg,
                             reply_markup=btns.ReplyKeyboardMarkup())

        await states.Registration.getting_name_state.set()


@dp.message_handler(commands=['show_users'])
async def show_users(message: types.Message):
    admin_id = 5928000362

    if message.from_user.id != admin_id:
        response = "Команда доступна только администратору."
        await message.answer(response)
        return

    users = database.get_users()

    if users:

        with open('users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Username", "Phone_number"])

            for user in users:
                writer.writerow([user[0], user[1], user[2]])

        with open('users.csv', 'rb') as file:
            await message.bot.send_document(admin_id, file)

        response = "Список пользователей сохранен в файле users.csv и отправлен администратору."
    else:
        response = "Список пользователей пуст."

    await message.answer(response)


@dp.message_handler(commands=['broadcast'], state=states.Broadcast.broadcast_message)
async def broadcast_command(message, state=states.Broadcast.broadcast_message):

    conn = sqlite3.connect('restodata.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users")
    users = cursor.fetchall()

    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text=message.text[11:])
        # Replace message.text[11:] with command_args[1] if you prefer using split

    await message.reply('Сообщение успешно отправлено всем пользователям.')
    await state.finish()


@dp.message_handler(state=states.Admin.get_status)
async def get_name(message, state=states.Admin.get_status):

    if message.text == 'Добавить товар':
        await message.answer('Введите наименование товара')
        await states.Add_product.get_name.set()

    elif message.text == 'broadcast':
        await message.answer('test')
        await states.Broadcast.broadcast_message.set()

    elif message.text == 'Меню клиента':
        user_id = message.from_user.id
        checker = database.check_user(user_id)

        if checker:
            await state.finish()
            await message.answer('Выберите продукт',
                                 reply_markup=btns.main_menu())

        else:
            start_txt = f'Добро пожаловать \n' \
                        f'Мы рады предложить вам широкий ассортимент высококачественных и стильных текстильных изделий, \n' \
                        f'которые сделают ваше заведение еще более привлекательным и профессиональным.\n'

            start_reg = f'Введите ваше имя: '

            await message.answer(start_txt)
            await message.answer(start_reg)

            await states.Registration.getting_name_state.set()


@dp.message_handler(state=states.Add_product.get_name)
async def product_name(message, state=states.Add_product.get_name):
    name = message.text

    await state.update_data(name=name)
    await message.answer(f'Теперь введите ID продукта {name}:>>')
    await states.Add_product.get_id.set()


@dp.message_handler(state=states.Add_product.get_id)
async def get_id(message, state=states.Add_product.get_id):
    name = message.text

    await state.update_data(id=name)
    await message.answer(f'Теперь введите стоимость:')
    await states.Add_product.get_price.set()


@dp.message_handler(state=states.Add_product.get_price)
async def product_price(message, state=states.Add_product.get_price):
    price = message.text

    await state.update_data(price=price)
    await message.answer(
        f'Теперь введите описание товара:>>\n\n'
        f'Модель \n' 
        f'Цена: \n'
        f'Цвет: \n'
        f'Описание: \n')

    await states.Add_product.get_info.set()


@dp.message_handler(state=states.Add_product.get_info)
async def product_info1(message, state=states.Add_product.get_info):
    info_pr = message.text

    await state.update_data(description=info_pr)
    await message.answer('Теперь загрузите фото товара>>')
    await states.Add_product.get_photo.set()


@dp.message_handler(content_types=['photo'], state=states.Add_product.get_photo)
async def product_photo(message, state=states.Add_product.get_photo):

    all_info = await state.get_data()
    name = all_info.get('name')
    prd_id = all_info.get('id')
    price = all_info.get('price')
    description = all_info.get('description')
    photo_id = all_info.get('picture')
    nt = all_info.get('notes')
    picture = message.photo[-1].file_id
    await state.update_data(photo=photo_id)

    database.add_products_to_db(name, prd_id, price, description, picture, nt)

    await message.answer('Товар добавлен', reply_markup=btns.admin_kb())
    await states.Admin.get_status.set()


@dp.message_handler(state=Registration.getting_name_state)
async def get_name(message, state=Registration.getting_name_state):
    user_answer = message.text

    await state.update_data(name=user_answer)
    await message.answer('Имя сохранил!\n\nОтправьте номер телефона!\n\n', reply_markup=btns.phone_number_kb())

    await Registration.getting_phone_number.set()


@dp.message_handler(state=Registration.getting_phone_number, content_types=['text', 'contact'])
async def get_number(message: types.Message, state: FSMContext):
    global user_answer

    if message.content_type == 'text':
        user_answer = message.text

        if not user_answer.replace('+', '').isdigit():
            await message.answer('Отправьте номер телефона')
            return

    elif message.content_type == 'contact':
        user_answer = message.contact.phone_number

    await state.update_data(number=user_answer)
    await message.answer(f'Пожалуйста, продолжайте оформление заказа, '
                         f'указывая необходимые товары для вашего ресторана\n\n. '
                         f'Мы готовы предложить вам наши лучшие цены, продукты и обеспечить ваше заведение высококачественным текстилем, '
                         f'который подчеркнет ваш стиль и профессионализм.', reply_markup=btns.main_menu())

    all_info = await state.get_data()
    name = all_info.get('name')
    phone_number = all_info.get('number')
    latitude = all_info.get('latitude')
    longitude = all_info.get('longitude')
    gender = user_answer
    user_id = message.from_user.id
    database.add_user(user_id, name, phone_number, latitude, longitude, gender)

    await state.finish()


@dp.message_handler(state=GetProduct.getting_pr_name, content_types=['text'])
async def choose_count(message):
    user_answer = message.text
    user_id = message.from_user.id

    user_data = await dp.current_state(user=user_id).get_data()
    category_id = user_data.get('category_id')

    actual_products = [i[0] for i in database.get_name_product(category_id)]

    if user_answer == 'Назад◀️':
        await message.answer('Выберите категорию🔽', reply_markup=btns.catalog_folder())
        await dp.current_state(user=user_id).finish()
        
        await dp.current_state(user=user_id).finish()

    elif user_answer in actual_products:

        product_info = database.get_all_info_product(user_answer)
        await bot.send_photo(user_id, photo=product_info[4],
                             caption=f'{product_info[0]}\n\nЦена: {product_info[2]} сум\n\n'
                                     f'Описание: {product_info[3]}\n\n'
                                     f'@ferrafastudio_bot\n\n',
                             reply_markup=btns.colour_kb())
        await message.answer('Выберите цвет')

        await dp.current_state(user=user_id).update_data(user_product=message.text, price=product_info[2])

        await states.GetProduct.getting_pr_colour.set()


@dp.message_handler(state=GetProduct.getting_pr_colour)
async def choose_colour(message, state=GetProduct.getting_pr_colour):
    user_answer = message.text
    colour = message.text

    if user_answer == 'Назад◀️':
        await message.answer('Выберите категорию🔽', reply_markup=btns.catalog_folder())
        await dp.current_state(user=message.from_user.id).finish()

    elif user_answer == '⚫️Черный' or user_answer == '⚪️Белый':
        await state.update_data(colour=colour)
        await message.answer('Выберите количество', reply_markup=btns.product_count())
        await state.set_state(states.GetProduct.getting_pr_count)


@dp.message_handler(state=GetProduct.getting_pr_count)
async def text_message3(message, state=GetProduct.getting_pr_count):
    product_count = message.text
    user_data = await state.get_data()
    user_product = user_data.get('user_product')
    category_id = user_data.get('category_id')
    pr_price = float(user_data.get('price'))
    colour = user_data.get('colour')

    if product_count.isnumeric():
        database.add_pr_to_cart2(message.from_user.id, user_product, pr_price, int(product_count), colour)

        await message.answer('Товар добавлен в корзину✅\n\nВыберите продукт🔽', reply_markup=btns.catalog_folder())
        await state.finish()

    # elif message.text != 'Назад◀️':
    #     await message.answer('Выберите количество используя кнопки🔽', reply_markup=btns.product_count())

    else:
        await message.answer('Выберите товар из списка🔽', reply_markup=btns.count_kb(category_id))
        await states.GetProduct.getting_pr_name.set()


@dp.message_handler(state=Cart.waiting_for_product)
async def cart_function(message, state=Cart.waiting_for_product):
    user_answer = message.text
    user_id = message.from_user.id

    if user_answer == 'Назад◀️':
        await message.answer('❗️Вы вернулись в Главное меню❗️\n\nВыберите раздел🔽', reply_markup=btns.main_menu())
        await dp.current_state(user=message.from_user.id).finish()

    elif user_answer == 'Очистить🆑':

        database.delete_from_cart(user_id)
        await message.answer('Корзина очищена✅\n\n❗️❗️Нажмите кнопку Назад❗️❗️')

    if user_answer == 'Оформить заказ✅':

        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = 'Ваш заказ✅🔽:\n\n'
            admin_message = 'Новый заказ✅✅:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: {i[5]} {i[-2]} шт = {i[3]}сум\n\n'
                result_answer += f'- {i[1]}: {i[5]} {i[-2]} шт = {i[3]}сум\n\n'
                total_price += i[3]

            result_answer += f' \nИтог: {total_price:}сум'
        await message.answer('Раздел оформления заказа🔽', reply_markup=btns.confirmation_kb())

    elif user_answer == 'Подтвердить':

        order_id = datetime.now().microsecond
        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = f'Ваш заказ № {order_id} :\n\n'
            admin_message = f'Новый заказ № {order_id}:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: {i[5]} {i[-2]} шт = {i[3]}сум\n\n'
                result_answer += f'- {i[1]}: {i[5]} {i[-2]} шт = {i[3]}сум\n\n'
                total_price += i[3]

            result_answer += f' \nИтог: {total_price:}сум\n\n'
            admin_message += f' Номер телефона: {i[2]}\n\nИтог: {total_price:}сум\n\n'

            delivery_date = datetime.now() + timedelta(days=21)
            delivery_date1 = datetime.now() + timedelta(days=7)

            result_answer += f'❗️ Дата доставки(Фартук): {delivery_date.strftime("%d.%m.%Y")}\n\n'
            result_answer += f'❗️ Дата доставки(Салфетки): {delivery_date1.strftime("%d.%m.%Y")}\n\n'

            admin_message += f'Дата доставки(Фартук): {delivery_date.strftime("%d.%m.%Y")}\n\n'
            admin_message += f'Дата доставки(Салфетки): {delivery_date1.strftime("%d.%m.%Y")}\n\n'

            await message.answer(result_answer, reply_markup=btns.main_menu())
            await message.answer('Успешно оформлен✅\n\n')
            await state.finish()
            await bot.send_message(5928000362, admin_message)

            database.delete_from_cart(user_id)


@dp.message_handler(content_types=['text'])
async def main_menu(message):
    user_answer = message.text
    user_id = message.from_user.id

    if user_answer == '🛒Корзина':

        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = 'Ваша корзина🛒:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: {i[5]} {i[-2]} шт = {i[3]}сум\n\n'
                total_price += i[3]

            result_answer += f' \nИтог: {total_price}'
            await message.answer(result_answer, reply_markup=btns.cart_kb())
            await Cart.waiting_for_product.set()

        else:
            await message.answer('Ваша корзина пустая🛒\n\n'
                                 'Для выбора продукта нажмите кнопку ❗️Каталог❗️')


    if user_answer == '📦Каталог':
        await message.answer('Выберите категорию🔽', reply_markup=btns.catalog_folder())

    elif user_answer == 'Назад🔙':
        await message.answer('❗️Вы вернулись в Главное меню❗️\n\nВыберите раздел🔽', reply_markup=btns.main_menu())
        await dp.current_state(user=user_id).finish()
        
    elif user_answer == 'Назад':
        await message.answer('Выберите раздел🔽', reply_markup=btns.catalog_folder())
        await dp.current_state(user=user_id).finish()
        
    elif user_answer == 'Салфетки':
        await message.answer('Выберите категорию🔽', reply_markup=btns.salfetki_kb())

    elif user_answer == 'Категория 1':
        await dp.current_state(user=user_id).update_data(category_id=11)
        await message.answer('Выберите продукт🔽', reply_markup=btns.spray_kb())
        await states.GetProduct.getting_pr_name.set()

    elif user_answer == 'Категория 2':
        await dp.current_state(user=user_id).update_data(category_id=22)
        await message.answer('Выберите продукт🔽', reply_markup=btns.tablets_kb())
        await states.GetProduct.getting_pr_name.set()

    elif user_answer == '':
        await dp.current_state(user=user_id).update_data(category_id=33)
        await message.answer('Выберите продукт🔽', reply_markup=btns.syrup_kb())
        await states.GetProduct.getting_pr_name.set()

    elif user_answer == 'Фартуки':
        await dp.current_state(user=user_id).update_data(category_id=44)
        await message.answer('Выберите продукт🔽', reply_markup=btns.pastes_kb())
        await states.GetProduct.getting_pr_name.set()

    elif user_answer == 'Назад◀️':
        await message.answer('Выберите категорию🔽', reply_markup=btns.catalog_folder())
        await dp.current_state(user=user_id).finish()
        
    elif user_answer == '👤Профиль':
        await message.answer('Выберите что хотите изменить', reply_markup=btns.change_data_kb())
        await states.Settings.set_setting.set()

    elif user_answer == 'О нас':
        await message.answer(about)

    elif user_answer == '☎️Обратная связь':
        await message.answer(contacts)

    elif user_answer == '📄Список заказов':

        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = 'Ваш заказ✅:\n\n'
            admin_message = 'Новый заказ✅✅:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: {i[5]} {i[-2]} шт = {i[3]}сум\n\n'
                result_answer += f'- {i[1]}: {i[5]} {i[-2]} шт = {i[3]}сум\n\n'
                total_price += i[3]

            result_answer += f' \nИтог: {total_price:}сум'
            admin_message += f' Номер телефона: {i[2]}\n\nИтог: {total_price:}сум'

            await message.answer(result_answer, reply_markup=btns.order_kb())

            await Order.waiting_accept.set()

        else:
            await message.answer('Ваша корзина пустая🛒\n\n'
                                 'Для выбора продукта нажмите кнопку ❗️Каталог❗️')

    logging.info(message.text)


@dp.message_handler(state=Order.waiting_accept)
async def accept_order(message):
    user_answer = message.text
    user_id = message.from_user.id

    if user_answer == 'Назад◀️':
        await message.answer('❗️Вы вернулись в Главное меню ActiveBee❗️\n\nВыберите раздел🔽', reply_markup=btns.main_menu())
        await dp.current_state(user=message.from_user.id).finish()

    elif user_answer == 'Оформить заказ':

        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = 'Ваш заказ✅🔽:\n\n'
            admin_message = 'Новый заказ✅✅:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: {i[5]} {i[-2]} шт = {i[3]}сум\n\n'
                result_answer += f'- {i[1]}: {i[5]} {i[-2]} шт = {i[3]}сум\n\n'
                total_price += i[3]

            result_answer += f' \nИтог: {total_price:}сум'
            admin_message += f'Номер телефона: {i[2]}\n\nИтог: {total_price:}сум'

            await message.answer(result_answer, reply_markup=btns.main_menu())
            await message.answer('Успешно оформлен✅\n\n')
            await bot.send_message(5928000362, admin_message)
            await dp.current_state(user=message.from_user.id).finish()
            database.delete_from_cart(user_id)





@dp.message_handler(state=Settings.set_setting, content_types=['text'])
async def set_name(message):
    user_answer = message.text
    user_id = message.from_user.id
    try:
        match user_answer:
            case 'Изменить имя':
                await message.answer('Отправьте имя')
                await Settings.set_name.set()

            case 'Изменить номер':
                await message.answer('Отправьте номер')
                await Settings.set_number.set()

    except Exception as e:
        print(e)
        await message.answer('Неверный ввод')

    try:
        match user_answer:
            case 'НАЗАД':
                await message.answer('Вы вернулись в Главное меню', reply_markup=btns.main_menu())
                await dp.current_state(user=user_id).finish()
            
    except Exception as e:
        print(e)
        await message.answer('Неверный ввод')


@dp.message_handler(state=states.Settings.set_name)
async def change_name_db(message, state=Settings.set_name):
    user_answer = message.text

    await state.update_data(name=user_answer)

    ch_name = await state.get_data()
    user_id = message.from_user.id
    database.change_name(user_id, ch_name)
    await state.finish()
    await message.answer('Имя пользователя "Успешно изменен"', reply_markup=btns.main_menu())


@dp.message_handler(state=Settings.set_number)
async def change_number_db(message, state=Settings.set_number):
    user_answer = message.text

    await state.update_data(phone_number=user_answer)

    ch_number = await state.get_data()
    user_id = message.from_user.id
    database.change_number(user_id, ch_number)
    await state.finish()
    await message.answer('Номер Успешно изменен', reply_markup=btns.main_menu())





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

