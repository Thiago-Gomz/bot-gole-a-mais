import telebot
import time
import feedparser
import threading
from flask import Flask
import os

# --- CONFIGURAÇÕES ---
TOKEN = '8507254870:AAEkof5aka8s_pdJ8KcyiZ1YuBirrUVUYZw'
CANAL_ID = '@PromoPorUmGoleAMais' 
SEU_ID_AMAZON = 'goleamais-20' 
# ---------------------

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

# --- VITRINE PROFISSIONAL PARA O GOOGLE (SEO) ---
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Por Um Gole A Mais | Promoção de Cerveja, Whisky e Bebidas</title>
        <meta name="description" content="Melhores ofertas de bebidas: Heineken, Whisky Red Label, Gin Tanqueray e Vinhos com desconto. Economize no seu próximo gole!">
        <style>
            body { font-family: 'Segoe UI', sans-serif; text-align: center; background: #0b090a; color: white; padding: 20px; margin: 0; }
            .card { background: #161a1d; padding: 40px 20px; border-radius: 25px; border: 2px solid #a4161a; box-shadow: 0 10px 30px rgba(0,0,0,0.5); max-width: 500px; margin: 50px auto; }
            h1 { color: #e5383b; font-size: 32px; margin-bottom: 10px; }
            p { color: #f5f3f4; line-height: 1.6; font-size: 18px; }
            .btn { display: inline-block; background: #ba181b; color: white; padding: 18px 35px; text-decoration: none; border-radius: 50px; font-weight: bold; margin-top: 25px; transition: 0.3s; }
            .btn:hover { background: #e5383b; transform: scale(1.05); }
            .keywords { margin-top: 30px; font-size: 11px; color: #660708; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🍻 Por Um Gole A Mais</h1>
            <p>O melhor grupo de <strong>promoção de bebidas</strong> do Brasil! Ofertas de <strong>Whisky</strong>, <strong>Cerveja</strong> e <strong>Gin</strong> 24h por dia.</p>
            <a href="https://t.me/PromoPorUmGoleAMais" class="btn">ENTRAR NO GRUPO DO TELEGRAM</a>
            <div class="keywords">
                Promoção de Heineken, Preço de Whisky, Cerveja Barata, Desconto em Bebidas, Ofertas de Vinho, Gin Tanqueray Promoção.
            </div>
        </div>
    </body>
    </html>
    """

# --- ROBÔ DE BUSCA E POSTAGEM (BACKEND) ---
def buscar_e_postar():
    while True:
        print("🔎 Buscando ofertas no POR UM GOLE A MAIS...")
        try:
            feed = feedparser.parse("https://www.pelando.com.br/rss/bebidas")
            for item in reversed(feed.entries):
                # Adiciona o seu ID de afiliado ao link
                link = f"{item.link}?tag={SEU_ID_AMAZON}"
                
                # Formato de mensagem chamativo
                msg = (
                    f"🚨 *OFERTA NO POR UM GOLE A MAIS!* 🚨\n\n"
                    f"🍹 {item.title}\n\n"
                    f"✅ *COMPRE AQUI:* {link}\n\n"
                    f"⚠️ _Preços sujeitos a alteração a qualquer momento._"
                )
                
                try:
                    bot.send_message(CANAL_ID, msg, parse_mode="Markdown")
                    print(f"✅ Postado: {item.title[:40]}...")
                    time.sleep(30) # Delay para evitar bloqueio do Telegram
                except Exception as e:
                    print(f"Erro ao postar mensagem: {e}")
        except Exception as e:
            print(f"Erro ao ler feed de notícias: {e}")
            
        print("😴 Rodada finalizada. Descansando 1 hora...")
        time.sleep(3600)

if __name__ == "__main__":
    # Inicia o robô em segundo plano
    threading.Thread(target=buscar_e_postar, daemon=True).start()
    
    # Inicia o servidor web para o Render e o Google
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
