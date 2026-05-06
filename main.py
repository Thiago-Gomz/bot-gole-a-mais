import telebot
import time
import feedparser

# --- CONFIGURAÇÕES ---
TOKEN = '8507254870:AAEkof5aka8s_pdJ8KcyiZ1YuBirrUVUYZw'
CANAL_ID = '@PromoPorUmGoleAMais' 
SEU_ID_AMAZON = 'thiago-20' # Verifique se seu ID é esse mesmo
# ---------------------

bot = telebot.TeleBot(TOKEN)

def buscar_e_postar():
    url_feed = "https://www.pelando.com.br/rss/bebidas"
    feed = feedparser.parse(url_feed)
    
    for item in feed.entries:
        link_afiliado = f"{item.link}?tag={SEU_ID_AMAZON}"
        mensagem = (
            f"🍷 *OFERTA NO GOLE A MAIS!* 🍻\n\n"
            f"{item.title}\n\n"
            f"🛒 Confira aqui: {link_afiliado}\n\n"
            f"🔞 Beba com responsabilidade."
        )
        try:
            bot.send_message(CANAL_ID, mensagem, parse_mode="Markdown")
            time.sleep(30) 
        except:
            pass

if __name__ == "__main__":
    while True:
        buscar_e_postar()
        time.sleep(3600)
