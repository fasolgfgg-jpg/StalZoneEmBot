import sys
import telebot
import Debug
import Tools
from Config import Config, ConfigError
import time as sleeper
from datetime import datetime, timedelta, timezone
import threading

# Проверяем конфиг до старта: если чего-то не хватает — падаем сразу и с понятным сообщением
try:
    Config.validate()
except ConfigError as e:
    sys.exit(f"\033[91m[Config]\033[0;0m {e}")

TOKEN = Config.get("TG_CLIENT_TOKEN")
bot = telebot.TeleBot(TOKEN)
Debug.NewFileLogs(datetime.now(timezone.utc).strftime("%Y.%d.%m %H %M %S"))
Debug.WriteLine("Info", f"Бот был запущен в {datetime.now(timezone.utc).strftime("%Y-%d-%m %H:%M:%S")}")


#----------------------------------------Commands------------------------------------#
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Команды бота находятся в разработке, вы можете подписаться на уведомления о выбросах в нашем канале: t.me/InformSCX")
    sleeper.sleep(10)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Команды бота находятся в разработке, вы можете подписаться на уведомления о выбросах в нашем канале: t.me/InformSCX")
    sleeper.sleep(10)
#----------------------------------------Commands------------------------------------#


#----------------------------------------Checker------------------------------------#

def check():
    StartTime = datetime.now().strftime("%H:%M:%S")
    while True:
        emission = False
        try:
            fdata = Tools.Tool.EmissionCheck().json()
            previous_start = datetime.fromisoformat(fdata["currentStart"].replace("Z", "+00:00"))

            StartTime = previous_start
            ctime = datetime.now(timezone.utc)
            l_bound = previous_start - timedelta(seconds=30)
            u_bound = previous_start + timedelta(seconds=30)
            emission = l_bound <= ctime <= u_bound
        except Exception as e:
            if str(e) == "'currentStart'":
                pass
            else:
                Debug.WriteLine("Error", f"Ошибка при попытке выполнить запрос {e}")

        if emission:
            Debug.WriteLine("Info", "Выброс скоро начнется! Сообщение готово к отправке")
            sender(StartTime)
            sleeper.sleep(200)
        else:
            Debug.WriteLine("Info","Выброс не ожидается")


        sleeper.sleep(25)
def sender(CurrentTime: datetime):

    StartTime = CurrentTime + timedelta(hours=3)
    EndTime = CurrentTime + timedelta(minutes=4) + timedelta(hours=3)

    import GetOnline
    try:
        try:
            f = open('MessageID.ids', 'r')
            end_id = f.readline()
            bot.delete_messages("@InformSCX", message_ids=[int(end_id)])
            f.close()
        except:
            pass
        photo = open("photo.png", "rb")
        bot.send_photo("@InformSCX", photo= photo, caption= "☢️ Выброс начался!\n\n"
                                     f"🕥 **Время начала:** {StartTime.strftime("%H:%M")} (по МСК)\n"
                                     f"🕚 **Время окончания:** {EndTime.strftime("%H:%M")} (по МСК)\n\n"
                                     f"👥 Онлайн: {GetOnline.Online.GetStalCraftOnline()}\n\n"
                                     f"[t.me/SZInform](https://t.me/SZInform)", parse_mode='Markdown')

        sleeper.sleep(240)

        f = open('MessageID.ids', 'a')
        #f.write(f"{em_id.message_id}\n")

        end_id = bot.send_message("@InformSCX", "☁️ Выброс закончился!")
        f.write(f"{end_id.message_id}\n")
        f.close()



        Debug.WriteLine("Info","Сообщение отправлено!")
    except Exception as e:
        Debug.WriteLine("Error",f"Ошибка при отправке сообщения: {e}")

#----------------------------------------Checker------------------------------------#

#check()
# Запуск чекера
threading.Thread(target=check).start()

# Запуск бота
bot.polling(none_stop=True)


