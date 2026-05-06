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

# --- VITRINE OTIMIZADA PARA GOOGLE (SEO COMPLETO) ---
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gole a Mais | Promoção de Cerveja, Whisky, Vinho e Bebidas em Oferta</title>
        <meta name="description" content="Melhores ofertas de bebidas alcoólicas. Promoção de cerveja Heineken, Stella, Whisky Red Label, Gin Tanqueray, Vinhos e muito mais. Economize no seu gole!">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; background: #0b090a; color: white; padding: 20px; margin: 0; }
            .card { background: #161a1d; padding: 40px 20px; border-radius: 20px; border: 1px solid #a4161a; box-shadow: 0 10px 30px rgba(0,0,0,0.5); max-width: 500px; margin: 50px auto; }
            h1 { color: #e5383b; font-size: 32px; margin-bottom: 10px; }
            p { color: #f5f3f4; line-height: 1.6; font-size: 18px; }
            .btn { display: inline-block; background: #ba181b; color: white; padding: 18px 35px; text-decoration: none; border-radius: 50px; font-weight: bold; margin-top: 25px; transition: 0.3s; }
            .btn:hover { background: #e5383b; transform: scale(1.05); }
            .lista-bebidas { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 20px; font-size: 14px; color: #b1a7a6; }
            .item { background: #660708; color: white; padding: 5px 12px; border-radius: 5px; }
            .footer-seo { margin-top: 40px; font-size: 10px; color: #660708; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🍻 Gole a Mais</h1>
            <p>Onde o <strong>churrasco</strong> fica mais barato! Monitoramos 24h as melhores <strong>promoções de cerveja</strong>, <strong>whisky importado</strong> e <strong>vinhos</strong>.</p>
            
            <div class="lista-bebidas">
                <span class="item">Heineken em Oferta</span>
                <span class="item">Whisky 12 anos</span>
                <span class="item">Gin & Tônica</span>
                <span class="item">Cerveja Barata</span>
                <span class="item">Vinho Tinto</span>
                <span class="item">Vodka Premium</span>
                <span class="item">Espumantes</span>
            </div>

            <a href="https://t.me/PromoPorUmGoleAMais" class="btn">ENTRAR NO GRUPO DO TELEGRAM</a>
            
            <p style="font-size: 14px; margin-top: 20px;">Receba alertas de <strong>preços baixos</strong> na Amazon, Mercado Livre e Magalu direto no celular.</p>
        </div>

        <div class="footer-seo">
            <h2>Pesquisas relacionadas:</h2>
            <p>Preço de cerveja hoje, promoção de pilsen, ofertas de artesanais, ipa em promoção, kit churrasco barato, onde comprar whisky original, desconto em adegas, melhores vinhos custo benefício 2026, ofertas de tequila, rum e licores.</p>
        </div>
    </body>
    </html>
    """

# --- ROBÔ DE BUSCA (BACKEND) ---
def buscar_e_postar():
    while True:
        print("🔎 Buscando novas ofertas de bebidas no Pelando...")
        try:
            feed = feedparser.parse("https://www.pelando.com.br/rss/bebidas")
            for item in reversed(feed.entries):
                link = f"{item.link}?tag={SEU_ID_AMAZON}"
                msg = f"🍷 *OFERTA NO GOLE A MAIS!*\n\n{item.title}\n\n🛒 Link: {link}"
                try:
                    bot.send_message(CANAL_ID, msg, parse_mode="Markdown")
                    time.sleep(20)
                except Exception as e:
                    print(f"Erro ao postar: {e}")
        except Exception as e:
            print(f"Erro ao buscar feed: {e}")
            
        print("😴 Aguardando 1 hora para a próxima busca...")
        time.sleep(3600)

if __name__ == "__main__":
    threading.Thread(target=buscar_e_postar, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
