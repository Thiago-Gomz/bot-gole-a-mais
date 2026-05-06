import telebot
import time
import feedparser
import threading
from flask import Flask # Adicionei o Flask (mais rápido para o Render detectar)
import os

# --- CONFIGURAÇÕES ---
TOKEN = '8507254870:AAEkof5aka8s_pdJ8KcyiZ1YuBirrUVUYZw'
CANAL_ID = '@PromoPorUmGoleAMais' 
SEU_ID_AMAZON = 'goleamais-20' 
# ---------------------

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def health_check():
    return "Robô Online", 200

def buscar_e_postar():
    while True:
        print("🔎 Buscando ofertas...")
        feed = feedparser.parse("https://www.pelando.com.br/rss/bebidas")
        for item in reversed(feed.entries):
            link = f"{item.link}?tag={SEU_ID_AMAZON}"
            msg = f"🍷 *OFERTA NO GOLE A MAIS!*\n\n{item.title}\n\n🛒 Link: {link}"
            try:
                bot.send_message(CANAL_ID, msg, parse_mode="Markdown")
                time.sleep(20)
            except: pass
        print("😴 Aguardando 1 hora...")
        time.sleep(3600)

if __name__ == "__main__":
    # Inicia o robô em segundo plano
    threading.Thread(target=buscar_e_postar, daemon=True).start()
    # Inicia o servidor web imediatamente na porta que o Render quer
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
