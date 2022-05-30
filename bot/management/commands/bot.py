from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.utils.request import Request
from bot.management.commands.func import start, full_name, phone_number, about, home, social, products, application, \
    about_name, home_name, social_name, products_name, application_name


class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            base_url=settings.PROXY_URL,
        )
        updater = Updater(
            bot=bot,
            use_context=True,

        )
        all_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                1: [
                    CommandHandler('start', start),
                    MessageHandler(Filters.text, full_name),
                ],
                2: [
                    CommandHandler('start', start),
                    MessageHandler(Filters.contact, phone_number)
                ],
                3: {
                    CommandHandler('start', start),
                    CallbackQueryHandler(about, pattern=f"^({about_name})$"),
                    CallbackQueryHandler(home, pattern=f"^({home_name})$"),
                    CallbackQueryHandler(social, pattern=f"^({social_name})$"),
                    CallbackQueryHandler(products, pattern=f"^({products_name})$"),
                    CallbackQueryHandler(application, pattern=f"^({application_name})$")
                },

            },
            fallbacks=[]
        )

        updater.dispatcher.add_handler(all_handler)
        updater.start_polling()
        updater.idle()
