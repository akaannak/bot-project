import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler,MessageHandler
from telegram.ext import Updater, messagequeue as mq
from telegram.ext import Filters, CallbackContext
import telebot
import pyjokes
from googletrans import Translator
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import SessionPasswordNeededError
import requests, random
from lxml import html
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import re
#from main2 import scrabThePage
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)
TOKEN = '5115307867:AAHIQOIXPprhC2YcpgrZzdz41YZjNpx6ioc'
bot = telebot.TeleBot(TOKEN)
defaultRecipient = 'anyakek'
# Этапы/состояния разговора
FIRST, SECOND = range(2)
api_id = 10221412  # Telegram api_id
api_hash = '32a69c2376c8ce1805e142083abb136a'  # Telegram api_hash
# Данные обратного вызова
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN = range(10)
upd = Updater(TOKEN, use_context=True)
dp = upd.dispatcher
jq = upd.job_queue
from collections import Counter

def send_message():
    with open('top.txt') as f:
        text = f.read()
    words = re.findall(r'\w+', text)
    cap_words = [word.upper() for word in words]
    word_counts = Counter(cap_words)
    sorted_dict = {}
    sorted_keys = sorted(word_counts, key=word_counts.get)
    for w in sorted_keys:
        sorted_dict[w] = word_counts[w]
    value = list(sorted_dict.keys())[-1]
    return value

def callback_alarm(context: CallbackContext):
    a = send_message()
    context.bot.send_message(chat_id=context.job.context, text=a)

def callback_timer(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Setting a timer for 1 minute!')

    job_minute = jq.run_repeating(callback_alarm, interval=86400, first=0)


timer_handler = CommandHandler('timer', callback_timer)
dp.add_handler(timer_handler)


def start(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s начал разговор", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("для нее", callback_data=str(ONE)),
            InlineKeyboardButton("для него", callback_data=str(TWO)),
        ],
        [InlineKeyboardButton("для меня", callback_data=str(THREE))],
        [InlineKeyboardButton("завершить сегодняший сеанс", callback_data=str(TEN))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        text="Выберите опцию :)", reply_markup=reply_markup
    )
    return FIRST


def start_over(update, _):
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("для нее", callback_data=str(ONE)),
            InlineKeyboardButton("для него", callback_data=str(TWO)),
        ],
        [InlineKeyboardButton("для меня", callback_data=str(THREE))],
        [InlineKeyboardButton("завершить сегодняший сеанс", callback_data=str(TEN))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Выберите опцию :)", reply_markup=reply_markup
    )
    return FIRST


def for_her(update, _):
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Комплимент", callback_data=str(FOUR)),
            InlineKeyboardButton("Анекдот", callback_data=str(FIVE))
         ],
        [InlineKeyboardButton("Вернуться в главное меню", callback_data=str(SEVEN))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Что мы отправим ей сегодня?", reply_markup=reply_markup
    )
    return FIRST


def for_him(update, _):
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Комплимент", callback_data=str(NINE)),
            InlineKeyboardButton("Анекдот", callback_data=str(FIVE))
         ],
        [InlineKeyboardButton("Вернуться в главное меню", callback_data=str(SEVEN))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Что мы отправим ему сегодня?", reply_markup=reply_markup
    )
    return FIRST


