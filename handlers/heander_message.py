import re
import datetime

def text_is_emply(text):
    if text == '':
        return True
    if text != '':
        return False

def handlers_message(text):

    info_message = {
        'text': '',
        'date': '',
        'status': ''
    } # создаём словарь который будем возвращать

    if 'через' in text.lower(): # проверяем есть ли в тексте "через"
        text = text.replace('через', '')
        if 'минуту' in text.lower(): # если через минуту
            text = text.replace('минуту', '').strip()
            if text_is_emply(text):
                info_message['status'] = 'no text'
                info_message['text'] = text
                return info_message
            else:
                info_message['text'] = text
                info_message['status'] = 'nice'
                info_message['date'] = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M")
                return info_message

        if 'час' in text.lower(): # если через час
            text = text.replace('час', '').strip()
            if text_is_emply(text):
                info_message['status'] = 'no text'
                info_message['text'] = text
                return info_message
            else:
                info_message['text'] = text
                info_message['status'] = 'nice'
                info_message['date'] = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
                return info_message

        #если нет через митинуту или через час дальше проверяем
        #Проверка если минуты
        time_rem = re.findall(r'\bмин(ут)|мин(ут)?\b', text)
        count_min = re.findall(r'\d+', text)
        if time_rem:
            text = re.sub(r'\bмин(уты)|мин(ут)?\b|через|\d+', '', text).strip() # убираем "минут" "мин" и все числа
            if text == '': # если нет текста
                info_message['status'] = 'no text'
                info_message['text'] = text
                return info_message
            info_message['text'] = text
            info_message['date'] = (datetime.datetime.now() + datetime.timedelta(minutes=int(count_min[0]))).strftime("%Y-%m-%d %H:%M")
            return info_message
        time_rem = re.findall(r'\bчаса|часов?\b', text)
        count_hour = re.findall(r'\d+', text)
        # Проверка если часы
        if time_rem:
            text = re.sub(r'\bчас(а)|час(ов)?\b|через|\d+', '', text).strip()  # убираем "минут" "мин" и все числа
            if text == '':  # если нет текста
                info_message['status'] = 'no text'
                info_message['text'] = text
                return info_message
            info_message['text'] = text
            info_message['date'] = (datetime.datetime.now() + datetime.timedelta(hours=int(count_hour[0]))).strftime("%Y-%m-%d %H:%M")
            return info_message

    #Начинаем проверять если есть завтра
    if 'завтра' in text.lower(): # обработка если есть "завтра"
        text = text.replace('завтра', '')
        info_message['date'] = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        if text == '':
            info_message['status'] = 'no text'
            info_message['text'] = text
            return info_message

        pattern = r'\b(?:[01]?\d|2[0-3]):[0-5]\d\b'
        # Поиск всех вхождений времени в строке
        time_found_hh_mm = re.findall(pattern, text)
        # pattern = r'\b(?:[01]?\d|2[0-3]):[0-5]\d\b'
        pattern = r'в \d+'
        time_found_only_hh = re.findall(pattern, text)
        if any([time_found_hh_mm, time_found_only_hh]):# проверяем указали ли время
            try:
                text = text.replace(time_found_hh_mm[0], '')
            except:
                text = text.replace(time_found_only_hh[0], '')

            time_found_only_hh = f"{time_found_only_hh[0].replace('в', '').strip()}:00"

            if ' в ' in text:
                text = text.replace('в', '')

            try:
                info_message['date'] = datetime.datetime.strptime(info_message['date'] + ' ' + time_found_hh_mm[0], "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
            except:
                info_message['date'] = datetime.datetime.strptime(info_message['date'] + ' ' + time_found_only_hh, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")

        else:
            info_message['date'] = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d") + ' 12:00'
        info_message['text'] = text.strip()
        info_message['status'] = 'nice'
        return info_message
    # проверка есть ли дата в тексте
    date_pattern = r'\b\d{4}\.\d{2}\.\d{2}\b'
    date_in_text = re.findall(date_pattern, text)
    if date_in_text:
        print('date')
        text = text.replace(date_in_text[0], '')

        pattern = r'\b(?:[01]?\d|2[0-3]):[0-5]\d\b'
        # Поиск всех вхождений времени в строке
        time_found = re.findall(pattern, text)
        pattern = r'в \d+'
        time_found_2 = re.findall(pattern, text)
        info_message['date'] = date_in_text[0].replace('.', '-')
        print(info_message)
        if any([time_found, time_found_2]):
            try:
                text = text.replace(time_found[0], '')
            except:
                text = text.replace(time_found_2[0], '')
                time_found_2 = f"{time_found_2[0].replace('в', '').strip()}:00"

            if ' в ' or 'в' in text:
                text = text.replace('в', '').strip()
            if text == '':
                info_message['status'] = 'no text'
                info_message['text'] = text
                return info_message

            # info_message['date'] = datetime.datetime.strptime(info_message['date'] + ' ' + time_found[0], "%Y-%m-%d %H:%M")
            # info_message['text'] = text.replace(time_found[0], '').strip()

            print(time_found_2)
            try:
                info_message['date'] = info_message['date'] + ' ' + time_found[0]
            except:
                info_message['date'] = info_message['date'] + ' ' + time_found_2
            # проверка на время, чтобы не было прошлого времени
            info_message['status'] = 'nice'
            return info_message
        else:
            info_message['text'] = text
            info_message['status'] = 'nice'
            return info_message

    #прошлая проверка окончена, начинаем искать дальше если не вернули, это последняя  проверка

    pattern = r'\b(?:[01]?\d|2[0-3]):[0-5]\d\b'
    # Поиск всех вхождений времени в строке
    time_found = re.findall(pattern, text)
    pattern = r'в \d+'
    time_found_2 = re.findall(pattern, text)
    info_message['date'] = (datetime.datetime.now()).strftime("%Y-%m-%d")
    if any([time_found, time_found_2]):  # проверяем указали ли время
        try:
            text = text.replace(time_found[0], '')
        except:
            text = text.replace(time_found_2[0], '')
        try:
            time_found_2 = f"{time_found_2[0].replace('в', '').strip()}:00"
        except:
            pass
        if ' в ' in text:
            text = text.replace(' в ', '').strip()
        if 'сегодня' in text.lower():
            text = text.lower().replace('сегодня', '').strip()
        if text == '':
            info_message['status'] = 'no text'
            info_message['text'] = text
            return info_message

        # info_message['date'] = datetime.datetime.strptime(info_message['date'] + ' ' + time_found[0], "%Y-%m-%d %H:%M")
        # info_message['text'] = text.replace(time_found[0], '').strip()
        try:
            info_message['date'] = datetime.datetime.strptime(info_message['date'] + ' ' + time_found[0],"%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
        except:
            info_message['date'] = datetime.datetime.strptime(info_message['date'] + ' ' + time_found_2, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
        #проверка на время, чтобы не было прошлого времени
        info_message['status'] = 'nice'
        info_message['text'] = text
        return info_message

    # если не прошло ничего но есть текст, то скорей всего дата не указа
    info_message['text'] = text
    info_message['status'] = 'no date'
    return info_message

# print(handlers_message('туса 2024.01.23 в 19:31'))
# print(handlers_message('туса сегодня 19:31'))