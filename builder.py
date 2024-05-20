from telebot import types


class Builder:
    @staticmethod
    def build_help_menu():
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_main = types.InlineKeyboardButton(text='Назад', callback_data='main_menu')
        keyboard.add(key_main)
        return keyboard

    @staticmethod
    def build_main_menu():
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_create_room = types.InlineKeyboardButton(text='Создать игру', callback_data='create')
        key_join_room = types.InlineKeyboardButton(text='Присоеденитьсяк игре', callback_data='join')
        key_score = types.InlineKeyboardButton(text='Рейтинг', callback_data='score')
        key_help = types.InlineKeyboardButton(text='Помощь', callback_data='help')
        keyboard.row_width = 1
        keyboard.add(key_create_room, key_join_room, key_score, key_help)
        return keyboard

    @staticmethod
    def build_game_type_menu():
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_open = types.InlineKeyboardButton(text='Открытая', callback_data='open')
        key_close = types.InlineKeyboardButton(text='Закрытая', callback_data='close')
        keyboard.row_width = 1
        keyboard.add(key_open, key_close)
        return keyboard

    @staticmethod
    def build_game_type_field():
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_1 = types.InlineKeyboardButton(text='Обычные', callback_data='EVKLID')
        key_2 = types.InlineKeyboardButton(text='На торе', callback_data='TORUS')
        key_3 = types.InlineKeyboardButton(text='На бутылке Клейна', callback_data='KLEIN')
        key_4 = types.InlineKeyboardButton(text='На проективной плоскости', callback_data='PROJECT')
        keyboard.row_width = 1
        keyboard.add(key_1, key_2, key_3, key_4)
        return keyboard

    @staticmethod
    def build_game_size_field():
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_1 = types.InlineKeyboardButton(text='3x3', callback_data='3')
        key_2 = types.InlineKeyboardButton(text='5x5', callback_data='5')
        key_3 = types.InlineKeyboardButton(text='7x7', callback_data='7')
        keyboard.row_width = 1
        keyboard.add(key_1, key_2, key_3)
        return keyboard