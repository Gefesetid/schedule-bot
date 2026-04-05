import telebot
import os
import requests
from bs4 import BeautifulSoup
import datetime

TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

def get_schedule(url):
    rows = url.find_all("tr")
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

                if num_lesson:
                    clean_num = int(num_lesson.replace(".", ""))
                    schedule_dict[clean_num] = subject
    return schedule_dict


schedule = [
    {
        1: "",
        2: "Техника коммуникации и основы командообразования",
        3: "Техника коммуникации и основы командообразования",
        4: "Программные средства создания Интернет-приложений",
        5: "Предпринимательская деятельность и управление проектами",
        6: "Бухгалтерский учет",
        7: "Бухгалтерский учет",
        8: "Системы управления базами данных"
    },
    {
        1: "Бухгалтерский учет",
        2: "Программные средства создания Интернет-приложений",
        3: "Физическая культура и здоровье",
        4: "Конструирование программ и языки программирования",
        5: "Конструирование программ и языки программирования",
        6: "Кураторский час",
        7: "Системы управления базами данных"
    },
    {
        1: "",
        2: "",
        3: "",
        4: "Тестирование программного обеспечения",
        5: "Техника коммуникации и основы командообразования",
        6: "Предпринимательская деятельность и управление проектами",
        7: "Бухгалтерский учет",
        8: "Бухгалтерский учет",
        9: "Веб-программирование на стороне сервера"
    },
    {
        1: "Конструирование программ и языки программирования",
        2: "Конструирование программ и языки программирования",
        3: "Бухгалтерский учет",
        4: "Физическая культура и здоровье",
        5: "Тестирование программного обеспечения",
        6: "Тестирование программного обеспечения",
        7: "Информационный час"
    },
    {
        1: "Системы управления базами данных",
        2: "Системы управления базами данных",
        3: "Техника коммуникации и основы командообразования",
        4: "Техника коммуникации и основы командообразования",
        5: "Предпринимательская деятельность и управление проектами",
        6: "Бухгалтерский учет",
        7: ""
    },
    {
        1: "Системы управления базами данных",
        2: "Программные средства создания Интернет-приложений",
        3: "Программные средства создания Интернет-приложений",
        4: "Тестирование программного обеспечения",
        5: "Физическая культура и здоровье",
        6: "Веб-программирование на стороне сервера",
        7: "Веб-программирование на стороне сервера"
    }
]

day_index = datetime.datetime.now().weekday()

Monday = 'https://docs.google.com/document/d/1sV5QloMUpfqkyfLLc59QmPTyBXNSUYA1/pub'
Tuesday = 'https://docs.google.com/document/d/16BoaCwKzlnWrmTYhuAcH42nhrv-IlOkt/pub'
Wednesday = 'https://docs.google.com/document/d/1nSdGG8YjdwCM9_KHVfXj0dk9tflhq_gX/pub'
Thursday = 'https://docs.google.com/document/d/1yCtjpPTl1hb6PhlqJMCbbch9Tbh5NtSQ/pub'
Friday = 'https://docs.google.com/document/d/1No-WT977T-oS3OTTTG8s5RTfJw4RKUeK/pub'
Saturday = 'https://docs.google.com/document/d/1biAObySxkm-xeFuR_1otpU_xT6YGMKmO/pub'

day_list = [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday]
if day_index < 6:
    current_url = day_list[day_index]
    response = requests.get(current_url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    result = get_schedule(soup)
    for key, value in result.items():
        if not value and key in schedule[day_index]:
            result[key] = schedule[day_index][key]
    
    text = "📅 Расписание на сегодня:\n\n"
    for num, subject in sorted(result.items()):
        status = subject if subject else "---"
        text += f"{num}. {status}\n"

    bot.send_message(CHAT_ID, text)
else:
    bot.send_message(CHAT_ID, "Сегодня воскресенье. Отдых.")
