from collections import Counter
import re
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import Updater
TOKEN = '5115307867:AAHIQOIXPprhC2YcpgrZzdz41YZjNpx6ioc'
upd = Updater(TOKEN, use_context=True)
dp = upd.dispatcher
jq = upd.job_queue


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
    context.bot.send_message(chat_id=context.job.context,
                             text='Вы еще не отправили сегодня комплимент ' + a)


def callback_timer(update: Update, context: CallbackContext):
    job_minute = jq.run_repeating(callback_alarm, interval=86400, first=0)
    job_minute.enabled = True


timer_handler = CommandHandler('timer', callback_timer)
dp.add_handler(timer_handler)
