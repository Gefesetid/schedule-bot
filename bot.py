import telebot
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

day_index = datetime.datetime.now().weekday()

day_list = [
    'https://docs.google.com/document/d/1sV5QloMUpfqkyfLLc59QmPTyBXNSUYA1/pub',  # Пн
    'https://docs.google.com/document/d/16BoaCwKzlnWrmTYhuAcH42nhrv-IlOkt/pub',  # Вт
    'https://docs.google.com/document/d/1nSdGG8YjdwCM9_KHVfXj0dk9tflhq_gX/pub',  # Ср
    'https://docs.google.com/document/d/1yCtjpPTl1hb6PhlqJMCbbch9Tbh5NtSQ/pub',  # Чт
    'https://docs.google.com/document/d/1No-WT977T-oS3OTTTG8s5RTfJw4RKUeK/pub',  # Пт
    'https://docs.google.com/document/d/1biAObySxkm-xeFuR_1otpU_xT6YGMKmO/pub'  # Сб
]

if day_index < 6:
    try:
        current_url = day_list[day_index]
        response = requests.get(current_url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        result = get_schedule(soup)
        # Накладываем изменения на базу
        for key, value in result.items():
            if not value[0] and key in schedule_base[day_index]:
                result[key][0] = schedule_base[day_index][key][0]
            if not value[-1] and key in schedule_base[day_index] and value[0][:3] != "нет":
                result[key][-1] = schedule_base[day_index][key][-1]

        # Если в изменениях вообще нет пары, берем её из базы
        for num, sub in schedule_base[day_index].items():
            if num not in result:
                result[num] = sub

        # Формируем текст
        text = f"Расписание на сегодня ({datetime.date.today()}):\n\n"

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
        bot.send_message(CHAT_ID, text)
    except Exception as e:
        bot.send_message(CHAT_ID, f"Произошла ошибка: {e}")
else:
    bot.send_message(CHAT_ID, "Сегодня воскресенье.")
