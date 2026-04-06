import telebot
from telebot import types
import os
import requests
from bs4 import BeautifulSoup
import datetime

TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)


def get_schedule(soup):
    rows = soup.find_all("tr")
    schedule_dict = {}
    found = False
    for row in rows:
        row_text = row.get_text()
        if "31-п" in row_text:
            found = True
            continue
        if found:
            if "100-б" in row_text:
                break
            cells = row.find_all("td")
            if len(cells) >= 5:
                num_lesson = cells[0].get_text(strip=True)
                subject = cells[4].get_text(strip=True)
                cab = cells[-1].get_text(strip=True)
                if num_lesson:
                    try:
                        clean_num = int(num_lesson.replace(".", ""))
                        schedule_dict[clean_num] = [subject, cab]
                    except ValueError:
                        continue
    return schedule_dict


# Базовое расписание
schedule_base = [
    # День 1
    {
        1: ["", ""],
        2: ["", ""],
        3: ["Техника коммуникации и основы командообразования", "29-С"],
        4: ["Техника коммуникации и основы командообразования", "29-С"],
        5: ["Программные средства создания Интернет-приложений", "16-Б/22-Б"],
        6: ["Предпринимательская деятельность и управление проектами", "1-С"],
        7: ["Бухгалтерский учет", "25-Б"],
        8: ["Бухгалтерский учет", "25-Б"],
        9: ["Системы управления базами данных", "22-Б/16-Б"]
    },
    # День 2
    {
        1: ["", ""],
        2: ["Бухгалтерский учет", "26-Б"],
        3: ["Программные средства создания Интернет-приложений", "16-Б/22-Б"],
        4: ["Физическая культура и здоровье", "с/з"],
        5: ["Конструирование программ и языки программирования", "17-С/36-Б"],
        6: ["Конструирование программ и языки программирования", "17-С/36-Б"],
        7: ["Кураторский час", "6-С"],
        8: ["Системы управления базами данных", "22-Б/16-Б"]
    },
    # День 3
    {
        1: ["", ""],
        2: ["", ""],
        3: ["", ""],
        4: ["Тестирование программного обеспечения", "20-Б/16-Б"],
        5: ["Техника коммуникации и основы командообразования", "29-С"],
        6: ["Предпринимательская деятельность и управление проектами", "6-С"],
        7: ["Бухгалтерский учет", "25-Б"],
        8: ["Бухгалтерский учет", "25-Б"],
        9: ["Веб-программирование на стороне сервера", "22-Б/16-Б"],
    },
    # День 4
    {
        1: ["Конструирование программ и языки программирования", "17-С/36-Б"],
        2: ["Конструирование программ и языки программирования", "17-С/36-Б"],
        3: ["Бухгалтерский учет", "26-Б"],
        4: ["Физическая культура и здоровье", "с/з"],
        5: ["Тестирование программного обеспечения", "20-Б/16-Б"],
        6: ["Тестирование программного обеспечения", "20-Б/16-Б"],
        7: ["Информационный час", "6-С"]
    },
    # День 5
    {
        1: ["Системы управления базами данных", "22-Б/36-Б"],
        2: ["Системы управления базами данных", "22-Б/36-Б"],
        3: ["Техника коммуникации и основы командообразования", "1-С"],
        4: ["Техника коммуникации и основы командообразования", "1-С"],
        5: ["Предпринимательская деятельность и управление проектами", "1-С"],
        6: ["Бухгалтерский учет", "25-Б"],
        7: ["", ""]
    },
    # День 6
    {
        1: ["Системы управления базами данных", "22-Б/36-Б"],
        2: ["Программные средства создания Интернет-приложений", "16-Б/22-Б"],
        3: ["Программные средства создания Интернет-приложений", "16-Б/22-Б"],
        4: ["Тестирование программного обеспечения", "20-Б/16-Б"],
        5: ["Физическая культура и здоровье", "с/з"],
        6: ["Веб-программирование на стороне сервера", "22-Б/16-Б"],
        7: ["Веб-программирование на стороне сервера", "22-Б/16-Б"]
    }
]

day_list = [
    'https://docs.google.com/document/d/1sV5QloMUpfqkyfLLc59QmPTyBXNSUYA1/pub',
    'https://docs.google.com/document/d/16BoaCwKzlnWrmTYhuAcH42nhrv-IlOkt/pub',
    'https://docs.google.com/document/d/1nSdGG8YjdwCM9_KHVfXj0dk9tflhq_gX/pub',
    'https://docs.google.com/document/d/1yCtjpPTl1hb6PhlqJMCbbch9Tbh5NtSQ/pub',
    'https://docs.google.com/document/d/1No-WT977T-oS3OTTTG8s5RTfJw4RKUeK/pub',
    'https://docs.google.com/document/d/1biAObySxkm-xeFuR_1otpU_xT6YGMKmO/pub'
]


def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    btns = [
        types.InlineKeyboardButton("Понедельник", callback_data="btn1"),
        types.InlineKeyboardButton("Вторник", callback_data="btn2"),
        types.InlineKeyboardButton("Среда", callback_data="btn3"),
        types.InlineKeyboardButton("Четверг", callback_data="btn4"),
        types.InlineKeyboardButton("Пятница", callback_data="btn5"),
        types.InlineKeyboardButton("Суббота", callback_data="btn6")
    ]
    keyboard.row(btns[0], btns[1])
    keyboard.row(btns[2], btns[3])
    keyboard.row(btns[4], btns[5])
    return keyboard


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет! Выбери день недели:", reply_markup=get_main_keyboard())


@bot.message_handler(func=lambda message: True)
def menu(message):
    bot.send_message(message.chat.id, "Выбери день недели:", reply_markup=get_main_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_schedule(call):
    if call.data == "back":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выбери день недели:",
            reply_markup=get_main_keyboard()
        )
        return

    day_map = {"btn1": 0, "btn2": 1, "btn3": 2, "btn4": 3, "btn5": 4, "btn6": 5}

    if call.data in day_map:
        day_index = day_map[call.data]
        try:
            current_url = day_list[day_index]
            response = requests.get(current_url)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            result = get_schedule(soup)

            for key, value in result.items():
                if not value[0] and key in schedule_base[day_index]:
                    result[key][0] = schedule_base[day_index][key][0]
                if not value[-1] and key in schedule_base[day_index] and value[0][:3] != "нет":
                    result[key][-1] = schedule_base[day_index][key][-1]

            for num, sub in schedule_base[day_index].items():
                if num not in result:
                    result[num] = sub

            text = f"Расписание на выбранный день ({datetime.date.today()}):\n\n"

            for num, subject in sorted(result.items()):
                stat_cabs = ""
                status = subject if bool(subject[0]) else "нет"

                if status != "нет" and "/" not in status[-1] and len(status[-1]) > 4:
                    stat_cabs = f"{status[-1][:4]}/{status[-1][4:]}"
                else:
                    stat_cabs = str(status[-1])

                if isinstance(status, list):
                    status = str(status[0]).replace("[", "").replace("'", "").replace("]", "").replace(",", "")

                if 3 < len(stat_cabs) < 9:
                    stat_cabs = stat_cabs.replace("/", "", 1)

                if status == "нет":
                    text += f"{num}. {status}\n"
                else:
                    text += f"{num}. {status}: {stat_cabs}\n"

            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("Назад", callback_data="back"))

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard
            )
        except Exception as e:
            bot.answer_callback_query(call.id, "Ошибка при загрузке данных")
            print(f"Error: {e}")


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
