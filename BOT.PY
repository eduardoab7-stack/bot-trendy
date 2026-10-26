import os
import requests
from playwright.sync_api import sync_playwright
import time

# --- CONFIGURACIÓN ---
# Reemplaza estos valores con los tuyos (mantén las comillas)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = eval(os.environ.get("CHAT_ID"))
def enviar_alerta():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    mensaje = "🚨 ¡ALERTA! Parece que el Calendario de Adviento de Trendy ya está en la página web."
    
    # Recorremos la lista de IDs
    for chat_id in TELEGRAM_CHAT_ID:
        payload = {
            "chat_id": chat_id,
            "text": mensaje
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print(f"✅ ¡Mensaje enviado con éxito a {chat_id}!")
            else:
                print(f"❌ Error al enviar mensaje a {chat_id}: {response.text}")
        except Exception as e:
            print(f"❌ Error de conexión con Telegram para {chat_id}: {e}")

def revisar_pagina():
    print("🔍 Revisando la página de Trendy...")
    with sync_playwright() as p:
        # Iniciamos el navegador en modo invisible (headless)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Vamos a la página. Damos 60 segundos de margen por si tarda en cargar
            page.goto("https://www.maquillajetrendyshop.com", wait_until="networkidle", timeout=60000)
            
            # Extraemos todo el texto visible de la página y lo pasamos a minúsculas
            texto_pagina = page.inner_text("body").lower()
            
            # Buscamos las palabras clave
            if "calendario de adviento 2026" in texto_pagina or "wonderland" in texto_pagina:
                print("🎉 ¡Se encontró la palabra clave en la página!")
                enviar_alerta()
            else:
                print("😴 Aún no aparece nada. El calendario no está en la página.")
                
        except Exception as e:
            print(f"⚠️ Hubo un error al revisar la página: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    revisar_pagina()