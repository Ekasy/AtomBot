import telebot
import weather, smart_talking, file_converter, news, text_recognising, schedule
import config

bot = telebot.TeleBot(config.TOKEN_BOT)


available_extension = ['djvu', 'doc', 'docx', 'txt', 'xlsx', 'ppt', 'jpg', 'png']


@bot.message_handler(content_types=['text'])
def bot_talking(message):
    bot.send_chat_action(message.chat.id, action='typing')
    if weather.is_weather(message.text.lower()):
        bot.send_message(message.chat.id, weather.get_weather(message.text.lower()))
    elif news.is_news(message.text.lower()):
        bot.send_message(message.chat.id, news.get_news(message.text.lower()))
    elif schedule.is_schedule(message.text.lower()):
        result = schedule.get_schedule(message.text.upper())
        if isinstance(result, str):
            bot.send_message(message.chat.id, result)
        else:
            bot.send_photo(message.chat.id, caption='Держи!', photo=result)
    else:
        bot.send_message(message.chat.id, smart_talking.get_smart_talking(message.text))


@bot.message_handler(content_types=['document', 'audio'])
def convert_docs(message):
    bot.send_message(message.chat.id, 'Сейчас преобразую')
    bot.send_chat_action(message.chat.id, action='typing')
    file_name = message.document.file_name
    file_path = bot.get_file(message.document.file_id).file_path
    extension = file_converter.get_extension(file_name)
    if extension == 'pdf':
        bot.send_message(message.chat.id, 'Эм... это уже pdf файл...')
    if extension in available_extension:
        link = file_converter.convert_to_pdf(file_name, extension, file_path, str(message.chat.id))
        bot.send_message(message.chat.id, link)


@bot.message_handler(content_types=['photo'])
def recognise_text_by_photo(message):
    bot.send_message(message.chat.id, 'Погоди секунду')
    bot.send_chat_action(message.chat.id, action='typing')
    file_id = message.json['photo'][0]['file_id']
    lang = None if message.caption is None else message.caption.lower()
    bot.send_message(message.chat.id, text_recognising.text_recognising(bot.get_file_url(file_id),
                                                                        lang))


bot.polling(none_stop=True)