def for_me(update, _):
    """Показ выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Узнать процент удачи на сегодня", callback_data=str(SIX)),
            InlineKeyboardButton("Успокаивающая картинка с котиком", callback_data=str(EIGHT)),
        ],
        [InlineKeyboardButton("Вернуться в главное меню", callback_data=str(SEVEN))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Ваши пожелания на сегодня?", reply_markup=reply_markup
    )
    return FIRST


def four(update, _):
    def scrabThePage2(page_number, complCollection, link):
        page = requests.get(link + str(page_number) + '/')
        tree2 = html.fromstring(page.content)
        complCollection.extend(tree2.xpath('//a[@class="post-copy btn"]/@data-clipboard-text'))

    def talk_to_me(update, _):
        global flag
        keyboard = [
            [InlineKeyboardButton("Вернуться в главное меню", callback_data=str(SEVEN))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = update.message.text
        mask = re.compile('[a-zA-Z0-9_]')
        is_correct_input = False
        sendToUsername = text
        is_correct_input = mask.search(sendToUsername)
        if not is_correct_input:
            update.message.reply_text("Введенное имя пользователя содержит недопустимые символы, повторите попытку", reply_markup=reply_markup)
        else:
            with open('top.txt', 'a') as file:
                file.write(text)
                file.write('\n')

            update.message.reply_text(random.choice(all_compliments), reply_markup=reply_markup)
            flag = False
    all_compliments = []
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Сбор комплиментов...")
    i = 1
    while i <= 6:
        scrabThePage2(i, all_compliments, 'https://datki.net/komplimenti/zhenshine/page/')
        i += 1
    bot.send_message(chat_id=update.effective_chat.id,
                     text='Сбор завершен')
    bot.send_message(chat_id=update.effective_chat.id, text='Введите имя пользователя: ')
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, talk_to_me))
def four2(update, _):
    def scrabThePage(page_number, complCollection, link):
        page = requests.get(link + str(page_number) + '/')
        tree = html.fromstring(page.content)
        complCollection.extend(tree.xpath('//a[@class="post-copy btn"]/@data-clipboard-text'))

    def talk_to_me(update, _):
        keyboard = [
            [InlineKeyboardButton("Вернуться в главное меню", callback_data=str(SEVEN))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text('', reply_markup=reply_markup)
        text = update.message.text
        update.message.reply_text(random.choice(all_compliments))


    all_compliments = []
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Сбор комплиментов...")
    i = 1
    while i <= 6:
        scrabThePage(i, all_compliments, 'https://datki.net/komplimenti/muzhchine/page/')
        i += 1
    bot.send_message(chat_id=update.effective_chat.id,
                     text='Сбор завершен')
    bot.send_message(chat_id=update.effective_chat.id, text='Введите имя пользователя: ')
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, talk_to_me))

def five(update, _):
    translator = Translator()
    joke = pyjokes.get_joke()
    result = translator.translate(joke, dest='ru')
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Вернуться в главное меню", callback_data=str(SEVEN))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=result.text, reply_markup=reply_markup)

def six(update, _):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Вернуться в главное меню", callback_data=str(SEVEN))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    n = random.randint(1, 101)
    query.edit_message_text(text=str(n) + '%', reply_markup= reply_markup)


def eight(update, _):

    def get_all_images(url):
        soup = bs(requests.get(url).content, "html.parser")
        urls = []
        for img in tqdm(soup.find_all("img"), "Extracting images"):
            img_url = img.attrs.get("src")
            if not img_url:
                # если img не содержит атрибута src, просто пропустите
                continue
            img_url = urljoin(url, img_url)
            if img_url[-4:len(url)] == '.jpg' or img_url[-4:len(url)] == '.png':
                urls.append(img_url)
        return urls

    #get_all_images('https://bigpicture.ru/100-luchshix-fotografij-koshek-vsex-vremen-i-narodov/')
    bot.send_photo(chat_id=update.effective_chat.id, photo=random.choice(get_all_images('https://bigpicture.ru/100-luchshix-fotografij-koshek-vsex-vremen-i-narodov/')))
    bot.send_message(chat_id=update.effective_chat.id, text='Что-то еще? Не волнуйся, картинка будет оставаться тут и радовать тебе взор :)')
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Узнать процент удачи на сегодня", callback_data=str(SIX)),
            InlineKeyboardButton("Успокаивающая картинка с котиком", callback_data=str(EIGHT)),
        ],
        [InlineKeyboardButton("Вернуться в главное меню", callback_data=str(SEVEN))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Выберите опцию :)", reply_markup=reply_markup
    )

def end(update, _):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="возвращайся снова!:)")
    return ConversationHandler.END



if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(for_her, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(for_him, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(for_me, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
                CallbackQueryHandler(five, pattern='^' + str(FIVE) + '$'),
                CallbackQueryHandler(six, pattern='^' + str(SIX) + '$'),
                CallbackQueryHandler(eight, pattern='^' + str(EIGHT) + '$'),
                CallbackQueryHandler(four2, pattern='^' + str(NINE) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(SEVEN) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(TEN) + '$'),
            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
