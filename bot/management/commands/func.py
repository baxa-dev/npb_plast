from django.conf import settings
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from bot.models import BotUser
from bot.management.commands.utils import get_BotUser

about_name = "about"
home_name = "home"
products_name = "products"
social_name = "social"
application_name = "application"
group_username = "@nbpplast"
a = """Компания ⚜️New Public Build⚜️- один из лидеров отрасли по производству полиэтиленовых труб!

❕Кратко о нас:

▪️2 года на рынке
▪️Трубы из первичного сырья;
▪️Доставка по всему Узбекистану;
▪️Работа с Гос. проектами
"""


def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user = get_BotUser(user_id)
    if user:
        if user.is_active:
            keyboard = [
                [
                    InlineKeyboardButton("О нас 🛡", callback_data=about_name),
                    InlineKeyboardButton("наши соц сети 🌐", callback_data=social_name)
                ],
                [
                    InlineKeyboardButton("заказать политиленвыйе трубы 🛠", callback_data=products_name)
                ]
            ]
            update.message.reply_html(
                "Официальный бот компании npb plast ."
                "Здесь Вы сможете выбрать нужную Вам трубы  и оставить заявку 👩‍💻",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return 3
    else:
        BotUser.objects.create(tg_id=user_id)
    update.message.reply_html("Введите свое полное имя")
    return 1


def full_name(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    user = get_BotUser(user_id)
    user.full_name = update.message.text
    user.save()

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton('Поделиться контактом', request_contact=True)]],
                                       resize_keyboard=True)
    update.message.reply_html("Отправьте свой номер телефона", reply_markup=reply_markup)
    return 2


def phone_number(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    user = get_BotUser(user_id)
    user.phone = update.message.contact.phone_number
    user.is_active = True
    user.save()
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("О нас 🛡", callback_data=about_name),
            InlineKeyboardButton("наши соть сети 🌐", callback_data=social_name)
        ],
        [
            InlineKeyboardButton("заказать политиленвыйе трубы 🛠", callback_data=products_name)
        ]
    ])
    update.message.reply_html(
        "Официальный бот компании npb plast . Здесь Вы сможете выбрать нужную Вам трубы  и оставить заявку 👩‍💻",
        reply_markup=keyboard)
    return 3


def home(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.delete_message()
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("О нас 🛡", callback_data=about_name),
            InlineKeyboardButton("наши соц сети 🌐", callback_data=social_name)
        ],
        [
            InlineKeyboardButton("заказать политиленвыйе трубы 🛠", callback_data=products_name)
        ]
    ])
    query.message.reply_html(
        "Официальный бот компании npb plast . Здесь Вы сможете выбрать нужную Вам трубы  и оставить заявку 👩‍💻",
        reply_markup=keyboard)


def about(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.delete_message()
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data=home_name)]])
    query.message.reply_html(a, reply_markup=keyboard)


def products(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("➕ оставить заявку", callback_data=application_name),
        InlineKeyboardButton("🔙 Назад", callback_data=home_name)
    ]])
    try:
        file = open(str(settings.STATIC_ROOT) + "/nbp.pdf", 'rb')
        query.delete_message()
        query.message.reply_document(document=file, reply_markup=keyboard)
    except FileNotFoundError:
        print(str(settings.STATIC_ROOT))


def social(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.delete_message()
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Фейсбук", url="https://m.facebook.com/npbplast/"),
        InlineKeyboardButton("Инстаграм", url="https://instagram.com/npb_plast?utm_medium=copy_link"),
        InlineKeyboardButton("Телеграм", callback_data="https://t.me/npb_plast"),
    ],
        [
            InlineKeyboardButton("🔙 Назад", callback_data=home_name)
        ]
    ])
    query.message.reply_html("Наши соц сети 🌐", reply_markup=keyboard)


def application(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer(text=f'Спасибо за отправку заявки! ✅', show_alert=True)
    user_id = query.from_user.id
    user = get_BotUser(user_id)
    context.bot.send_message(chat_id=group_username, parse_mode="html",
                             text='<b>{}</b>\n<b>👤Имя:</b> {}\n<b>📞Номер телефона:</b> {} '
                             .format('политиленвыйе трубы 🛠'.title(), user.full_name, user.phone))
