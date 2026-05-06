import telebot
import time
import feedparser

# --- CONFIGURAÇÕES ---
TOKEN = '8507254870:AAEkof5aka8s_pdJ8KcyiZ1YuBirrUVUYZw'
CANAL_ID = '@PromoPorUmGoleAMais' 
SEU_ID_AMAZON = 'goleamais-20'  # ID ATUALIZADO ✅
# ---------------------

bot = telebot.TeleBot(TOKEN)

def buscar_e_postar():
    print("Buscando novas ofertas de bebidas...") # Isso vai aparecer no log do Render
    url_feed = "https://www.pelando.com.br/rss/bebidas"
    feed = feedparser.parse(url_feed)
    
    # Inverte a ordem para postar as mais recentes primeiro
    for item in reversed(feed.entries):
        # Cria o link com o seu ID de associado
        link_afiliado = f"{item.link}?tag={SEU_ID_AMAZON}"
        
        mensagem = (
            f"🍷 *OFERTA NO GOLE A MAIS!* 🍻\n\n"
            f"{item.title}\n\n"
            f"🛒 Confira aqui: {link_afiliado}\n\n"
            f"🔞 Beba com responsabilidade."
        )
        
        try:
            bot.send_message(CANAL_ID, mensagem, parse_mode="Markdown")
            print(f"Postado: {item.title}")
            time.sleep(30) # Espera 30 segundos entre um post e outro para o Telegram não bloquear
        except Exception as e:
            print(f"Erro ao postar: {e}")
            pass

if __name__ == "__main__":
    print("Robô Gole a Mais iniciado com sucesso!")
    while True:
        buscar_e_postar()
        # O robô vai descansar por 1 hora (3600 segundos) antes de olhar o site de novo
        print("Aguardando 1 hora para a próxima verificação...")
        time.sleep(3600)
