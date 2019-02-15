import json
from datetime import datetime

import requests
from hurry.filesize import size


def start(bot, update):
    print("Start for {}".format(bot))
    bot.send_message(chat_id=update.message.chat_id, text="RuTracker.org bot! Пиши /help и узнай как со мной общаться.")


def __convert_topic_info_in_human_format(topic_id: int):
    r = requests.get("http://api.rutracker.org/v1/get_tor_topic_data?by=topic_id&val={}".format(topic_id))
    if r.status_code is not 200:
        return
    response_json = json.loads(r.content)
    topic_info = response_json.get('result').get(str(topic_id))
    if type(topic_info) is not dict:
        return

    topic_title = topic_info.get("topic_title")
    reg_time = topic_info.get("reg_time")
    size_v = topic_info.get("size")
    date_h = datetime.fromtimestamp(reg_time).strftime("%B %d, %Y")
    size_h = size(size_v)

    return "{}\nДата: {}\nРазмер: {}".format(topic_title, date_h, size_h)


def get_section(bot, update, args):
    print("Getting section for {}".format(bot))
    forum_section_id = args[0]
    count = int(args[1])
    if not forum_section_id.isdigit():
        bot.send_message(chat_id=update.message.chat_id, text="ID форума не целое число")
        return
    r = requests.get("http://api.rutracker.org/v1/static/pvc/f/{}".format(forum_section_id))
    if r.status_code is not 200:
        bot.send_message(chat_id=update.message.chat_id, text="Не удалось получить данные(.")
        return
    response_json = json.loads(r.content)
    results = response_json.get('result')
    if type(results) is not dict:
        bot.send_message(chat_id=update.message.chat_id, text="Полученные данные не валидные")
        return

    sorted_keys = sorted([int(x) for x in list(results.keys())], reverse=True)
    for i in range(count):
        topic_id = sorted_keys[i]
        res_item = __convert_topic_info_in_human_format(topic_id)
        bot.send_message(chat_id=update.message.chat_id, text=res_item)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Неизвестная команда")
