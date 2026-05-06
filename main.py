import telebot
import time
import feedparser
import threading
import http.server
import socketserver

# --- CONFIGURAÇÕES DO THIAGO ---
TOKEN = '8507254870:AAEkof5aka8s_pdJ8KcyiZ1YuBirrUVUYZw'
CANAL_ID = '@PromoPorUmGoleAMais' 
SEU_ID_AMAZON = 'goleamais-20' 
# ------------------------------

bot = telebot.TeleBot(TOKEN)

# 1. SERVIDOR PARA O RENDER NÃO DAR ERRO (KEEP ALIVE)
def serve():
    # O Render busca uma porta aberta. Vamos abrir a 8080.
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    # Isso permite que o Render veja que o serviço está "vivo"
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f" Servidor de verificação rodando na porta {PORT}")
        httpd.serve_forever()

# 2. LÓGICA DE BUSCA DE OFERTAS
def buscar_e_postar():
    print("🔎 Buscando novas ofertas no Pelando...")
    url_feed = "https://www.pelando.com.br/rss/bebidas"
    feed = feedparser.parse(url_feed)
    
    # Inverte para postar as mais recentes por último (ordem cronológica)
    for item in reversed(feed.entries):
        # Monta o seu link de afiliado Amazon
        link_afiliado = f"{item.link}?tag={SEU_ID_AMAZON}"
        
        mensagem = (
            f"🍷 *OFERTA NO GOLE A MAIS!* 🍻\n\n"
            f"{item.title}\n\n"
            f"🛒 Confira aqui: {link_afiliado}\n\n"
            f"🔞 Beba com responsabilidade."
        )
        
        try:
            bot.send_message(CANAL_ID, mensagem, parse_mode="Markdown")
            print(f"✅ Postado: {item.title}")
            time.sleep(30) # Intervalo anti-spam do Telegram
        except Exception as e:
            print(f"❌ Erro ao postar: {e}")

# 3. LOOP PRINCIPAL DO ROBÔ
def loop_robo():
    print("🚀 Robô Gole a Mais iniciado com sucesso!")
    while True:
        buscar_e_postar()
        print("😴 Aguardando 1 hora para a próxima varredura...")
        time.sleep(3600) # Checa de hora em hora

if __name__ == "__main__":
    # Inicia o servidor web em segundo plano para o Render ficar feliz
    t = threading.Thread(target=serve)
    t.daemon = True
    t.start()
    
    # Inicia o robô no processo principal
    loop_robo()
