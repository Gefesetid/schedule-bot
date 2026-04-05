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

                if num_lesson:
                    try:
                        clean_num = int(num_lesson.replace(".", ""))
                        schedule_dict[clean_num] = subject
                    except ValueError:
                        continue
    return schedule_dict


schedule_base = [
    {1: "", 2: "Техника коммуникации...", 3: "Техника коммуникации...", 4: "ПС создания Интернет-приложений", 5: "Предпринимательская деят.", 6: "Бухгалтерский учет", 7: "Бухгалтерский учет", 8: "СУБД"},
    {1: "Бухгалтерский учет", 2: "ПС создания Интернет-приложений", 3: "Физкультура", 4: "Конструирование программ", 5: "Конструирование программ", 6: "Кураторский час", 7: "СУБД"},
    {1: "", 2: "", 3: "", 4: "Тестирование ПО", 5: "Техника коммуникации...", 6: "Предпринимательская деят.", 7: "Бухгалтерский учет", 8: "Бухгалтерский учет", 9: "Веб-программирование"},
    {1: "Конструирование программ", 2: "Конструирование программ", 3: "Бухгалтерский учет", 4: "Физкультура", 5: "Тестирование ПО", 6: "Тестирование ПО", 7: "Информационный час"},
    {1: "СУБД", 2: "СУБД", 3: "Техника коммуникации...", 4: "Техника коммуникации...", 5: "Предпринимательская деят.", 6: "Бухгалтерский учет", 7: ""},
    {1: "СУБД", 2: "ПС создания Интернет-приложений", 3: "ПС создания Интернет-приложений", 4: "Тестирование ПО", 5: "Физкультура", 6: "Веб-программирование", 7: "Веб-программирование"}
]

day_index = datetime.datetime.now().weekday()

day_list = [
    'https://docs.google.com/document/d/1sV5QloMUpfqkyfLLc59QmPTyBXNSUYA1/pub',
    'https://docs.google.com/document/d/16BoaCwKzlnWrmTYhuAcH42nhrv-IlOkt/pub',
    'https://docs.google.com/document/d/1nSdGG8YjdwCM9_KHVfXj0dk9tflhq_gX/pub',
    'https://docs.google.com/document/d/1yCtjpPTl1hb6PhlqJMCbbch9Tbh5NtSQ/pub', 
    'https://docs.google.com/document/d/1No-WT977T-oS3OTTTG8s5RTfJw4RKUeK/pub', 
    'https://docs.google.com/document/d/1biAObySxkm-xeFuR_1otpU_xT6YGMKmO/pub'
]

if day_index < 6:
    try:
        current_url = day_list[day_index]
        response = requests.get(current_url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        result = get_schedule(soup)
        
        for key, value in result.items():
            if not value and key in schedule_base[day_index]:
                result[key] = schedule_base[day_index][key]
        
        for num, sub in schedule_base[day_index].items():
            if num not in result:
                result[num] = sub

        text = f"Расписание на сегодня ({datetime.date.today()}):\n\n"
        for num, subject in sorted(result.items()):
            status = subject if subject else "---"
            text += f"{num}. {status}\n"

        bot.send_message(CHAT_ID, text)
    except Exception as e:
        bot.send_message(CHAT_ID, f"Произошла ошибка: {e}")
else:
    bot.send_message(CHAT_ID, "Сегодня воскресенье.")
