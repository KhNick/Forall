import telebot

from builder import Builder
from room import Room
from scorer import Scorer

bot = telebot.TeleBot('6858483270:AAFMMZef-VL0-u-HCoJdf54sNdGPLOqFFEQ')

players_usernames = {}

players_games = {}

close_games = {}

players_messages = {}

rooms = []


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/begin':
        m = bot.send_message(message.from_user.id, "Введи username")
        call_del(m)
        bot.register_next_step_handler(message, draw_menu)
    else:
        m = bot.send_message(message.from_user.id, 'Напиши /begin')
        call_del(m)


def draw_menu(message):
    players_usernames[message.from_user.id] = message.text
    m = bot.send_message(message.from_user.id, text="Основное меню", reply_markup=Builder.build_main_menu())
    call_del(m)


def get_room_number(id):
    for i in range(len(rooms)):
        if rooms[i].id1 == id or rooms[i].id2 == id:
            return i
    return -1


def call_del(message):
    id = message.chat.id
    if not id in players_messages:
        players_messages[id] = []
    for old_message in players_messages[id]:
        bot.delete_message(old_message.chat.id, old_message.id, 0)
    players_messages[id] = [message]

def try_to_join(message):
    id = -1
    for i in players_usernames:
        if players_usernames[i] == message.text:
            id = i
    if id == -1:
        m = bot.send_message(message.from_user.id, text="Вы ошиблись", reply_markup=Builder.build_main_menu())
        call_del(m)
        return
    rooms.append(Room(id, message.from_user.id, close_games[id][0], close_games[id][1]))
    m1 = bot.send_message(message.from_user.id, text="Ваш ход " + players_usernames[message.from_user.id],
                          reply_markup=rooms[-1].get_keyboard())
    m2 = bot.send_message(id, text="Ждите ход, " + players_usernames[message.from_user.id],
                          reply_markup=rooms[-1].get_keyboard())
    call_del(m1)
    call_del(m2)
    close_games.pop(id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    data = call.data
    message = call.message
    if data == "create":
        m = bot.send_message(message.chat.id, text="Выберите тип игры", reply_markup=Builder.build_game_type_menu())
        call_del(m)
        return
    if data == "join":
        m = bot.send_message(message.chat.id, text="Введите username друга, создавшего закрытую игру")
        call_del(m)
        bot.register_next_step_handler(message, try_to_join)
        return
    if data == "open":
        players_games[message.chat.id] = []
        m = bot.send_message(message.chat.id, text="Выберите размер поля", reply_markup=Builder.build_game_size_field())
        call_del(m)
        return
    if data == "close":
        close_games[message.chat.id] = []
        m = bot.send_message(message.chat.id, text="Выберите размер поля", reply_markup=Builder.build_game_size_field())
        call_del(m)
        return
    if data in ["3", "5", "7"] and message.chat.id in players_games and len(players_games[message.chat.id]) == 0:
        players_games[message.chat.id].append(int(data))
        m = bot.send_message(message.chat.id, text="Выберите тип поля", reply_markup=Builder.build_game_type_field())
        call_del(m)
        return
    if data in ["3", "5", "7"] and message.chat.id in close_games and len(close_games[message.chat.id]) == 0:
        close_games[message.chat.id].append(int(data))
        m = bot.send_message(message.chat.id, text="Выберите тип поля", reply_markup=Builder.build_game_type_field())
        call_del(m)
        return
    if data in ["EVKLID", "KLEIN", "TORUS", "PROJECT"] and message.chat.id in players_games and len(players_games[message.chat.id]) == 1:
        players_games[message.chat.id].append(data)
        for id in players_games:
            if (id != message.chat.id) and (players_games[id] == players_games[message.chat.id]):
                rooms.append(Room(id, message.chat.id, players_games[id][0], players_games[id][1]))
                m1 = bot.send_message(message.chat.id, text="Ваш ход " + players_usernames[message.chat.id],
                                      reply_markup=rooms[-1].get_keyboard())
                m2 = bot.send_message(id, text="Ждите ход, " + players_usernames[message.chat.id],
                                      reply_markup=rooms[-1].get_keyboard())
                call_del(m1)
                call_del(m2)
                players_games.pop(id)
                players_games.pop(message.chat.id)
                break

        return
    if data in ["EVKLID", "KLEIN", "TORUS", "PROJECT"] and message.chat.id in close_games and len(close_games[message.chat.id]) == 1:
        close_games[message.chat.id].append(data)
        m1 = bot.send_message(message.chat.id, text="Ждите друга или выйдете через /begin" + players_usernames[message.chat.id])
        call_del(m1)
        return

    if data == "score":
        scorer = Scorer()
        m = bot.send_message(call.message.chat.id, text="Ваш рейтинг: " +
                             str(scorer.get_score_from_id(call.message.chat.id)),
                             reply_markup=Builder.build_help_menu())
        call_del(m)

    if data == "help":
        m = bot.send_message(call.message.chat.id, text="    Тип поля отвечает типу закленности, обычный - без, тор"
                                                        "нормально зацикленный по обоим сторонам, бутылка - нормально"
                                                        "зацикленный по горизонтали и инвертированный по вертикали, "
                                                        "проективная плоскость - инвертирована полностью.\n\n  "
                                                        "   Для поля 3х3 нужно собрать 3, для поля 5х5 нужно собрать 4"
                                                        "для полля 7х7 нужно собрать 5. \n\n  Для "
                                                        "перезагрузки просто снова пропишите /begin",
                             reply_markup=Builder.build_help_menu())
        call_del(m)
    if data == "main_menu":
        m = bot.send_message(call.message.chat.id, text="Основное меню", reply_markup=Builder.build_main_menu())
        call_del(m)
    user_id = message.chat.id
    num = get_room_number(user_id)
    if num != -1:
        data = list(map(int, data.split()))
        code, messages = rooms[num].put_symbol(user_id, data, bot, players_usernames)
        for i in messages:
            call_del(i)
        if code == -2:
            m = bot.send_message(rooms[num].id1, text="Основное меню", reply_markup=Builder.build_main_menu())
            # call_del(m)
            players_messages[rooms[num].id1].append(m)
            m = bot.send_message(rooms[num].id2, text="Основное меню", reply_markup=Builder.build_main_menu())
            # call_del(m)
            players_messages[rooms[num].id2].append(m)
            rooms.pop(num)


bot.polling(none_stop=True, interval=0)
