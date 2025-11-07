AUTHORIZED_USERS = [
    5164885358,  # Замените на Telegram ID учредителя
    6218636186   # Замените на Telegram ID генерального директора
]

def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS
