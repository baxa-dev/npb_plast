from bot.models import BotUser

def get_BotUser(tg_id) -> BotUser:
    try:
        return BotUser.objects.get(tg_id=tg_id)
    except BotUser.DoesNotExist:
        return None