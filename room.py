from telebot import types

from field import Field

from scorer import Scorer

class Room:
    def __init__(self, id1, id2, n, g_type):
        self.id1 = id1
        self.id2 = id2
        self.field = Field(n, n, g_type)

    def get_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        keyboard.row_width = self.field.width
        for i in range(self.field.height):
            l = []
            for j in range(self.field.height):
                key = types.InlineKeyboardButton(text=self.field.field_storage[i][j] + " ",
                                                 callback_data=str(i) + " " + str(j))  # кнопка
                l.append(key)
            keyboard.add(*l)
        return keyboard

    def put_symbol(self, id, cord, bot, names):
        messages = []
        if self.field.full_cells_count % 2 == 1:
            cur_id = self.id1
        else:
            cur_id = self.id2
        if cur_id != id:
            return -1, messages
        self.field.put(cord[0], cord[1])
        a, b, c, d = self.field.is_end()
        if a:
            if b == -1:
                m = bot.send_message(self.id1 + self.id2 - cur_id, text="Ничья", reply_markup=self.get_keyboard())
                messages.append(m)
                scorer = Scorer()
                if self.id2 != self.id1:
                    m = bot.send_message(cur_id, text="Ничья", reply_markup=self.get_keyboard())
                    scorer.draw(self.id1, self.id2)
                    messages.append(m)
            else:
                m = bot.send_message(self.id1 + self.id2 - cur_id, text="Лох", reply_markup=self.get_keyboard())
                messages.append(m)
                scorer = Scorer()
                if self.id2 != self.id1:
                    m = bot.send_message(cur_id, text="Гигачад", reply_markup=self.get_keyboard())
                    messages.append(m)
                    scorer.win(cur_id, self.id1 + self.id2 - cur_id)
            return -2, messages

        m = bot.send_message(self.id1 + self.id2 - cur_id, text="Ходите, " + names[self.id1 + self.id2 - cur_id], reply_markup=self.get_keyboard())
        messages.append(m)
        if self.id2 != self.id1:
            m = bot.send_message(cur_id, text="Ждите ход " + names[self.id1 + self.id2 - cur_id], reply_markup=self.get_keyboard())
            messages.append(m)
        return 0, messages



